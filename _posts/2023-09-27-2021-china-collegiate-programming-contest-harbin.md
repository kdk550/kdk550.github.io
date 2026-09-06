---
layout: post
title: "The 2021 China Collegiate Programming Contest (Harbin) JBEIDG"
date: 2023-09-27 23:09:00 +0800
updated: 2023-09-27 23:10:00 +0800
description: "The 2021 China Collegiate Programming Contest (Harbin) 目录 - The 2021 China Collegiate Programming Contest (Harbin) - VP概况 - J - Local Minimum - B - Magical Sub…"
excerpt: "The 2021 China Collegiate Programming Contest (Harbin) 目录 - The 2021 China Collegiate Programming Contest (Harbin) - VP概况 - J - Local Minimum - B - Magical Sub…"
categories: []
tags: ["mathematics", "dynamic programming", "contest"]
comments: false
related_posts: false
---
{% raw %}
# [The 2021 China Collegiate Programming Contest (Harbin)](https://codeforces.com/gym/103447)

目录

- [The 2021 China Collegiate Programming Contest (Harbin)](/blog/2023/2021-china-collegiate-programming-contest-harbin/#the-2021-china-collegiate-programming-contest-harbin)
  - [VP概况](/blog/2023/2021-china-collegiate-programming-contest-harbin/#vp概况)
  - [J - Local Minimum](/blog/2023/2021-china-collegiate-programming-contest-harbin/#j---local-minimum)
  - [B - Magical Subsequence](/blog/2023/2021-china-collegiate-programming-contest-harbin/#b---magical-subsequence)
  - [E - Power and Modulo](/blog/2023/2021-china-collegiate-programming-contest-harbin/#e---power-and-modulo)
  - [I - Power and Zero](/blog/2023/2021-china-collegiate-programming-contest-harbin/#i---power-and-zero)
  - [D - Math master](/blog/2023/2021-china-collegiate-programming-contest-harbin/#d---math-master)
  - [G - Damaged Bicycle](/blog/2023/2021-china-collegiate-programming-contest-harbin/#g---damaged-bicycle)

## VP概况

队友不应该写签到，签到应该我来写，以至于多了 <span class="math inline">\(2\)</span> 罚时，后面的题放心交给队友就好。  
![image](/assets/img/blog/posts/b3a14cc40fe14660b34cbe780d2afb495d5cc9d1e4c980c7ecda4f915007fdf2.png)  
![image](/assets/img/blog/posts/62f36f5430ac4aa1449151ed71452e4145439caae778eee1a9b2398e6a69a752.png)

## [J - Local Minimum](https://codeforces.com/gym/103447/problem/J)

问矩阵中有多少个元素 <span class="math inline">\(A_{i,j}\)</span> 同时是第 <span class="math inline">\(r\)</span> 行，第 <span class="math inline">\(c\)</span> 列上的最小元素

<span class="math inline">\(n = 1000\)</span> 直接暴力



```cpp
const int N = 1e3 + 10;
ll a[N][N], n, m, res, r[N], c[N];
void solve()
{
	cin>>n>>m;
	for(int i = 1; i <= n; i++)
		for(int j = 1; j <= m; j++)
			cin>>a[i][j];

	memset(r, 0x3f, sizeof r);
	memset(c, 0x3f, sizeof c);
	for(int i = 1; i <= n; i++)
		for(int j = 1; j <= m; j++)
			r[i] = min(a[i][j], r[i]);
	for(int j = 1; j <= m; j++)
		for(int i = 1; i <= n; i++)
			c[j] = min(a[i][j], c[j]);	
	for(int i = 1; i <= n; i++)
		for(int j = 1; j <= m; j++)
			if(a[i][j] == r[i] && a[i][j] == c[j])
				res++;
	cout<<res<<'\n';
}
```



## [B - Magical Subsequence](https://codeforces.com/gym/103447/problem/B)

问子序列第 <span class="math inline">\(2 \times i\)</span> 元素和 第<span class="math inline">\(2 \times i - 1\)</span> 位元素的和为 <span class="math inline">\(X\)</span> 时，子序列的最大长度是？

定义状态 <span class="math inline">\(f_{i,j}\)</span> ，表示第 <span class="math inline">\(i\)</span> 位，元素和为 <span class="math inline">\(j\)</span> 的子序列最大长度

预处理 <span class="math inline">\(suf_{i,j}\)</span> 表示第 <span class="math inline">\(i\)</span> 位，后缀中值为 <span class="math inline">\(k\)</span> 的元素位置

转移方程：

<div class="math display">\[f_{suf_{i,j-a_i},j} = f_{i-1,j} + 2
\]</div>

```cpp
const int N = 1e5 + 10;
 
int f[N][210];
int a[N], suf[N][110];
 
void solve()
{
	ll n;
	cin>>n;
	for(int i = 1; i <= n; i++)
		cin>>a[i];
	memset(suf, -1, sizeof suf);
	for(int i = n; i >= 1; i--)
	{
		for(int j = 1; j <= 100; j++)
			suf[i][j] = suf[i + 1][j];
		if(i + 1 <= n)
			suf[i][a[i + 1]] = i + 1;
	}
	int res = 0;
	for(int i = 1; i <= n; i++)
	{
		for(int j = 1; j <= 200; j++)
			f[i][j] = max(f[i - 1][j], f[i][j]);
		for(int j = a[i] + 1; j <= 200; j++)
		{
			if(j - a[i] > 100)	break;
			int k = j - a[i];
			if(suf[i][k] == -1)	continue;
			f[suf[i][k]][j] = max(f[i - 1][j] + 2, f[suf[i][k]][j]);
			res = max(f[suf[i][k]][j], res);
		}
	}
	cout<<res<<'\n';
}
```



## [E - Power and Modulo](https://codeforces.com/gym/103447/problem/E)

考虑到 <span class="math inline">\(a_i \leq 10^9\)</span>，那么对于取模来说，在 <span class="math inline">\(n\)</span> 足够大的情况下，一定存在

<span class="math inline">\(2^{i - 2} \% m= 2^{i - 2}\)</span>

<span class="math inline">\(2^{i - 1} \% m= a_i\)</span>



```cpp
const int N = 1e5 + 10;
ll a[N], n;
ll bmi[N];
void solve()
{
	cin>>n;
	for(int i = 1; i <= n; i++)
		cin>>a[i];
	bmi[1] = 1;	
	for(int i = 2; i <= 60; i++)
		bmi[i] = bmi[i - 1] * 2;
	ll m = -1;
 
	for(int i = 1; i <= n; i++)
	{
		// cout<<a[i]<<" "<<bmi[i]<<'\n';
		if(a[i] == bmi[i])
			continue;
		else
		{
			m = bmi[i] - a[i];
			break;
		}
	}
	// cout<<m<<" ";
	if(m == -1)
	{
		cout<<-1<<'\n';
		return;
	}
	bool ok = true;
	ll base = 1 % m;
	for(int i = 1; i <= n; i++)
	{
	 	if(base != a[i])
			ok = false;
		base *= 2;
		base %= m;
	}
	if(ok)
		cout<<m<<'\n';
	else
		cout<<-1<<'\n';
 
}
```



## [I - Power and Zero](https://codeforces.com/gym/103447/problem/I)

发现各个二进制位的有多少个，若满足 <span class="math inline">\(cnt_0 \geq cnt_1 \geq \dots \geq cnt_{32}\)</span> ，则答案最优，不断去调整即可



```cpp
const int N = 2e5 + 10;
 
int cnt[40];
void solve()
{       
    memset(cnt, 0, sizeof cnt);
    int n;  cin>>n;
    for(int i = 1; i <= n; i++)
    {
        int x;  cin>>x;
        int t = 0;
        while(x)
        {
            cnt[t++] += (x % 2);
            x /= 2;
        }
    }
    while(1)
    {
        bool ok = false;
        for(int i = 1; i <= 32; i++)
        {
            if(cnt[i] > cnt[i - 1])
            {
                ok = true;
                cnt[i]--;
                cnt[i - 1] += 2;
                break;
            }
        }
        if(!ok)
            break;
    }
    cout<<cnt[0]<<'\n';
    return;
}
```



## [D - Math master](https://codeforces.com/gym/103447/problem/D)

用二进制数 <span class="math inline">\(S\)</span> 表示分子剩余部分，我们从低位去检查分母即可



```cpp
#define int __int128
#define ll __int128
 
using namespace std;
 
inline __int128 read(){__int128 x=0,f=1;char ch=getchar();while(ch<'0'||ch>'9'){if(ch=='-'){f=-1;}ch=getchar();}while(ch>='0'&&ch<='9'){x=x*10+ch-'0';ch=getchar();}return x*f;}
inline void write(__int128 x){if (x < 0){putchar('-');x = -x;}if (x > 9) write(x / 10);putchar(x % 10 + '0');}
ll a[50], b[50], c[50];
void solve()
{       
    ll p, q;    
    // cin>>p>>q;
    p = read(), q = read();
    int n = 0, m = 0;
    __int128 t = p;
    while(t)    a[n++] = t % 10, t /= 10;
    t = q;
    while(t)    b[m++] = t % 10, t /= 10;
    for(int S = 0; S < (1 << n); S++)
    {
        ll tp = 0, cnt = 0, d[11];
        memset(d, 0, sizeof d);
        for(int i = n - 1; i >= 0; i--)
            if((S >> i) & 1)
                cnt++, tp = tp * 10 + a[i];
            else    d[a[i]]--;
        __int128 tq =(__int128)tp * q;
        if(tq % p != 0 || tp == 0)  continue;
        tq /= p;
        t = tq;
        int j = 0;
        for(int i = 0; i < m; i++)
            if(b[i] == t % 10)
                j++, t /= 10;
            else 
                d[b[i]]++;
        bool ok = true;
        for(int i = 0; i <= 9; i++)
            if(d[i] != 0)   ok = false;
        if(ok && t == 0 && tq != 0 && tp != 0)
            q = min(q, (ll)tq), p = min(p, (ll)tp);                
    }
    write(p);   cout<<" ";  write(q);
    cout<<'\n';
    return;
}
```



## [G - Damaged Bicycle](https://codeforces.com/gym/103447/problem/G)

<span class="math inline">\(P_S\)</span> 记录集合内单车都是坏的

官方题解：

<span class="math inline">\(f_{i,S}\)</span> 为访问 <span class="math inline">\(S\)</span> 集合内的单车，最终停在 <span class="math inline">\(i\)</span> 号点的最小期望时间，访问 <span class="math inline">\(i\)</span> 之前就找到了好单车、<span class="math inline">\(i\)</span> 是第一辆好 单车、<span class="math inline">\(i\)</span> 还是坏的。



```cpp
#include<bits/stdc++.h>

using namespace std;

typedef long long ll;

const int N = 1e5 + 10;
int t, r;
int n, m;
vector<pair<int, int>> e[N];
int k;
int pos[N];
bool vis[N];
double p[20];
int d[20][N];
void dij(int id, int start)
{
    priority_queue<pair<int,int>, vector<pair<int, int>>, greater<pair<int, int>>> q;
    memset(vis, false, sizeof vis);
    for(int i = 1; i <= n; i++)
        d[id][i] = 1e9;
    d[id][start] = 0;
    q.push({0, start});
    while(q.size() >= 1)
    {
        auto t = q.top();       q.pop();
        int u = t.second;
        if(vis[u])   continue;
        vis[u] = true;
        for(auto [v, w] : e[u])
        {
            if(d[id][v] > d[id][u] + w)
            {
                d[id][v] = d[id][u] + w;
                q.push({d[id][v], v});
            }
        }
    }
}
double f[20][1 << 20];
double P[1 << 20];
void solve()
{
    cin>>t>>r;
    cin>>n>>m;
    for(int i = 1; i <= m; i++)
    {
        int u, v, w;    
        cin>>u>>v>>w;
        e[u].push_back({v, w});
        e[v].push_back({u, w});
    }
    cin>>k;
    p[0] = 1.0;
    pos[0] = 1;
    for(int i = 1; i <= k; i++)
    {
        cin>>pos[i]>>p[i];
        p[i] = p[i] / 100;
        if(pos[i] == 1)
        {
            p[0] = p[i]; 
            i--, k--;
        }
    }
    for(int i = 0; i <= k; i++)
        dij(i, pos[i]);

    if(d[0][n] >= 1e9)
    {
        cout<<-1<<'\n';
        return;
    }
    double res = p[0] * d[0][n] / t + (1.0 - p[0]) * d[0][n] / r;
    for(int S = 1; S < (1 << k); S++)
    {
        P[S] = p[0];
        for(int j = 0; j < k; j++)
            f[j][S] = 1e15;
        for(int j = 0; j < k; j++)
            if((S >> j) & 1) 
                P[S] *= p[j + 1];
    }
    for(int j = 0; j < k; j++)
    {
        f[j][1 << j] = p[0] * d[0][pos[j + 1]] / t;
        f[j][1 << j] += (1 - p[0]) * d[0][n] / r;
        f[j][1 << j] += p[0] * (1 - p[j + 1]) * d[j + 1][n] / r;
        res = min(f[j][1 << j] + P[1 << j] * d[j + 1][n] / t, res);
    }

    for(int S = 1; S < (1 << k); S++)
    {
        for(int i = 0; i < k; i++)
        {
            if(((S >> i) & 1) == 0) continue;
            for(int j = 0; j < k; j++)
            {
                if(((S >> j) & 1) == 0 || i == j) continue;
                f[i][S] = min(f[j][S ^ (1 << i)] + P[S ^ (1 << i)] * d[j + 1][pos[i + 1]] / t, f[i][S]);
            }
            f[i][S] += P[S ^ (1 << i)] * (1 - p[i + 1]) * d[i + 1][n] / r;
            res = min(f[i][S] + P[S] * d[i + 1][n] / t, res);
        }
    }
    cout<<fixed << setprecision(10) <<res<<'\n';
    // printf("%.10lf\n", res);
}

int main()
{
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
    solve();
}
```
{% endraw %}
