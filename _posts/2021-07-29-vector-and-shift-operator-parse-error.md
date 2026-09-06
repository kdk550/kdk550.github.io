---
layout: post
title: "vector    及被认为是移位运算符而编译错误"
date: 2021-07-29 11:33:00 +0800
updated: 2023-01-21 19:11:00 +0800
description: "vector菜鸟编程链接 STL容器的可变长度数组，头文件 include 1. vector v(N,i) 建立一个可变长度数组v，内部元素类型为int，最开始有N个元素，都初始化为i。可省略i（默认值为0），也可以把（N，i）省略，此时这个数组的长度就是0.也可以用double 2. v.push\\ back(a…"
excerpt: "vector菜鸟编程链接 STL容器的可变长度数组，头文件 include 1. vector v(N,i) 建立一个可变长度数组v，内部元素类型为int，最开始有N个元素，都初始化为i。可省略i（默认值为0），也可以把（N，i）省略，此时这个数组的长度就是0.也可以用double 2. v.push\\ back(a…"
categories: []
tags: ["posts"]
comments: false
related_posts: false
---
{% raw %}
[vector菜鸟编程链接](https://www.runoob.com/w3cnote/cpp-vector-container-analysis.html)

**STL容器的可变长度数组，头文件#include<vector>**

**1.   vector<int>v(N,i)　建立一个可变长度数组v，内部元素类型为int，最开始有N个元素，都初始化为i。可省略i（默认值为0），也可以把（N，i）省略，此时这个数组的长度就是0.也可以用double**

**2.  v.push\_back(a)  将元素a插入到数组v的末尾，并增加数组长度**

**3.  v.size()   返回数组v的长度**

**4.  v.resize(n,m)  重新调整数组大小为n，如果n比原来的小，这删除多余的信息，如果n比原来大，则新增的部分都初始化为m，其中m也是可以省略**

**可以像普通数组一样使用方括号索引，比如v[2333]就可以访问对应的元素，但注意数组的大小必须小于索引，否则和访问普通数组越界一样而访问无效内存，可以使用push\_back或resize成员函数来增加数组长度**

**5.  vector<int>**

**6.  v.begin()返回数组v首元素（也就是v[0]）的指针（迭代器）**

**7.  v.end()  返回数组v首元素末尾的下一个元素的指针（迭代器），，此指针有点类似于空指针，不指向任何元素**

**区别**

**verctor<int>是声明向量容器；  
例如 verctor<int> v,就是创建了一个名字叫v的向量容器。  
  
vector<int>::iterator是定义向量迭代器  
例如，vector<int>::iterator it 就可以  
for(it=v.begin();it!=v.end();it++)  
cout<<\*it<<endl;**

**另外：**

**v[i]和\*(v.begin()+i)是一样的，都是取对应元素的值**

**被认为是移位运算符而编译错误：**

洛谷[P3613 【深基15.例2】寄包柜](https://www.luogu.com.cn/problem/P3613)

洛谷评测错误信息  
**/tmp/compiler\_z06mpz4\_/src: 在函数‘int main()’中:
/tmp/compiler\_z06mpz4\_/src:8:19: 错误：在嵌套模板实参列表中应当使用‘> >’而非‘>>’
vector<vector<int>>locker(n + 1);
^~
> >
/tmp/compiler\_z06mpz4\_/src:15:25: 警告：comparison of integer expressions of different signedness: ‘std::vector<int>::size\_type’ {aka ‘long unsigned int’} and ‘int’ [-Wsign-compare]
if (locker[i].size() < j + 1)
~~~~~~~~~~~~~~~~~^~~~~~~**

错误代码：



```
#include<iostream>
#include<vector>
using namespace std;
int n, q, opt, i, j, k;
int main()
{
    cin >> n >> q;
    vector<vector<int>>locker(n + 1);
    while (q--)
    {
        cin >> opt;
        if (opt == 1)
        {
            cin >> i >> j >> k;
            if (locker[i].size() < j + 1)
                locker[i].resize(j + 1);
            locker[i][j] = k;
        }
        else {
            cin >> i >> j;
            cout << locker[i][j] << endl;
        }
    }
    return 0;
}
```



后面我加了一个空格，才AC



```
vector< vector<int> >locker(n + 1);
```



**这是因为被认为是移位运算符而编译错误**
{% endraw %}
