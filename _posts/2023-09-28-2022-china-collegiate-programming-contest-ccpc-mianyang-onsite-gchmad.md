---
layout: post
title: "2022 China Collegiate Programming Contest (CCPC) Mianyang Onsite GCHMAD"
date: 2023-09-28 11:01:00 +0800
updated: 2023-09-28 11:02:00 +0800
description: "2022 China Collegiate Programming Contest (CCPC) Mianyang Onsite 目录 - 2022 China Collegiate Programming Contest (CCPC) Mianyang Onsite - VP 情况 - G - Let Them E…"
excerpt: "2022 China Collegiate Programming Contest (CCPC) Mianyang Onsite 目录 - 2022 China Collegiate Programming Contest (CCPC) Mianyang Onsite - VP 情况 - G - Let Them E…"
categories: []
tags: ["mathematics", "dynamic programming", "contest"]
comments: false
related_posts: false
---
{% raw %}
# [2022 China Collegiate Programming Contest (CCPC) Mianyang Onsite](https://codeforces.com/gym/104065)

目录

- [2022 China Collegiate Programming Contest (CCPC) Mianyang Onsite](/blog/2023/2022-china-collegiate-programming-contest-ccpc-mianyang-onsite-gchmad/#2022-china-collegiate-programming-contest-ccpc-mianyang-onsite)
  - [VP 情况](/blog/2023/2022-china-collegiate-programming-contest-ccpc-mianyang-onsite-gchmad/#vp-情况)
  - [G - Let Them Eat Cake](/blog/2023/2022-china-collegiate-programming-contest-ccpc-mianyang-onsite-gchmad/#g---let-them-eat-cake)
  - [C - Catch You Catch Me](/blog/2023/2022-china-collegiate-programming-contest-ccpc-mianyang-onsite-gchmad/#c---catch-you-catch-me)
  - [H - Life is Hard and Undecidable, but...](/blog/2023/2022-china-collegiate-programming-contest-ccpc-mianyang-onsite-gchmad/#h---life-is-hard-and-undecidable-but)
  - [M - Rock-Paper-Scissors Pyramid](/blog/2023/2022-china-collegiate-programming-contest-ccpc-mianyang-onsite-gchmad/#m---rock-paper-scissors-pyramid)
  - [A - Ban or Pick, What's the Trick](/blog/2023/2022-china-collegiate-programming-contest-ccpc-mianyang-onsite-gchmad/#-a---ban-or-pick-whats-the-trick)
  - [D - Gambler's Ruin](/blog/2023/2022-china-collegiate-programming-contest-ccpc-mianyang-onsite-gchmad/#d---gamblers-ruin)

## VP 情况

队友告诉我题意很顺利过了两签到，对着C虚空写法，搞了一个if(n=3)while(1)的样例发现构造假了，然后马上过了，但是罚时很多然后队友过了石头剪刀布，读了A，很快想到了dp和转移方程，但不知道怎么转移好，最后结束比赛了，看了大家用记忆化搜索竟然这么好些，然后补了DM，这个D我想了很久，一直不懂怎么枚举和三分这个赔率，写了好几个版本，直到今天终于想明白了。  
![image](/assets/img/blog/posts/f78ecbe53dd891c6275ceb1e5b2402b36c76c391fc78e99ddc447ad52f15d2b9.png)

## [G - Let Them Eat Cake](https://codeforces.com/gym/104065/problem/G)

每轮操作删掉一半的数，已得知操作次数最多只有 <span class="math inline">\(\log n\)</span> 轮，直接模拟



```cpp
int n;
const int N = 1e5 + 10;
 
void solve()
{
	cin>>n;
	int res = 0;
	vector<int> a, b;
	for(int i = 1; i <= n; i++)
	{
		int x;	cin>>x;
		b.push_back(x);
	}
	int sz = n;
	while(sz != 1)
	{
		res++;
		a = b;
		b.clear();
		int m = a.size();
		for(int i = 0; i < m; i++)
		{
			// cout<<a[i]<<"  ";
			// if(i - 1 >= 0)
			// 	cout<<a[i - 1]<<" ";
			// if(i + 1 < m)
			// 	cout<<a[i + 1]<<" ";
			// cout<<'\n';
			bool ok = false;
			if(i - 1 >= 0 && a[i - 1] > a[i])
			{
				ok = true;
			}
 
			if(i + 1 < m && a[i + 1] > a[i])
				ok = true;
			if(!ok)
				b.push_back(a[i]);
		}
		sz = b.size();
	}
	cout<<res<<'\n';
}
```



## [C - Catch You Catch Me](https://codeforces.com/gym/104065/problem/C)

对于1的儿子，其答案是以其儿子为根子树的深度



```cpp
int n;
const int N = 1e5 + 10;
 
int dep[N], f[N];
vector<int> e[N];
void dfs(int u, int from)
{
	dep[u] = dep[from] + 1;
	f[u] = dep[u];
	for(auto v : e[u])
	{
		if(v == from)	continue;
		dfs(v, u);
		f[u] = max(f[u], f[v]);
	}
}
void solve()
{
	cin>>n;
	for(int i = 1; i < n; i++)
	{
		int u, v;	cin>>u>>v;
		e[u].push_back(v);
		e[v].push_back(u);
	}
	dfs(1, 0);
	long long res = 0;
	for(auto v : e[1])
	{
		res = res + f[v] - 1;
	}
	cout<<res<<'\n';
}
```



## [H - Life is Hard and Undecidable, but...](https://codeforces.com/gym/104065/problem/H)

构造方式见代码



```cpp
ll k;
int dx[] = {1, 1};
int dy[] = {1, 0};
int res[310][310];
void solve()
{
	cin>>k;
	int x = 1, y = 1;
	for(int i = 1; i <= 2 * k; i++)
	{
		x = x + dx[0];
		y = y + dy[0];
		res[x][y] = 1;
	} 	
	int n = 0;
	for(int i = 1; i <= 300; i++)
		for(int j = 1; j <= 300; j++)
			n += res[i][j];
	cout<<n<<'\n';
	for(int i = 1; i <= 300; i++)
		for(int j = 1; j <= 300; j++)
			if(res[i][j] == 1)
				cout<<i<<" "<<j<<'\n';
}
```



## [M - Rock-Paper-Scissors Pyramid](https://codeforces.com/gym/104065/problem/M)

观察出有单调栈的特点，根据特点直接去模拟单调栈



```cpp
const int N = 1e6 + 10;
typedef long long ll;
int n, a[N];
void solve()
{
    string s;   cin>>s;
    n = s.size();
    s = "?" + s;
    for(int i = 1; i <= n; i++)
    {
        if(s[i] == 'S') 
            a[i] = 0;
        else if(s[i] == 'P')    
            a[i] = 1;
        else 
            a[i] = 2;
    }
    stack<int> stk; stk.push(a[1]);
    for(int i = 2; i <= n; i++)
    {
        while(!stk.empty() && a[i] == (stk.top() - 1 + 3) % 3)
            stk.pop();
        stk.push(a[i]);        
    }
    while(stk.size() > 1)
        stk.pop();
    if(stk.top() == 0)
        cout<<"S";
    else if(stk.top() == 1)
        cout<<"P";
    else 
        cout<<"R";
    cout<<'\n';
}
```



## [A - Ban or Pick, What's the Trick](https://codeforces.com/gym/104065/problem/A)

轮流操作，我可以选择选一个我方能力值最大的英雄，也可以禁掉对方能力值最大的英雄

<span class="math inline">\(f_{pos,i,j}\)</span>状态就是第 <span class="math inline">\(pos\)</span> 轮，A选了 <span class="math inline">\(i\)</span> 个英雄，<span class="math inline">\(B\)</span> 选了 <span class="math inline">\(j\)</span> 个英雄，而双方禁用的英雄数量是可以确定的，用记忆化搜索写就行



```cpp
const int N = 2e5 + 10;
 
typedef long long ll;
 
ll n, k;
ll a[N], b[N];
ll f[2 * N][11][11], tmp;
//  第 pos 次操作, A 选了 j 个, B 选了 p 个
ll dfs(int pos, int i, int j)
{
    if(pos == 2 * n) return 0;
    int dela = i + pos / 2 - j;
    int delb = j + (pos + 1) / 2 - i;
    if(f[pos][i][j] != tmp)
        return f[pos][i][j];
    ll res;
    if(pos % 2 == 0)
    {
        res = -1e18;
        if(dela + 1 <= n && i + 1 <= k)
            res = max(dfs(pos + 1, i + 1, j) + a[dela + 1], res);
        res = max(dfs(pos + 1, i, j), res);
    }
    else
    {
        res = 1e18;
        if(delb + 1 <= n && j + 1 <= k)
            res = min(dfs(pos + 1, i, j + 1) - b[delb + 1], res);
        res = min(dfs(pos + 1, i, j), res);
    }
    f[pos][i][j] = res;
    return res;
}
 
void solve()
{
    cin>>n>>k;
    for(int i = 1; i <= n; i++)
        cin>>a[i];
    for(int i = 1; i <= n; i++)
        cin>>b[i];
    sort(a + 1, a + 1 + n);
    sort(b + 1, b + 1 + n);
    reverse(a + 1, a + 1 + n);
    reverse(b + 1, b + 1 + n);
    memset(f, 0x3f, sizeof f);
    tmp = f[0][0][0];
    cout<<dfs(0, 0, 0)<<'\n';
    // cout<<f[1][0][0]<<'\n';
}
```



## [D - Gambler's Ruin](https://codeforces.com/gym/104065/problem/D)

选择枚举一个队的赔率，三分另一个队的赔率

1. 将两队预测胜率从小到大排序
2. 前缀和处理
3. 枚举A队赔率
4. 三分另一队赔率

这个我很快想到了解法，但是一直不知道怎么处理1,2操作，写了好多个版本一直过不了样例，过了1周再写就过了



```cpp
typedef long long ll;
 
const int mod = 1e9 + 7;
const int N = 1e6 + 10;
 
map<double, ll> mp;
int n, m;
vector<pair<double, ll>> a, b;
ll sx[N], sy[N];
double res;
double f(int idx, int idy)
{
    double s1 = 1.0 * a[idx].first * sx[idx];
    double s2 = 1.0 * b[idy].first * sy[idy];    
    return 1.0 * sx[idx] + sy[idy] - max(s1, s2); 
}
void work(int idx)
{
    int l = 0, r = m - 1;
    while(l < r)
    {
        int lmid = l + (r - l) / 3;
        int rmid = r - (r - l) / 3;
        double fl = f(lmid, idx), fr = f(rmid, idx);
        if(fl <= fr)
            l = lmid + 1;
        else r = rmid - 1;
        res = max({fl, fr, res});
        // cout<<l<<" "<<r<<'\n';
    }
}
void solve()
{       
    cin>>n;
    for(int i = 1; i <= n; i++)
    {
        double p;   ll c;   cin>>p>>c;
        mp[p] += c;
    }
    a.push_back({0, 0});
    b.push_back({0, 0});
    for(auto [x, y] : mp)
    {
        if(x != 0.0)
            a.push_back({1.0 / x, y});
        if(x != 1.0)
            b.push_back({1.0 / (1.0 - x), y});
    }
    sort(a.begin(), a.end());
    sort(b.begin(), b.end());
    n = a.size(), m = b.size();
    for(int i = 0; i < n; i++)
    {
        sx[i] = a[i].second;
        if(i >= 1)  sx[i] += sx[i - 1];
    }
    for(int i = 0; i < m; i++)
    {
        sy[i] = b[i].second;
        if(i >= 1)  sy[i] += sy[i - 1];
    }
    for(int i = 0; i < n; i++)
        work(i);
    cout<<fixed<<setprecision(10)<<res<<'\n';
    return;
}
```
{% endraw %}
