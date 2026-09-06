---
layout: post
title: "二分查找与二分答案（待补充）"
date: 2021-07-27 23:30:00 +0800
updated: 2023-01-21 19:11:00 +0800
description: "------------------------------------------------------------------------------------"
excerpt: "------------------------------------------------------------------------------------"
categories: []
tags: ["algorithm basics"]
comments: false
related_posts: false
---
{% raw %}
```
int mid=(left+right)/2;
//会有超过int类型的可能性
int mid=left+(right-left)/2;
//这么做可以避免运算溢出
```



 ------------------------------------------------------------------------------------



```
int search(int x)
{
    int left = 1, right = n;
    while (left <= right)
    {
        int mid = left+( right-left) / 2;
        if (a[mid] == x)    return eeee(mid);
        else if (a[mid] > x)    right = mid - 1;
        else left = mid + 1;
    }
    return -1;

}
```
{% endraw %}
