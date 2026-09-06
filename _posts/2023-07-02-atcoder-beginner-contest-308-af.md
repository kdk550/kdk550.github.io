---
layout: post
title: "AtCoder Beginner Contest 308 A~F"
date: 2023-07-02 18:00:00 +0800
updated: 2024-09-29 23:15:00 +0800
description: "AtCoder Beginner Contest 308 ![image-20230702174419133]() 手速有点慢 A - New Scheme 判断给定数字是否满足条件 B - Default Price 给出要买的颜色，和一些颜色价格，算出总花费，用 map mp; 统计要买的数量，然后直接算 C…"
excerpt: "AtCoder Beginner Contest 308 ![image-20230702174419133]() 手速有点慢 A - New Scheme 判断给定数字是否满足条件 B - Default Price 给出要买的颜色，和一些颜色价格，算出总花费，用 map mp; 统计要买的数量，然后直接算 C…"
categories: []
tags: ["algorithm basics", "contest"]
comments: false
related_posts: false
---
{% raw %}
[AtCoder Beginner Contest 308](https://atcoder.jp/contests/abc308)

![image-20230702174419133]()

手速有点慢

## **A - New Scheme**

判断给定数字是否满足条件



```cpp
void solve()
{       
	bool ok = true;
	int a[10];
	for(int i = 1; i <= 8; i++)
		cin>>a[i];
	for(int i = 1; i <= 8; i++)
	{
		if(i >= 2 && a[i] < a[i - 1])
			ok = false;
		if(a[i] % 25 != 0)
			ok = false;
		if(a[i] < 100 || a[i] > 675)
			ok = false;
	}
	if(ok)
		cout<<"Yes\n";
	else
		cout<<"No\n";
    return;
}
```



## **B - Default Price**

给出要买的颜色，和一些颜色价格，算出总花费，用 `map<string, int> mp;` 统计要买的数量，然后直接算



```cpp
map<string, int> mp;
void solve()
{       
    int n, m;
    cin>>n>>m;
 
    for(int i = 1; i <= n; i++)
    {
        string t;   cin>>t;
        mp[t]++;
    }
    string op[1100];
    for(int i = 1; i <= m; i++)
        cin>>op[i];
    int p0, cnt = 0;
    cin>>p0;
    int res = 0;
    for(int i = 1; i <= m; i++)
    {
        int x;  cin>>x;
        if(mp[op[i]] >= 1)
            res += x * mp[op[i]], cnt += mp[op[i]];
    }
    cout<<res + (n - cnt) * p0<<'\n';
    return;
}
```



## **C - Standings**

tag：排序，模拟

为避免精度产生的误差，cmp为

<div class="math display">\[\dfrac{a}{a + b} &lt; \dfrac{c}{c + d}	\\
	ac + ac &lt; ca + cb
\]</div>

```cpp
array<ll, 3> ar[N];
bool cmp(array<ll, 3> t1, array<ll, 3> t2)
{
    ll a = t1[0] * (t2[0] + t2[1]), b = t2[0] * (t1[0] + t1[1]);
    if(a == b)
    {
        return t1[2] < t2[2];
    }
    else 
        return a > b;
}
void solve()
{       
    int n;  cin>>n;
    for(int i = 1; i <= n; i++)
    {
        cin>>ar[i][0]>>ar[i][1];
        ll t = __gcd(ar[i][0], ar[i][1]);
        ar[i][0] /= t, ar[i][1] /= t, ar[i][2] = i;
    }
    sort(ar + 1, ar + 1 + n, cmp);
    for(int i = 1; i <= n; i++)
        cout<<ar[i][2]<<" ";
    cout<<'\n';
    return;
}
```



## **D - Snuke Maze**

bfs 再记录当前走到哪个字母的信息即可



```cpp
char op[N][N];
int f[N][N];
int dx[] = {0, 0, -1, 1};
int dy[] = {-1, 1, 0, 0};
void solve()
{       
    int n, m;   cin>>n>>m;
    for(int i = 1; i <= n; i++)
        for(int j = 1; j <= m; j++)
        {
            cin>>op[i][j];
            f[i][j] = 1e9;
        }
    
    map<char, int> mp;
    mp['s'] = 1;
    mp['n'] = 2;
    mp['u'] = 3;
    mp['k'] = 4;
    mp['e'] = 5;
    queue<array<int, 3>> q;
 
    if(op[1][1] == 's')
    {
        q.push({1, 1, 1});
        f[1][1] = 0;
    }
    while(!q.empty())
    {
        auto t = q.front(); q.pop();
        int tx = t[0];
        int ty = t[1];
        int flag = t[2];
        if(flag == 5)   flag = 1;
        else flag++;
        for(int i = 0; i < 4; i++)
        {
            int x = tx + dx[i];
            int y = ty + dy[i];
            if(x < 1 || x > n || y < 1 || y > m)    continue;
            int g = mp[op[x][y]];
            if(flag != g)   continue;
            if(f[x][y] > f[tx][ty] + 1)
            {
                f[x][y] = f[tx][ty] + 1;
                q.push({x, y, g});
            }
        }
    }   
    if(f[n][m] == 1e9)
        cout<<"No\n";
    else
        cout<<"Yes\n";
    return;
}
```



## **E - MEX**

统计后缀信息，sx统计后缀含有 <span class="math inline">\(\texttt{X}\)</span> 集合 <span class="math inline">\(0,1,2\)</span> 的数量， se统计后缀含有 <span class="math inline">\(\texttt{EX}\)</span> 集合 <span class="math inline">\(0,1,2,01,02,12\)</span> 的数量，然后直接对每个 <span class="math inline">\(\texttt{M}\)</span> 对应的数字和后缀 <span class="math inline">\(\texttt{se}\)</span> 分类讨论即可

我这题的写法没那么美观，但看起来很暴力。



```cpp
ll m[N][11], e[N][11], x[N][11];
ll sm[N][11], se[N][11], sx[N][11];
 
int n, a[N];
char op[N];
void solve()
{       
    cin>>n;
    for(int i = 1; i <= n; i++)
        cin>>a[i];
    for(int i = 1; i <= n; i++)
        cin>>op[i];
    for(int i = 1; i <= n; i++)
    {
        if(op[i] == 'M')
            m[i][a[i]]++;
        else if(op[i] == 'E')
            e[i][a[i]]++;
        else if(op[i] == 'X')
            x[i][a[i]]++;
    }
    for(int i = n; i >= 1; i--)
        for(int j = 2; j >= 0; j--)
            sx[i][j] = sx[i + 1][j] + x[i][j];
    for(int i = n; i >= 1; i--)
    {
        for(int j = 5; j >= 0; j--)
        {
            se[i][j] = se[i + 1][j];
        }
        if(op[i] == 'E')
        {
            if(a[i] == 0)
            {
                //cout<<"!!\n";
                se[i][0] += sx[i][0];
                se[i][3] += sx[i][1];
                se[i][4] += sx[i][2];
            }   
            else if(a[i] == 1)
            {
                se[i][1] += sx[i][1];
                se[i][3] += sx[i][0];
                se[i][5] += sx[i][2];
            } 
            else if(a[i] == 2)
            {
                se[i][2] += sx[i][2];
                se[i][4] += sx[i][0];
                se[i][5] += sx[i][1];
            }
        }
    }
 
 
 
    ll res = 0;
    for(int i = 1; i <= n; i++)
    {
        if(op[i] == 'M')
        {
            if(a[i] == 0)
            {
                res += 2ll * (se[i][1] + se[i][3]);
                res += se[i][2] + se[i][4] + se[i][0];
                res += 3ll * se[i][5];
            }   
            else if(a[i] == 1)
            {
                res += 2ll * (se[i][0] + se[i][3]);
                res += 3ll * se[i][4];
            } 
            else if(a[i] == 2)
            {
                res += se[i][0] + se[i][4];
                res += 3ll * se[i][3];
            }
        }
    }
    cout<<res<<'\n';
    return;
}
```



## **F - Vouchers**

贪心，对优惠券按折扣降序排序，将所有商品价格放进`multiset`，然后找出已有商品大于等于要求金额最小的商品，将它从multiset中删除



```cpp
int n, m;
ll a[N];
pair<ll, ll> b[N];
multiset<int> s;
bool cmp(pair<ll, ll> t1, pair<ll, ll> t2)
{
    if(t1.second == t2.second)
        return t1.first > t2.first;
    return t1.second > t2.second;
}   
 
void solve()
{       
    cin>>n>>m;
    ll res = 0;
    for(int i = 1; i <= n; i++)
    {
        cin>>a[i];
        res += a[i];
        s.insert(a[i]);
    }
    for(int i = 1; i <= m; i++)
        cin>>b[i].first;
    for(int i = 1; i <= m; i++)
        cin>>b[i].second;
    sort(b + 1, b + 1 + m, cmp);
    for(int i = 1; i <= m; i++)
    {
        if(s.lower_bound(b[i].first) == s.end())
            continue;
        int p = *s.lower_bound(b[i].first);
        res -= b[i].second;
        s.erase(s.find(p));
    }
    cout<<res<<'\n';
    return;
}
```



## **G - Minimum Xor Pair Query**

待补，赛时写了trie，但没搞出来，好像正解也不是这个  
去看佬们的blog学习
{% endraw %}
