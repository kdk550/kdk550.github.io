---
layout: post
title: "2020-2021 ACM-ICPC, Asia Nanjing Regional Contest KLMEFAH"
date: 2023-08-25 03:07:00 +0800
updated: 2023-08-25 19:39:00 +0800
description: "2020-2021 ACM-ICPC, Asia Nanjing Regional Contest (XXI Open Cup, Grand Prix of Nanjing) 目录 - 2020-2021 ACM-ICPC, Asia Nanjing Regional Contest (XXI Open Cup, G…"
excerpt: "2020-2021 ACM-ICPC, Asia Nanjing Regional Contest (XXI Open Cup, Grand Prix of Nanjing) 目录 - 2020-2021 ACM-ICPC, Asia Nanjing Regional Contest (XXI Open Cup, G…"
categories: []
tags: ["contest"]
comments: false
related_posts: false
---
{% raw %}
# [2020-2021 ACM-ICPC, Asia Nanjing Regional Contest (XXI Open Cup, Grand Prix of Nanjing)](https://codeforces.com/gym/102992)

目录

- [2020-2021 ACM-ICPC, Asia Nanjing Regional Contest (XXI Open Cup, Grand Prix of Nanjing)](/blog/2023/2020-2021-acm-icpc-asia-nanjing-regional-contest/#2020-2021-acm-icpc-asia-nanjing-regional-contest-xxi-open-cup-grand-prix-of-nanjing)
  - [K - K Co-prime Permutation](/blog/2023/2020-2021-acm-icpc-asia-nanjing-regional-contest/#k---k-co-prime-permutation)
  - [L - Let's Play Curling](/blog/2023/2020-2021-acm-icpc-asia-nanjing-regional-contest/#l---lets-play-curling)
  - [M - Monster Hunter](/blog/2023/2020-2021-acm-icpc-asia-nanjing-regional-contest/#m---monster-hunter)
  - [E - Evil Coordinate](/blog/2023/2020-2021-acm-icpc-asia-nanjing-regional-contest/#e---evil-coordinate)
  - [F - Fireworks](/blog/2023/2020-2021-acm-icpc-asia-nanjing-regional-contest/#f---fireworks)
  - [A - Ah, It's Yesterday Once More](/blog/2023/2020-2021-acm-icpc-asia-nanjing-regional-contest/#a---ah-its-yesterday-once-more)
  - [Harmonious Rectangle](/blog/2023/2020-2021-acm-icpc-asia-nanjing-regional-contest/#harmonious-rectangle)

## [K - K Co-prime Permutation](https://codeforces.com/gym/102992/problem/K)

将数字shift k 个即可，注意特判



```cpp
#include<bits/stdc++.h>

using namespace std;


int n, k;
int res[1000010];
void solve()
{
	cin>>n>>k;
	if(k == 0)
	{
		cout<<-1;
		return;
	}
	res[1] = k;
	for(int i = 2; i <= k; i++)
		res[i] = i - 1;
	for(int i = k + 1; i <= n; i++)
		res[i] = i;
	for(int i = 1; i <= n; i++)
	{
		cout<<res[i];
		if(i != n)
			cout<<" ";
	}
}

int main()
{
	ios::sync_with_stdio(false);cin.tie(nullptr);cout.tie(nullptr);

	solve();

}
```



## [L - Let's Play Curling](https://codeforces.com/gym/102992/problem/L)

问蓝球中间的红球最多能有多少个

双指针弄一下

演了队友3发罚时，晕



```cpp
#include<bits/stdc++.h>

using namespace std;
typedef long long ll;
const int N = 2e5 + 10;

int n, m;
int a[N], b[N], d[N];
bool vis[N];
vector<int> vx;
void solve()
{
	cin>>n>>m;
	
	vx.clear();
	for(int i = 0; i <= n + m; i++)
		a[i] = b[i] = d[i] = 0, vis[i] = false;

	for(int i = 1; i <= n; i++)
	{
		cin>>a[i];
		vx.push_back(a[i]);
	}
	for(int i = 1; i <= m; i++)
	{
		cin>>b[i];
		vx.push_back(b[i]);
	}
	// sort(a + 1, a + 1 + n);
	sort(vx.begin(), vx.end());
	vx.erase(unique(vx.begin(), vx.end()), vx.end());
	for(int i = 1; i <= n; i++)
	{
		int p = lower_bound(vx.begin(), vx.end(), a[i]) 
		- vx.begin();
		d[p]++;
	}
	for(int i = 1; i <= m; i++)
	{
		int p = lower_bound(vx.begin(), vx.end(), b[i]) 
		- vx.begin();
		vis[p] = true;
	}	
	int k = vx.size();
	int res = 0;
	for(int i = 0; i < k; i++)
	{
		int ans = 0;
		if(vis[i] == false && d[i] >= 1)
		{
			int j = i;
			ans = d[j];
			while(j + 1 < k && vis[j + 1] == false && d[j + 1] >= 1)
			{
				j++;
				ans = ans + d[j];
			}
			res = max(ans, res);
			i = j;
		}
	}
	if(res != 0)
	{
		cout<<res<<'\n';
	}
	else
		cout<<"Impossible\n";
}

int main()
{
	ios::sync_with_stdio(false);cin.tie(nullptr);cout.tie(nullptr);
	int tc;	cin>>tc;
	for(int i = 1; i <= tc; i++)
		solve();

}
```



## [M - Monster Hunter](https://codeforces.com/gym/102992/problem/M)

树上背包典题

定义状态<span class="math inline">\(f_{u,i,0/1}\)</span> 定义状态为以 <span class="math inline">\(u\)</span> 为根的子树，已经删掉了 <span class="math inline">\(i\)</span> 个结点,<span class="math inline">\(0/1\)</span> 分别代表没删自己和删了自己

因为可以子节点也可以被删掉，转移的时候要减去子节点的权值，具体看代码吧



```cpp
#include<bits/stdc++.h>

using namespace std;
typedef long long ll;
const int N = 2e3 + 10;
const ll inf = 1ll << 60;
int n;
ll f[N][N][2], sz[N], w[N], h[N], tmp[N][2];
vector<int> e[N];

void dfs(int u)
{
	h[u] = w[u];
	sz[u] = 0;
	for(auto v : e[u])
	{
		dfs(v);
		h[u] += w[v];
	}


	for(int i = 0; i <= N - 10; i++)
		f[u][i][0] = f[u][i][1] = inf;
	f[u][1][0] = h[u];
	f[u][0][1] = 0;
	sz[u] = 1;
	for(auto v : e[u])
	{
		for(int i = 0; i <= sz[u] + sz[v]; i++)
			tmp[i][0] = inf, tmp[i][1] = inf;
		for(int i = 0; i <= sz[u]; i++)
			for(int j = 0; j <= sz[v]; j++)
			{
				tmp[i + j][0] = min(tmp[i + j][0], f[u][i][0] + f[v][j][1] - w[v]);
				tmp[i + j][0] = min(tmp[i + j][0], f[u][i][0] + f[v][j][0]);

				tmp[i + j][1] = min(tmp[i + j][1], f[u][i][1] + f[v][j][1]);
				tmp[i + j][1] = min(tmp[i + j][1], f[u][i][1] + f[v][j][0]);

			}
		sz[u] += sz[v];
		for(int i = sz[u]; i >= 0; i--)
			f[u][i][0] = tmp[i][0], f[u][i][1] = tmp[i][1];
	}
}

void solve()
{
	cin>>n;
	for(int i = 1; i <= n; i++)
	{
		e[i].clear();
		w[i] = h[i] = 0;
	}

	for(int i = 2; i <= n; i++)
	{
		int p;	cin>>p;
		e[p].push_back(i); 
	}
	for(int i = 1; i <= n; i++)
		cin>>w[i];
	dfs(1);
	// for(int i = 1; i <= n; i++)
	// {
	// 	cout<<"i: "<<i<<"   " ;
	// 	for(int j = 0; j <= n; j++)
	// 	{
	// 		cout<<f[i][j]<<" ";
	// 	}
	// 	cout<<'\n';
	// }
	for(int i = n; i >= 0; i--)
	{
		cout<<min(f[1][i][0], f[1][i][1]);
		if(i != 0)
			cout<<" ";
	}
	cout<<'\n';

}

int main()
{
	ios::sync_with_stdio(false);cin.tie(nullptr);cout.tie(nullptr);
	ios::sync_with_stdio(false);cin.tie(nullptr);cout.tie(nullptr);
	int tc;	cin>>tc;
	for(int i = 1; i <= tc; i++)
		solve();
}
```



## [E - Evil Coordinate](https://codeforces.com/gym/102992/problem/E)

check 一下16种RLUD的排列是否有一种符合即可

我懒得预处理出全排列，写了一个更暴力求排列的了



```cpp
#include<bits/stdc++.h>

using namespace std;
typedef long long ll;
const int N = 2e5 + 10;

ll mx,my;
string s;
void solve()
{

	cin>>mx>>my;
	cin>>s;
	
	int cnt[5];	memset(cnt, 0, sizeof cnt);
	for(auto it : s)
	{
		if(it=='R')		cnt[1]++;
		if(it=='L')		cnt[2]--;
		if(it=='U')		cnt[3]++;
		if(it=='D')		cnt[4]--;
	}
	// for(int i = 1; i <= 4; i++)
	// 	cout<<cnt[i]<<"  ";
	// cout<<'\n';
	for(int i = 1; i <= 4; i++)
	{
		for(int j = 1; j <= 4; j++)
		{
			for(int k = 1; k <= 4; k++)
			{
				for(int l = 1; l <= 4; l++)
				{
					if(i != j && i != k && i != l
						&& j != k && j != l
						&& k != l)
					{
						int x = 0, y = 0;
						int tx = 0, ty = 0;

						bool ok = true;

						if(i == 1 || i == 2)
						{
							x = x + cnt[i];
							if(y == my && ((tx <= mx && mx <= x) || (tx >= mx && mx >= x)))
								ok = false;
							tx = x;
						}
						else 
						{
							y = y + cnt[i];
							if(x == mx && ((ty <= my && my <= y) || (ty >= my && my >= y)))
								ok = false;
							ty = y;
						}

						if(j == 1 || j == 2)
						{
							x = x + cnt[j];
							if(y == my && ((tx <= mx && mx <= x) || (tx >= mx && mx >= x)))
								ok = false;
							tx = x;
						}
						else
						{
							y = y + cnt[j];
							if(x == mx && ((ty <= my && my <= y) || (ty >= my && my >= y)))
								ok = false;
							ty = y;							
						}
						
						if(k == 1 || k == 2)
						{
							x = x + cnt[k];
							if(y == my && ((tx <= mx && mx <= x) || (tx >= mx && mx >= x)))
								ok = false;
							tx = x;
						}
						else
						{
							y = y + cnt[k];
							if(x == mx && ((ty <= my && my <= y) || (ty >= my && my >= y)))
								ok = false;
							ty = y;							
						}

						if(l == 1 || l == 2)
						{
							x = x + cnt[l];
							if(y == my && ((tx <= mx && mx <= x) || (tx >= mx && mx >= x)))
								ok = false;
							tx = x;
						}
						else
						{
							y = y + cnt[l];
							if(x == mx && ((ty <= my && my <= y) || (ty >= my && my >= y)))
								ok = false;
							ty = y;							
						}

						if(ok)
						{
							// cout<<i<<"  "<<j<<"  "<<k<<"  "<<l<<'\n';
							// cout<<cnt[i]<<"  "<<cnt[j]<<"  "<<cnt[k]<<"  "<<cnt[l]<<'\n';
							cnt[2] = abs(cnt[2]);
							cnt[4] = abs(cnt[4]);
							while(cnt[i] >= 1)
							{
								cnt[i]--;
								if(i == 1)	cout<<'R';
								else if(i == 2) cout<<'L';
								else if(i == 3)	cout<<"U";
								else if(i == 4)	cout<<"D";
							}
							while(cnt[j] >= 1)
							{
								cnt[j]--;
								if(j == 1)	cout<<'R';
								else if(j == 2) cout<<'L';
								else if(j == 3)	cout<<"U";
								else if(j == 4)	cout<<"D";
							}
							while(cnt[k] >= 1)
							{
								cnt[k]--;
								if(k == 1)	cout<<'R';
								else if(k == 2) cout<<'L';
								else if(k == 3)	cout<<"U";
								else if(k == 4)	cout<<"D";
							}							
							while(cnt[l] >= 1)
							{
								cnt[l]--;
								if(l == 1)	cout<<'R';
								else if(l == 2) cout<<'L';
								else if(l == 3)	cout<<"U";
								else if(l == 4)	cout<<"D";
							}
							cout<<'\n';
							return;
						}

					}
				}
			}
		}
	}
	cout<<"Impossible\n";
	// if(my == 0 && (0 <= mx && mx <= x) || )

}

int main()
{
	ios::sync_with_stdio(false);cin.tie(nullptr);cout.tie(nullptr);
	int tc;	cin>>tc;
	for(int i = 1; i <= tc; i++)
		solve();
}
```



## [F - Fireworks](https://codeforces.com/gym/102992/problem/F)

发现是一个可以三分函数



```cpp
#include<bits/stdc++.h>

using namespace std;
typedef long long ll;
const int N = 2e5 + 10;


int n, m, v;
double p, q;
double qmi(double a, int b)
{
	double res = 1.0;
	while(b)
	{
		if(b & 1)	res = res * a;
		a = a * a;
		b >>= 1;
	}
	return res;
}

double calc(int x)
{
	return (1.0 * n * x + m) / (1.0 - qmi(q, x)); 
}

void solve()
{
	cin>>n>>m>>v;
	p = 1.0 * v / 10000;
	q = 1.0 - p;
	int l = 1, r = 1e9;
	while(r - l > 2)
	{
		int lmid = l + (r - l) / 3;
		int rmid = r - (r - l) / 3;
		if(calc(lmid) <= calc(rmid))
			r = rmid;
		else l = lmid;
	} 
	double res = 1e18;
	for(int i = l; i <= r; i++)
		res = min(res, calc(i));
	//double res = min(calc(l), calc(r));
	printf("%.7lf\n", res);
}

int main()
{
	
	// ios::sync_with_stdio(false);cin.tie(nullptr);cout.tie(nullptr);
	
	int tc;	cin>>tc;
	for(int i = 1; i <= tc; i++)
		solve();
}
```



## [A - Ah, It's Yesterday Once More](https://codeforces.com/gym/102992/problem/A)

尽可能地构造出分叉可以多走的迷宫，使得指令无效，而不是构造步数尽可能多的



```cpp
//  AC one more times

#include <bits/stdc++.h>

using namespace std;

typedef long long ll;

//const int mod = 1e9 + 7;
const int N = 2e5 + 10;


//  AC one more times

#include <bits/stdc++.h>

using namespace std;

typedef long long ll;
int a[30][30] = {{0 ,1  ,2, 3,  4,  5,  6,  7,  8,  9,  10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20},
    {1, 0,  1,  1,  1,  0,  0,  0,  1,  1,  1,  0,  0,  0,  1,  1,  1,  0,  1,  1,  1},
    {2, 0,  1,  0,  1,  1,  0,  0,  1,  0,  1,  1,  0,  0,  1,  0,  1,  1,  0,  0,  1},
    {3, 0,  1,  1,  0,  1,  1,  0,  1,  1,  0,  1,  1,  0,  1,  1,  0,  1,  1,  0,  1},
    {4, 0,  0,  1,  1,  0,  1,  1,  0,  1,  1,  0,  1,  1,  0,  1,  1,  0,  1,  1,  1},
    {5, 0,  0,  0,  1,  1,  0,  1,  1,  0,  1,  1,  0,  1,  1,  0,  1,  1,  0,  0,  0},
    {6, 1,  1,  1,  0,  1,  1,  0,  1,  1,  0,  1,  1,  0,  1,  1,  0,  1,  1,  0,  0},
    {7, 1,  0,  1,  1,  0,  1,  1,  0,  1,  1,  0,  1,  1,  0,  1,  1,  0,  1,  1,  0},
    {8, 1,  1,  0,  1,  1,  0,  1,  1,  0,  1,  1,  0,  1,  1,  0,  1,  1,  0,  1,  1},
    {9, 0,  1,  1,  0,  1,  1,  0,  1,  1,  0,  1,  1,  0,  1,  1,  0,  1,  1,  0,  1},
{10,    0,  0,  1,  1,  0,  1,  1,  0,  1,  1,  0,  1,  1,  0,  1,  1,  0,  1,  1,  1},
{11,    0,  0,  0,  1,  1,  0,  1,  1,  0,  1,  1,  0,  1,  1,  0,  1,  1,  0,  0,  0},
{12,    1,  1,  1,  0,  1,  1,  0,  1,  1,  0,  1,  1,  0,  1,  1,  0,  1,  1,  0,  0},
{13,    1,  0,  1,  1,  0,  1,  1,  0,  1,  1,  0,  1,  1,  0,  1,  1,  0,  1,  1,  0},
{14,    1,  1,  0,  1,  1,  0,  1,  1,  0,  1,  1,  0,  1,  1,  0,  1,  1,  0,  1,  1},
{15,    0,  1,  1,  0,  1,  1,  0,  1,  1,  0,  1,  1,  0,  1,  1,  0,  1,  1,  0,  1},
{16,    0,  0,  1,  1,  0,  1,  1,  0,  1,  1,  0,  1,  1,  0,  1,  1,  0,  1,  1,  1},
{17,    0,  0,  0,  1,  1,  0,  1,  1,  0,  1,  1,  0,  1,  1,  0,  1,  1,  0,  0,  0},
{18,    1,  1,  1,  0,  1,  1,  0,  1,  1,  0,  1,  1,  0,  1,  1,  0,  1,  1,  0,  0},
{19,    1,  0,  1,  1,  0,  1,  0,  0,  1,  1,  0,  1,  0,  0,  1,  1,  0,  1,  0,  0},
{20,    1,  1,  0,  1,  1,  1,  0,  0,  0,  1,  1,  1,  0,  0,  0,  1,  1,  1,  0,  0}};



void solve()
{       
    cout<<"20 20\n";
    for(int i = 1; i <= 20; i++)
    {
        for(int j = 1; j <=20; j++)
            cout<<a[i][j];
        cout<<'\n';
    }

    return;
}


  
int main()
{
    std::ios::sync_with_stdio(false);   cin.tie(nullptr), cout.tie(nullptr);
    
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



## [Harmonious Rectangle](https://codeforces.com/gym/102992/problem/H)

可以看出列数 > 9 就必定有 <span class="math inline">\(3 ^ {n \times m}\)</span> 个解，通过抽屉原理，我们只要预处理出 <span class="math inline">\(9 \leq \max(n, m)\)</span> 的解即可，注意 <span class="math inline">\(\min(n, m) = 0\)</span> 的特判



<table>
<thead>
<tr>
<th>1</th>
<th>2</th>
<th>3</th>
<th>1</th>
<th>2</th>
<th>3</th>
<th>1</th>
<th>2</th>
<th>3</th>
<th>1</th>
</tr>
</thead>
<tbody>
<tr>
<td>2</td>
<td>3</td>
<td>1</td>
<td>2</td>
<td>3</td>
<td>1</td>
<td>2</td>
<td>3</td>
<td>1</td>
<td>2</td>
</tr>
<tr>
<td>3</td>
<td>1</td>
<td>2</td>
<td>3</td>
<td>1</td>
<td>2</td>
<td>3</td>
<td>1</td>
<td>2</td>
<td>3</td>
</tr>
<tr>
<td>1</td>
<td>2</td>
<td>3</td>
<td>1</td>
<td>2</td>
<td>3</td>
<td>1</td>
<td>2</td>
<td>3</td>
<td>1</td>
</tr>
<tr>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
</tbody>
</table>




```cpp
//  AC one more times

#include <bits/stdc++.h>

using namespace std;

typedef long long ll;

const int mod = 1e9 + 7;
const int N = 2e5 + 10;

ll n, m, g[15][15], res = 0;
// int r[20][20];
// int dx[] = {0, 1, 1, 1, 2, 2, 2, 3, 3, 3};
// int dy[] = {0, 1, 2, 3, 1, 2, 3, 1, 2, 3};
ll qmi(ll a, ll b, ll mod)
{
    ll ans = 1 % mod;
    while(b)
    {
        if(b & 1) ans = ans * a % mod;
        a = a * a % mod;
        b >>= 1;
    }
    return ans;
}
bool check(int n, int m)
{
	for(int i = 1; i < n; i++)
		for(int j = 1; j < m; j++)
			if((g[i][j] == g[n][j] && g[i][m] == g[n][m]) || 
				(g[i][j] == g[i][m] && g[n][j] == g[n][m]))
			{
			// cout<<"!!\n";	
				return true;
			}
	return false;
}
void dfs(int x, int y)
{
	// cout<<x<<" "<<y<<'\n';
	for(int c = 1; c <= 3; c++)
	{
		g[x][y] = c;
		bool ok = false;
		if(check(x, y))
			ok = true;
		if(ok)
		{
			res = res + qmi(3, (m * (n - x) + m - y), mod);
			res %= mod;
			// cout<<res<<'\n';
		}
		if(!ok)
		{
			int tx = x, ty = y;
			ty++;	if(ty == m + 1)	tx++, ty = 1;
			if(tx <= n)
				dfs(tx, ty);
		}
		// g[x][y] = 0;

    }

}

ll a[20][20] = {{0},
{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
{0, 0, 15, 339, 4761, 52929, 517761, 4767849, 43046721, 387420489, 486784380},
{0, 0, 339, 16485, 518265, 14321907, 387406809, 460338013, 429534507, 597431612, 130653412},
{0, 0, 4761, 518265, 43022385, 486780060, 429534507, 792294829, 175880701, 246336683, 953271190},
{0, 0, 52929, 14321907, 486780060, 288599194, 130653412, 748778899, 953271190, 644897553, 710104287},
{0, 0, 517761, 387406809, 429534507, 130653412, 246336683, 579440654, 412233812, 518446848, 947749553},
{0, 0, 4767849, 460338013, 792294829, 748778899, 579440654, 236701429, 666021604, 589237756, 662963356},
{0, 0, 43046721, 429534507, 175880701, 953271190, 412233812, 666021604, 767713261, 966670169, 322934415},
{0, 0, 387420489, 597431612, 246336683, 644897553, 518446848, 589237756, 966670169, 968803245, 954137859},
{0, 0, 486784380, 130653412, 953271190, 710104287, 947749553, 662963356, 322934415, 954137859, 886041711}};
void solve()
{       
	// for(int i = 1; i <= 10; i++)
	// {
	// 	cout<<"{0, ";
	// 	for(int j = 1; j <= 10; j++)
	// 	{
	// 		res = 0;
	// 		// memset(g, 0, sizeof g);
	// 		n = i, m = j;
	// 		dfs(1, 1);
	// 		cout<<res<<", ";
	// 	}
	// 	cout<<"},\n";
	// }
	cin>>n>>m;
	if(min(n, m) == 1)
		cout<<"0\n";
	else if(max(n, m) < 9)
		cout<<a[n][m] % mod<<'\n';
	else
		cout<<qmi(3,1ll * n * m, mod)<<'\n';
    return;
}


  
int main()
{
    //std::ios::sync_with_stdio(false);   cin.tie(nullptr), cout.tie(nullptr);
    
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
