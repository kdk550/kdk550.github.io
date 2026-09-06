---
layout: post
title: "选择排序"
date: 2021-07-23 20:14:00 +0800
updated: 2023-01-21 19:09:00 +0800
description: "选择排序的算法时间复杂度为O（n^2） 空间复杂度为O（n）"
excerpt: "选择排序的算法时间复杂度为O（n^2） 空间复杂度为O（n）"
categories: []
tags: ["algorithm basics"]
comments: false
related_posts: false
---
{% raw %}
```
//选择排序
#include<iostream>
using namespace std;
int main()
{
    int n;
    cin >> n;
    int a[1010];
    for (int i = 1; i <= n; i++)
    {
        cin >> a[i];
    }
    for (int i = 1; i <= n-1; i++)
    {
        for (int j = i + 1; j <=n; j++)
        {
            if (a[i] > a[j])
            {
                int temp = a[j];
                a[j] = a[i];
                a[i] = temp;
            }
        }
    }
    for (int i = 1; i <= n; i++)
        cout << a[i]<<"   ";
    return 0;
}
```



 选择排序的算法时间复杂度为O（n^2）

空间复杂度为O（n）
{% endraw %}
