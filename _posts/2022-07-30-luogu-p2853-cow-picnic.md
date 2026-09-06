---
layout: post
title: "P2853 [USACO06DEC]Cow Picnic S"
date: 2022-07-30 16:51:00 +0800
updated: 2022-07-31 10:08:00 +0800
description: "[P2853 [USACO06DEC]Cow Picnic S](https://www.luogu.com.cn/problem/P2853) 和这道差不多P3916 图的遍历，图的遍历通过方向建边使子节点被标记最大编号。这题可以通过奶牛找牧场 分析：从奶牛的位置开始dfs，对每个被dfs的点进行标记，最后统计有多…"
excerpt: "[P2853 [USACO06DEC]Cow Picnic S](https://www.luogu.com.cn/problem/P2853) 和这道差不多P3916 图的遍历，图的遍历通过方向建边使子节点被标记最大编号。这题可以通过奶牛找牧场 分析：从奶牛的位置开始dfs，对每个被dfs的点进行标记，最后统计有多…"
categories: []
tags: ["graph theory"]
comments: false
related_posts: false
---
{% raw %}
# [P2853 [USACO06DEC]Cow Picnic S](https://www.luogu.com.cn/problem/P2853)

 

# 和这道差不多[P3916 图的遍历](https://www.luogu.com.cn/problem/P3916)，图的遍历通过方向建边使子节点被标记最大编号。这题可以通过奶牛找牧场

分析：从奶牛的位置开始dfs，对每个被dfs的点进行标记，最后统计有多少个点的标记的数量等于奶牛的值。

代码：



```
#include<iostream>
#include<algorithm>
#include<string>
#include<cstring>
#include<vector>


using namespace std;
int k,n,m;
vector<int> edge[10010];
bool st[1010];
int pos[1010];
int cnt[1010];
void dfs(int u)
{
    cnt[u]++;
    st[u]=true;
    for(auto v:edge[u])
        if(st[v]==false)
            dfs(v);
}
int main()
{
    cin>>k>>n>>m;
    for(int i=1;i<=k;i++)   cin>>pos[i];
    for(int i=1;i<=m;i++)
    {
        int u,v;    cin>>u>>v;
        edge[u].push_back(v);
    }
    for(int i=1;i<=k;i++)
    {
        memset(st,false,sizeof st);
        dfs(pos[i]);
    }
    int ans=0;
    for(int i=1;i<=n;i++)
        if(cnt[i]==k)    ans++;
    
    cout<<ans<<endl;
    return 0;
}
```
{% endraw %}
