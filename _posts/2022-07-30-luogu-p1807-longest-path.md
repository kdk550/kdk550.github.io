---
layout: post
title: "P1807 最长路"
date: 2022-07-30 16:14:00 +0800
updated: 2022-07-31 10:08:00 +0800
description: "P1807 最长路 在DAG上拓扑排序dp，题目数据没有环 分析： f[v]=max(f[v],f[u]+value[u][i];"
excerpt: "P1807 最长路 在DAG上拓扑排序dp，题目数据没有环 分析： f[v]=max(f[v],f[u]+value[u][i];"
categories: []
tags: ["graph theory"]
comments: false
related_posts: false
---
{% raw %}
# [P1807 最长路](https://www.luogu.com.cn/problem/P1807)

在DAG上拓扑排序dp，题目数据没有环

分析：   f[v]=max(f[v],f[u]+value[u][i];



```
#include<iostream>
#include<cstring>
#include<vector>
#include<set>
#include<map>
#include<queue>
#include<algorithm>
using namespace std;


const int mod=80112002;
vector<int> son[100010],value[100010];
int in[100010],out[100010];
long long f[100010],ans=0;
int n,m;
void bfs()
{ 
    queue<int> q;
    for(int i=1;i<=n;i++)   
    {
        f[i]=-1e9;
        if(in[i]==0)
            q.push(i);
    }
    f[1]=0;
    while(!q.empty())
    {
        int u=q.front();q.pop();
        //cout<<u<<" ";
        int len=son[u].size();
        for(int i=0;i<len;i++)
        {
            int v=son[u][i];
            f[v]=max(f[v],f[u]+value[u][i]);
            if(--in[v]==0)
            {
                q.push(v);
            }
        }
    }
    if(f[n]!=-1e9)cout<<f[n]<<endl;
    else cout<<-1<<endl;
}

int main()
{
    cin>>n>>m;
    for(int i=1;i<=m;i++)
    {
        int x,y,z;    cin>>x>>y>>z;
        son[x].push_back(y);
        value[x].push_back(z);
        in[y]++,out[x]++;
    }
    bfs();
    return 0;
}
```
{% endraw %}
