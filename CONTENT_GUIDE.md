# 博客维护教程

本文是这个 GitHub Pages 博客的日常维护手册。所有文章都使用同一套规则，不区分来源或迁移时间。

## 1. 仓库和目录

站点仓库位于：

```text
/home/magicat/workspace/00文档/blogs/kdk550.github.io
```

它是一个独立的 Git 仓库，远程地址是：

```text
git@github.com-kdk550:kdk550/kdk550.github.io.git
```

主要目录：

| 路径 | 用途 |
| --- | --- |
| `_posts/` | 已发布的博客文章 |
| `_drafts/` | 尚未发布的草稿 |
| `_pages/` | About、Blog、404 等固定页面 |
| `_news/` | News 页面中的公告 |
| `assets/img/blog/posts/` | 文章图片 |
| `scripts/verify_built_site.py` | 当前站点的构建验收工具 |
| `scripts/normalize_blog_posts.py` | 本次统一命名使用的一次性整理工具，不用于日常写作 |
| `scripts/migrate_cnblogs_to_al_folio.py` | 历史归档迁移脚本，禁止对当前站点重新运行 |
| `migration-report.json` | 历史迁移报告，不是当前文章的事实来源 |

博客园的完整原始归档位于：

```text
/home/magicat/workspace/00文档/blogs/20260711
```

除非要查历史资料，否则不要修改归档目录。

## 2. 文章文件名和 URL

文章放在 `_posts/`，文件名必须是：

```text
YYYY-MM-DD-english-semantic-slug.md
```

例如：

```text
_posts/2023-09-28-2022-china-collegiate-programming-contest-ccpc-mianyang-onsite-gchmad.md
```

文件名规则：

- 日期使用文章的发布日期。
- slug 使用英文语义名称，不使用拼音。
- 只使用小写英文字母、数字和短横线。
- 中文、空格、括号、斜杠、冒号等符号转换为短横线或删除。
- 文件名中不要写博客园文章 ID，也不要使用 `cnblogs-数字`。
- 如果两个标题相同，为 slug 添加能区分主题的英文词，例如 `...-segment-tree` 和 `...-dynamic-programming`。

Jekyll 根据文件名和 `_config.yml` 中的规则生成 URL：

```text
/blog/<年份>/<slug>/
```

不要在文章 front matter 中写 `slug:` 或 `permalink:`。修改文件名会改变公开 URL，因此改名后要搜索并同步站内链接。

## 3. 新增文章

进入仓库：

```bash
cd /home/magicat/workspace/00文档/blogs/kdk550.github.io
```

在 `_posts/` 创建文件，例如：

```text
_posts/2026-09-06-my-new-algorithm-note.md
```

推荐从下面的模板开始：

```markdown
---
layout: post
title: "文章标题"
date: 2026-09-06 20:00:00 +0800
updated: 2026-09-06 20:00:00 +0800
description: "一两句话概括文章内容。"
excerpt: "一两句话概括文章内容。"
categories: []
tags: ["algorithm basics"]
comments: false
related_posts: false
---

正文从这里开始。
```

`title` 可以是中文，也可以是英文；只有文件名和 URL 必须使用英文 slug。常用字段含义如下：

- `layout: post`：使用博客文章布局。
- `title`：页面标题。
- `date`：发布日期和时间，决定文章排序以及 URL 年份。
- `updated`：最后修改时间。
- `description`、`excerpt`：列表页、搜索和分享摘要。
- `categories`：当前站点统一留空，分类用标签代替。
- `tags`：文章标签，例如 `"dynamic programming"`、`"graph theory"`。
- `comments`：是否显示评论区域。
- `related_posts`：是否显示相关文章。

不要添加以下历史字段：

```yaml
canonical:
source_url:
source_categories:
source_platform_tags:
promoted_body_tags:
permalink:
cnblogs_post_id:
```

## 4. 草稿

文章还没写完时放入 `_drafts/`，例如：

```text
_drafts/unfinished-graph-note.md
```

草稿不会被正常生产构建发布。完成后再移入 `_posts/`，并改成带日期的英文文件名。

## 5. 修改已有文章

可以按标题搜索文章：

```bash
rg -l 'title: "文章标题"' _posts
```

直接编辑 Markdown 正文和 front matter。修改后应同步更新 `updated` 时间。

如果修改了文件名，先记录旧 URL 和新 URL，再搜索仓库中的旧路径：

```bash
rg -n '旧的文章 slug|/blog/2023/旧的文章 slug/' .
```

