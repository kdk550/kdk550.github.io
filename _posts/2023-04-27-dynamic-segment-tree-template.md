---
layout: post
title: "线段树的动态开点模板"
date: 2023-04-27 18:00:00 +0800
updated: 2023-04-27 18:01:00 +0800
description: "学习自 数据结构学习笔记(5)动态开点线段树动态开点线段树\") 动态开点线段树 感谢大佬们博客的帮助"
excerpt: "学习自 数据结构学习笔记(5)动态开点线段树动态开点线段树\") 动态开点线段树 感谢大佬们博客的帮助"
categories: []
tags: ["data structures"]
comments: false
related_posts: false
---
{% raw %}
学习自

[数据结构学习笔记(5)动态开点线段树](https://zhuanlan.zhihu.com/p/559047943 "数据结构学习笔记(5)动态开点线段树")

[动态开点线段树](https://www.luogu.com.cn/blog/Locked-Fog/dong-tai-kai-dian-xian-duan-shu "动态开点线段树")

感谢大佬们博客的帮助



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
	int l, r;
	ll s, tag;
}seg[N * 30];
int n, m, tot = 1;

void update(int &id)
{
	seg[id].s = seg[seg[id].l].s + seg[seg[id].r].s;
}

void settag(int id, int sz, ll t)
{
	seg[id].s += t * sz;
	seg[id].tag += t;
}

void pushdown(int id, int l, int r)
{
	if(seg[id].tag == 0) return;
	if(seg[id].l == 0)	seg[id].l = ++tot;
	if(seg[id].r == 0)	seg[id].r = ++tot;


	int mid = (l + r) >> 1;
	if(seg[id].l != 0)
		settag(seg[id].l, mid - l + 1, seg[id].tag);
	if(seg[id].r != 0)
		settag(seg[id].r, r - mid, seg[id].tag);
	seg[id].tag = 0;
}

void change(int &id, int l, int r, int pos, int val)
{
	if(!id) 
		id = ++tot;
	if(l == r)
	{
		seg[id].s = val;
		return;
	}
	int mid = (l + r) >> 1;
	if(pos <= mid)
		change(seg[id].l, l, mid, pos, val);
	else
		change(seg[id].r, mid + 1, r, pos, val);
	update(id);
}

void modify(int &id, int l, int r, int ql, int qr, ll t)
{
	if(!id)
		id = ++tot;
	if(l == ql && r == qr)
	{
		settag(id, r - l + 1, t);
		return;
	}
	pushdown(id, l ,r);
	int mid = (l + r) >> 1;
	if(qr <= mid)
		modify(seg[id].l, l, mid, ql, qr, t);
	else if(ql > mid)	
		modify(seg[id].r, mid + 1, r, ql, qr, t);
	else
	{
		modify(seg[id].l, l, mid, ql, mid, t);
		modify(seg[id].r, mid + 1, r, mid + 1, qr, t);
	}
	update(id);
}


ll query(int id, int l, int r, int ql, int qr)
{
	if(!id)
		id = ++tot;
	if(l == ql && r == qr)
	{
		return seg[id].s;
	}
	pushdown(id, l, r);
	int mid = (l + r) >> 1;
	if(qr <= mid)
		return query(seg[id].l, l, mid, ql, qr);
	else if(ql > mid)	
		return query(seg[id].r, mid + 1, r, ql, qr);
	else
		return query(seg[id].l, l, mid, ql, mid) +
			   query(seg[id].r , mid + 1, r, mid + 1, qr);
}


void solve()
{   
	cin>>n>>m;
	for(int i = 1; i <= n; i++)
	{
		int x, root = 1;	cin>>x;
		change(root, 1, n, i, x);
	}
	while(m--)
	{
		int opt, l, r;	cin>>opt>>l>>r;
		if(opt == 1)
		{
			ll x;	cin>>x;
			int root = 1;
			modify(root, 1, n, l, r, x);
		}
		else
			cout<<query(1, 1, n, l, r)<<endl;
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
{% endraw %}
