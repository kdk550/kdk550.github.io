---
layout: post
title: "洛谷P2089 烤鸡"
date: 2021-07-25 21:25:00 +0800
updated: 2023-01-21 19:10:00 +0800
description: "暴力枚举 我现在还不会搜索 这么多}是我程序循环出了问题找的过程中产生的,是我for循环地末尾循环体用的都是a出错"
excerpt: "暴力枚举 我现在还不会搜索 这么多}是我程序循环出了问题找的过程中产生的,是我for循环地末尾循环体用的都是a出错"
categories: []
tags: ["algorithm basics"]
comments: false
related_posts: false
---
{% raw %}
暴力枚举

我现在还不会搜索



```cpp
#include<iostream>
using namespace std;
int main()
{
	int n=0, ans=0;
	cin >> n;
	for(int a=1;a<=3;a++)
	{
		for (int b = 1; b<= 3; b++)
		{ 
			for (int c = 1; c <= 3; c++)
			{ 
				for (int d = 1; d <= 3; d++)
				{ 
					for (int e = 1; e <= 3; e++)
					{ 
						for (int f = 1; f <= 3; f++)
						{ 
							for (int g = 1; g <= 3; g++)
							{
							
								for (int h = 1; h <= 3; h++)
								{
									for (int i = 1; i <= 3; i++)
									{				
										for (int j = 1; j <= 3;j++)
										{
											if (a + b + c + d + e + f + g + h + i + j == n)  	
											{
												ans=ans+1;
											}
										}
									}
							    }
							}
						}
					}
							
				} 
			} 
		} 
	}											
	cout << ans << endl;
	for(int a=1;a<=3;a++)
	{
		for (int b = 1; b<= 3; b++)
		{ 
			for (int c = 1; c <= 3;c++)
			{ 
				for (int d = 1; d <= 3; d++)
				{ 
					for (int e = 1; e <= 3; e++)
					{ 
						for (int f = 1; f <= 3; f++)
						{ 
							for (int g = 1; g <= 3; g++)
							{
							
								for (int h = 1; h <= 3; h++)
								{
									for (int i = 1; i <= 3; i++)
									{				
										for (int j = 1; j <= 3; j++)
										{
											if (a + b + c + d + e + f + g + h + i + j == n)  	
											{
												cout<<a<<" "<<b<<" "<<c<<" "<<d<<" "<<e<<" "<<f<<" "<<g<<" "<<h<<" "<<i<<" "<<j<<endl;
											}											
										}
									}
							    }
							}
						}
					}
							
				} 
			} 
		} 
	}		
	return 0;
```



　　这么多}是我程序循环出了问题找的过程中产生的,是我for循环地末尾循环体用的都是a出错
{% endraw %}
