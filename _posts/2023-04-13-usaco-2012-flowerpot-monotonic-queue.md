---
layout: post
title: "[USACO12MAR]Flowerpot S 单调队列"
date: 2023-04-13 21:23:00 +0800
updated: 2023-04-13 21:24:00 +0800
description: "[[USACO12MAR]Flowerpot S](https://www.luogu.com.cn/problem/P2698 \"[USACO12MAR]Flowerpot S\") tag:单调队列 很惭愧，今天发现自己连滑动窗口都不会了，遂做了一些题 两滴水的高度之差大于等于D的情况下的最小花盆宽度 暴力思路：对…"
excerpt: "[[USACO12MAR]Flowerpot S](https://www.luogu.com.cn/problem/P2698 \"[USACO12MAR]Flowerpot S\") tag:单调队列 很惭愧，今天发现自己连滑动窗口都不会了，遂做了一些题 两滴水的高度之差大于等于D的情况下的最小花盆宽度 暴力思路：对…"
categories: []
tags: ["algorithm basics", "data structures"]
comments: false
related_posts: false
---
{% raw %}
[[USACO12MAR]Flowerpot S](https://www.luogu.com.cn/problem/P2698 "[USACO12MAR]Flowerpot S")

tag:单调队列

很惭愧，今天发现自己连滑动窗口都不会了，遂做了一些题

两滴水的高度之差大于等于D的情况下的最小花盆宽度

暴力思路：对于任意两点求水滴高度差是否大于等于D，若大于等于<span class="math inline">\(D\)</span>则计算最下的两点距离 <span class="math inline">\(w\)</span>

但这显然是能过但不完全过，手玩一下样例，是求<span class="math inline">\(\text{区间的最小长度}\)</span>，在<span class="math inline">\(\text{区间最大值和区间最小值的差}\)</span> <span class="math inline">\(\geq D\)</span>的情况下。

那么答案即为:



```cpp
	ans = min(ans, a[i].fi - a[l].fi);
```



发现和滑动窗口很像，但每次往区间加入元素，那如何区间弹出元素？  
只要计算答案的时候每次左移<span class="math inline">\(\text{区间左端点}l\)</span>即可，



```cpp
//  AC one more times

#include <bits/stdc++.h>

using namespace std;

#define fi first
#define se second
#define pb push_back
#define endl '\n'
#define all(x) (x).begin(), (x).end()
#define inf64 0x3f3f3f3f3f3f3f3f

typedef long long ll;
typedef unsigned long long ull;
typedef pair<int, int> pii;
typedef pair<long long,long long> pll;

const int mod = 1e9 + 7;
const int N = 1e5 + 10;




int n, d;
int q1[N], q2[N];
//  max    min
int h1 = 1, t1 = 0, h2 = 1, t2 = 0;
pii a[N];


void solve()
{
    cin>>n>>d;
    for(int i = 1; i <= n; i++)
        cin>>a[i].fi>>a[i].se;

    sort(a + 1, a + n + 1);
    int l = 1;
    int ans = 1e9;
    for(int i = 1; i <= n; i++)
    {
        while(h1 <= t1 && a[q1[t1]].se < a[i].se)
            t1--;
        q1[++t1] = i;

        while(h2 <= t2 && a[q2[t2]].se > a[i].se)
            t2--;
            
        q2[++t2] = i;
        while(l <= i && a[q1[h1]].se - a[q2[h2]].se >=d)
        {
            ans = min(ans, a[i].fi - a[l].fi);
            l++;
            while(h1 <= t1 && q1[h1] < l)
                h1++;
            while(h2 <= t2 && q2[h2] < l)
                h2++;
        }
    }

    if(ans == 1e9)
    {
        cout<<-1<<endl;
    }
    else
        cout<<ans<<endl;



    return;
}


int main()
{
    std::ios::sync_with_stdio(false);   cin.tie(nullptr), cout.tie(nullptr);
    // 特殊输入 请注释上方，如__int128等
    int TC = 1;
    //cin >> TC;
    for(int tc = 1; tc <= TC; tc++)
    {
        //cout << "Case #" << tc << ": ";
        solve();
    }


    return 0;
}

```
{% endraw %}
