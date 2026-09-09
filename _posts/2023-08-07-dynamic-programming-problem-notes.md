---
layout: post
title: "一些DP"
date: 2023-08-07 15:11:00 +0800
updated: 2023-08-08 21:38:00 +0800
description: "一些做题节选，整理动态规划、树形 DP 与图论题目的解题记录。"
excerpt: "一些做题节选，整理动态规划、树形 DP 与图论题目的解题记录。"
categories: []
tags: ["dynamic programming"]
comments: false
related_posts: false
---
{% raw %}
# 一些做题节选

目录

- [一些做题节选](/blog/2023/dynamic-programming-problem-notes/#一些做题节选)
  - [P1273 有线电视网](/blog/2023/dynamic-programming-problem-notes/#p1273-有线电视网)
  - [P2279 [HNOI2003] 消防局的设立](/blog/2023/dynamic-programming-problem-notes/#p2279-hnoi2003-消防局的设立)
  - [P5662 [CSP-J2019] 纪念品](/blog/2023/dynamic-programming-problem-notes/#p5662-csp-j2019-纪念品)
  - [CF219 Choosing Capital for Treeland](/blog/2023/dynamic-programming-problem-notes/#cf219-choosing-capital-for-treeland)
  - [CF767C Garland](/blog/2023/dynamic-programming-problem-notes/#cf767c-garland)
  - [ZJOI2007] 时态同步](/blog/2023/dynamic-programming-problem-notes/#zjoi2007-时态同步)
  - [P2279 [HNOI2003] 消防局的设立](/blog/2023/dynamic-programming-problem-notes/#p2279-hnoi2003-消防局的设立-1)
  - [P2899 [USACO08JAN] Cell Phone Network G](/blog/2023/dynamic-programming-problem-notes/#p2899-usaco08jan-cell-phone-network-g)
  - [P2986 [USACO10MAR] Great Cow Gathering G](/blog/2023/dynamic-programming-problem-notes/#p2986-usaco10mar-great-cow-gathering-g)
  - [P2585 [ZJOI2006] 三色二叉树](/blog/2023/dynamic-programming-problem-notes/#p2585-zjoi2006-三色二叉树)
  - [P1272 重建道路](/blog/2023/dynamic-programming-problem-notes/#p1272-重建道路)
  - [P3177 [HAOI2015] 树上染色](/blog/2023/dynamic-programming-problem-notes/#p3177-haoi2015-树上染色)
  - [P3174 [HAOI2009] 毛毛虫](/blog/2023/dynamic-programming-problem-notes/#p3174-haoi2009-毛毛虫)
  - [P3052 [USACO12MAR] Cows in a Skyscraper G](/blog/2023/dynamic-programming-problem-notes/#p3052-usaco12mar-cows-in-a-skyscraper-g)
  - [P2396 yyy loves Maths VII](/blog/2023/dynamic-programming-problem-notes/#p2396-yyy-loves-maths-vii)
  - [P2622 关灯问题II](/blog/2023/dynamic-programming-problem-notes/#p2622-关灯问题ii)
  - [P2915 [USACO08NOV] Mixed Up Cows G](/blog/2023/dynamic-programming-problem-notes/#p2915-usaco08nov-mixed-up-cows-g)

## [P1273 有线电视网](https://www.luogu.com.cn/problem/P1273)

树上背包的变形

<div class="math display">\[f_{u, j + k} =  \max_{v \in son(u)} f_{u, j} + f_{v, k} - w_{u,v}
\]</div>

这里写成 <span class="math inline">\(j + k\)</span> 是为了和代码一致。

<span class="math inline">\(f_{u,j + k}\)</span> 代表以 <span class="math inline">\(u\)</span> 为根的子树中，选择了 <span class="math inline">\(j + k\)</span> 个叶子结点的利润最大值。

<span class="math inline">\(w_{u, v}\)</span> 代表 <span class="math inline">\(u\)</span> 到 <span class="math inline">\(v\)</span> 的边权。

然后就是很朴素的树上背包了，注意维护的是利润的最大值，有负数出现，需要初始化一下，详细见代码。



```cpp
int n, m, w[N];
int sz[N], f[N][N], tmp[N], dep[N];
vector<pair<int, int>> e[N];
void dfs(int u)
{
    if(u >= n - m + 1)
    {
        f[u][1] = w[u];
        sz[u] = 1;
        return;
    }
    sz[u] = 0;
    for(auto [v, w] : e[u])
    {
        dfs(v);
        for(int i = 0; i <= sz[u] + sz[v]; i++)
            tmp[i] = f[u][i];
        for(int i = 0; i <= sz[u]; i++)
            for(int j = 0; j <= sz[v]; j++)
                tmp[i + j] = max(tmp[i + j], f[u][i] + f[v][j] - w);
        sz[u] += sz[v]; 
        for(int i = sz[u]; i >= 0; i--)
            f[u][i] = tmp[i];   
        // for(int i = sz[u]; i >= 0; i--)
        // {
        //     cout<<"U: "<<u<<"  V: "<<v<<"  sz[u]: "<<i<<"   f_u_sz: "<<f[u][i]<<'\n';
        // }
    }
}
void solve()
{       
    cin>>n>>m;
    for(int i = 1; i <= n - m; i++)
    {
        int k;  cin>>k;
        for(int j = 1; j <= k; j++)
        {
            int v, k;   cin>>v>>k;
            e[i].push_back({v, k});
        }
    }
    for(int i = n - m + 1; i <= n; i++)
        cin>>w[i];
    for(int i = 1; i <= n; i++)
    {
        f[i][0] = 0;
        for(int j = 1; j <= n; j++)
            f[i][j] = -inf;
    }

    dfs(1);
    for(int i = m; i >= 0; i--)
    {
        if(f[1][i] >= 0)
        {
            cout<<i<<'\n';
            return;
        }
    }
    return;
}

```



## [P2279 [HNOI2003] 消防局的设立](https://www.luogu.com.cn/problem/P2279)

类似题目[P2899 [USACO08JAN] Cell Phone Network G](https://www.luogu.com.cn/problem/P2899)，不同处在于只覆盖相邻的

  

设 <span class="math inline">\(f_{u, i}\)</span> 为以u为根的子树，消防局可以覆盖的范围，其中 <span class="math inline">\(i \in [0, 4]\)</span>，分别代表可以覆盖到 <span class="math inline">\(dep_u + 2\)</span>, <span class="math inline">\(dep_u + 1\)</span>, <span class="math inline">\(dep_u\)</span>,<span class="math inline">\(dep_u - 1\)</span>,<span class="math inline">\(dep_u - 2\)</span>层。

有转移方程

<div class="math display">\[f_{u, 0} = 1 + \sum_{v \in son(u)} f_{v, 4}
\\

f_{u, 1} = \sum_{v \in son(u)} f_{v, 3} - \max_{v \in son(u)} (f_{v,3} - f_{v, 0})
\\

f_{u, 2} = \sum_{v \in son(u)} f_{v, 2} - \max_{v \in son(u)} (f_{v, 2} - f_{v, 1})
\\

f_{u, 3} = \sum_{v \in son(u)} f_{v, 2}
\\

f_{u, 4} = \sum_{v \in son(u)} f_{v, 3}
\\
\]</div>

注意！还需要在dp中对最小值进行转移

`for(int i = 1; i <= 4; i++) f[u][i] = min(f[u][i - 1], f[u][i]);`



```cpp
int n;
int dep[N], f[N][10];    
vector<int> e[N];
void dfs(int u, int from)
{
    f[u][0] = 1;
    f[u][1] = f[u][2] = 1e8;
    int s1 = 0, s2 = 0;
    for(auto v : e[u])
    {
        if(v == from)   continue;  
        dfs(v, u); 
        f[u][0] = f[u][0] + f[v][4]; 
        s1 = s1 + f[v][3];
        s2 = s2 + f[v][2];
        f[u][3] = f[u][3] + f[v][2];
        f[u][4] = f[u][4] + f[v][3];
    }
    for(auto v : e[u])
    {
        if(v == from)   continue;  
        f[u][1] = min(s1 - f[v][3] + f[v][0], f[u][1]);
        f[u][2] = min(s2 - f[v][2] + f[v][1], f[u][2]);
    }
    for(int i = 1; i <= 4; i++)    f[u][i] = min(f[u][i - 1], f[u][i]);
}
void solve()
{       
    cin>>n;
    for(int v = 2; v <= n; v++)
    {
        int u;    cin>>u;
        e[u].push_back(v);
        e[v].push_back(u);
    }
    dfs(1, 0);
    cout<<min({f[1][0], f[1][1], f[1][2]})<<'\n';

    return;
}

```



## [P5662 [CSP-J2019] 纪念品](https://www.luogu.com.cn/problem/P5662)

只要领悟到当天买的可以当天卖，求出今天买明天卖的最大值，就很简单了



```cpp
int t, n, m, a[110][110], res;
int f[N];
void solve()
{       
    cin>>t>>n>>m;
    for(int i = 1; i <= t; i++)
        for(int j = 1; j <= n; j++)
            cin>>a[i][j];
    for(int k = 1; k < t; k++)
    {
	    memset(f, 0, sizeof f);
    	for(int i = 1; i <= n; i++)
    	{
	    	for(int j = a[k][i]; j <= m; j++)
	    		f[j] = max(f[j], f[j - a[k][i]] - a[k][i] + a[k + 1][i]);
	    }
	    m = max(f[m] + m, m);
    }
    cout<<m<<'\n';
    return;
}
```



![image-20230807142317075](/assets/img/blog/posts/image-20230807142317075.png)

后面蓝色大部分都是分组背包+完全背包的题

## [CF219 Choosing Capital for Treeland](https://www.luogu.com.cn/problem/CF219D)

换根dp

<span class="math inline">\(1\)</span> 为根结点, <span class="math inline">\(f_u\)</span> 为以 <span class="math inline">\(u\)</span> 为根的子树不需要反转的道路数量

<span class="math inline">\(g_v\)</span> 为以 <span class="math inline">\(v\)</span> 为整棵树的根结点，在以 <span class="math inline">\(1\)</span> 为整棵树的根结点下 <span class="math inline">\(v\)</span> 的父亲 <span class="math inline">\(u\)</span> 的子树不需要反转的道路数量

有点绕，不知道意思清不清晰



```cpp
f[u] = f[u] + f[v];
if(S.count({u, v})) f[u]++;
```




```cpp
g[v] = g[u] + f[u] - f[v] + (S.count({v, u}) ? 1 : -1);
```




```cpp
ll n, f[N], g[N];
vector<int> e[N];
set<pair<int, int>> S;
void dfs(int u, int from)
{
    for(auto v : e[u])
    {
        if(v == from)   continue;
        dfs(v, u);
        f[u] = f[u] + f[v];
        if(S.count({u, v})) f[u]++;
    } 
}
void dfs2(int u, int from)
{

    for(auto v : e[u])
    {
        if(v == from)   continue;
        g[v] = g[u] + f[u] - f[v] + (S.count({v, u}) ? 1 : -1);
        dfs2(v, u);        
    }
}


void solve()
{       

    cin>>n;
    for(int i = 1; i < n; i++)
    {
        int u, v;  cin>>u>>v;
        S.insert({u, v});
        e[u].push_back(v);
        e[v].push_back(u);
    }
    dfs(1, 0);
    dfs2(1, 0);
    int miv = -1;
    vector<int> res;
    for(int u = 1; u <= n; u++)
    {
        if(f[u] + g[u] > miv)
        {
            miv = f[u] + g[u];
            res.clear();
        }
        if(f[u] + g[u] == miv)
            res.push_back(u);
    }
    cout<<n - miv - 1<<'\n';
    for(auto u : res)
        cout<<u<<' ';
    cout<<'\n';


    return;
}
```



## [CF767C Garland](https://www.luogu.com.cn/problem/CF767C)

<span class="math inline">\(sum = \sum _ {i = 1} ^ {n} a_i\)</span>

<span class="math inline">\(f_u = a_u + \sum _ {v \in son(u)} f_v\)</span>

直接dfs判断是否有 <span class="math inline">\(f_u = sum / 3\)</span>

注意特判 <span class="math inline">\(u\)</span> 的次数可以出现超过2次，因为有负数点权,记得把子树情况，和 `sum % 3 != 0`的特判



```cpp
int n, f[N], w[N];
vector<int> e[N];
bool ok = true;
int res[N], cnt, sum;

void dfs(int u, int from)
{
    f[u] = w[u];
    for(auto v : e[u])
    {
        if(v == from)   continue;
        dfs(v, u);
        f[u] = f[u] + f[v];
    }
    if(f[u] == sum / 3)
    {
        f[u] = 0;
        res[++cnt] = u;
    }
    //f[u] = w[u];
}



void solve()
{       

    cin>>n;
    int root = 0;
    for(int i = 1; i <= n; i++)
    {
        int u;  cin>>u>>w[i];
        if(u == 0)  root = i;
        else e[u].push_back(i);
        sum += w[i];
    }
    //cout<<root<<'\n';
    dfs(root, 0);    
    if(sum % 3 != 0 || cnt <= 2)
    {
        cout<<-1<<'\n';
        return;
    }
    cout<<res[1]<<" "<<res[2]<<'\n';
    return;
}
```



## [ZJOI2007] 时态同步](https://www.luogu.com.cn/problem/P1131)

深度小的增长到深度大的

<span class="math inline">\(f_u = \max_{v \in son(u)} f_v + w\)</span>

<span class="math inline">\(res = \sum _ {u = 1} ^ {n} \sum _ {v \in son(u)} f_u - f_v - w\)</span>

<span class="math inline">\(w\)</span> 为 <span class="math inline">\(u\)</span> 和 <span class="math inline">\(v\)</span> 之间的边权



```cpp
int n;
ll dep[N], f[N];    
vector<pair<int, int>> e[N];
ll res;
void dfs(int u, int from)
{
    for(auto [v, w] : e[u])
    {
        if(v == from)   continue;  
        dfs(v, u);         
        f[u] = max(f[u], f[v] + w);
    }
    for(auto [v, w] : e[u])
    {
        if(v == from)   continue;
        res += (f[u] - f[v] - w);
    }
    
}
void solve()
{       
    cin>>n;
    int s;  cin>>s;
    for(int i = 1; i < n; i++)
    {
        int u, v, w;    cin>>u>>v>>w;
        e[u].push_back({v, w});
        e[v].push_back({u, w});
    }
    dfs(s, 0);
    cout<<res<<'\n';

    return;
}
```



## [P2279 [HNOI2003] 消防局的设立](https://www.luogu.com.cn/problem/P2279)

不是最大独立集

1 个点可以覆盖其爷爷，父亲，自己，也可以被儿子，孙子覆盖

考虑各个点之间的覆盖转移

注意转移最小值



```cpp
int n;
int dep[N], f[N][10];    
vector<int> e[N];
void dfs(int u, int from)
{
    f[u][0] = 1;
    f[u][1] = f[u][2] = 1e8;
    int s1 = 0, s2 = 0;
    for(auto v : e[u])
    {
        if(v == from)   continue;  
        dfs(v, u); 
        f[u][0] = f[u][0] + f[v][4]; 
        s1 = s1 + f[v][3];
        s2 = s2 + f[v][2];
        f[u][3] = f[u][3] + f[v][2];
        f[u][4] = f[u][4] + f[v][3];
    }
    for(auto v : e[u])
    {
        if(v == from)   continue;  
        f[u][1] = min(s1 - f[v][3] + f[v][0], f[u][1]);
        f[u][2] = min(s2 - f[v][2] + f[v][1], f[u][2]);
    }
    for(int i = 1; i <= 4; i++)    f[u][i] = min(f[u][i - 1], f[u][i]);
}
void solve()
{       
    cin>>n;
    for(int v = 2; v <= n; v++)
    {
        int u;    cin>>u;
        e[u].push_back(v);
        e[v].push_back(u);
    }
    dfs(1, 0);
    cout<<min({f[1][0], f[1][1], f[1][2]})<<'\n';

    return;
}


```



## [P2899 [USACO08JAN] Cell Phone Network G](https://www.luogu.com.cn/problem/P2899)

思路同上题

## [P2986 [USACO10MAR] Great Cow Gathering G](https://www.luogu.com.cn/problem/P2986)

换根dp



```cpp
int n;
ll m,c[N], f[N], g[N], sz[N];
vector<pll> e[N];

void dfs1(int u,int fa)
{
    for(auto v : e[u])
    {
        if(v.fi == fa) continue;
        dfs1(v.fi, u);
        sz[u] += sz[v.fi];
        f[u] += f[v.fi] + sz[v.fi] * v.se;
    }
    sz[u] += c[u];
}
void dfs2(int u,int fa)
{
    for(auto v : e[u])
    {
        if(v.fi == fa) continue;
        g[v.fi] = g[u] + f[u] - f[v.fi] - sz[v.fi] * v.se + (m - sz[v.fi]) * v.se;
        dfs2(v.fi, u);
    }
}
void solve()
{   
    cin>>n;
    for(int i = 1; i <= n; i++)
    {
        cin>>c[i];
        m += c[i];
    }

    for(int i = 1; i < n; i++)
    {
        ll u, v, w; cin>>u>>v>>w;
        e[u].pb({v, w});
        e[v].pb({u, w});
    }
    dfs1(1, 0);
    dfs2(1, 0);
    ll ans = 1e18;
    for(int i = 1; i <= n; i++)
        ans = min(ans, f[i] + g[i]);
    cout<<ans<<endl;
    return;
}
```



## [P2585 [ZJOI2006] 三色二叉树](https://www.luogu.com.cn/problem/P2585)

树形dp

我喜欢把树建出来再做



```cpp
int n;
int f[N][4], g[N][4];
// R G B
vector<int> e[N];
string s;
int cnt = 1;
int k = 0;
void build(int u)
{

    if(s[k] == '2')
    {
        int l = ++cnt, r = ++cnt;
        e[u].push_back(l);
        e[u].push_back(r);
        k++;
        build(l);
        build(r);
    }
    else if(s[k] == '1')
    {
        int l = ++cnt;
        e[u].push_back(l);
        k++;
        build(l);
    }
    else if(s[k] == '0')
        k++;
}
void dfs(int u, int from)
{
    for(auto v : e[u])
    {
        if(v == from)   continue;  
        dfs(v, u); 
    }
    if(e[u].size() == 2)
    {
        int v1 = e[u][0], v2 = e[u][1];
        f[u][1] = max({f[v1][2] + f[v2][3], f[v1][3] + f[v2][2]});
        f[u][2] = max({f[v1][1] + f[v2][3], f[v1][3] + f[v2][1]}) + 1;
        f[u][3] = max({f[v1][1] + f[v2][2], f[v1][2] + f[v2][1]});

        g[u][1] = min({g[v1][2] + g[v2][3], g[v1][3] + g[v2][2]});
        g[u][2] = min({g[v1][1] + g[v2][3], g[v1][3] + g[v2][1]}) + 1;
        g[u][3] = min({g[v1][1] + g[v2][2], g[v1][2] + g[v2][1]});
    }
    else if(e[u].size() == 1)
    {
        int v = e[u][0];
        f[u][1] = max(f[v][2], f[v][3]);
        f[u][2] = max(f[v][1], f[v][3]) + 1;
        f[u][3] = max(f[v][1], f[v][2]);

        g[u][1] = min(g[v][2], g[v][3]);
        g[u][2] = min(g[v][1], g[v][3]) + 1;
        g[u][3] = min(g[v][1], g[v][2]);
    }
    else
    {
        f[u][2] = g[u][2] = 1;
    }
}
void solve()
{       
    
    cin>>s;
    build(1);
    n = cnt;
    dfs(1, 0);
    cout<<max({f[1][1], f[1][2], f[1][3]})<<" "<<min({g[1][1], g[1][2], g[1][3]})<<'\n';
    return;
}
```



## [P1272 重建道路](https://www.luogu.com.cn/problem/P1272)

我的dp记录删除多少个点的最小代价，故复杂度是<span class="math inline">\(O(N^2)\)</span>



```cpp
int n, k;
vector<int> e[N];
int sz[N], f[N][N], tmp[N];
void dfs(int u, int from)
{
    f[u][0] = sz[u] = 0;
    for(auto v : e[u])
    {
        if(v == from)   continue;
        dfs(v, u);
        for(int i = 1; i <= sz[u] + sz[v]; i++)
            tmp[i] = inf;
        for(int i = 0; i <= sz[u]; i++)
        {
            for(int j = 0; j < sz[v]; j++)
                tmp[i + j] = min(tmp[i + j], f[u][i] + f[v][j]);
            tmp[i + sz[v]]  = min(tmp[i + sz[v]], f[u][i] + 1);
        }

        sz[u] += sz[v]; 
        for(int i = sz[u]; i >= 0; i--)
            f[u][i] = tmp[i];   
    }
    sz[u]++;
}
void solve()
{       
    cin>>n>>k;
    for(int i = 1; i < n; i++)
    {
        int u, v;   cin>>u>>v;
        e[u].push_back(v);
        e[v].push_back(u);
    }
    dfs(1, 0); 
    int res = f[1][n - k];
    for(int i = 2; i <= n; i++)
         if(sz[i] >= k)
            res = min(f[i][sz[i] - k] + 1, res);
    cout<<res<<'\n';
    return;
}
```



## [P3177 [HAOI2015] 树上染色](https://www.luogu.com.cn/problem/P3177)

一条边经过次数是 <span class="math inline">\(times = j \times (k - j) + (sz_v - j) \times (n - k + j - sz_v)\)</span>

<span class="math inline">\(j\)</span> 是子树的黑节点， <span class="math inline">\(sz_v\)</span> 是子树的结点数量



```cpp
const int N = 2e3 + 10;
const ll inf = 1ll << 60;
int n, k;
ll sz[N], w[N], f[N][N], tmp[N];
vector<pair<ll, ll>> e[N];
void dfs(int u, int from)
{
    f[u][0] = f[u][1] = 0;
    sz[u] = 1;
    for(auto [v, w] : e[u])
    {
        if(v == from)   continue;
        dfs(v, u);
        for(int i = 0; i <= sz[u] + sz[v]; i++)
            tmp[i] = -inf;
        for(int i = 0; i <= sz[u]; i++)
            for(int j = 0; j <= sz[v]; j++)
            {
                ll times = j * (k - j) + (sz[v] - j) * (n - k + j - sz[v]);
                tmp[i + j] = max(tmp[i + j], f[u][i] + f[v][j] + times * w);
            }
        sz[u] += sz[v]; 
        for(int i = sz[u]; i >= 0; i--)
            f[u][i] = tmp[i];   
    }
}

void solve()
{       
    cin>>n>>k;
    for(int i = 2; i <= n; i++)
    {
        int u, v, w;    cin>>u>>v>>w;
        e[u].push_back({v, w});
        e[v].push_back({u, w});
    }
    dfs(1, 0);
    cout<<f[1][k]<<'\n';
    return;
}

```



## [P3174 [HAOI2009] 毛毛虫](https://www.luogu.com.cn/problem/P3174)

树形dp

<div class="math display">\[f_u = \max _ {v \in son(u) f_v} + \max(\texttt{u的儿子个数},1)
\]</div>

代表以 <span class="math inline">\(u\)</span> 为根的子树的猫猫虫一半（或者说半条链？）

<span class="math inline">\(f_u\)</span> 这里没有考虑以 <span class="math inline">\(u\)</span> 为根的子树链由不同的两个子结点 <span class="math inline">\(v1\)</span>, <span class="math inline">\(v2\)</span> 拼成

graph
from --- u
u --- v1
u --- v2

所以要记录一下子树的次大值

<div class="math display">\[res = \max _ {u = 1} ^ {n} (f_u + [from != 0], f_u + m2 - 1 + [from != 0])
\]</div>

<span class="math inline">\(from\)</span> 代表 <span class="math inline">\(u\)</span> 的父亲，不要忘记算父亲的贡献了, <span class="math inline">\(m2\)</span> 是次大值

这里给了树边很迷惑，代码处理了不连通的情况（但树是一定连通的，而且将m=n-1，还是可以AC，给的就是树，m这个变量没用）



```cpp
const int N = 3e5 + 10;
int n, m;
int f[N];
int res = 1;
bool vis[N];
vector<int> e[N];
void dfs(int u, int from)
{
    vis[u] = true;
    int cnt = 0, m1 = 0, m2 = 0;
    for(auto v : e[u])
    {
        if(v == from)   continue;
        cnt++;
        dfs(v, u);
        if(f[v] >= m1)
            m2 = m1, m1 = f[v];
        else if(f[v] > m2)
            m2 = f[v];
        f[u] = max(f[v], f[u]);
    }
    f[u] = f[u] + (m1 == 0 ? 1 : cnt);
    res = max(f[u] + (from != 0), res);
    res = max(f[u] + m2 - 1 + (from != 0), res);        
}

void solve()
{       
    cin>>n>>m;
    for(int i = 1; i <= m; i++)
    {
        int u, v;    cin>>u>>v;
        e[u].push_back(v);
        e[v].push_back(u);
    }
    for(int i = 1; i <= n; i++)
        if(!vis[i])
            dfs(i, 0);
    cout<<res<<'\n';
    return;
}

```



## [P3052 [USACO12MAR] Cows in a Skyscraper G](https://www.luogu.com.cn/problem/P3052)

一样状压

<span class="math inline">\(f_{i, s}\)</span> 代表用了 <span class="math inline">\(i\)</span> 个背包， <span class="math inline">\(S\)</span> 是二进制下的数 ，<span class="math inline">\(S\)</span> 的第 <span class="math inline">\(k\)</span> 位为 <span class="math inline">\(1\)</span> 表示装了这个物品

时间复杂度 <span class="math inline">\(O(2^N N^2)\)</span>

初始化及其转移方程

<div class="math display">\[f_{1, (1 &lt;&lt; j)} = a_j
\\
f_{i, S + (1 &lt;&lt; j)} = \min f_{i, S} + a_j
\\
f_{i + 1, S + (1 &lt;&lt; j)} = \min a_j
\]</div><div class="math display">\[res = \min _{i = 1} ^ {n} i \times [f[i][(1 &lt;&lt; n) - 1] != inf]
\]</div>

答案写的有点抽象



```cpp
const int M = 18;
int n, m;
int f[M + 1][(1 << M) + 1], a[M + 1];

void solve()
{       
    cin>>n>>m;
    memset(f, 0x3f, sizeof f);
    int t = f[0][0];
    for(int i = 0; i < n; i++)
    {
        cin>>a[i];
        f[1][1 << i] = a[i];
    }
    for(int i = 0; i <= n; i++)
        for(int S = 0; S <= (1 << n) - 1; S++)
            if(f[i][S] != t)
                for(int j = 0; j < n; j++)
                {
                    if((S >> j) & 1)    continue;
                    if(f[i][S] + a[j] <= m)
                        f[i][S + (1 << j)] = min(f[i][S] + a[j], f[i][S + (1 << j)]);
                    else 
                        f[i + 1][S + (1 << j)] = min(a[j], f[i][S + (1 << j)]);
                }
    int res = n;
    for(int i = 1; i <= n; i++)
        if(f[i][(1 << n) - 1] != t)
            res = min(res, i);
    cout<<res<<'\n';
    return;
}
```



## [P2396 yyy loves Maths VII](https://www.luogu.com.cn/problem/P2396)

状压dp用lowbit优化

显然：

<div class="math display">\[f_{S} = \sum _ {i \in S} f_{S - (1 &lt;&lt; i)}
\]</div>

<span class="math inline">\(O(N2 ^ N)\)</span> TLE了

发现距离而言 ，状态 <span class="math inline">\(S\)</span> 能走到的距离可以由两段加起来，第一段是二进制数位下（从左往右）第一位数的距离贡献，第二段是之前算出过的距离，也就是<span class="math inline">\(\texttt{S - 第一位数的距离贡献}\)</span> ，显然可以转移，这个操作的时间复杂度 <span class="math inline">\(O(2^N)\)</span>， 有：

<div class="math display">\[g_{S} = g_{(S \&amp; - S)} + g_{S - (S \&amp; -S)}
\]</div>

前面算距离运用了lowbit，那算方案数呢？也使用lowbit优化，原理相似，这样复杂度 <span class="math inline">\(O(2^N \log N)\)</span> 就可以通过了



```cpp
const int M = 24;
int n, m;
int f[1 << M], g[1 << M], b[M];

void solve()
{       
    cin>>n;
    for(int i = 0; i < n; i++)
        cin>>g[1 << i];
    cin>>m;
    for(int i = 1; i <= m; i++)
        cin>>b[i];
    
    f[0] = 1;
    for(int S = 1; S < (1 << n); S++)
    {
        int st = S;
        g[S] = g[S - (S & -S)] + g[S & -S];
        if(g[S] == b[1] || g[S] == b[2])  continue;
        for(; st; st -= st & -st)
            f[S] = (f[S] + f[S - (st & -st)]) % mod;
    }
    cout<<f[(1 << n) - 1]<<'\n';
    return;
}
```



## [P2622 关灯问题II](https://www.luogu.com.cn/problem/P2622)

状压水题，容易发现状态之间转移和之前不一样，我们直接跑个bfs来转移即可

<span class="math inline">\(S\)</span> 代表二进制下的灯的状态，<span class="math inline">\(f_S\)</span> 代表到达 <span class="math inline">\(S\)</span> 状态按按钮的最少次数

<div class="math display">\[f_S = \min f_S' + 1
\]</div>

```cpp
const int M = 10;
int n, m;
int f[1 << M];
int a[110][11];
bool vis[1 << M];
void solve()
{       
    cin>>n>>m;
    for(int i = 1; i <= m; i++)
        for(int j = 0; j < n; j++)
            cin>>a[i][j];
    memset(f, 0x3f, sizeof f);
    int inf = f[0];
    f[(1 << n) - 1] = 0, vis[(1 << n) - 1] = true;
    queue<int> q;
    q.push((1 << n) - 1);
    while(q.size() >= 1)
    {
        auto S = q.front(); q.pop();
        for(int i = 1; i <= m; i++)
        {
            int st = S;
            for(int j = 0; j < n; j++)
            {
                if(a[i][j] == 1 && (st >> j) & 1)
                    st = st - (1 << j);
                else if(a[i][j] == -1 && !((st >> j) & 1))
                    st = st + (1 << j);
            }
            if(!vis[st])
            {
                vis[st] = true, f[st] = f[S] + 1;
                q.push({st});
            }
        }
    }
    if(f[0] >= inf) f[0] = -1;
    cout<<f[0]<<'\n';
    return;
}
```



## [P2915 [USACO08NOV] Mixed Up Cows G](https://www.luogu.com.cn/problem/P2915)

状压DP

<span class="math inline">\(f_{i, S}\)</span> 代表二进制状态下，以第 <span class="math inline">\(i\)</span> 头作为结尾的方案数， 其中<span class="math inline">\(S\)</span> 是二进制数，第 <span class="math inline">\(j\)</span> 位代表第 <span class="math inline">\(j\)</span> 头牛是否放进队列牛

考虑转移就有 把第 <span class="math inline">\(i\)</span> 头牛 放到 第 <span class="math inline">\(j\)</span> 头牛后面，于是就有了以下式子

<div class="math display">\[f_{i, S} = \sum_{i \in S, j \in S, i \ne j, abs(a_i) - abs(a_j) &gt; k} f_{j, S - (1 &lt;&lt; i)}
\]</div>

时间复杂度 <span class="math inline">\(O(N^2 2^N)\)</span>



```cpp
const int M = 16;
int n, k, a[M + 1];
ll f[M + 1][1 << M];
void solve()
{       
    cin>>n>>k;
    memset(f, 0, sizeof f);
    for(int i = 0; i < n; i++)
    {
        cin>>a[i];
        f[i][1 << i] = 1;
    }

    for(int S = 1; S < 1 << n; S++)
        for(int i = 0; i < n; i++)
            if((S >> i) & 1)
                for(int j = 0; j < n; j++)
                    if(i != j && (S >> j) & 1 && abs(a[j] - a[i]) > k)
                        f[i][S] = f[i][S] + f[j][S - (1 << i)];
    ll res = 0;
    for(int i = 0; i < n; i++)
        res = res + f[i][(1 << n) - 1];
    cout<<res<<'\n';
    return;
}
```
{% endraw %}
