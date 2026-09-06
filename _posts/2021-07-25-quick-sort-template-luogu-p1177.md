---
layout: post
title: "快速排序——模板           洛谷P1177 【模板】快速排序"
date: 2021-07-25 15:09:00 +0800
updated: 2023-01-21 19:09:00 +0800
description: "algorithm自带的sort，sort是升序， 降序"
excerpt: "algorithm自带的sort，sort是升序， 降序"
categories: []
tags: ["algorithm basics"]
comments: false
related_posts: false
---
{% raw %}
```
#include<iostream>
#include<cstdio>
int a[10000001];
using namespace std;
void qsort(int i, int j)
{
    int left = i, right = j;
    int flag = a[(left+ right) / 2];
    int tmp;
    do {
        while (a[left] < flag)        left++;
        while (a[right] > flag)        right--;
        if (left <= right)
        {
            tmp = a[left];
            a[left] = a[right];
            a[right] = tmp;
            left++;
            right--;
        }
    } while (left <= right);
    if (left < j)    qsort(left, j);
    if (right > i)    qsort(i, right);
}
int main()
{
    int n;
    cin >> n;
    for (int i = 1; i <= n; i++)        cin >> a[i];
    qsort(1, n);
    for (int i = 1; i <= n; i++)
        cout << a[i]<<" ";
    return 0;
}
```



 algorithm自带的sort，sort是升序，

<https://www.cnblogs.com/icesunbo/p/11484046.html>

<https://www.cnblogs.com/buanxu/p/12772700.html>



```
#include<iostream>
#include<cstdio>
#include<algorithm>
using namespace std;
int a[1000010], n;
int main()
{

    cin >> n;
    for (int i = 0; i <n; i++)
        cin >> a[i];
    sort(a , a + n);
    for (int i = 0; i <n; i++)
        cout << a[i] << " ";
    return 0;
}
```



降序



```cpp
#include<iostream>
#include<cstdio>
#include<algorithm>
using namespace std;
int a[1000010], n;
bool compare(int a, int b)
{
	return a > b;
}
int main()
{

	cin >> n;
	for (int i = 0; i < n; i++)
		cin >> a[i];
	sort(a, a + n,compare);
	for (int i = 0; i < n; i++)
		cout << a[i] << " ";
	return 0;
}
```
{% endraw %}
