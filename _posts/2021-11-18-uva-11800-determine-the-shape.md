---
layout: post
title: "UVA11800 Determine the Shape"
date: 2021-11-18 00:21:00 +0800
updated: 2021-11-18 00:21:00 +0800
description: "题意得： 1.Square 四条边相等，四个角相等 2.Rectangle 对边相等，四个角相等 3.Rhombus 四条边相等，对角相等 4.Parallelogram 对边相等，对边平行 5.Trapezium 两条边平行 6.Ordinary Quadrilateral 前面条件不满足，就输出这个 思路：由于题…"
excerpt: "题意得： 1.Square 四条边相等，四个角相等 2.Rectangle 对边相等，四个角相等 3.Rhombus 四条边相等，对角相等 4.Parallelogram 对边相等，对边平行 5.Trapezium 两条边平行 6.Ordinary Quadrilateral 前面条件不满足，就输出这个 思路：由于题…"
categories: []
tags: ["computational geometry"]
comments: false
related_posts: false
---
{% raw %}
**题意得：**

**1.Square 　　　　　　　　四条边相等，四个角相等**

**2.Rectangle　　  　　　　  对边相等，四个角相等**

**3.Rhombus　　　 　　　　四条边相等，对角相等**

**4.Parallelogram　  　　　　对边相等，对边平行**

**5.Trapezium　　　　　　　两条边平行**

**6.Ordinary Quadrilateral　　前面条件不满足，就输出这个**

**思路：由于题目给出的样例告诉我们点不是按照顺序给的，于是先对点按逆时针排序ABCD**

**逆时针排序的方法是凸包，ch[ ]为凸包的点**

**但其实有一种方法可以不用凸包的，从一般四边形开始到正方形，用一个值记录最大符合哪一种形状，**

