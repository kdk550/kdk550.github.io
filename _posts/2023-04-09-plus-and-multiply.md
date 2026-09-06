---
layout: post
title: "B. Plus and Multiply"
date: 2023-04-09 22:29:00 +0800
updated: 2023-04-09 22:31:00 +0800
description: "B. Plus and Multiply 手模拟了一下 观察每个式子，化简得到: $a^x + by = n $ 由于$a^x$是指数增长，直接枚举它的幂次即可，注意对$a=1$的情况特判"
excerpt: "B. Plus and Multiply 手模拟了一下 观察每个式子，化简得到: $a^x + by = n $ 由于$a^x$是指数增长，直接枚举它的幂次即可，注意对$a=1$的情况特判"
categories: []
tags: ["contest", "constructive algorithms"]
comments: false
related_posts: false
---
{% raw %}
[B. Plus and Multiply](https://codeforces.com/problemset/problem/1542/B "B. Plus and Multiply")

手模拟了一下

![image](/assets/img/blog/posts/df171d633a4ddf933e51940513770845ba4f8fe5b5053e0541206c5ce6797885.jpg)  
观察每个式子，化简得到:

$a^x + by = n $ 
由于$a^x$是指数增长，直接枚举它的幂次即可，注意对$a=1$的情况特判


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

const int mod = 1e9 + 7;
const int N = 1e5 + 10;

void solve()
{
    ll n, a, b;
    cin>>n>>a>>b;
    if(b == 1)
    {
        cout<<"YES"<<endl;
        return;
    }
    if(a == 1)
    {
        if((n - 1) % b == 0)
        {
            cout<<"YES"<<endl;

        }
        else
            cout<<"NO"<<endl;
        return;
    }
    bool ok = false;
    for(ll i = 0; pow(a, i) <= n; i++)
    {
        ll t1 = pow(a, i);
        if((n - t1) % b == 0)
            ok = true;
    }
    if(ok)
        cout<<"YES"<<endl;
    else cout<<"NO"<<endl;


    return;
}


int main()
{
    //std::ios::sync_with_stdio(false);   cin.tie(nullptr), cout.tie(nullptr);
    // 特殊输入 请注释上方，如__int128等
    int TC = 1;

    cin >> TC;
    for(int tc = 1; tc <= TC; tc++)
    {
        //cout << "Case #" << tc << ": ";
        solve();
    }



    return 0;
}
```
{% endraw %}
