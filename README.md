# kdk550.github.io

magicat 的个人网站与技术博客：<https://kdk550.github.io/>

站点使用 [al-folio](https://github.com/alshedivat/al-folio) 主题，基于官方模板 `084c7eae` 配置，通过 GitHub Actions 构建后发布到 `gh-pages` 分支。

## 内容结构

- `_pages/`：首页、博客列表和 404 页面。
- `_posts/`：Markdown 博客文章。
- `assets/img/blog/`：博客文章使用的本地图片。
- `_config.yml`：站点、主题、数学公式、搜索和归档配置。
- `scripts/migrate_cnblogs_to_al_folio.py`：从本地博客园归档重建文章的可重复执行脚本。

公开站点使用统一的英文 tags：博客园的 16 个原始分类和 5 篇正文中的 11 个手写 `tag:` 语义提示，经合并、翻译后形成 12 个 tags。原始中文分类仍保留在文章 front matter 的 `source_categories` 和 `migration-report.json` 中。

## 本地预览

官方推荐使用 Docker：

```bash
docker compose pull
docker compose up
```

然后访问 <http://localhost:8080>。也可以在安装 Ruby 和 Bundler 后运行：

```bash
bundle install
bundle exec jekyll serve
```

## 文章迁移与验证

从本地归档重新生成博客文章：

```bash
./scripts/migrate_cnblogs_to_al_folio.py \
  --archive /home/magicat/00文档/blogs/20260711/archive
```

构建完成后，验证文章、分页、图片、内部链接与技术内容：

```bash
./scripts/verify_built_site.py
```

迁移统计保存在 `migration-report.json`。

## 发布

1. 把源码推送到 `master`。
2. `.github/workflows/deploy.yml` 自动构建并更新 `gh-pages`。
3. GitHub 仓库的 Pages 发布源设为 `gh-pages` 分支的 `/(root)`。

初次发布前，需在 `Settings → Actions → General → Workflow permissions` 选择 **Read and write permissions**。

## 历史与授权

- 旧 Hexo/ARIA 站点保留在 Git 标签 `pre-al-folio-20260711`，不再作为当前站点文件。
- al-folio 基于 MIT License，授权文本见 [LICENSE](LICENSE)。
