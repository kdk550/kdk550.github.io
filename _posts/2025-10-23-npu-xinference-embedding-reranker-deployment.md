---
layout: post
title: "npu配置Xinference环境，并部署embedding和rerank模型"
date: 2025-10-23 16:32:00 +0800
updated: 2025-10-23 16:32:00 +0800
description: "在我司服务器上部署，但是尝试了其他文章的docker镜像，出现算子错误等问题，后面又用回 参考文献 后面我直接通过打开 http://127.0.0.1:9997 配置embedding和rerank模型。"
excerpt: "在我司服务器上部署，但是尝试了其他文章的docker镜像，出现算子错误等问题，后面又用回 参考文献 后面我直接通过打开 http://127.0.0.1:9997 配置embedding和rerank模型。"
categories: []
tags: ["AI"]
comments: false
related_posts: false
---
{% raw %}
在我司服务器上部署，但是尝试了其他文章的docker镜像，出现算子错误等问题，后面又用回

参考文献  
<https://blog.csdn.net/sccum/article/details/145995250>  
<https://blog.csdn.net/qq_41994821/article/details/147223327>  
<https://ascend.readthedocs.io/zh-cn/latest/sources/sentence_transformers/install.html>



```bash
docker run -it -d --net=host --shm-size=20g  \
  --name Xinf \
  --device /dev/davinci4 \
  --device /dev/davinci5 \
  --device /dev/davinci_manager \
  --device /dev/devmm_svm \
  --device /dev/hisi_hdc \
  -v /usr/local/dcmi:/usr/local/dcmi \
  -v /usr/local/bin/npu-smi:/usr/local/bin/npu-smi \
  -v /usr/local/Ascend/driver/lib64/:/usr/local/Ascend/driver/lib64/ \
  -v /usr/local/Ascend/driver/version.info:/usr/local/Ascend/driver/version.info \
  -v /etc/ascend_install.info:/etc/ascend_install.info \
  -v /root/.cache:/root/.cache \
  -v /share/models/embedding/bge-reranker-v2-m3:/bge-reranker-v2-m3:ro \
  -p 9997:9997 \
  -it $IMAGE bash

# 终端1
export XINFERENCE_ENDPOINT=http://0.0.0.0:9997
xinference-local --host 0.0.0.0 --port 9997
# 终端2
export XINFERENCE_ENDPOINT=http://127.0.0.1:9997
## 本地下载重排序模型之后
xinference launch --model-name bge-reranker-v2-m3 --model-type rerank --model-path /bge-reranker-v2-m3
```



后面我直接通过打开`http://127.0.0.1:9997`配置embedding和rerank模型。
{% endraw %}
