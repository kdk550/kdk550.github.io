---
layout: post
title: "计数排序               洛谷P1271 【深基9.例1】选举学生会"
date: 2021-07-23 19:19:00 +0800
updated: 2023-01-21 19:09:00 +0800
description: "第一次提交全WA了，想想不对我的代码没有出现问题，在输出后面加上空格才AC（捂脸 piao这个数组可以用一个变量来代替，来节省空间"
excerpt: "第一次提交全WA了，想想不对我的代码没有出现问题，在输出后面加上空格才AC（捂脸 piao这个数组可以用一个变量来代替，来节省空间"
categories: []
tags: ["algorithm basics"]
comments: false
related_posts: false
---
{% raw %}
```
#include<iostream>
#include<cmath>
using namespace std;
long long ren[1010];
long long piao[2000010];
int main()
{
    int n, m;
    cin >> n >> m;
    for (int i = 1; i <= m; i++)
    {
        cin >> piao[i];
        ren[piao[i]]++;
    }
    for (int i = 1; i <= n; i++)
    {
        if (ren[i] != 0)
        {
            for (int j = 1; j <= ren[i]; j++)
                cout << i<<" ";
        }
    }
    return 0;
}
```



第一次提交全WA了，想想不对我的代码没有出现问题，在输出后面加上空格才AC（捂脸

piao这个数组可以用一个变量来代替，来节省空间
{% endraw %}
