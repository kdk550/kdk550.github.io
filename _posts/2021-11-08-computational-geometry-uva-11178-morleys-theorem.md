---
layout: post
title: "计算几何Uva11178 - Morley's Theorem"
date: 2021-11-08 23:08:00 +0800
updated: 2021-11-15 22:57:00 +0800
description: "这里模板是AcWing y总的和算法竞赛入门经典的 题目让我们求三角形角的三等分角与其他三等分角的交点的笛卡尔坐标（原pdf有图很详细，这里可能表述错误） 但实际上就是模板操作 例如题目图中∠D的求法，作法 1.求出三等分角，2.旋转，3.求交点 都可用模板完成 ∠E和∠F也是同样的求法，并运用三角形的对称性，只用写…"
excerpt: "这里模板是AcWing y总的和算法竞赛入门经典的 题目让我们求三角形角的三等分角与其他三等分角的交点的笛卡尔坐标（原pdf有图很详细，这里可能表述错误） 但实际上就是模板操作 例如题目图中∠D的求法，作法 1.求出三等分角，2.旋转，3.求交点 都可用模板完成 ∠E和∠F也是同样的求法，并运用三角形的对称性，只用写…"
categories: []
tags: ["computational geometry"]
comments: false
related_posts: false
---
{% raw %}
这里模板是AcWing y总的和算法竞赛入门经典的

题目让我们求三角形角的三等分角与其他三等分角的交点的笛卡尔坐标（原pdf有图很详细，这里可能表述错误）

但实际上就是模板操作

例如题目图中∠D的求法，作法   1.求出三等分角，2.旋转，3.求交点    都可用模板完成

∠E和∠F也是同样的求法，并运用三角形的对称性，只用写一个函数。



```
//Uva  11178 - Morley's Theorem

#include<iostream>
#include<vector>
#include<cmath>
#include<algorithm>
#include<math.h>
using namespace std;


struct Point 
{
    double x,y;
    Point(double x=0,double y=0):x(x),y(y){ }
};
typedef Point Vector;


Vector operator -(Point A,Point B)
{
    return Vector(A.x-B.x,A.y-B.y);
}

Vector operator +(Point A,Point B)
{
    return Vector(A.x+B.x,A.y+B.y);
}

Vector operator *(Point A,double p)
{
    return Vector(A.x*p,A.y*p);
}

Vector operator /(Vector A,double p)
{
    return Vector(A.x/p,A.y/p);
}

double dot(Point a,Point b)
{
    return a.x*b.x+a.y*b.y;
}

double cross(Point a,Point b)
{
    return a.x*b.y-b.x*a.y;
}

double get_length(Point a)
{
    return sqrt(dot(a,a));
}

double get_angle(Vector a,Vector b)
{
    return acos(dot(a,b)/get_length(a)/get_length(b));
}


Point rotate(Point a,double angle)
{
    return Point(a.x*cos(angle)-a.y*sin(angle),a.x*sin(angle)+a.y*cos(angle));   
}

Point get_line_intersection(Point p,Point v,Point q,Point w)
{
    Vector u=p-q;
    double t=cross(w,u)/cross(v,w);
    return p+v*t; 
}

Point getD(Point A,Point B,Point C)
{
    Point v1=C-B;
    double ang1=get_angle(A-B,v1);
    v1=rotate(v1,ang1/3);

    Point v2=B-C;
    double ang2=get_angle(A-C,v2);
    v2=rotate(v2,-ang2/3);

    return get_line_intersection(B,v1,C,v2);
}
Point readpoint()
{
    double x,y;
    cin>>x>>y;
    return Vector{x,y};
}
int main()
{
    int t;
    cin>>t;
    while(t--)
    {
        Point A,B,C,D,E,F;
        double a,b,c,d,e,f;
        A=readpoint();
        B=readpoint();
        C=readpoint();
     
        
        D=getD(A,B,C);
        E=getD(B,C,A);
        F=getD(C,A,B);
        printf("%.6lf %.6lf %.6lf %.6lf %.6lf %.6lf\n",D.x,D.y,E.x,E.y,F.x,F.y);
    }
    return 0;
}
```
{% endraw %}
