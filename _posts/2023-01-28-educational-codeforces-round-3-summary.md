---
layout: post
title: "Educational Codeforces Round 3 个人总结A-E"
date: 2023-01-28 17:02:00 +0800
updated: 2023-09-01 12:48:00 +0800
description: "Educational Codeforces Round 3 A. USB Flash Drives - 降序排序后，贪心，甚至不会爆longlong B. The Best Gift - 大意：有多少种互不相同不同的组合 - 用map记录这个类型出现的次数 - 一本书的贡献为 与这本书不同类型的数量 C. Load…"
excerpt: "Educational Codeforces Round 3 A. USB Flash Drives - 降序排序后，贪心，甚至不会爆longlong B. The Best Gift - 大意：有多少种互不相同不同的组合 - 用map记录这个类型出现的次数 - 一本书的贡献为 与这本书不同类型的数量 C. Load…"
categories: []
tags: ["contest", "algorithm basics"]
comments: false
related_posts: false
---
{% raw %}
[Educational Codeforces Round 3](https://codeforces.com/contest/609 "Educational Codeforces Round 3")

A. USB Flash Drives

- 降序排序后，贪心，甚至不会爆longlong



```cpp
void solve()
{
    int n,m;
    cin>>n>>m;
    vector<int> a(n);
    for(int i=0;i<n;i++)
        cin>>a[i];
    sort(all(a));reverse(all(a));
    int s=0,ans=0;
    for(int i=0;i<n;i++)
    {
        if(s>=m)    break;
        s+=a[i],ans++;
    }
    cout<<ans<<endl;
    return;
}
```



B. The Best Gift

- 大意：有多少种互不相同不同的组合
- 用map记录这个类型出现的次数
- 一本书的贡献为 与这本书不同类型的数量



```cpp
void solve()
{
    int n,m;
    cin>>n>>m;
    LL ans=0,s=0;
    vector<int> a(n);
    map<int,int> mp;
    for(int i=0;i<n;i++)
    {
        cin>>a[i];
        mp[a[i]]++;
        s++;
    }
    for(auto it:mp)
    {
        ans+=(it.se*(s-it.se));
    }
    cout<<ans/2ll<<endl;
 
    return;
}
```



C. Load Balancing

- 大意:求让最大值和最小值的差最小的操作次数
- 对数组进行排序，使之升序
- <span class="math inline">\(s\)</span> 为所有数之和，<span class="math inline">\(k\)</span> 代表平均数，<span class="math inline">\(r\)</span> 代表余数
- $k = \frac{s}{n} $, $ r =s\%n $
- 当 $ r=0 $ ，最大值和最小值的差为 <span class="math inline">\(0\)</span>，答案即为<span class="math inline">\(\sum_{i=1}^n \max(a_i-k,0)\)</span>
- 当 $ r=1 $ ，最大值和最小值的差为 <span class="math inline">\(1\)</span>，答案即为<span class="math inline">\(\sum_{i=1}^{n-r} \max(a_i-k,0)+\sum_{i=n-r+1}^{n} \max(a_i-k-1,0)\)</span>



```cpp
LL a[N],b[N];
void solve()
{
    LL n;
    cin>>n;
    LL ans=0,s=0;
    for(int i=1;i<=n;i++)
    {
        cin>>a[i];
        s+=a[i];
    }
    sort(a+1,a+1+n);
    LL k=s/n,r=s%n;
    for(int i=1;i<=n;i++)
        b[i]=k;
    for(int i=n;i>=n-r+1;i--)
    {   
        b[i]++;
    }
    for(int i=1;i<=n;i++)
        ans+=max(a[i]-b[i],0ll);
 
    cout<<ans<<endl;
    return;
}
```



D. Gadgets for dollars and pounds

- 二分，前缀和，贪心
- 大意：在 <span class="math inline">\(n\)</span> 天中买东西，每天有不同的汇率，<span class="math inline">\(m\)</span> 个商品，只能使用pounds或dollars，要买 <span class="math inline">\(k\)</span> 个，但只有 <span class="math inline">\(s\)</span> 元钱，判断能不能买，能输出哪天能买完，和哪一天买第几个商品
- 在 <span class="math inline">\(1,...,n\)</span> 天中，若第 <span class="math inline">\(x\)</span> 天能买完 <span class="math inline">\(k\)</span> 个，那 第 <span class="math inline">\(k+1\)</span> 天也能买完，也就是在 <span class="math inline">\(1,...,n\)</span> 天中找到最小满足条件的 <span class="math inline">\(x\)</span>，且第 <span class="math inline">\(x-1\)</span> 天不能买完，这是有单调性的，所以我们二分哪天能买完
- check中，在 <span class="math inline">\(1,...,x\)</span> 天中找到最小pounds和dollars的汇率分别是<span class="math inline">\(a1\)</span> 和 <span class="math inline">\(b1\)</span>，设消费为 <span class="math inline">\(sum\)</span> 。题目并没有限制每天购买商品的数量，我们等到汇率最小那天买完是最划算的**贪心**
- 这里就有一个问题，如何去确定换了前去买用pounds，还是用dollars的？
- 因为买<span class="math inline">\(k\)</span> <span class="math inline">\((1 ≤ k ≤ 2·10^5)\)</span> 个商品，可以对pounds，和dollars进行排序，用前缀和处理
- <span class="math inline">\(sum=s1[x]·a1+s2[y]·b1\)</span> <span class="math inline">\((0 ≤ x ≤ \text{pounds商品个数},0 ≤ y ≤ \text{dollars商品个数},x+y=k)\)</span>,运用前缀和就可以在<span class="math inline">\(O(k)\)</span>的时间内处理出第 <span class="math inline">\(x\)</span> 天结束的最小花销
- 剩下的输出方案,记录下最小花销下的 <span class="math inline">\(x\)</span> 、 <span class="math inline">\(y\)</span> 和 pounds和dollars 汇率最小的日子就很容易解决了

代码有点丑QAQ



```cpp
const int N = 200010;


LL n,m,k,s,a[N],b[N];
int id,d1,d2;
LL cnt1=0,cnt2=0,s1[N],s2[N];

PII c1[N],c2[N];

bool check(LL x)
{
    LL a1=1e18,b1=1e18;
    for(int i=1;i<=x;i++)
    {
        if(a[i]<a1)
            d1=i,a1=a[i];
        if(b[i]<b1)
            d2=i,b1=b[i];
    }

    LL sum=1e18;
    for(int i=0;i<=k;i++)
    {
        if( !(i<=cnt1&&k-i<=cnt2))    continue;
        LL t1=s1[i],t2=s2[k-i];
        LL r1=t1*a1,r2=t2*b1;
        if(r1+r2<sum)
            sum=r1+r2,id=i;
    }
    if(sum<=s)    return true;
    else return false;
}
void solve()
{
    cin>>n>>m>>k>>s;
    for(int i=1;i<=n;i++)
        cin>>a[i];
    for(int i=1;i<=n;i++)
        cin>>b[i];
    for(int i=1;i<=m;i++)
    {
        LL t,cc; cin>>t>>cc;
        if(t==1)    c1[++cnt1].fi=cc,c1[cnt1].se=i;
        else 
            c2[++cnt2].fi=cc,c2[cnt2].se=i;
    }
    sort(c1+1,c1+1+cnt1);
    sort(c2+1,c2+1+cnt2);
    for(int i=1;i<=cnt1;i++)
        s1[i]=s1[i-1]+c1[i].fi;
    for(int i=1;i<=cnt2;i++)
        s2[i]=s2[i-1]+c2[i].fi;
    if(check(n)==false)
    {
        cout<<-1<<endl;    return;
    }

    int l=1,r=n;
    while(l<r)
    {
        int mid=(l+r)>>1;
        if(check(mid))  r=mid;
        else l=mid+1;
    }
    if(check(l))
    {
        cout<<l<<endl;
        vector<PII> ans;
        int j=0;
        for(int i=1;i<=id;i++)
            ans.pb({d1,c1[++j].se});
        j=0;
        for(int i=id+1;i<=k;i++)
            ans.pb({d2,c2[++j].se});
        for(auto &it:ans)
            cout<<it.se<<" "<<it.fi<<endl;
    }
    return;
}

```



## [Minimum spanning tree for each edge](https://codeforces.com/contest/609/problem/E)

给你 <span class="math inline">\(n\)</span> 个点，<span class="math inline">\(m\)</span> 条边，如果对于一个最小生成树中要求必须包括第 <span class="math inline">\(i(1 \le i \le m)\)</span> 条边，那么最小生成树的权值总和最小是多少。

graph
1 --- 2
1 --- 3
2 --- 4
2 --- 5
3 --- 6
3 --- 7

graph
1 --- 2
1 --- 3
2 --- 4
2 --- 5
3 --- 6
3 --- 7
5 --- 6

我们若是在最小生成树的基础上再连一条边，也就是将 <span class="math inline">\(u\)</span> 和 <span class="math inline">\(v\)</span> 连边，这时候出现了一个环，我们考虑在这个环上面删去最大边权即可，可以用树上倍增解决



```cpp
const int N = 2e5 + 10;

const int M = 2e5 + 10;
const int LOGN = 20;
int n, m, p[N], dep[N], fa[N][LOGN + 2];
ll g[N][LOGN + 2];
ll res;
array<ll, 3> e2[M];
vector<pair<ll, ll>> e[N];
struct Edge
{
    ll u, v, w;
    bool operator <(const Edge& W)const
    {
        return w < W.w;
    }
}edge[M];
int find(int x)
{
    if (p[x] != x)  p[x] = find(p[x]);
    return p[x];
}
void kruskal()
{
    sort(edge + 1, edge + 1 + m);
    for (int i = 1; i <= n; i++)    p[i] = i;
    // for (int i = 1; i <= m; i++)
    // {
    //     ll u = edge[i].u, v = edge[i].v, w = edge[i].w;

    //     // cout<<u<<" "<<v<<"   "<<w<<'\n';
    // }

    // cout<<'\n';
    for (int i = 1; i <= m; i++)
    {
        ll u = edge[i].u, v = edge[i].v, w = edge[i].w;
        // u = find(u), v = find(v);
        // cout<<u<<" "<<v<<"   "<<w<<'\n';

        if (find(u) != find(v))
        {
            p[find(u)] = find(v);
            res += w;
            e[u].push_back({v, w});
            e[v].push_back({u, w});
        }
    }
}
void dfs(int u, int from)
{
    dep[u] += dep[from] + 1;
    for(auto [v, w] : e[u]) {
        if(v == from) continue;
        fa[v][0] = u;
        g[v][0] = w;
        dfs(v, u);
    }
}
void lca_init()
{
    for(int j = 1; j <= LOGN; j++)
        for(int i = 1; i <= n; i++)
        {
            fa[i][j] = fa[fa[i][j - 1]][j - 1];
            g[i][j] = max(g[i][j - 1], g[fa[i][j - 1]][j - 1]);
        }
}
ll lca_query(int u, int v)
{
    ll ret = 0;
    if(dep[u] < dep[v])   swap(u, v);
    int d = dep[u] - dep[v];
    for(int j = LOGN; j >= 0; j--)
        if(d & (1 << j))
            ret = max(ret, g[u][j]), u = fa[u][j];
    // cout<<u<<"  "<<v<<"  "<<dep[u]<<"   "<<dep[v]<<"  "<<ret<<'\n';
    if(u == v)    return ret;
    for(int j = LOGN; j >= 0; j--)
        if(fa[u][j] != fa[v][j])
        {
            ret = max({ret, g[u][j], g[v][j]});
            // cout<<g[u][j]<<"  "<<g[v][j]<<'\n';
            u = fa[u][j], v = fa[v][j];
        }
    return max({g[u][0], g[v][0], ret});
}
void solve()
{
    cin >> n >> m;
    for (int i = 1; i <= m; i++)
    {
        int u, v, w;    cin >> u >> v >> w;
        edge[i] = {u, v, w};
        e2[i] = {u, v, w};
    }
    kruskal();
    // cout<<res<<'\n';
    dfs(1, 0);  lca_init();
    for(int i = 1; i <= m; i++)
    {
        ll t = lca_query(e2[i][0], e2[i][1]);
        cout<<res + e2[i][2] - t<<'\n'; 
        // cout<<e2[i][0]<<"  "<<e2[i][1]<<"   "<<t<<'\n';
    }
    // cout<<"L : ";
    // for(int i = 1; i <= n; i++)
    //     cout<<l[i]<<"  ";
    // cout<<'\n';
    return; 
}

```
{% endraw %}
