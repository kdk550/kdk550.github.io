---
layout: post
title: "数论分块总结"
date: 2023-05-08 10:32:00 +0800
updated: 2023-05-08 11:44:00 +0800
description: "AtCoder abc230\\ e E - Fraction Floor Sum AtCoder abc230\\ e Fraction Floor Sum 求: \\[\\sum {i = 1}^N ⌊\\dfrac{N}{i}⌋ \\] 是一个很裸的数论分块 P2261 [CQOI2007]余数求和 [P2261 [CQO…"
excerpt: "AtCoder abc230\\ e E - Fraction Floor Sum AtCoder abc230\\ e Fraction Floor Sum 求: \\[\\sum {i = 1}^N ⌊\\dfrac{N}{i}⌋ \\] 是一个很裸的数论分块 P2261 [CQOI2007]余数求和 [P2261 [CQO…"
categories: []
tags: ["mathematics"]
comments: false
related_posts: false
---
{% raw %}
## AtCoder abc230\_e E - Fraction Floor Sum

[AtCoder abc230\_e Fraction Floor Sum](https://atcoder.jp/contests/abc230/tasks/abc230_e?lang=en "AtCoder abc230_e Fraction Floor Sum")

求:

<div class="math display">\[\sum_{i = 1}^N ⌊\dfrac{N}{i}⌋
\]</div>

是一个很裸的数论分块



```cpp
ll ans = 0;
void solve()
{   
	ll n;	cin>>n;
	for(ll l = 1; l <= n; l++)
	{
		ll d = n / l, r = n / d;
		ans += (r - l + 1) * d;
		l = r;
	}
	cout<<ans<<endl;
    return;
}
```



## P2261 [CQOI2007]余数求和

[P2261 [CQOI2007]余数求和](https://www.luogu.com.cn/problem/P2261 "P2261 [CQOI2007]余数求和")

化简一下：

<div class="math display">\[G(n, k) = \sum_{i = 1}^n k \bmod i = \sum_{i = 1}^n (k - i  \times⌊\dfrac{k}{i} ⌋) = n \times k - \sum_{i = 1}^n i  \times⌊\dfrac{k}{i}⌋ 
\]</div>

- 发现$\sum_{i = 1}^n i  \times⌊\dfrac{k}{i}⌋ $可以数论分块来做
- 式子<span class="math inline">\(i \times⌊\dfrac{k}{i}⌋\)</span> 中<span class="math inline">\(⌊\dfrac{k}{i}⌋\)</span> 是确定的，对于<span class="math inline">\([l, r]\)</span>的贡献区间用一个等差数列前n项和数列解决



```cpp
ll n, k;
void solve()
{
	cin>>n>>k;
	ll res = n * k;
	for(ll l = 1; l <= n; l++)
	{
		ll d = k / l, r;
		if(d == 0)
			r = n;
		else	
			r = min(n, k / d);
		ll m = r - l + 1;
		res -= d * (l + r) * m / 2;
		l = r;
	}
	cout<<res<<endl;
}
```



## The 18th Zhejiang Provincial Collegiate Programming Contest F. Fair Distribution

[F. Fair Distribution](https://codeforces.com/gym/103055/problem/F "F. Fair Distribution")

参考：[Fair Distribution（分块除法）](https://zhuanlan.zhihu.com/p/416369031 "Fair Distribution（分块除法）")，[x / k向上取整转换为向下取整](https://blog.csdn.net/qq_39445165/article/details/118117368 "x / k向上取整转换为向下取整")

操作可以减少<span class="math inline">\(n\)</span>，增加<span class="math inline">\(m\)</span>,求最小操作数使得<span class="math inline">\(m \bmod n = 0\)</span>

设 <span class="math inline">\(m\)</span> 的操作数为：<span class="math inline">\(⌈\dfrac{m}{n -x} ⌉ \times (n - x) - m\)</span>

设 <span class="math inline">\(n\)</span> 的操作数: <span class="math inline">\(x\)</span>

则<span class="math inline">\(\text{ans} = ⌈\dfrac{m}{n - x} ⌉ \times (n - x) - m + x\)</span>

设 <span class="math inline">\(l = n - x\)</span>，则有<span class="math inline">\(x = n - l\)</span>  
即：

<div class="math display">\[⌈\dfrac{m}{n - x} ⌉ \times (n - x) - m + x = ⌈\dfrac{m}{l} ⌉ \times l - m + n - l
\]</div>

这里有一个<span class="math inline">\(-l\)</span>直接用数论分块做不了，我们用向上取整转化成向下取整消去，向上取整转化成向下取整有这样的公式:

<div class="math display">\[⌈\dfrac{x}{k} ⌉ = ⌊\dfrac{x + k - 1}{k} ⌋
\]</div>

这里还有减去一个<span class="math inline">\(l\)</span>

<div class="math display">\[⌈\dfrac{m}{l}⌉ \times l - l  = ⌊\dfrac{m - 1}{l} ⌋ \times l
\]</div>

所以：

<div class="math display">\[⌈\dfrac{m}{n - x} ⌉ \times (n - x) - m + x =  ⌊\dfrac{m - 1}{l} ⌋ \times l - m + n
\]</div>

然后进行数论分块



```cpp

ll n, m;
void solve()
{
	cin>>n>>m;
	if(m % n == 0)
	{
		cout<<0<<endl;
		return;
	}
	else if(m < n)
	{
		cout<<n - m<<endl;
		return;
	}
	ll res = 1e18;
	for(ll l = 1; l <= n; l++)
	{
		ll d = (m - 1) / l, r;
		if((m - 1) / d == 0)
			r = n;
		else
			r = (m - 1) / d;
		res = min(res, (m - 1) / l * l - m + n);
		l = r;
	}
	cout<<res<<endl;
}
```
{% endraw %}
