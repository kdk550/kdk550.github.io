---
layout: post
title: "New Year Tree"
date: 2023-04-03 11:37:00 +0800
updated: 2023-04-03 11:37:00 +0800
description: "New Year Tree 线段树，打标记，位运算 1. 操作1，区间赋值，很容易的线段树操作 2. 对于询问以 \\(u\\) 为根的子树上的所有节点的颜色数量，一开始我在线段树里开了一个大小61的数组，喜提MLE，但后续观察发现， \\(1 << 60 \\leq \\text{longlong}\\) ，所以我们设每种颜色…"
excerpt: "New Year Tree 线段树，打标记，位运算 1. 操作1，区间赋值，很容易的线段树操作 2. 对于询问以 \\(u\\) 为根的子树上的所有节点的颜色数量，一开始我在线段树里开了一个大小61的数组，喜提MLE，但后续观察发现， \\(1 << 60 \\leq \\text{longlong}\\) ，所以我们设每种颜色…"
categories: []
tags: ["data structures"]
comments: false
related_posts: false
---
{% raw %}
[New Year Tree](https://codeforces.com/problemset/problem/620/E "New Year Tree")

线段树，打标记，位运算

1. 操作1，区间赋值，很容易的线段树操作
2. 对于询问以<span class="math inline">\(u\)</span>为根的子树上的所有节点的颜色数量，一开始我在线段树里开了一个大小61的数组，喜提MLE，但后续观察发现，<span class="math inline">\(1 &lt;&lt; 60   \leq \text{longlong}\)</span>，所以我们设每种颜色$ c_i $的值为<span class="math inline">\(1 &lt;&lt; c_i\)</span>,对于update,左区间和右区间的颜色进行或运算即可，统计的颜色数量做一个1~60的位运算判断即可。

细节见代码
{% endraw %}
