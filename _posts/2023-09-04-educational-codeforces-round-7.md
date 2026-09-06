---
layout: post
title: "Educational Codeforces Round 7 A - E"
date: 2023-09-04 00:57:00 +0800
updated: 2023-09-04 00:58:00 +0800
description: "Educational Codeforces Round 7 目录 - Educational Codeforces Round 7 - A - Infinite Sequence - B - The Time - C - Not Equal on a Segment - D - Optimal Number Per…"
excerpt: "Educational Codeforces Round 7 目录 - Educational Codeforces Round 7 - A - Infinite Sequence - B - The Time - C - Not Equal on a Segment - D - Optimal Number Per…"
categories: []
tags: ["contest", "dynamic programming", "algorithm basics"]
comments: false
related_posts: false
---
{% raw %}
# [Educational Codeforces Round 7](https://codeforces.com/contest/622)

目录

- [Educational Codeforces Round 7](/blog/2023/educational-codeforces-round-7/#educational-codeforces-round-7)
  - [A - Infinite Sequence](/blog/2023/educational-codeforces-round-7/#a---infinite-sequence)
  - [B - The Time](/blog/2023/educational-codeforces-round-7/#b---the-time)
  - [C - Not Equal on a Segment](/blog/2023/educational-codeforces-round-7/#c---not-equal-on-a-segment)
  - [D - Optimal Number Permutation](/blog/2023/educational-codeforces-round-7/#d---optimal-number-permutation)
  - [E - Ants in Leaves](/blog/2023/educational-codeforces-round-7/#e---ants-in-leaves)

## [A - Infinite Sequence](https://codeforces.com/contest/622/problem/A)

简单数学，直接暴力模拟



```cpp
void solve()
{       
    ll n;   cin>>n;
    ll s = 0, base = 1;
    while(s + base < n)
    {
        s += base;
        base++;
    }
    cout<<n - s<<'\n';
    return;
}
```



## [B - The Time](https://codeforces.com/contest/622/problem/B)

模拟时间



```cpp
void solve()
{       
    char a,b,c,d,e;
    cin>>a>>b>>e>>c>>d;
    int t = (a - '0') * 10 * 60 + (b - '0') * 60 
    + (c - '0') * 10 + (d - '0');
    int add;    cin>>add;
    t += add;
    int h = t / 60;
    h %= 24;
    int m = t % 60;
    if(h < 10)  cout<<0<<h;
    else   cout<<h;
    cout<<":";
    if(m < 10)  cout<<0<<m;
    else   cout<<m;
    cout<<'\n';
    return;
}
 
```



## [C - Not Equal on a Segment](https://codeforces.com/contest/622/problem/C)

我的做法是 对于<span class="math inline">\([l, r]\)</span> 区间，其区间最大值和最小值都等于 <span class="math inline">\(x\)</span> ，那么一定无解，相反的，只要最大值不等于 <span class="math inline">\(x\)</span> ，或最小值不等于 <span class="math inline">\(x\)</span> 那么一定有解，我们用 ST表处理区间最值，并维护位置即可

看了题解发现只要维护与自己相同前一个数的下标即可



```cpp
typedef long long ll;

ll n, s;
 
bool check(ll x)
{
    ll t = x;
    ll sub = 0;
    while(t)
    {
        t /= 10;
        sub += 9;
    }
    if(x - sub >= s)
        return true;
    else return false;
}
void solve()
{       
    cin>>n>>s;
    ll l = 1, r = n + 2;
    while(l < r)
    { 
        ll mid = (l + r) >> 1;
        if(check(mid))  r = mid;
        else l = mid + 1;
    }
    ll res = 0;
    if(l <= n && check(l))    res = n - l + 1;
    // cout<<l<<" "<<res<<'\n';
 
    // cout<<l<<" "<<res<<'\n';
    if(l > n)   l = n + 1;
    
    for(ll i = s; i <= l - 1; i++)
    {
        ll t = i;
        ll sub = 0;
        while(t)
        {
            sub = sub + (t % 10);
            t /= 10;
        }
        if(i - sub >= s)    res++;
 
    }
    cout<<res<<'\n';
 
    return;
}

```



## [D - Optimal Number Permutation](https://codeforces.com/contest/622/problem/D)

观察到:

- <span class="math inline">\(i = n\)</span>时贡献为 <span class="math inline">\(0\)</span>
- 其他贡献为 <span class="math inline">\((n - i) \times |y_i - x_i + i - n|\)</span>
- 不难发现可以构造出 <span class="math inline">\(y_i - x_i = -(i - n)\)</span> ，使得 <span class="math inline">\(|y_i - x_i + i - n| = 0\)</span>
- 打表发现，<span class="math inline">\(1\)</span> 的距离要是 <span class="math inline">\(n - 1\)</span>，更多的 <span class="math inline">\(i\)</span> 的距离要是 <span class="math inline">\(n - i\)</span>
- 手动放一个<span class="math inline">\(n = 9\)</span> 的情况，<span class="math inline">\(1,3,5,7,9,7,5,3,1,2,4,6,8,8,6,4,2,9\)</span>， <span class="math inline">\(n = 10\)</span> 的情况，<span class="math inline">\(1,3,5,7,9,9,7,5,3,1,2,4,6,8,10,8,6,4,2,10\)</span>
- 发现了奇数，偶数分开放，<span class="math inline">\(n\)</span> 来插空（取决于 <span class="math inline">\(n\)</span> 的奇偶性）



```cpp
int n;
void solve()
{       
    cin>>n;
    for(int i = 1; i < n; i += 2)
        cout<<i<<" ";
    if(n & 1)
        cout<<n<<" ";
    for(int i = ((n - 1) % 2 == 1 ? n - 1 : n - 2); i >= 1; i -= 2)
        cout<<i<<" ";
    for(int i = 2; i < n; i += 2)
        cout<<i<<" ";
    if(n % 2 == 0)
        cout<<n<<" ";
    for(int i = ((n - 1) % 2 == 0 ? n - 1 : n - 2); i >= 1; i -= 2)
        cout<<i<<" ";
    cout<<n;
    cout<<'\n';
    
    return;
}
```



## [E - Ants in Leaves](https://codeforces.com/contest/622/problem/E)

对于相同时间在相同节点排队的贡献是排队的蚂蚁数量

luogu的题解也说得很详细了

graph
1 --- 2
1 --- 3
1 --- 4
2 --- 5
2 --- 6
2 --- 7



```cpp
const int N = 5e5 + 10;


int n, m, a[N], dep[N];
vector<int> e[N];

void dfs(int u, int from)
{
    dep[u] = dep[from] + 1;
    bool ok = false;
    for(auto v : e[u])
    {
        if(v == from)   continue;
        ok = true;
        dfs(v, u);
    }
    if(!ok)
        a[++m] = dep[u];
}
void solve()
{       
    cin>>n;
    for(int i = 1; i < n; i++)
    {
        int u, v;   cin>>u>>v;
        e[u].push_back(v);
        e[v].push_back(u);
    }
    dep[1] = 0;
    int res = 0;
    for(auto v : e[1])
    {
        m = 0;
        dfs(v, 1);
        sort(a + 1, a + 1 + m);
        for(int i = 1; i <= m; i++) a[i] = max(a[i - 1] + 1, a[i]);
        res = max(a[m], res);
    }
    cout<<res<<'\n';
    return;
}
```
{% endraw %}
