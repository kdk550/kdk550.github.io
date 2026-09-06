---
layout: post
title: "[NOIP2015 普及组] 扫雷游戏"
date: 2021-07-23 00:35:00 +0800
updated: 2023-01-21 19:09:00 +0800
description: "这是我的题解,洛谷100全AC了，但或许会有小瑕疵 那个判定地雷还可以做的更好"
excerpt: "这是我的题解,洛谷100全AC了，但或许会有小瑕疵 那个判定地雷还可以做的更好"
categories: []
tags: ["algorithm basics"]
comments: false
related_posts: false
---
{% raw %}
```cpp
#include<iostream>
#include<cstdio>
using namespace std;
int main()
{
	char a[110][110] = { 0 };　　　　　　　　　　//由于输入与输入不同，0可以将要检测的包围起来　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　//函数外定义的变量初始默认值为0，当然这里也可以
	int n, m;
	cin >> n >> m;
	//输入
	for (int i = 1; i <= n; i++)
	{
		for (int k = 1; k <= m; k++)
		{
			cin >> a[i][k];
		}
	}//输入
	for (int i = 1; i <= n; i++)
	{
		for (int k = 1; k <= m; k++)
		{
			if (a[i][k] != '*')
			{
				int sum = 0;
				if (a[i - 1][k - 1] == '*')	sum++;
				if (a[i - 1][k] == '*')	sum++;
				if (a[i - 1][k + 1] == '*')	sum++;
				if (a[i][k - 1] == '*')	sum++;
				if (a[i][k + 1] == '*')	sum++;
				if (a[i + 1][k - 1] == '*')	sum++;
				if (a[i + 1][k] == '*')	sum++;
				if (a[i + 1][k + 1] == '*')	sum++;　　　　//对周围的地雷进行判定
				cout << sum++;
			}
			else
				cout << "*";
		}
		cout << endl;
	}


	return 0;
}
```



　这是我的题解,洛谷100全AC了，但或许会有小瑕疵

那个判定地雷还可以做的更好
{% endraw %}
