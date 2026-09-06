---
layout: post
title: "C. Ehab and Path-etic MEXs"
date: 2023-05-06 17:53:00 +0800
updated: 2023-05-06 17:53:00 +0800
description: "C. Ehab and Path-etic MEXs 1. 对于成链的情况， \\(\\text{MEX} = n - 1\\) 2. 一般的，一定有一条路径包含0和1，则可以确定 \\(\\text{MEX} \\geq 2\\) ，观察发现，对于度数 \\(\\geq 3\\) 的点，我们在他的三条边赋值为0, 1, 2使得其他路径…"
excerpt: "C. Ehab and Path-etic MEXs 1. 对于成链的情况， \\(\\text{MEX} = n - 1\\) 2. 一般的，一定有一条路径包含0和1，则可以确定 \\(\\text{MEX} \\geq 2\\) ，观察发现，对于度数 \\(\\geq 3\\) 的点，我们在他的三条边赋值为0, 1, 2使得其他路径…"
categories: []
tags: ["contest", "constructive algorithms"]
comments: false
related_posts: false
---
{% raw %}
[C. Ehab and Path-etic MEXs](https://codeforces.com/problemset/problem/1325/C "C. Ehab and Path-etic MEXs")

1. 对于成链的情况，<span class="math inline">\(\text{MEX} = n - 1\)</span>
2. 一般的，一定有一条路径包含0和1，则可以确定<span class="math inline">\(\text{MEX} \geq 2\)</span>，观察发现，对于度数<span class="math inline">\(\geq 3\)</span>的点，我们在他的三条边赋值为0, 1, 2使得其他路径的边有:

- 0,1,...
- 0,2,...
- 1,2,...  
  即一条路径上的边不能同时有0,1,2，使得<span class="math inline">\(\text{MEX} \leq 2\)</span>，对其他边任意赋值即可



```cpp
int n, ans[N];
vector<int> e[N];

void solve()
{
    cin>>n;
    for(int i = 1; i <= n - 1; i++)
    {
        int u, v;   cin>>u>>v;
        e[u].push_back(i);
        e[v].push_back(i);
        ans[i] = -1;
    }
    int vex = 0, cur = 0;
    for(int i = 1; i <= n; i++)
        if(e[i].size() >= 3)
            vex = i;
    for(auto &v : e[vex])
        ans[v] = cur++;
    for(int i = 1; i <= n - 1; i++)
    {
        if(ans[i] == -1)
            ans[i] = cur++;
        cout<<ans[i]<<endl;
    }
    return;
}
```
{% endraw %}