目录、相关文章和其他文章中的链接都要改成新的 `/blog/年份/新 slug/`。

历史迁移脚本会重新生成旧格式文章并覆盖正文，不能用于日常编辑：

```text
scripts/migrate_cnblogs_to_al_folio.py
```

它和 `migration-report.json` 仅用于保存历史迁移过程。当前站点的文章以 `_posts/` 为唯一事实来源。

## 6. 图片

建议为每篇文章建立独立图片目录：

```text
assets/img/blog/posts/my-new-algorithm-note/example.png
```

Markdown 中使用根相对路径：

```markdown
![算法流程图](/assets/img/blog/posts/my-new-algorithm-note/example.png)
```

注意事项：

- 路径大小写必须和真实文件名完全一致。
- 不要使用电脑上的绝对路径，例如 `/home/magicat/...`。
- 不要把新图片放入历史目录 `assets/img/blog/cnblogs/`。
- 图片文件名建议只使用英文、数字、短横线和常见扩展名。
- 图片和文章一起提交到 Git。

## 7. Markdown 写法

行内公式：

```markdown
时间复杂度是 \(O(n\log n)\)。
```

独立公式：

```markdown
\[
f(x)=\sum_{i=1}^{n}x_i
\]
```

代码块：

````markdown
```cpp
#include <iostream>

int main() {
    std::cout << "Hello";
}
```
````

表格：

```markdown
| 方法 | 复杂度 |
| --- | --- |
| 排序 | \(O(n\log n)\) |
| 哈希 | \(O(n)\) |
```

普通站内文章链接：

```markdown
[上一篇文章](/blog/2023/algorithm-notes/)
```

外部链接直接使用完整 URL：

```markdown
[Codeforces](https://codeforces.com/)
```

## 8. 本地预览

Docker 方式：

```bash
cd /home/magicat/workspace/00文档/blogs/kdk550.github.io
docker compose up
```

然后打开 <http://localhost:8080>。结束预览时按 `Ctrl+C`。

如果已经安装 Ruby 和 Bundler，也可以使用：

```bash
bundle install
bundle exec jekyll serve
```

## 9. 发布前检查

先构建生产站点：

```bash
JEKYLL_ENV=production bundle exec jekyll build
```

再运行验收工具：

```bash
./scripts/verify_built_site.py
```

它会检查：

- 所有 `_posts/` 文件名和日期格式。
- 文章是否含有已经废弃的历史字段。
- 每篇文章是否生成对应 HTML。
- 文章页面是否有必要的 article 元数据。
- 文章、图片、脚本、样式和站内链接是否有效。
- Blog 分页和标签归档是否一致。
- 首页、Blog、News 导航是否存在。

提交前再运行：

```bash
git diff --check
git status
```

## 10. 提交和发布到 GitHub

确认变更内容：

```bash
git status
git diff --stat
git diff -- _posts/某篇文章.md
```

提交：

```bash
git add _posts assets/img/blog/posts _pages _news CONTENT_GUIDE.md scripts/verify_built_site.py
git commit -m "Update blog content"
```

推送：

```bash
git push origin master
```

GitHub Actions 会构建并发布 GitHub Pages。线上地址是：

<https://kdk550.github.io/>

## 11. 常见问题

### 文件名含中文或大写字母

把文件名改成小写英文 slug，例如：

```text
2026-09-06-graph-algorithm-note.md
```

### Front matter 解析失败

确认文件第一行是 `---`，并且字段末尾还有第二个独立的 `---`。YAML 字符串中含冒号、方括号或引号时，使用双引号包裹。

### 图片显示不出来

检查图片是否位于 `assets/img/blog/posts/`，并确认 Markdown 路径以 `/assets/` 开头、大小写完全一致。

### 验证器提示旧字段

删除文章中的 `canonical`、`source_url`、`source_categories`、`source_platform_tags`、`promoted_body_tags`、`permalink` 和 `cnblogs_post_id`。历史报告中的这些字段可以保留，因为它不属于活动文章。

### 改名后链接失效

用 `rg` 搜索旧 slug，更新目录、相关文章和其他文章中的链接，然后重新构建验证。

### Git push 失败

先检查远程地址和 SSH 身份：

```bash
git remote -v
ssh -T git@github.com-kdk550
```

如果看到 `Hi kdk550! You've successfully authenticated`，说明 SSH 认证成功；随后检查当前分支、提交状态以及网络连接。
