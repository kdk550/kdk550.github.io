# kdk550.github.io

magicat 的个人网站与技术博客：<https://kdk550.github.io/>

站点使用 [al-folio](https://github.com/alshedivat/al-folio) 主题，基于官方模板 `084c7eae` 配置，通过 GitHub Actions 构建后发布到 `gh-pages` 分支。

## 内容结构

- `_pages/`：首页、博客列表和 404 页面。
- `_posts/`：Markdown 博客文章。
- `assets/img/blog/posts/`：博客文章使用的本地图片。
- `_config.yml`：站点、主题、数学公式、搜索和归档配置。
- `scripts/normalize_blog_posts.py`：本次统一英文命名使用的一次性整理工具，不用于日常写作。
- `scripts/migrate_cnblogs_to_al_folio.py`：历史归档迁移脚本，仅供查阅，禁止对当前站点重新运行。
- `CONTENT_GUIDE.md`：新增、修改、预览和发布内容的完整说明。

标签由每篇文章 front matter 中的 `tags` 自动发现，博客页会自动展示所有标签并生成归档，无需在 `_config.yml` 或验证脚本中维护固定列表。当前文章统一使用英文文件名和 URL；历史来源字段只可能出现在 `migration-report.json` 等归档资料中。

日常内容维护请参阅 [CONTENT_GUIDE.md](CONTENT_GUIDE.md)。

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

## 历史迁移与当前验证

历史迁移脚本仅用于了解过去的导入流程，不要对当前仓库运行。当前发布前只需构建并执行验证器：

构建完成后，验证 `_posts/` 中的全部文章、动态分页、自动标签归档、图片与内部链接：

```bash
./scripts/verify_built_site.py
```

历史迁移统计仍保存在 `migration-report.json`，但不参与当前验证。

## 发布

1. 把源码推送到 `master`。
2. `.github/workflows/deploy.yml` 自动构建并更新 `gh-pages`。
3. GitHub 仓库的 Pages 发布源设为 `gh-pages` 分支的 `/(root)`。

初次发布前，需在 `Settings → Actions → General → Workflow permissions` 选择 **Read and write permissions**。

## 历史与授权

- 旧 Hexo/ARIA 站点保留在 Git 标签 `pre-al-folio-20260711`，不再作为当前站点文件。
- al-folio 基于 MIT License，授权文本见 [LICENSE](LICENSE)。
