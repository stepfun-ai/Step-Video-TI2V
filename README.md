<p align="center">
  <img src="assets/logo.png"  height=100>
</p>
<div align="center">
  <a href="https://yuewen.cn/videos"><img src="https://img.shields.io/static/v1?label=Step-Video&message=Web&color=green"></a> &ensp;
  <a href="https://arxiv.org/abs/2502.10248"><img src="https://img.shields.io/static/v1?label=Tech Report&message=Arxiv&color=red"></a> &ensp;
  <a href="https://x.com/StepFun_ai"><img src="https://img.shields.io/static/v1?label=X.com&message=Web&color=blue"></a> &ensp;
</div>

<div align="center">
  <a href="https://huggingface.co/stepfun-ai/stepvideo-ti2v"><img src="https://img.shields.io/static/v1?label=Step-Video-TI2V&message=HuggingFace&color=yellow"></a> &ensp;
</div>

## 🔥🔥🔥 News!!
* Mar 17, 2025: 👋 We release the inference code and model weights of Step-Video-Ti2V. [Download](https://huggingface.co/stepfun-ai/stepvideo-ti2v)
* Mar 17, 2025: 🎉 We have made our technical report available as open source. [Read](https://arxiv.org/abs/2502.10248)




## Motion Control

<table border="0" style="width: 100%; text-align: center; margin-top: 1px;">
  <tr>
    <th style="width: 33%;">战马跳跃</th>
    <th style="width: 33%;">战马蹲下</th>
    <th style="width: 33%;">战马向前奔跑，然后转身</th>
  </tr>
  <tr>
    <td><video src="https://github.com/user-attachments/assets/e664f45c-b8cd-4f89-9858-eaaef54aa0f6" width="30%" controls autoplay loop muted></video></td>
    <td><video src="https://github.com/user-attachments/assets/eb2d09b0-cc37-4f27-85c7-a31b6840fa69" width="30%" controls autoplay loop muted></video></td>
    <td><video src="https://github.com/user-attachments/assets/d17eba41-82f6-4ee2-8a99-3f21af112af0" width="30%" controls autoplay loop muted></video></td>
  </tr>
</table>

## Motion Dynamics Control


<table border="0" style="width: 100%; text-align: center; margin-top: 10px;">
  <tr>
    <th style="width: 33%;">两名男子在互相拳击，镜头环绕两人拍摄。(motion_score: 2)</th>
    <th style="width: 33%;">两名男子在互相拳击，镜头环绕两人拍摄。(motion_score: 5)</th>
    <th style="width: 33%;">两名男子在互相拳击，镜头环绕两人拍摄。(motion_score: 20)</th>
  </tr>
  <tr>
    <td><video src="https://github.com/user-attachments/assets/31c48385-fe83-4961-bd42-7bd2b1edeb19" width="33%" controls autoplay loop muted></video></td>
    <td><video src="https://github.com/user-attachments/assets/913a407e-55ca-4a33-bafe-bd5e38eec5f5" width="33%" controls autoplay loop muted></video></td>
    <td><video src="https://github.com/user-attachments/assets/119a3673-014f-4772-b846-718307a4a412" width="33%" controls autoplay loop muted></video></td>
  </tr>
</table>

🎯 Tips 
The default motion_score = 5 is suitable for general use. If you need more stability, set motion_score = 2, though it may lack dynamism in certain movements. For greater movement flexibility, you can use motion_score = 10 or motion_score = 20 to enable more intense actions. Feel free to customize the motion_score based on your creative needs to fit different use cases.

## Camera Control

<table border="0" style="width: 100%; text-align: center; margin-top: 1px;">
  <tr>
    <th style="width: 33%;">镜头环绕女孩，女孩在跳舞</th>
    <th style="width: 33%;">镜头缓慢推进，女孩在跳舞</th>
    <th style="width: 33%;">镜头拉远，女孩在跳舞</th>
  </tr>
  <tr>
    <td><video src="https://github.com/user-attachments/assets/257847bc-5967-45ba-a649-505859476aad" height="30%" controls autoplay loop muted></video></td>
    <td><video src="https://github.com/user-attachments/assets/d310502a-4f7e-4a78-882f-95c46b4dfe67" height="30%" controls autoplay loop muted></video></td>
    <td><video src="https://github.com/user-attachments/assets/f6426fc7-2a18-474c-9766-fc8ae8d8d40d" height="30%" controls autoplay loop muted></video></td>
  </tr>
</table>


### Supported Camera Movements | 支持的运镜方式

| Camera Movement               | 运镜方式           |
|--------------------------------|--------------------|
| **Fixed Camera**               | 固定镜头           |
| **Pan Up/Down/Left/Right**     | 镜头上/下/左/右移 |
| **Tilt Up/Down/Left/Right**    | 镜头上/下/左/右摇 |
| **Zoom In/Out**                | 镜头放大/缩小       |
| **Dolly In/Out**               | 镜头推进/拉远       |
| **Camera Rotation**            | 镜头旋转           |
| **Tracking Shot**  | 镜头跟随 |
| **Orbit Shot** | 镜头环绕  |
| **Rack Focus**  | 焦点转移           |


🔧 Motion Score Considerations
motion_score = 5 or 10 offers smoother and more accurate motion than motion_score = 2, with motion_score = 10 providing the best responsiveness and camera tracking. Choosing the right setting enhances motion precision and fluidity.
 
## Anime Style

<table border="0" style="width: 100%; text-align: center; margin-top: 1px;">
  <tr>
    <th style="width: 33%;">女生向前行走，背景是虚化模糊的效果</th>
    <th style="width: 33%;">女人眨眼，然后对着镜头做飞吻的动作。</th>
    <th style="width: 10%;">狸猫战士双手缓缓上扬，雷电从手中向四周扩散，\<br>身后灵兽影像的双眼闪烁强光，\<br>张开巨口发出低吼</th>
  </tr>
  <tr>
    <td><video src="https://github.com/user-attachments/assets/80be13a1-ea65-45c5-b7f4-c2488acbf2a3" height="33%" controls autoplay loop muted></video></td>
    <td><video src="https://github.com/user-attachments/assets/67038b85-19d4-4313-b386-f578b75dcad7" height="33%" controls autoplay loop muted></video></td>
    <td><video src="https://github.com/user-attachments/assets/73ffd269-a5c8-4255-8809-161501273bfd" height="33%" controls autoplay loop muted></video></td>
  </tr>

</table>


## Table of Contents

1. [Introduction](#1-introduction)
2. [Model Summary](#2-model-summary)
3. [Model Download](#3-model-download)
4. [Model Usage](#4-model-usage)
5. [Benchmark](#5-benchmark)
6. [Online Engine](#6-online-engine)
7. [Citation](#7-citation)
8. [Acknowledgement](#8-ackownledgement)



## 1. Introduction
We present Step-Video-TI2V, a state-of-the-art text-driven image-to-video generation model with 30B parameters, capable of generating videos up to 102 frames
based on both text and image inputs. We build Step-Video-TI2V-Eval as a new benchmark for the text-driven image-to-video task and compare Step-Video-TI2V
with open-source and commercial TI2V engines using this dataset. Experimental results demonstrate the state-of-the-art performance of Step-Video-TI2V in the
image-to-video generation task. Both Step-Video-TI2V and Step-Video-TI2V-Eval are available.

## 2. Model Summary
Step-Video-TI2V based on Step-Video-T2V. To incorporate the image condition as the first frame of the generated video, we encode it into latent representations using Step-Video- T2V’s Video-VAE and concatenate them along the channel dimension of the video latent. Additionally, we introduce a motion score condition, enabling users to control the dynamic level of the video generated from the image condition. Figure 1 shows an overview of our framework, highlighting these two modifications to the pre-trained T2V model. 

<p align="center">
  <img width="80%" src="assets/model.png">
</p>

## 3. Model Download
| Models   | 🤗Huggingface    |  🤖Modelscope |
|:-------:|:-------:|:-------:|
| Step-Video-T2V | [download](https://huggingface.co/stepfun-ai/stepvideo-ti2v) | 


## 4. Model Usage

### 📜 4.1  Dependencies and Installation

```bash
git clone https://github.com/stepfun-ai/Step-Video-TI2V.git
conda create -n stepvideo python=3.10
conda activate stepvideo

cd Step-Video-TI2V
pip install -e .
```

###  🚀 4.2. Inference Scripts
```bash
python api/call_remote_server.py --model_dir where_you_download_dir &  ## We assume you have more than 4 GPUs available. This command will return the URL for both the caption API and the VAE API. Please use the returned URL in the following command.

parallel=4  # or parallel=8
url='127.0.0.1'
model_dir=where_you_download_dir

torchrun --nproc_per_node $parallel run_parallel.py --model_dir $model_dir --vae_url $url --caption_url $url  --ulysses_degree  $parallel --prompt "笑起来" --first_image_path ./assets/demo.png --infer_steps 50  --cfg_scale 9.0 --time_shift 13.0 --motion_score 5.0
```

We list some more useful configurations for easy usage:

|        Argument        |  Default  |                Description                |
|:----------------------:|:---------:|:-----------------------------------------:|
|       `--model_dir`       |   None    |   The model checkpoint for video generation    |
|     `--prompt`     | “笑起来”  |      The text prompt for I2V generation      |
|    `--first_image_path`    |    ./assets/demo.png    |     The reference image path for I2V task.     |
|    `--infer_steps`     |    50     |     The number of steps for sampling      |
| `--cfg_scale` |    9.0    |    Embedded  Classifier free guidance scale       |
|     `--time_shift`     |    7.0    | Shift factor for flow matching schedulers. |
|     `--motion_score`   |    5.0  | Score to control the motion level of the video. |
|        `--seed`        |     None  |   The random seed for generating video, if None, we init a random seed    |
|  `--use-cpu-offload`   |   False   |    Use CPU offload for the model load to save more memory, necessary for high-res video generation    |
|     `--save-path`      | ./results |     Path to save the generated video      |


## 5. Benchmark
We first evaluated on VBench-I2V is a comprehensive benchmark suite that deconstructs “video generation
quality” into specific, hierarchical, and disentangled dimensions, each with tailored prompts and evaluation methods. We utilize the VBench-I2V benchmark to assess the performance of Step-Video-
TI2V alongside other TI2V models.

<p align="center">
  <img width="80%" src="assets/compare_1.png">
</p>

We are releasing [Step-Video-Ti2V Eval](https://github.com/stepfun-ai/Step-Video-T2V/blob/main/benchmark/Step-Video-TI2V-Eval) , a new benchmark designed for the text-driven image-to-video
generation task. The dataset comprises 178 real-world and 120 anime-style prompt-image pairs, ensuring broad coverage of diverse user scenarios. To achieve comprehensive representation, we
developed a fine-grained schema for data collection in both categories. We compare Step-Video-TI2V with two recently released open-source TI2V models, OSTopA and
OSTopB, as well as two close-source commercial TI2V models, CSTopC and CSTopD. All these four models originate from China. Generally, Step-Video-TI2V achieves state-of-the-art performance on the total score across the
three evaluation dimensions in Step-Video-TI2V-Eval, either outperforming or matching leading open-source and closed-source commercial TI2V models. We also presented two results of Step-Video-TI2V, with the motion
set to 5 and 10, respectively. As expected, this mechanism effectively balances the motion dynamics
and stability (or consistency) of the generated videos.

<p align="center">
  <img width="80%" src="assets/compare_2.png">
</p>



## 6. Online Engine
The online version of Step-Video-T2V is available on [跃问视频](https://yuewen.cn/videos), where you can also explore some impressive examples.

## 7. Citation
```
@misc{ma2025stepvideot2vtechnicalreportpractice,
      title={Step-Video-Ti2V Technical Report: The Practice, Challenges, and Future of Video Foundation Model}, 
      author={Guoqing Ma and Haoyang Huang and Kun Yan and Liangyu Chen and Nan Duan and Shengming Yin and Changyi Wan and Ranchen Ming and Xiaoniu Song and Xing Chen and Yu Zhou and Deshan Sun and Deyu Zhou and Jian Zhou and Kaijun Tan and Kang An and Mei Chen and Wei Ji and Qiling Wu and Wen Sun and Xin Han and Yanan Wei and Zheng Ge and Aojie Li and Bin Wang and Bizhu Huang and Bo Wang and Brian Li and Changxing Miao and Chen Xu and Chenfei Wu and Chenguang Yu and Dapeng Shi and Dingyuan Hu and Enle Liu and Gang Yu and Ge Yang and Guanzhe Huang and Gulin Yan and Haiyang Feng and Hao Nie and Haonan Jia and Hanpeng Hu and Hanqi Chen and Haolong Yan and Heng Wang and Hongcheng Guo and Huilin Xiong and Huixin Xiong and Jiahao Gong and Jianchang Wu and Jiaoren Wu and Jie Wu and Jie Yang and Jiashuai Liu and Jiashuo Li and Jingyang Zhang and Junjing Guo and Junzhe Lin and Kaixiang Li and Lei Liu and Lei Xia and Liang Zhao and Liguo Tan and Liwen Huang and Liying Shi and Ming Li and Mingliang Li and Muhua Cheng and Na Wang and Qiaohui Chen and Qinglin He and Qiuyan Liang and Quan Sun and Ran Sun and Rui Wang and Shaoliang Pang and Shiliang Yang and Sitong Liu and Siqi Liu and Shuli Gao and Tiancheng Cao and Tianyu Wang and Weipeng Ming and Wenqing He and Xu Zhao and Xuelin Zhang and Xianfang Zeng and Xiaojia Liu and Xuan Yang and Yaqi Dai and Yanbo Yu and Yang Li and Yineng Deng and Yingming Wang and Yilei Wang and Yuanwei Lu and Yu Chen and Yu Luo and Yuchu Luo and Yuhe Yin and Yuheng Feng and Yuxiang Yang and Zecheng Tang and Zekai Zhang and Zidong Yang and Binxing Jiao and Jiansheng Chen and Jing Li and Shuchang Zhou and Xiangyu Zhang and Xinhao Zhang and Yibo Zhu and Heung-Yeung Shum and Daxin Jiang},
      year={2025},
      eprint={2502.10248},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2502.10248}, 
}
```

