---
layout: post
title: "Educational Codeforces Round 6 A - E"
date: 2023-09-03 02:15:00 +0800
updated: 2023-09-03 02:15:00 +0800
description: "Educational Codeforces Round 6 目录 - Educational Codeforces Round 6 - A - Professor GukiZ's Robot - B - Grandfather Dovlet’s calculator - C - Pearls in a Row…"
excerpt: "Educational Codeforces Round 6 目录 - Educational Codeforces Round 6 - A - Professor GukiZ's Robot - B - Grandfather Dovlet’s calculator - C - Pearls in a Row…"
categories: []
tags: ["mathematics", "data structures", "contest", "dynamic programming", "algorithm basics"]
comments: false
related_posts: false
---
{% raw %}
# [Educational Codeforces Round 6](https://codeforces.com/contest/620)

目录

- [Educational Codeforces Round 6](/blog/2023/educational-codeforces-round-6/#educational-codeforces-round-6)
  - [A - Professor GukiZ's Robot](/blog/2023/educational-codeforces-round-6/#a---professor-gukizs-robot)
  - [B - Grandfather Dovlet’s calculator](/blog/2023/educational-codeforces-round-6/#b---grandfather-dovlets-calculator)
  - [C - Pearls in a Row](/blog/2023/educational-codeforces-round-6/#c---pearls-in-a-row)
  - [D - Professor GukiZ and Two Arrays](/blog/2023/educational-codeforces-round-6/#d---professor-gukiz-and-two-arrays)
  - [E - New Year Tree](/blog/2023/educational-codeforces-round-6/#e---new-year-tree)

## [A - Professor GukiZ's Robot](https://codeforces.com/contest/620/problem/A)

易得 <span class="math inline">\(\max(abs(x2 - x1), abs(y2 - y1))\)</span>



```cpp
void solve()
{       
    ll a, b, x, y;
    cin>>a>>b>>x>>y;
    ll t1 = abs(x - a);
    ll t2 = abs(y - b);
    cout<<max(t1, t2)<<'\n';
    return;
}
```



## [B - Grandfather Dovlet’s calculator](https://codeforces.com/contest/620/problem/B)

直接暴力判断



```cpp
int d[] = {6, 2, 5, 5, 4, 5, 6, 3, 7, 6};
void solve()
{       
    int res = 0;
    int l, r;   cin>>l>>r;
    for(int i = l; i <= r; i++)
    {
        int t = i;
        while(t)
        {
            res += d[t % 10];
            t /= 10;
        }
    }
    cout<<res<<'\n';
    return;
}
```



## [C - Pearls in a Row](https://codeforces.com/contest/620/problem/C)

定义 <span class="math inline">\(f_i\)</span> 为考虑前 <span class="math inline">\(i\)</span> 个数，其区间最多的数量

我们先存下每个数 <span class="math inline">\(x\)</span> 的下一个位置 <span class="math inline">\(last\)</span>

于是转移方程

<div class="math display">\[f_{last} = \max(f_{i - 1} + 1, f_i - 1);
\]</div>

然后倒着求出区间，再对区间扩宽一下



```cpp
const int N = 3e5 + 10;
 
 
int n, a[N], cnt;
vector<pair<int, int>> res;
vector<int> e[N];
map<int, int> mp;
int f[N]; 
void solve()
{       
    cin>>n;
    for(int i = 1; i <= n; i++)
    {
        cin>>a[i];
        if(mp[a[i]] == 0)   mp[a[i]] = ++cnt;
        a[i] = mp[a[i]];
        e[a[i]].push_back(i);
    }
    for(int i = 1; i <= n; i++)
    {
        f[i] = max(f[i - 1], f[i]);
        int p = lower_bound(e[a[i]].begin(), e[a[i]].end(), i) - e[a[i]].begin();
        int len = e[a[i]].size();
        if(p + 1 < len)
            f[e[a[i]][p + 1]] = max(f[i - 1] + 1, f[e[a[i]][p + 1]]);
        // cout<<i<<"  "<<f[i]<<'\n';
    }
    if(f[n] == 0)
    {
        cout<<-1<<'\n';return;
    }
    cout<<f[n]<<'\n';
    int t = f[n];
    for(int i = n; i >= 1; i--)
    {
        int p = lower_bound(e[a[i]].begin(), e[a[i]].end(), i) - e[a[i]].begin();
        if(p >= 1 && f[e[a[i]][p - 1] - 1] == t - 1)
        {
            // cout<<e[a[i]][p - 1]<<" "<<i<<'\n';
            res.push_back({e[a[i]][p - 1], i});
            t--;
            i = e[a[i]][p - 1];
        }
    }
    sort(res.begin(), res.end());
    res[0].first = 1;
    for(int i = 0; i < f[n] - 1; i++)
    {
        // cout<<i<<" "<<i + 1<<'\n';
        res[i].second = res[i + 1].first - 1;
    }
 
    res[f[n] - 1].second = n;
    for(auto [l, r] : res)
        cout<<l<<" "<<r<<'\n';
    return;
}
```



## [D - Professor GukiZ and Two Arrays](https://codeforces.com/contest/620/problem/D)

3 种情况:

1. 不换
2. 换一个
3. 换两个

   对于前两种我们可以在 <span class="math inline">\(O(N)\)</span> 或 <span class="math inline">\(O(N^2)\)</span> 内求出来，也比较简单

   <span class="math inline">\(s1\)</span> 代表 a 数组之和， s2 代表 b 数组之和

   但第三种直接枚举所有情况有 <span class="math inline">\(O(N^4)\)</span> 种，看上去不能直接做这时候注意到 <span class="math inline">\(res = \min abs(s1 - x + z - s2 - x + z)\)</span>，可以试着去枚举 <span class="math inline">\(x\)</span>，使<span class="math inline">\(s1 - s2 - 2 \times x + 2 \times z\)</span> 尽可能接近 <span class="math inline">\(0\)</span>，那就可以用到二分了，注意我们二分 <span class="math inline">\(s1 - s2 - 2 \times x + 2 \times z \geq 0\)</span>，其中 <span class="math inline">\(abs(s1 - s2 - 2 \times x + 2 \times z)\)</span>的最小值可能出现到<span class="math inline">\(s1 - s2 - 2 \times x + 2 \times z &lt; 0\)</span> 的时候，所以我们二分的时候多求一下答案即可，时间复杂度 <span class="math inline">\(O(N^2\log N^2)\)</span>

   

```cpp
// LUOGU_RID: 123639937
// AC one more times

#include <bits/stdc++.h>

using namespace std;

typedef long long ll;

const int mod = 1e9 + 7;
const int N = 4e6 + 10;

int n, m;
vector<array<ll, 3>> e1, e2;
ll a[N], b[N], s1, s2, res;

int p1 = -1, p2 = -1, p3 = -1, p4 = -1;

void calc(ll t, ll x, ll y, ll z, ll pos)
{
    if(pos < 0 || pos > m 
        || (z == -1 && e2[pos][2] >= 1) 
        || (z >= 1 && e2[pos][2] == -1))
        return;
    // cout<<t<<"  "<<x<<" "<<y<<" "<<e4[pos].first<<'\n';
    // cout<<" res: "<<res<<"  ";
    if(abs(t - 2ll * x + 2ll * e2[pos][0]) < res)
    {
        res = abs(t - 2ll * x + 2ll * e2[pos][0]);
        p1 = y, p2 = e2[pos][1];
        p3 = z, p4 = e2[pos][2];
    }
    // cout<<res<<'\n';
}

void solve()
{       
    cin>>n;
    for(int i = 1; i <= n; i++)
    {
        cin>>a[i];
        s1 += a[i];
    }   
    cin>>m;
    for(int i = 1; i <= m; i++)
    {
        cin>>b[i];
        s2 += b[i];
    }   
    if(s1 == s2)
    {
        cout<<0<<'\n';
        cout<<0<<'\n';
        return;
    }
    ll t = s1 - s2;
    res = abs(s1 - s2);
    for(int i = 1; i <= n; i++)
        for(int j = 1; j <= m; j++)
            if(abs(s1 - a[i] + b[j] - (s2 + a[i] - b[j])) < res)
            {
                res = abs(s1 - a[i] + b[j] - (s2 + a[i] - b[j]));
                p1 = i, p2 = j;
            }
    for(int i = 1; i <= n; i++)
        for(int j = i + 1; j <= n; j++)
            e1.push_back({a[i] + a[j], i, j});
    for(int i = 1; i <= m; i++)
        for(int j = i + 1; j <= m; j++)
            e2.push_back({b[i] + b[j], i, j});
    sort(e2.begin(), e2.end());
    m = e2.size() - 1;
    for(auto [x, y, z] : e1)
    {
        ll t1 = t - 2ll * x;
        ll l = 0, r = m;
        while(l < r)
        {
            ll mid = (l + r) >> 1;
            calc(t, x, y, z, mid);
            calc(t, x, y, z, mid + 1);
            if(t1 + 2ll * e2[mid][0] >= 0)    r = mid;
            else l = mid + 1;
        } 
    }

    if(p1 == -1)
    {
        cout<<res<<"\n"<<0<<'\n';        
    }
    else if(p3 == -1)
    {
        cout<<res<<'\n'<<1<<"\n"<<p1<<" "<<p2<<'\n';
    }
    else
    {
        cout<<res<<'\n'<<2<<"\n"<<p1<<" "<<p2<<'\n'<<p3<<" "<<p4<<'\n';
    }
    return;
}
```



   ## [E - New Year Tree](https://codeforces.com/contest/620/problem/E)

   DFS序 + 线段树

   如果直接对线段树的每个节点开个数组，那么空间是无法接受的，但是颜色最多只有 <span class="math inline">\(60\)</span> 种，我们可以考虑二进制去维护颜色种类和标记

   具体的其中 <span class="math inline">\(c = 1000001_2\)</span> ，第 <span class="math inline">\(i\)</span> 位为 <span class="math inline">\(1\)</span> 代表存在 第 <span class="math inline">\(i + 1\)</span> 种颜色（为了与代码对应）

   

```cpp
//  AC one more times
#include <bits/stdc++.h>

using namespace std;

typedef long long ll;

const int mod = 1e9+7;
const int N = 4e5+10;

struct info 
{
    ll col;
};


struct segtree 
{
    struct info val;
    ll tag, sz;
}seg[N * 4];
int l[N], r[N], tot, tid[N], c[N];
vector<int> e[N];
info operator +(const info &a, const info &b)
{
    info t;
    t.col = 0;
   // cout<<"a  b:  "<<a.col<<" "<<b.col<<endl;
    for(ll i = 1; i <= 60; i++)
        if( a.col & (1ll << i) || b.col & (1ll << i))
        {
           // cout<<"1<<i: "<<(1ll<<i)<<endl;
            t.col |= (1ll << i);
          // cout<<"t.col "<<t.col<<endl;
        }
    
    return t;
}
void update(int id)
{
  //  cout<<id<<endl;
    seg[id].val = seg[id * 2].val + seg[id * 2 + 1].val;
   // cout<<"col:: "<<id<<" " <<seg[id].val.col<<" \n";
}
void build(int id,int tl, int tr)
{
    seg[id].sz = tr - tl + 1;
    if(tl == tr)
    {
        seg[id].val.col = (1ll << c[tid[tl]]);
       // cout<<seg[id].val.col<<" ";
        return;
    }
    int mid = (tl + tr) >> 1;
    build(id * 2, tl, mid);
    build(id * 2 + 1, mid + 1, tr);
    update(id);
}
void settag(int id, ll col)
{
    seg[id].tag = col;
    seg[id].val.col = (1ll << col);
}
void pushdown(int id)
{
    if(seg[id].tag != 0)
    {
        settag(id * 2, seg[id].tag);
        settag(id * 2 + 1,seg[id].tag);
        seg[id].tag = 0;
    }
}
void modify(int id, int tl, int tr, int ql, int qr, ll col)
{
    //cout<<id<<" "<<tl<<" "<<tr<<" " << ql<<" "<<qr<<"  "<<col<<endl;
    if(ql == tl && qr == tr)
    {
        settag(id, col);
        return;
    }
    pushdown(id);
    int mid = (tl + tr) >> 1;
    if(qr <= mid)
        modify(id * 2, tl, mid, ql, qr, col);
    else if(ql > mid)
        modify(id * 2 + 1, mid + 1, tr, ql, qr, col);
    else 
        modify(id * 2, tl, mid, ql, mid, col),
        modify(id * 2 + 1, mid + 1, tr, mid + 1, qr, col);
    update(id);
}
info query(int id, int tl, int tr, int ql, int qr)
{
    if(tl == ql && tr == qr)
    {
        return seg[id].val;
    }
    pushdown(id);
    int mid = (tl + tr) >> 1;
    if(qr <= mid)
        return query(id * 2, tl, mid, ql, qr);
    else if(ql > mid)
        return query(id * 2 + 1, mid + 1, tr, ql, qr);
    else 
        return query(id * 2, tl, mid, ql, mid) +
               query(id * 2 + 1, mid + 1, tr, mid + 1, qr);
}
void dfs(int u, int fa)
{
    l[u] = ++tot;
    tid[tot] = u;
    for(int v : e[u])
    {
        if(v == fa)   continue;
        dfs(v, u);
    }
    r[u] = tot;
}
void solve()
{
    int n, q;
    cin>>n>>q;
    for(int i = 1; i <= n; i++)
        cin>>c[i];
        
    for(int i = 1; i <= n - 1; i++)
    {
        int u, v;    cin>>u>>v;
        e[u].push_back(v);     e[v].push_back(u);
    }
    dfs(1, -1);
    /*
7 2
1 1 1 1 1 1 1
1 2
1 3
1 4
3 5
3 6
3 7
1 3 2
2 1
*/
    /*
    for(int i=1;i<=n;i++)
        cout<<l[i]<<" ";
    cout<<endl;
    for(int i=1;i<=n;i++)
        cout<<r[i]<<" ";
    cout<<endl;
    for(int i=1;i<=n;i++)
        cout<<tid[i]<<" ";
    cout<<endl;    
    */
    build(1, 1, n);
            //cout<<"-------------\n";

    for(int i = 1; i <= q; i++)
    {
        int op; cin>>op;
        if(op == 1)
        {
            ll u, cc;  cin>>u>>cc;
           // u=tid[u];
       //     cout<<"-----------\n";
            modify(1, 1, n, l[u], r[u], cc);
     //      cout<<"--------------\n";
     //       cout<<l[u]<<" "<<r[u]<<" "<<cc<<endl;
        }
        else 
        {
            int u;  cin>>u;
            //u=tid[u];
            info t = query(1, 1, n, l[u], r[u]);
            int ans = 0;
           // cout<<t.col<<endl;
            for(ll i = 1; i <= 60; i++)
            {
                if((1ll << i) & t.col)
                    ans++;
                //cout<<i<<" "<<t.col[i]<<endl;
            }
            cout<<ans<<'\n';
        }
        //cout<<"-------------\n";

    }
    
    return;
}

  
int main()
{
    std::ios::sync_with_stdio(false);   cin.tie(nullptr), cout.tie(nullptr);
  
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
