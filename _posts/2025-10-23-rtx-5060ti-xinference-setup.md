---
layout: post
title: "RTX5060TI 配置Xinference"
date: 2025-10-23 16:57:00 +0800
updated: 2025-10-23 16:58:00 +0800
description: "RTX5060TI 配置Xinference CUDA 配置环境和安装依赖 下载模型 在这个网站自助 运行Xinference windows不支持0.0.0.需要使用127.0.0.1 ip的方式 xinference-local --host 0.0.0.0 --port 9997 xinference-loca…"
excerpt: "RTX5060TI 配置Xinference CUDA 配置环境和安装依赖 下载模型 在这个网站自助 运行Xinference windows不支持0.0.0.需要使用127.0.0.1 ip的方式 xinference-local --host 0.0.0.0 --port 9997 xinference-loca…"
categories: []
tags: ["AI"]
comments: false
related_posts: false
---
{% raw %}
# RTX5060TI 配置Xinference

## CUDA



```bash
(llama-factory) D:\P\llm\LLaMA-Factory>nvcc -V
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2025 NVIDIA Corporation
Built on Wed_Apr__9_19:29:17_Pacific_Daylight_Time_2025
Cuda compilation tools, release 12.9, V12.9.41
Build cuda_12.9.r12.9/compiler.35813241_0

(llama-factory) D:\P\llm\LLaMA-Factory>nvidia-smi
Thu Oct 23 15:24:02 2025
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 576.88                 Driver Version: 576.88         CUDA Version: 12.9     |
|-----------------------------------------+------------------------+----------------------+
| GPU  Name                  Driver-Model | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA GeForce RTX 5060 Ti   WDDM  |   00000000:01:00.0  On |                  N/A |
|  0%   38C    P0             24W /  180W |    2728MiB /  16311MiB |      0%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+
```



## 配置环境和安装依赖



```bash
conda create -n Xinference python=3.10.14
conda activate Xinference
pip install "xinference[all]"
pip uninstall torch torchvision torchaudio -y
pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu128 --no-deps
```



## 下载模型

在这个网站自助 <https://modelscope.cn/>

## 运行Xinference

windows不支持0.0.0.需要使用127.0.0.1 ip的方式

xinference-local --host 0.0.0.0 --port 9997

xinference-local --host 127.0.0.1 --port 9997

[Windows下启动Xinference报错 RuntimeError: Cluster is not available after multiple attempts-CSDN博客](https://blog.csdn.net/TZfool/article/details/141167586 "Windows下启动Xinference报错 RuntimeError: Cluster is not available after multiple attempts-CSDN博客")
{% endraw %}
