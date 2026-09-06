---
layout: post
title: "The 2022 ICPC Asia Nanjing Regional Contest"
date: 2023-09-01 00:45:00 +0800
updated: 2023-09-01 00:45:00 +0800
description: "The 2022 ICPC Asia Nanjing Regional Contest 出题人题解 目录 - The 2022 ICPC Asia Nanjing Regional Contest - I - Perfect Palindrome - G - Inscryption - A - Stop, Yeste…"
excerpt: "The 2022 ICPC Asia Nanjing Regional Contest 出题人题解 目录 - The 2022 ICPC Asia Nanjing Regional Contest - I - Perfect Palindrome - G - Inscryption - A - Stop, Yeste…"
categories: []
tags: ["contest"]
comments: false
related_posts: false
---
{% raw %}
# [The 2022 ICPC Asia Nanjing Regional Contest](https://codeforces.com/gym/104128)

[出题人题解](https://sua.ac/wiki/2022-icpc-nanjing/)

目录

- [The 2022 ICPC Asia Nanjing Regional Contest](/blog/2023/2022-icpc-asia-nanjing-regional-contest/#the-2022-icpc-asia-nanjing-regional-contest)
  - [I - Perfect Palindrome](/blog/2023/2022-icpc-asia-nanjing-regional-contest/#i---perfect-palindrome)
  - [G - Inscryption](/blog/2023/2022-icpc-asia-nanjing-regional-contest/#g---inscryption)
  - [A - Stop, Yesterday Please No More](/blog/2023/2022-icpc-asia-nanjing-regional-contest/#a---stop-yesterday-please-no-more)
  - [D - Chat Program](/blog/2023/2022-icpc-asia-nanjing-regional-contest/#d---chat-program)
  - [B - Ropeway](/blog/2023/2022-icpc-asia-nanjing-regional-contest/#b---ropeway)

vp的不是很好，就不放出来了，也算是补了一些题目了

## [I - Perfect Palindrome](https://codeforces.com/gym/104128/problem/I)

输出 <span class="math inline">\(\min _ {i = a} ^ {z} |s| - cnt[i]\)</span>



```cpp
#include<bits/stdc++.h>

using namespace std;

int a[30];

void solve()
{
	memset(a, 0, sizeof a);
	string s;	cin>>s;
	int n = s.size();
	int res = n;
	for(auto it : s)
	{
		a[it - 'a' + 1]++;
	}
	for(int i = 1; i <= 26; i++)
		res = min(n - a[i], res);
	cout<<res<<'\n';
}


int main()
{
	ios::sync_with_stdio(false);	cin.tie(nullptr);	cout.tie(nullptr);
	int tc = 1;
	cin>>tc;	
	while(tc--)
	solve();
}
```



## [G - Inscryption](https://codeforces.com/gym/104128/problem/G)

反悔贪心

对于 <span class="math inline">\(0\)</span> 的情况，优先做 <span class="math inline">\(-1\)</span> 的操作，若数量不够，就将之前 <span class="math inline">\(0\)</span> 做 <span class="math inline">\(-1\)</span> 的操作改为做 <span class="math inline">\(1\)</span> 的操作



```cpp
#include<bits/stdc++.h>

using namespace std;

const int N = 1e6 + 10;

typedef long long ll;
int n, a[N];

void solve()
{
    int sz = 1, s = 1;
    int e = 0, t = 0;
    cin>>n;
    for(int i = 1; i <= n; i++)
        cin>>a[i];
    for(int i = 1; i <= n; i++)
    {
        if(a[i] == 1)
            sz += 1, s += 1;
        else if(a[i] == -1)
        {
            if(sz >= 2)
                sz--;
            else if(t >= 1)
            {
                s++, sz++, t--;
            }
            else if(sz < 2)
            {
                cout<<-1<<'\n';return;
            } 
        }
        else if(a[i] == 0)
        {
            if(sz >= 2)
                sz--, t++;
            else s++, sz++;
        }
        // cout<<i<<"  "<<s<<"  "<<sz<<'\n';
    }
    // cout<<s<<"  "<<sz<<'\n';
    ll g = __gcd(s, sz);
    s /= g, sz /= g;
    cout<<s<<" "<<sz<<'\n';
}


int main()
{
    ios::sync_with_stdio(false);    cin.tie(nullptr);   cout.tie(nullptr);
    int tc = 1;
    cin>>tc;    
    while(tc--)
        solve();
}
```



## [A - Stop, Yesterday Please No More](https://codeforces.com/gym/104128/problem/A)



```cpp
#include<bits/stdc++.h>

using namespace std;

const int N = 2e3 + 10;
const int M = 1e3;
typedef long long ll;


int n, m, k, f[N][N];
string s;
int tl, tr, tu, td;
int l, r, u, d;
void solve()
{
    cin>>n>>m>>k;
    cin>>s;

    tl = 1, tr = m, tu = 1, td = n;
    l = 1, r = m, u = 1, d = n;
    for(auto it : s)
    {
        if(it == 'L')   tl++, tr++;
        if(it == 'R')   tl--, tr--;
        if(it == 'U')   tu++, td++;
        if(it == 'D')   tu--, td--;
        l = max(tl, l), r = min(tr, r);
        u = max(tu, u), d = min(td, d);
    }
    // cout<<"u: "<<u<<"  d: "<<d<<"   l: "<<l<<"  r: "<<r<<'\n';
    if(u > d || l > r)
    {
        if(k == 0)  cout<<n * m<<'\n';
        else cout<<0<<'\n';
        return;
    }
    int sum = (r - l + 1) * (d - u + 1);
    // cout<<sum<<'\n';
    int need = sum - k;
    if(need < 0)
    {
        cout<<0<<'\n';
        return;
    }
    // cout<<need<<'\n';
    for(int i = 0; i <= 2 * n + 5; i++)
        for(int j = 0; j <= 2 * m + 5; j++)
            f[i][j] = 0;    
    int nc = n + 1, mc = m + 1;
    int x = nc, y = mc;
    f[x][y] = 1;
    for(auto it : s)
    {
        if(it == 'L')   y++;
        if(it == 'R')   y--;
        if(it == 'U')   x++;
        if(it == 'D')   x--;
        f[x][y] = 1;
    }
    for(int i = 1; i <= 2 * n + 5; i++)
        for(int j = 1; j <= 2 * m + 5; j++)
            f[i][j] = f[i][j] + f[i - 1][j] + f[i][j - 1] - f[i - 1][j - 1];
    int res = 0;
    for(int i = 1; i <= n; i++)
    {
        for(int j = 1; j <= m; j++)
        {
            int x2 = nc - i, y2 = mc - j;
            int t = f[d + x2][r + y2] - f[u - 1 + x2][r + y2] 
            - f[d + x2][l - 1 + y2] + f[u - 1 + x2][l - 1 + y2];
        // int t = f[D + biasR][R + biasC] - f[U - 1 + biasR][R + biasC] 
        // - f[D + biasR][L - 1 + biasC] + f[U - 1 + biasR][L - 1 + biasC];
        // if (t == delta) ans++;
            if(t == need)
                res++;
        }
    }
    cout<<res<<'\n';
}


int main()
{
    ios::sync_with_stdio(false);    cin.tie(nullptr);   cout.tie(nullptr);
    int tc = 1;
    cin>>tc;    
    while(tc--)
        solve();
}
```



## [D - Chat Program](https://codeforces.com/gym/104128/problem/D)

二分答案，二分过程中对加上数列会大于二分值的数第一个位置和最后一个位置处理。



```cpp
//  AC one more times

#include <bits/stdc++.h>

using namespace std;

typedef long long ll;

const int mod = 1e9 + 7;
const int N = 2e5 + 10;

ll n, k, m, c, d;
ll a[N];

int event[N];
bool check(ll x)
{
    // cout<<"X: "<<x<<"  ";
    for(int i = 0; i <= n; i++)
        event[i] = 0;
    int sum = 0;
    for(ll i = 1; i <= n; i++)
    {
        if(a[i] >= x)
            sum++;
        else
        {
            ll t = a[i] + c + min(i - 1, m - 1) * d;
            if(t < x)   continue;
            event[max(1ll, i - m + 1)]++;
            // 第一次进入数列 
            t = a[i] + c;
            if(t >= x)
                event[i + 1]--; // 只用1个数字
            else
            {
                t = t - x;
                t = abs(t);
                t = t / d + (t % d != 0) + 1;
                if(i - t + 2 >= 1)  
                    event[i - t + 2]--;
                // cout<<i<<" "<<a[i]<<" "<< i - t + 2<<'\n';
            }
        }
    }
    for(int i = 1; i <= n - m + 1; i++)
    {
        sum += event[i];
        if(sum >= k)
            return true;
    }
    return false;
}
void solve()
{       
    cin>>n>>k>>m>>c>>d;
    for(int i = 1; i <= n; i++)
        cin>>a[i];
    ll l = 0, r = 1e15;
    while(l < r)
    {
        ll mid = (l + r + 1) >> 1;
        if(check(mid))  l = mid;
        else r = mid - 1;
    }
    cout<<l<<'\n';

    return;
}
  
int main()
{
    // std::ios::sync_with_stdio(false);   cin.tie(nullptr), cout.tie(nullptr);
    
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



## [B - Ropeway](https://codeforces.com/gym/104128/problem/B)

补题本来是写线段树的，发现TLE4，然后悟出了单调队列优化dp，第一次写单调队列优化dp



```cpp
//  AC one more times

#include <bits/stdc++.h>

using namespace std;

typedef long long ll;

const int mod = 1e9 + 7;
const int N = 5e5 + 10;


ll n, k, q, w[N], z[N], a[N], f[N], g[N], h[N], r[N], sum, tmp[N];
string s;
 

void calc1()
{
    deque<pair<ll, ll>> q;
    ll l = 2, r = n + 2;
    q.push_back({1, 0});
    f[1] = 0;
    for(int i = l; i <= r; i++)
    {
        while(!q.empty() && q.front().first + k < i)    q.pop_front();
        f[i] = q.front().second + w[i];
        if(s[i] == '1') q.clear();
        while(!q.empty() && f[i] <= q.back().second)    q.pop_back();
        q.push_back({i, f[i]});
    }   
}
void calc2()
{
    deque<pair<ll, ll>> q;
    ll l = 1, r = n + 1;
    q.push_back({n + 2, 0});
    g[n + 2] = 0;
    for(int i = r; i >= l; i--)
    {
        while(!q.empty() && q.front().first > i + k)    q.pop_front();
        g[i] = q.front().second + w[i];
        if(s[i] == '1') q.clear();
        while(!q.empty() && g[i] <= q.back().second)    q.pop_back();
        q.push_back({i, g[i]});
    }  
}
ll calc(ll p, ll v)
{
    deque<pair<ll, ll>> q;
    w[p] = v;
    ll res = 1e18;
    int l = max(1ll, p - k), r = p - 1;
    for(int i = l; i <= r; i++)
    {
        if(s[i] == '1') q.clear();
        while(!q.empty() && q.front().first + k < i)    q.pop_front();
        h[i] = f[i];
        while(!q.empty() && h[i] <= q.back().second)    q.pop_back();
        q.push_back({i, h[i]});
    }
    l = p, r = min(p + k, n + 2);
    for(int i = l; i <= r; i++)
    {
        while(!q.empty() && q.front().first + k < i)    q.pop_front();
        h[i] = q.front().second + w[i];
        // cout<<i<<" "<<h[i]<<"  "<<h[i] + g[i] - z[i]<<'\n';
        res = min(h[i] + g[i] - z[i], res);
        if(s[i] == '1') q.clear();
        while(!q.empty() && h[i] <= q.back().second)    q.pop_back();
        q.push_back({i, h[i]});
    }
    w[p] = z[p];
    return res;
}
void solve()
{       
    cin>>n>>k;
    sum = w[1] = w[n + 2] = 0;
    for(int i = 2; i <= n + 1; i++)    cin>>w[i];

    cin>>s;
    s = "01" + s + "1";
    // reverse(w + 1, w + 1 + n + 2);
    // reverse(s.begin(), s.end());
    for(int i = 1; i <= n + 2; i++)
        z[i] = w[i], tmp[i] = w[i];
    calc1();
    calc2();
    // for(int i = 1; i <= n + 2; i++)
    //     h[i] = f[i];

    cin>>q;
    for(int i = 1; i <= q; i++)
    {
        ll p, v;    cin>>p>>v;
        p++;
        cout<<calc(p, v)<<'\n';
    }
    return;
}

int main()
{
    std::ios::sync_with_stdio(false);   cin.tie(nullptr), cout.tie(nullptr);
    
    int TC = 1;
    
    cin >> TC;    
    for(int tc = 1; tc <= TC; tc++)
    {
        // cout << "Case #" << tc << ": ";         
        solve();
    }


    return 0;
}
```
{% endraw %}
