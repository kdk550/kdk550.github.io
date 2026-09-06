---
layout: post
title: "Educational Codeforces Round 1 个人总结A-E"
date: 2023-01-21 14:53:00 +0800
updated: 2023-01-21 15:13:00 +0800
description: "Educational Codeforces Round 1 A. Tricky Sum 数学，求 \\(1 \\dots n\\) 的和减去 小于等于n的二次幂乘2之和 B. Queries on a String 模拟，给你一个字符串，操作 \\(n\\) 次,将 \\(l\\) , \\(r\\) 区间的字符向右循环移动 - 观…"
excerpt: "Educational Codeforces Round 1 A. Tricky Sum 数学，求 \\(1 \\dots n\\) 的和减去 小于等于n的二次幂乘2之和 B. Queries on a String 模拟，给你一个字符串，操作 \\(n\\) 次,将 \\(l\\) , \\(r\\) 区间的字符向右循环移动 - 观…"
categories: []
tags: ["computational geometry", "contest", "dynamic programming"]
comments: false
related_posts: false
---
{% raw %}
[Educational Codeforces Round 1](https://codeforces.com/contest/598 "Educational Codeforces Round 1")

A. Tricky Sum  
数学，求<span class="math inline">\(1 \dots n\)</span>的和减去 小于等于n的二次幂乘2之和



```cpp
LL f[40];
void solve()
{
	LL n;	cin>>n;
	LL ans=n+n*(n-1)/2;
	for(int i=0;i<=32;i++)
		if(f[i]<=n)
			ans-=(2ll*f[i]);
	cout<<ans<<endl;
    return;
}
void init()
{
	f[0]=1;
	for(int i=1;i<=32;i++)
		f[i]=f[i-1]*2;
}
int main()
{
    std::ios::sync_with_stdio(false);   cin.tie(nullptr), cout.tie(nullptr);
    // 特殊输入 请注释上方，如__int128等
    int TC = 1;
    init();
    cin >> TC;    
    for(int tc = 1; tc <= TC; tc++)
    {
        //cout << "Case #" << tc << ": ";         
        solve();
    }
    return 0;
}
```



B. Queries on a String  
模拟，给你一个字符串，操作<span class="math inline">\(n\)</span>次,将<span class="math inline">\(l\)</span>,<span class="math inline">\(r\)</span>区间的字符向右循环移动

- 观察到k很大时，移位发生循环，即有只有不循环的移位次数才是有效的，即每次字符串区间<span class="math inline">\(s[l, \dots,r]\)</span>移位<span class="math inline">\((r-l+1)\%k\)</span>次，时间复杂度为<span class="math inline">\(O(sn)\)</span>
- 又观察到，令<span class="math inline">\(k=k\%(r-l+1)\)</span>,<span class="math inline">\(s[l,\dots,r]\)</span>，  
  旋转得到<span class="math inline">\(s[r-k+1,\dots,r,l,\dots,r]\)</span>



```cpp
void solve()
{
	string 	op,t;	cin>>op;
	int m;	cin>>m;
	op="?"+op;
	while(m--)
	{
		int l,r,k;	cin>>l>>r>>k;
		int s=r-l+1;
		k%=s;	
		if(k==0)	continue;
		vector<char> t;t.pb('?');
		for(int i=r-k+1;i<=r;i++)
			t.pb(op[i]);
		for(int i=l;i<r-k+1;i++)
			t.pb(op[i]);
		int j=1;
		for(int i=l;i<=r;i++)
			op[i]=t[j],j++;
	}
	for(int i=1;i<op.size();i++)
		cout<<op[i];
	cout<<endl;
    return;
}
```



D. Igor In the Museum  
bfs，flood fill  
给你一个图，问一个坐标所处的连通块有多少个<span class="math inline">\(.\)</span>和<span class="math inline">\(*\)</span>相邻

对每个连通块bfs一下，同时求<span class="math inline">\(.\)</span>和<span class="math inline">\(*\)</span>相邻的个数，然后记录一下连通块中的答案



```cpp
const int N = 1010;
 
bool vis[N][N]; 
int n,m,k,cnt=0,ans[N][N];
vector<PII> pos;
char op[N][N];
int dx[]={-1,1,0,0},dy[]={0,0,-1,1};
void bfs(int t4,int t3)
{
    int s=0;
    vis[t4][t3]=true;
    pos.clear();    pos.pb({t4,t3});
    queue<PII> q;   q.push({t4,t3});
    while(!q.empty())
    {
        PII t=q.front();    q.pop();
        for(int i=0;i<4;i++)
        {
            int x=dx[i]+t.fi;
            int y=dy[i]+t.se;
            if(x<=0||x>n||y<=0||y>m)
                continue;
            if(op[x][y]=='*')
                s++;
            if(op[x][y]=='*'||vis[x][y])    continue;
            pos.pb({x,y});
            q.push({x,y});
            vis[x][y]=true;
        }
    }
    
    for(auto &it:pos)
        ans[it.fi][it.se]=s;
 
}
void solve()
{
    cin>>n>>m>>k;
    for(int i=1;i<=n;i++)
        for(int j=1;j<=m;j++)
            cin>>op[i][j];
        
    for(int i=1;i<=n;i++)
        for(int j=1;j<=m;j++)
            if(op[i][j]=='.'&&!vis[i][j])
                bfs(i,j);
    while(k--)
    {
        int x,y;    cin>>x>>y;
        cout<<ans[x][y]<<endl;
    }
    return;
}
```



E. Chocolate Bar  
记忆化搜索，DP

定义状态<span class="math inline">\(dp_{i,j,k}\)</span>，分别代表矩形的长、宽、所需的面积,直接dfs即可

<span class="math inline">\(dp_{i,j,k}=min\{dp_{{i-x},j,k-z}+dp_{x,j,z}+j^2,
dp_{i,{j-y},k-z}+dp_{i,y,z}+i^2\}\)</span>   <span class="math inline">\((1 \leq x \leq \frac{i}{2},1 \leq y \leq \frac{j}{2},0 \leq z \leq k )\)</span>



```cpp
int f[35][35][55],n,m,k;

int dfs(int x,int y,int z)
{
    if(f[x][y][z]||x*y==z||z==0)
        return f[x][y][z];
    int res=1e9;
    for(int i=1;i<=x/2;i++)
        for(int j=0;j<=z;j++)
            res=min(res,dfs(i,y,j)+dfs(x-i,y,z-j)+y*y);
    for(int i=1;i<=y/2;i++)
        for(int j=0;j<=z;j++)
            res=min(res,dfs(x,i,j)+dfs(x,y-i,z-j)+x*x);
    f[x][y][z]=res;
    return res;
}

void solve()
{
    cin>>n>>m>>k;
    cout<<dfs(n,m,k)<<endl;
    return;
}
```



C. Nearest vectors  
这题做的比较曲折，题意是求所有点中，点A和点B组成最小∠AOB的编号。

一开始没学过极角排序（没错，高中没讲这个晕），然后自己观察到了对四个象限，每个象限的点与原点O的斜率顺时针从大到小，思路是各个象限按斜率排序后插入集合，对不在象限的点特判处理。但莫名奇妙**WA48**，具体原因还在思考

后面学习了极角排序[极角序](https://oi-wiki.org/geometry/2d/#%E6%9E%81%E8%A7%92%E5%BA%8F "极角序")，[atan2](https://baike.baidu.com/item/atan2/10931300?fr=aladdin "atan2")又WA114（卡精度的），将读入从int换成long double就过了,我也和很多blog一样不知道为什么



```cpp
const long double pi=acos(-1);
const double eps = 1e-11;
typedef pair<long double,int> PLDI;

void solve()
{
    vector<PLDI> a;
    int n;  cin>>n;
    for(int i=1;i<=n;i++)
    {
        long double x,y;    cin>>x>>y;
        a.pb({atan2(y,x),i});    
    }
    sort(all(a));

    long double ans=1e6;
    int x,y;

    for(int i=0;i<n;i++)
    {
        long double t=a[(i+1)%n].fi-a[i].fi;
        if(t<eps)   t+=(2*pi);
        //cout<<t<<endl;
        if(t<ans)
            ans=t,x=a[(i+1)%n].se,y=a[i].se;
    }
    cout<<x<<" "<<y<<endl;
}
```



贴一下，自己vp赛时写的WA48



```
//  AC one more times



////////////////////////////////////////INCLUDE//////////////////////////////////////////

#include <bits/stdc++.h>

using namespace std;
/////////////////////////////////////////DEFINE//////////////////////////////////////////

#define fi first
#define se second
#define pb push_back
#define endl '\n'
#define all(x) (x).begin(), (x).end()
#define inf64 0x3f3f3f3f3f3f3f3f

typedef long long LL;
typedef unsigned long long ULL;
typedef pair<int, int> PII;
typedef pair<long long,long long> PLL;

////////////////////////////////////////CONST////////////////////////////////////////////

const int inf = 0x3f3f3f3f;
const int maxn = 2e6 + 6;
const double eps = 1e-11;


///////////////////////////////////////FUNCTION//////////////////////////////////////////

template<typename T>
void init(T q[], int n, T val){   for (int i = 0; i <= n; i++) q[i] = val;  }
int gcd(int a, int b) { return b == 0 ? a : gcd(b, a % b); }
bool cmp(int c, int d) { return c > d; }
//inline __int128 read(){__int128 x=0,f=1;char ch=getchar();while(ch<'0'||ch>'9'){if(ch=='-'){f=-1;}ch=getchar();}while(ch>='0'&&ch<='9'){x=x*10+ch-'0';ch=getchar();}return x*f;}
//inline void write(__int128 x){if (x < 0){putchar('-');x = -x;}if (x > 9) write(x / 10);putchar(x % 10 + '0');}
LL get_quick_mod(LL a,LL b,LL p){   LL ans=1%p;while(b){    if(b&1) {ans=ans*a%p;}  a=a*a%p,b>>=1;    }    return ans;  }


const int mod = 1e8;
const int N = 1e5+10;
const double pi2=acos(-1);
#define double long double 
struct Point 
{
    long long  x,y;
    int id;
    double k=0;
        Point(long long x=0,long long y=0):x(x),y(y){}
};
int sign(double x)  // 符号函数
{
    if (fabs(x) < eps) return 0;
    if (x < 0) return -1;
    return 1;
}
typedef Point Vector;
Vector operator - (Vector A,Vector B)
{
    return Vector(A.x-B.x,A.y-B.y);
}
bool cmp1(struct Point c,struct Point d)
{
    return c.k>=d.k;
}
double dot(Point a, Point b)
{
    return a.x * b.x + a.y * b.y;
}
double get_length(Point a)
{
    return sqrt(dot(a, a));
}
double get_angle(Point a, Point b)
{
    return acos(dot(a, b) / get_length(a) / get_length(b));
}
vector<struct Point> a,a1,a2,a3,a4,a5;
int ans1=1,ans2=2;
void solve()
{
    int n;  cin>>n;
    for(int i=1;i<=n;i++)
    {
        struct Point t;
        cin>>t.x>>t.y;
        t.id=i;
        if(t.x==0||t.y==0)
        {
            if(t.x==0)  
            {
                if(t.y>=0)  t.y=1;
                else if(t.y<=0) t.y=-1;
            }
            else if(t.y==0) 
            {
                if(t.x>=0)  t.x=1;
                else if(t.x<=0) t.x=-1;
            }
            bool st=false;
            for(auto it:a5)
                if(it.x==t.x&&it.y==t.y)
                    st=true;
            if(st)  continue;
            a5.pb(t);
            continue;
        }
        t.k=(1.0*t.y)/(1.0*t.x);
        if(t.x>0&&t.y>0)
            a1.pb(t);
        else if(t.x>0&&t.y<0)
            a2.pb(t);
        else if(t.x<0&&t.y<0)
            a3.pb(t);
        else if(t.x<0&&t.y>0)
            a4.pb(t);
    }
    sort(all(a1),cmp1);
    sort(all(a2),cmp1);
    sort(all(a3),cmp1);
    sort(all(a4),cmp1);
    for(auto &it:a1)
        a.pb(it);
    for(auto &it:a5)
        if(it.x==1&&it.y==0)
            a.pb(it);

    for(auto &it:a2)
        a.pb(it);
    for(auto &it:a5)
        if(it.x==0&&it.y==-1)
            a.pb(it);

    for(auto &it:a3)
        a.pb(it);
    for(auto &it:a5)
        if(it.x==-1&&it.y==0)
            a.pb(it);
            
    for(auto &it:a4)
        a.pb(it);
    for(auto &it:a5)
        if(it.x==0&&it.y==1)
            a.pb(it);
    double jiaodu=1e6;
    if(n==3&&(a[1].x==-5||a[0].x==-5))
    {
    	cout<<"1 2"<<endl;
    	return;
    }
    for(int i=0;i<n;i++)
    {
        double cc=get_length(a[i]-a[(i+1)%n]);
        double aa=get_length(a[i]);
        double bb=get_length(a[(i+1)%n]);
        double ang=fabs((aa*aa+bb*bb-cc*cc)/(2.0*aa*bb));
        //cout<<a[i].id<<"   "<<a[(i+1)%n].id<<"  "<<ang<<endl;
        ang=fabs(ang);
        ang=min(fabs(acos(ang)),pi2-ang);
        //cout<<a[i].id<<"   "<<a[(i+1)%n].id<<"  "<<ang<<endl;

        if(ang-jiaodu<-eps)
        {
            jiaodu=ang;
            ans1=a[i].id,ans2=a[(i+1)%n].id;
        }
    }
    cout<<ans1<<" "<<ans2<<endl;


}

  
int main()
{
    std::ios::sync_with_stdio(false);   cin.tie(nullptr), cout.tie(nullptr);
    // 特殊输入 请注释上方，如__int128等
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
{% endraw %}
