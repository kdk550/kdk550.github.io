---
layout: post
title: "UVA11437 Triangle Fun"
date: 2021-11-15 22:53:00 +0800
updated: 2021-11-15 23:36:00 +0800
description: "这是一道入门计算几何题，偏数学，和算法关系不大 我逛了一圈题解发现都是用的数学求法，这里我就用计算几何来水我第一篇洛谷题解 步骤： 1.求三等分点 2.求交点 3.叉积求面积 梅涅劳斯定理也可以做，详情见洛谷题解"
excerpt: "这是一道入门计算几何题，偏数学，和算法关系不大 我逛了一圈题解发现都是用的数学求法，这里我就用计算几何来水我第一篇洛谷题解 步骤： 1.求三等分点 2.求交点 3.叉积求面积 梅涅劳斯定理也可以做，详情见洛谷题解"
categories: []
tags: ["computational geometry"]
comments: false
related_posts: false
---
{% raw %}
这是一道入门计算几何题，偏数学，和算法关系不大

我逛了一圈题解发现都是用的数学求法，这里我就用计算几何来水我第一篇洛谷题解  
步骤：  
1.求三等分点  
2.求交点  
3.叉积求面积

梅涅劳斯定理也可以做，详情见[洛谷题解](https://www.luogu.com.cn/problem/solution/UVA11437)



```cpp
#include<iostream>
#include<algorithm>
#include<cmath>
#include<math.h>
#include<vector>
using namespace std;

//模板 
#define x first 
#define y second

typedef pair<double,double>PDD;

PDD operator + (PDD A,PDD B)
{
	return {A.x+B.x,A.y+B.y};
}
PDD operator - (PDD A,PDD B)
{
	return {A.x-B.x,A.y-B.y};
}
PDD operator * (PDD A,double p)
{
	return {A.x*p,A.y*p};
}

PDD operator / (PDD A,double p)
{
	return {A.x/p,A.y/p};
}
PDD get_point(PDD B,PDD C)
{
	PDD v1=B+(C-B)/3;
	return {v1.x,v1.y};
}
double cross(PDD a,PDD b)
{
	return a.x*b.y-a.y*b.x;
}
PDD getlineintersection(PDD p,PDD v,PDD q,PDD w)
{
	auto u=p-q;
	double t=cross(w,u)/cross(v,w);
	return PDD{p.x+v.x*t,p.y+v.y*t};
}


int main()
{
	int n;
	cin>>n;
	while(n--)
	{
		PDD A,B,C,D,E,F;
		double x1,y1,x2,y2,x3,y3;
		cin>>x1>>y1>>x2>>y2>>x3>>y3;

		A={x1,y1},B={x2,y2},C={x3,y3};

		D=get_point(B,C);
		E=get_point(C,A);
		F=get_point(A,B);
		//求三等分点 
		
  		PDD P,Q,R;
  		
  		P=getlineintersection(A,D-A,B,E-B);
  		Q=getlineintersection(B,E-B,C,F-C);
  		R=getlineintersection(C,F-C,A,D-A);
  		//求交点 
  		
		printf("%.0lf\n",cross(Q-P,R-P)/2);
		//叉积求面积 
	}	
	return 0;	
}
```
{% endraw %}
