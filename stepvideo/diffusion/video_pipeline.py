# Copyright 2025 StepFun Inc. All Rights Reserved.

from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass

import numpy as np
import pickle
import torch
from diffusers.pipelines.pipeline_utils import DiffusionPipeline
from diffusers.utils import BaseOutput
import asyncio

from stepvideo.modules.model import StepVideoModel
from stepvideo.diffusion.scheduler import FlowMatchDiscreteScheduler
from stepvideo.utils import VideoProcessor
from torchvision import transforms
from PIL import Image as PILImage

import os


def call_api_gen(url, api, port=8080):
    url =f"http://{url}:{port}/{api}-api"
    import aiohttp
    async def _fn(samples, *args, **kwargs):
        if api=='vae':
            data = {
                    "samples": samples,
                }
        elif api=='vae-encode':
            data = {
                    "videos": samples,
                }
        elif api == 'caption':
            data = {
                    "prompts": samples,
                }
        else:
            raise Exception(f"Not supported api: {api}...")
        
        async with aiohttp.ClientSession() as sess:
            data_bytes = pickle.dumps(data)
            async with sess.get(url, data=data_bytes, timeout=12000) as response:
                result = bytearray()
                while not response.content.at_eof():
                    chunk = await response.content.read(1024)
                    result += chunk
                response_data = pickle.loads(result)
        return response_data
        
    return _fn




@dataclass
class StepVideoPipelineOutput(BaseOutput):
    video: Union[torch.Tensor, np.ndarray]
    

