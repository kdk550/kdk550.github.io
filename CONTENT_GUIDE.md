# 内容维护说明

本文档说明如何在 WSL 中新增、修改、预览和发布博客内容。

## 仓库边界

日常编辑只在 GitHub Pages 仓库中进行：

```text
/home/magicat/00文档/kdk550.github.io
```

下列目录是原始归档，保持只读：

```text
/home/magicat/00文档/blogs/20260711
```

## 新增博客文章

在 `_posts/` 中创建 `YYYY-MM-DD-slug.md`。`slug` 必须只使用小写英文、数字和连字符。例如：

```text
_posts/2026-07-15-my-new-post.md
```

最小可用模板：

```markdown
---
layout: post
title: "文章标题"
date: 2026-07-15 20:00:00 +0800
description: "显示在博客列表和搜索结果中的摘要。"
categories: []
tags: ["AI", "posts"]
comments: false
related_posts: false
---

这里是正文。
```

手写文章不要添加 `cnblogs_post_id`，文件名也不要使用 `cnblogs-数字` 格式。front matter 中不要设置 `slug` 或 `permalink`；站点会根据文件名自动生成稳定 URL。这样重新运行迁移脚本时不会删除手写文章。

暂未准备发布的文章请放入 `_drafts/`，不要在 `_posts/` 中使用未来日期或 `published: false`。验证器会要求 `_posts/` 中的每个手写文章都出现在构建结果中。

## 标签自动识别

在文章 front matter 的 `tags` 中直接填写标签：

```yaml
tags: ["AI", "model deployment"]
```

站点会自动：

1. 从所有文章收集标签。
2. 在 Blog 页展示标签。
3. 将标签转换为 URL slug，并生成 `/blog/tag/<slugified-tag>/` 归档页。
4. 在本地验证时动态核对标签链接和归档。

新增标签时无需修改 `_config.yml` 或验证脚本。标签名称仍由作者决定，站点不会根据正文猜测语义标签。为保持现有 taxonomy 一致，标签必须使用简短、英文、可复用的名称。

## 公式、代码、图片和表格

行内公式：

```markdown
The complexity is \(O(n\log n)\).
```

独立公式：

<!-- prettier-ignore -->
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
| Method  | Complexity     |
| ------- | -------------- |
| Sorting | \(O(n\log n)\) |
| Hashing | \(O(n)\)       |
```

图片建议按文章单独建目录：

```text
assets/img/blog/posts/my-new-post/example.png
```

在 Markdown 中引用：

```markdown
![图片说明](/assets/img/blog/posts/my-new-post/example.png)
```

不要把手写文章的图片放入 `assets/img/blog/cnblogs/`；该目录由迁移脚本管理，重新迁移时会被重建。

## 修改已迁移文章

先按标题查找文件：

```bash
cd /home/magicat/00文档/kdk550.github.io
rg -l 'title: "文章标题"' _posts
```

迁移文章的正文位于 `{% raw %}` 和 `{% endraw %}` 之间，直接在两个标记之间编辑。修改公开标签时只改 `tags`；`source_categories`、`source_platform_tags` 和 `promoted_body_tags` 是原始数据追溯信息。

需要注意：`scripts/migrate_cnblogs_to_al_folio.py` 会重新生成所有带 `cnblogs_post_id` 的文章。直接对迁移文章做的正文修改，在下次重新迁移时会被覆盖。

## About 和 News

- About 页：`_pages/about.md`
- Blog 页布局：`_pages/blog.md`
- News 列表页：`_pages/news.md`
- News 内容：`_news/YYYY-MM-DD-slug.md`

News 文件示例：

```markdown
---
layout: post
date: 2026-07-15 20:00:00 +0800
inline: true
related_posts: false
---

Published a new article.
```

## 本地预览和验证

使用 Docker 预览：

```bash
cd /home/magicat/00文档/kdk550.github.io
docker compose up
```

然后访问 <http://localhost:8080>。

已安装 Ruby 和 Bundler 时：

```bash
bundle install
bundle exec jekyll serve
```

发布前生成生产站点并验证：

```bash
JEKYLL_ENV=production bundle exec jekyll build
./scripts/verify_built_site.py
```

验证器会严格核对 121 篇迁移文章，同时允许任意数量的手写文章。它会根据 `_posts/` 源文件动态计算手写文章和预期分页，再与实际构建的文章、分页、标签链接和标签归档交叉核对。

## 提交和发布

```bash
git status
git diff --check
git add _posts/ assets/img/blog/ _news/ _pages/ CONTENT_GUIDE.md
git commit -m "Add new blog post"
git push origin master
```

推送到 `master` 后，GitHub Actions 会构建站点并发布到 `gh-pages`。线上地址为 <https://kdk550.github.io/>。
