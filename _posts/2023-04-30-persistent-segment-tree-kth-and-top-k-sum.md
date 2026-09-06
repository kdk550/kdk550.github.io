---
layout: post
title: "可持久化线段树模板 区间第k小数,区间前k大数之和"
date: 2023-04-30 01:09:00 +0800
updated: 2023-04-30 17:32:00 +0800
description: "第K小数 The 17th Zhejiang Provincial Collegiate Programming Contest E题 区间前k大数之和 VP的时候小师妹读了这道题告诉我，很快想到了一个错误解法，后面画图发现答案是 \\(\\text{平方和} + \\text{区间前k大之和}\\) ，想不到用什么数据结构…"
excerpt: "第K小数 The 17th Zhejiang Provincial Collegiate Programming Contest E题 区间前k大数之和 VP的时候小师妹读了这道题告诉我，很快想到了一个错误解法，后面画图发现答案是 \\(\\text{平方和} + \\text{区间前k大之和}\\) ，想不到用什么数据结构…"
categories: []
tags: ["data structures"]
comments: false
related_posts: false
---
{% raw %}
[第K小数](https://www.acwing.com/problem/content/257/ "第K小数")



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

const int mod = 998244353;
const int N = 5e5 + 10;

struct segtree
{
	int l, r, s;
}seg[N * 30];

vector<int> vx; 
int n, q, a[N], rt[N], tot;

void update(int id)
{
	seg[id].s = seg[seg[id].l].s + seg[seg[id].r].s;
}

int build(int l, int r)
{
	int id = ++tot;
	if(l == r)
		return id;
	int mid = (l + r) >> 1;
	seg[id].l = build(l, mid);
	seg[id].r = build(mid + 1, r);
	return id; 
}

int change(int u, int l, int r, int pos)
{
	int id = ++tot;
	seg[id] = seg[u];
	if(l == r)	
	{
		seg[id].s++;
		return id;
	}
	int mid = (l + r) >> 1;
	if(pos <= mid)
		seg[id].l = change(seg[u].l, l, mid, pos);
	else
		seg[id].r = change(seg[u].r, mid + 1, r, pos);
	update(id);
	return id;
}

int query(int v, int u, int l, int r, int x)
{
	if(l == r)
		return l;
	int cnt = seg[seg[u].l].s - seg[seg[v].l].s;
	int mid = (l + r) >> 1;
	if(x <= cnt)
		return query(seg[v].l, seg[u].l, l, mid, x);
	else
		return query(seg[v].r, seg[u].r, mid + 1, r, x - cnt);		
}

void solve()
{   
	cin>>n>>q;
	for(int i = 1; i <= n; i++)
	{
		cin>>a[i];
		vx.push_back(a[i]);
	}
	sort(vx.begin(), vx.end());
	vx.erase(unique(vx.begin(), vx.end()), vx.end());
	rt[0] = build(1, vx.size());
	for(int i = 1; i <= n; i++)
		rt[i] = change(rt[i - 1], 1, vx.size(), lower_bound(vx.begin(), vx.end(), a[i]) - vx.begin() + 1);
	
	while(q--)
	{
		int l, r, k;	cin>>l>>r>>k;
		cout<<vx[query(rt[l - 1], rt[r], 1, vx.size(), k) - 1]<<endl;
	}		
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



[The 17th Zhejiang Provincial Collegiate Programming Contest](https://codeforces.com/gym/102770 "The 17th Zhejiang Provincial Collegiate Programming Contest E") E题  
区间前k大数之和  
VP的时候小师妹读了这道题告诉我，很快想到了一个错误解法，后面画图发现答案是<span class="math inline">\(\text{平方和} + \text{区间前k大之和}\)</span> ，想不到用什么数据结构去维护，只好草草下播

baidu：区间前K大之和，第一个就是这题，发现作法是可持久化线段树，于是开始学习了动态开点和可持久化线段树。

基于前缀和的思想，我们对于第<span class="math inline">\(r\)</span>版本 - 第<span class="math inline">\(l\)</span>版本，若<span class="math inline">\([l, r]\)</span>区间，<span class="math inline">\([mid + 1, r]\)</span>数字数量<span class="math inline">\(tmp \geq x\)</span>,则从<span class="math inline">\([mid + 1, r]\)</span>得到答案  
否则递归到<span class="math inline">\([l, mid]\)</span>获得答案，同时加上<span class="math inline">\([mid + 1, r]\)</span>的和

最后这题卡endl,我调了一下午！



```
#include<bits/stdc++.h>

using namespace std;

const int N = 1e5 + 10;
typedef long long ll;


int n, m, q, tot, rt[N], a[N];
ll mi[N];
vector<int> vx;

struct segtree
{
	int l, r, cnt;
	ll s, val; 
}seg[N * 30];

void update(int id)
{
	seg[id].s = seg[seg[id].l].s + seg[seg[id].r].s;
	seg[id].cnt = seg[seg[id].l].cnt + seg[seg[id].r].cnt;
}

int build(int l, int r)
{
	int id = ++tot;
	if(l == r)
	{
		return id;
	}
	int mid = (l + r) >> 1;
	seg[id].l = build(l, mid);
	seg[id].r = build(mid + 1, r);
	update(id);
	return id;
}

int change(int u, int l, int r, int pos)
{
	int id = ++tot;
	seg[id] = seg[u];
	if(l == r)
	{
		seg[id].s = seg[id].s + vx[pos - 1];
		seg[id].cnt = seg[id].cnt + 1;
		seg[id].val = vx[l - 1];
		return id;
	}
	int mid = (l + r) >> 1;
	if(pos <= mid)
		seg[id].l = change(seg[id].l, l, mid, pos);
	else
		seg[id].r = change(seg[id].r, mid + 1, r, pos);
	update(id);
	return id;
}

ll query(int v, int u, int l, int r, int k)
{
	if(l == r)
	{
		return seg[u].val * k;
	}
	int mid = (l + r) >> 1;
	int tmp = seg[seg[u].r].cnt - seg[seg[v].r].cnt;
	if(tmp >= k)
		return query(seg[v].r, seg[u].r, mid + 1, r, k);
	else
		return seg[seg[u].r].s - seg[seg[v].r].s
		+ query(seg[v].l, seg[u].l, l, mid, k - tmp);
}

void  solve()
{
	tot = 0;
	vx.clear();
	
	cin>>n;
	for(int i = 1; i <= n; i++)
	{
		cin>>a[i];
		vx.push_back(a[i]);
	}
	
	sort(vx.begin(), vx.end());
	vx.erase(unique(vx.begin(), vx.end()), vx.end());	
	int m = vx.size();
	
	rt[0] = build(1, m);
	for(int i = 1; i <= n; i++)
	{
		int pos = lower_bound(vx.begin(), vx.end(), a[i]) - vx.begin() + 1;
		rt[i] = change(rt[i - 1], 1, m, pos);
	}

	cin>>q;
	for(int i = 1; i <= q; i++)
	{
		int l, r, k;	cin>>l>>r>>k;
		int mm = r - l + 1;
		int x = l, y = l + mm - 1;
		ll ans = query(rt[x - 1], rt[y], 1, m, k) + mi[mm];
		cout<<ans<<'\n'; 
	}
}

int main()
{
	ios::sync_with_stdio(false);
	cin.tie(nullptr);
	cout.tie(nullptr);
	int tc = 1;
	for(int i = 1; i <= 100000; i++)
		mi[i] = mi[i - 1] + 1ll * i * i;	
	cin>>tc;
	while(tc--)
	{
		solve();
	}
}
```
{% endraw %}