**用一个函数去实现，调用(a,b,c,d),(a,c,b,d),(a,b,d,c)来处理顺序不同的情况，由于我不是这种做法，我这里不展开，可以[见这位大佬的博客](https://tigerisland.blog.csdn.net/article/details/88784414)**



```
A=ch[0],B=ch[1],C=ch[2],D=ch[3];
```



**再分别求出各个点的距离**



```
        double sab,sbc,scd,sda,sad,sac,sbd;
        sab=get_length(B-A),sbc=get_length(C-B);
        scd=get_length(D-C),sda=get_length(A-D);
```



**各个点的角度**



```
        //求角度 
        double a,b,c,d;
        a=get_angle(D-A,B-A);
        b=get_angle(A-B,C-B);
        c=get_angle(B-C,D-C);
        d=get_angle(C-D,A-D);    
```



*需要加入一个特判，虽然题目里面说不会存在三点共线的问题，但还是存在的，使凸包会退化成线或者点*



```
        if(n<4)
        {
            printf("Ordinary Quadrilateral\n");
            continue;
        }
```



**判断形状**

**cross是叉积判断是否平行，平行的情况为0**



```
        if(dcmp(a-b)==0 && dcmp(b-c)==0 && dcmp(c-d)==0 && dcmp(d-a)==0 && dcmp(sab-sbc)==0 && dcmp(sbc-scd)==0 && dcmp(scd-sda)==0)
        {
            printf("Square\n");
        }
        else if(dcmp(a-b)==0 && dcmp(b-c)==0 && dcmp(c-d)==0 && dcmp(d-a)==0 && dcmp(sab-scd)==0 && dcmp(sda-sbc)==0)
        {
            printf("Rectangle\n");
        }
        else if(dcmp(sab-sbc)==0 && dcmp(sbc-scd)==0 && dcmp(scd-sda)==0&&dcmp(a-c)==0&&dcmp(b-d)==0)
        {
            printf("Rhombus\n");
        }
          else if(dcmp(sab-scd)==0 && dcmp(sbc-sda)==0&&dcmp(a-c)==0&&dcmp(b-d)==0)
          {
              printf("Parallelogram\n");
          }
          else if(dcmp(cross(B-A,C-D))==0 || dcmp(cross(C-B,D-A))==0)
          {
              printf("Trapezium\n");
          }
          else 
          {
              printf("Ordinary Quadrilateral\n");
          }
          
```



***完整AC代码：***



```
  1 #include<iostream>
  2 #include<cmath>
  3 #include<math.h>
  4 #include<algorithm>
  5 #include<vector>
  6 using namespace std;
  7 
  8 #define x first
  9 #define y second 
 10 
 11 const double eps=1e-9;
 12 typedef pair<double,double>PDD;
 13 
 14 PDD A,B,C,D;
 15 
 16 PDD operator - (PDD A,PDD B)
 17 {
 18     return PDD{A.x-B.x,A.y-B.y};
 19 }
 20 int dcmp(double x)
 21 {
 22     if(fabs(x)<eps)    return 0;
 23     if(x<0)        return -1;
 24     return 1;
 25 }
 26 
 27 
 28 double get_length(PDD A)
 29 {
 30     return sqrt(A.x*A.x+A.y*A.y);
 31 }
 32 
 33 
 34 double dot(PDD A,PDD B)
 35 {
 36     return A.x*B.x+A.y*B.y;
 37 }
 38 
 39 double get_angle(PDD A,PDD B)
 40 {
 41     return acos(dot(A,B)/get_length(A)/get_length(B));
 42 }
 43 
 44 double cross(PDD A,PDD B)
 45 {
 46     return A.x*B.y-A.y*B.x;
 47 }
 48 
 49 
 50 int convexhull(PDD* p,int n,PDD* ch)
 51 {
 52     p[0]=A,p[1]=B,p[2]=C,p[3]=D;
 53     sort(p,p+n);
 54     int m=0;
 55     for(int i=0;i<n;i++)
 56     {
 57         while(m>1 && cross(ch[m-1]-ch[m-2],p[i]-ch[m-2])<=0)    m--;
 58         ch[m++]=p[i]; 
 59     }
 60     int k=m;
 61     for(int i=n-2;i>=0;i--)
 62     {
 63         while(m>k && cross(ch[m-1]-ch[m-2],p[i]-ch[m-2])<=0)    m--;
 64         ch[m++]=p[i];
 65     }
 66     if(n>1) m--;
 67     
 68     A=ch[0],B=ch[1],C=ch[2],D=ch[3];
 69     //逆时针赋值
 70     return m;
 71 }
 72 
 73 
 74 int main()
 75 {
 76     int t,flag=0;
 77     cin>>t;
 78     while(t--)
 79     {
 80         PDD ch[10],p[10];
 81         double x1,y1,x2,y2,x3,y3,x4,y4;
 82         cin>>x1>>y1>>x2>>y2>>x3>>y3>>x4>>y4;
 83         
 84         A={x1,y1},B={x2,y2},C={x3,y3},D={x4,y4};
 85         p[0]=A,p[1]=B,p[2]=C,p[3]=D;
 86         
 87         int n=convexhull(p,4,ch);
 88         
 89         double sab,sbc,scd,sda,sad,sac,sbd;
 90         sab=get_length(B-A),sbc=get_length(C-B);
 91         scd=get_length(D-C),sda=get_length(A-D);
 92 
 93         
 94         //求角度 
 95         double a,b,c,d;
 96         a=get_angle(D-A,B-A);
 97         b=get_angle(A-B,C-B);
 98         c=get_angle(B-C,D-C);
 99         d=get_angle(C-D,A-D);    
100         
101         
102         
103         printf("Case %d: ",++flag);
104         if(n<4)
105         {
106             printf("Ordinary Quadrilateral\n");
107             continue;
108         }
109     
110         if(dcmp(a-b)==0 && dcmp(b-c)==0 && dcmp(c-d)==0 && dcmp(d-a)==0 && dcmp(sab-sbc)==0 && dcmp(sbc-scd)==0 && dcmp(scd-sda)==0)
111         {
112             printf("Square\n");
113         }
114         else if(dcmp(a-b)==0 && dcmp(b-c)==0 && dcmp(c-d)==0 && dcmp(d-a)==0 && dcmp(sab-scd)==0 && dcmp(sda-sbc)==0)
115         {
116             printf("Rectangle\n");
117         }
118         else if(dcmp(sab-sbc)==0 && dcmp(sbc-scd)==0 && dcmp(scd-sda)==0&&dcmp(a-c)==0&&dcmp(b-d)==0)
119         {
120             printf("Rhombus\n");
121         }
122           else if(dcmp(sab-scd)==0 && dcmp(sbc-sda)==0&&dcmp(a-c)==0&&dcmp(b-d)==0)
123           {
124               printf("Parallelogram\n");
125           }
126           else if(dcmp(cross(B-A,C-D))==0 || dcmp(cross(C-B,D-A))==0)
127           {
128               printf("Trapezium\n");
129           }
130           else 
131           {
132               printf("Ordinary Quadrilateral\n");
133           }
134           
135     }
136     return 0;
137 }
```



最后贴一下这题的艰辛，我快累死了

![](/assets/img/blog/posts/4f4dd7c3450ba3d7380d38ed416edfd60f1d34767e831087335f1e839d66c63d.png)
{% endraw %}