class StepVideoPipeline(DiffusionPipeline):
    r"""
    Pipeline for text-to-video generation using StepVideo.

    This model inherits from [`DiffusionPipeline`]. Check the superclass documentation for the generic methods
    implemented for all pipelines (downloading, saving, running on a particular device, etc.).

    Args:
        transformer ([`StepVideoModel`]):
            Conditional Transformer to denoise the encoded image latents.
        scheduler ([`FlowMatchDiscreteScheduler`]):
            A scheduler to be used in combination with `transformer` to denoise the encoded image latents.
        vae_url:
            remote vae server's url.
        caption_url:
            remote caption (stepllm and clip) server's url.
    """

    def __init__(
        self,
        transformer: StepVideoModel,
        scheduler: FlowMatchDiscreteScheduler,
        vae_url: str = '127.0.0.1',
        caption_url: str = '127.0.0.1',
        save_path: str = './results',
        name_suffix: str = '',
    ):
        super().__init__()

        self.register_modules(
            transformer=transformer,
            scheduler=scheduler,
        )
        
        self.vae_scale_factor_temporal = self.vae.temporal_compression_ratio if getattr(self, "vae", None) else 8
        self.vae_scale_factor_spatial = self.vae.spatial_compression_ratio if getattr(self, "vae", None) else 16
        self.video_processor = VideoProcessor(save_path, name_suffix)
        
        self.vae_url = vae_url
        self.caption_url = caption_url
        self.setup_api(self.vae_url, self.caption_url)
    
    def setup_pipeline(self, args):
        self.args = args
        self.video_processor = VideoProcessor(self.args.save_path, self.args.name_suffix)
        self.setup_api(args.vae_url, args.caption_url)
        return self

    def setup_api(self, vae_url, caption_url):
        self.vae_url = vae_url
        self.caption_url = caption_url
        self.caption = call_api_gen(caption_url, 'caption')
        self.vae = call_api_gen(vae_url, 'vae')
        self.vae_encode = call_api_gen(vae_url, 'vae-encode')
        return self
    
    def encode_prompt(
        self,
        prompt: str,
        neg_magic: str = '',
        pos_magic: str = '',
    ):
        device = self._execution_device
        prompts = [prompt+pos_magic]
        bs = len(prompts)
        prompts += [neg_magic]*bs
        
        data = asyncio.run(self.caption(prompts))
        prompt_embeds, prompt_attention_mask, clip_embedding = data['y'].to(device), data['y_mask'].to(device), data['clip_embedding'].to(device)

        return prompt_embeds, clip_embedding, prompt_attention_mask

    def decode_vae(self, samples):
        samples = asyncio.run(self.vae(samples.cpu()))
        return samples

    def encode_vae(self, img):
        latents = asyncio.run(self.vae_encode(img))
        return latents

    def check_inputs(self, num_frames, width, height):
        num_frames = max(num_frames//17*17, 1)
        width = max(width//16*16, 16)
        height = max(height//16*16, 16)
        return num_frames, width, height

    def prepare_latents(
        self,
        batch_size: int,
        num_channels_latents: 64,
        height: int = 544,
        width: int = 992,
        num_frames: int = 204,
        dtype: Optional[torch.dtype] = None,
        device: Optional[torch.device] = None,
        generator: Optional[Union[torch.Generator, List[torch.Generator]]] = None,
        latents: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        if latents is not None:
            return latents.to(device=device, dtype=dtype)

        num_frames, width, height = self.check_inputs(num_frames, width, height)
        shape = (
            batch_size,
            max(num_frames//17*3, 1),
            num_channels_latents,
            int(height) // self.vae_scale_factor_spatial,
            int(width) // self.vae_scale_factor_spatial,
        )   # b,f,c,h,w
        if isinstance(generator, list) and len(generator) != batch_size:
            raise ValueError(
                f"You have passed a list of generators of length {len(generator)}, but requested an effective batch"
                f" size of {batch_size}. Make sure the batch size matches the length of the generators."
            )

        if generator is None:
            generator = torch.Generator(device=self._execution_device)

        latents = torch.randn(shape, generator=generator, device=device, dtype=dtype)
        return latents

    
    def resize_to_desired_aspect_ratio(self, video, aspect_size):
        ## video is in shape [f, c, h, w]
        height, width = video.shape[-2:]
        
        aspect_ratio = [w/h for h, w in aspect_size]
        # # resize
        aspect_ratio_fact = width / height
        bucket_idx = np.argmin(np.abs(aspect_ratio_fact - np.array(aspect_ratio)))
        aspect_ratio = aspect_ratio[bucket_idx]
        target_size_height, target_size_width = aspect_size[bucket_idx]
        
        if aspect_ratio_fact < aspect_ratio:
            scale = target_size_width / width
        else:
            scale = target_size_height / height

        width_scale = int(round(width * scale))
        height_scale = int(round(height * scale))


        # # crop
        delta_h = height_scale - target_size_height
        delta_w = width_scale - target_size_width
        assert delta_w>=0
        assert delta_h>=0
        assert not all(
            [delta_h, delta_w]
        )  
        top = delta_h//2
        left = delta_w//2

        ## resize image and crop
        resize_crop_transform = transforms.Compose([
            transforms.Resize((height_scale, width_scale)),
            lambda x: transforms.functional.crop(x, top, left, target_size_height, target_size_width),
        ])

        video = torch.stack([resize_crop_transform(frame.contiguous()) for frame in video], dim=0)
        return video


    def prepare_condition_hidden_states(
        self, 
        img: Union[str, PILImage.Image, torch.Tensor]=None, 
        batch_size: int = 1,
        num_channels_latents: int = 64,
        height: int = 544,
        width: int = 992,
        num_frames: int = 204,
        dtype: Optional[torch.dtype] = None,
        device: Optional[torch.device] = None
    ):
        if isinstance(img, str):
            assert os.path.exists(img)
            img = PILImage.open(img) 
        
        if isinstance(img, PILImage.Image):
            img_tensor = transforms.ToTensor()(img.convert('RGB'))*2-1
        else:
            img_tensor = img
            
        num_frames, width, height = self.check_inputs(num_frames, width, height)
            
        img_tensor = self.resize_to_desired_aspect_ratio(img_tensor[None], aspect_size=[(height, width)])[None]

        img_emb = self.encode_vae(img_tensor).repeat(batch_size, 1,1,1,1).to(device)
        
        padding_tensor = torch.zeros((batch_size, max(num_frames//17*3, 1)-1, num_channels_latents, int(height) // self.vae_scale_factor_spatial, int(width) // self.vae_scale_factor_spatial,), device=device)
        condition_hidden_states = torch.cat([img_emb, padding_tensor], dim=1) 

        condition_hidden_states = condition_hidden_states.repeat(2, 1,1,1,1) ## for CFG
        return condition_hidden_states.to(dtype)

    @torch.inference_mode()
    def __call__(
        self,
        prompt: Union[str, List[str]] = None,
        height: int = 544,
        width: int = 992,
        num_frames: int = 102,
        num_inference_steps: int = 50,
        guidance_scale: float = 9.0,
        time_shift: float = 13.0,
        neg_magic: str = "",
        pos_magic: str = "",
        num_videos_per_prompt: Optional[int] = 1,
        generator: Optional[Union[torch.Generator, List[torch.Generator]]] = None,
        latents: Optional[torch.Tensor] = None,
        first_image: Union[str, PILImage.Image, torch.Tensor] = None,
        motion_score: float = 2.0,
        output_type: Optional[str] = "mp4",
        output_file_name: Optional[str] = "",
        return_dict: bool = True,
    ):
        r"""
        The call function to the pipeline for generation.

        Args:
            prompt (`str` or `List[str]`, *optional*):
                The prompt or prompts to guide the image generation. If not defined, one has to pass `prompt_embeds`.
                instead.
            height (`int`, defaults to `544`):
                The height in pixels of the generated image.
            width (`int`, defaults to `992`):
                The width in pixels of the generated image.
            num_frames (`int`, defaults to `204`):
                The number of frames in the generated video.
            num_inference_steps (`int`, defaults to `50`):
                The number of denoising steps. More denoising steps usually lead to a higher quality image at the
                expense of slower inference.
            guidance_scale (`float`, defaults to `9.0`):
                Guidance scale as defined in [Classifier-Free Diffusion Guidance](https://arxiv.org/abs/2207.12598).
                `guidance_scale` is defined as `w` of equation 2. of [Imagen
                Paper](https://arxiv.org/pdf/2205.11487.pdf). Guidance scale is enabled by setting `guidance_scale >
                1`. Higher guidance scale encourages to generate images that are closely linked to the text `prompt`,
                usually at the expense of lower image quality. 
            num_videos_per_prompt (`int`, *optional*, defaults to 1):
                The number of images to generate per prompt.
            generator (`torch.Generator` or `List[torch.Generator]`, *optional*):
                A [`torch.Generator`](https://pytorch.org/docs/stable/generated/torch.Generator.html) to make
                generation deterministic.
            latents (`torch.Tensor`, *optional*):
                Pre-generated noisy latents sampled from a Gaussian distribution, to be used as inputs for image
                generation. Can be used to tweak the same generation with different prompts. If not provided, a latents
                tensor is generated by sampling using the supplied random `generator`.
            first_image (`str`, `PIL.Image`, `torch.Tensor`):
                A path for the reference image
            output_type (`str`, *optional*, defaults to `"pil"`):
                The output format of the generated image. Choose between `PIL.Image` or `np.array`.
            output_file_name(`str`, *optional*`):
                The output mp4 file name.
            return_dict (`bool`, *optional*, defaults to `True`):
                Whether or not to return a [`StepVideoPipelineOutput`] instead of a plain tuple.

        Examples:

        Returns:
            [`~StepVideoPipelineOutput`] or `tuple`:
                If `return_dict` is `True`, [`StepVideoPipelineOutput`] is returned, otherwise a `tuple` is returned
                where the first element is a list with the generated images and the second element is a list of `bool`s
                indicating whether the corresponding generated image contains "not-safe-for-work" (nsfw) content.
        """

        # 1. Check inputs. Raise error if not correct
        device = self._execution_device

        # 2. Define call parameters
        if prompt is not None and isinstance(prompt, str):
            batch_size = 1
        elif prompt is not None and isinstance(prompt, list):
            batch_size = len(prompt)
        else:
            batch_size = prompt_embeds.shape[0]

        do_classifier_free_guidance = guidance_scale > 1.0

        # 3. Encode input prompt
        prompt_embeds, prompt_embeds_2, prompt_attention_mask = self.encode_prompt(
            prompt=prompt,
            neg_magic=neg_magic,
            pos_magic=pos_magic,
        )

        transformer_dtype = self.transformer.dtype
        prompt_embeds = prompt_embeds.to(transformer_dtype)
        prompt_attention_mask = prompt_attention_mask.to(transformer_dtype)
        prompt_embeds_2 = prompt_embeds_2.to(transformer_dtype)

        # 4. Prepare timesteps
        self.scheduler.set_timesteps(
            num_inference_steps=num_inference_steps,
            time_shift=time_shift,
            device=device
        )

        # 5. Prepare latent variables
        num_channels_latents = self.transformer.config.in_channels
        latents = self.prepare_latents(
            batch_size * num_videos_per_prompt,
            num_channels_latents,
            height,
            width,
            num_frames,
            torch.bfloat16,
            device,
            generator,
            latents,
        )
        condition_hidden_states = self.prepare_condition_hidden_states(
            first_image, 
            batch_size * num_videos_per_prompt,
            num_channels_latents,
            height,
            width,
            num_frames,
            dtype=torch.bfloat16,
            device=device)

        # 7. Denoising loop
        with self.progress_bar(total=num_inference_steps) as progress_bar:
            for i, t in enumerate(self.scheduler.timesteps):
                latent_model_input = torch.cat([latents] * 2) if do_classifier_free_guidance else latents
                latent_model_input = latent_model_input.to(transformer_dtype)
                # broadcast to batch dimension in a way that's compatible with ONNX/Core ML
                timestep = t.expand(latent_model_input.shape[0]).to(latent_model_input.dtype)

                noise_pred = self.transformer(
                    hidden_states=latent_model_input,
                    timestep=timestep,
                    encoder_hidden_states=prompt_embeds,
                    encoder_attention_mask=prompt_attention_mask,
                    encoder_hidden_states_2=prompt_embeds_2,
                    condition_hidden_states=condition_hidden_states,
                    motion_score=motion_score,
                    return_dict=False,
                )
                # perform guidance
                if do_classifier_free_guidance:
                    noise_pred_text, noise_pred_uncond = noise_pred.chunk(2)
                    noise_pred = noise_pred_uncond + guidance_scale * (noise_pred_text - noise_pred_uncond)

                # compute the previous noisy sample x_t -> x_t-1
                latents = self.scheduler.step(
                    model_output=noise_pred,
                    timestep=t,
                    sample=latents
                )
                
                progress_bar.update()

        if not torch.distributed.is_initialized() or int(torch.distributed.get_rank())==0:
            if not output_type == "latent":
                video = self.decode_vae(latents)
                video = self.video_processor.postprocess_video(video, output_file_name=output_file_name, output_type=output_type)
            else:
                video = latents

            # Offload all models
            self.maybe_free_model_hooks()

            if not return_dict:
                return (video, )

            return StepVideoPipelineOutput(video=video)
        

        