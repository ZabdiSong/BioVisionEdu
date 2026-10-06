# BIOVISION：本地打开与 GitHub 上传

## 现在在本地使用

完整解压，双击根目录的 `index.html`。桌面 Chrome/Edge/Firefox 等支持 JavaScript 与 WebGL 的浏览器可运行课程和 3D。没有 WebGL 时仍可阅读解释、答题和下载模型。不要只拷贝一个 HTML。

如果浏览器限制本地文件的存储，进入解压目录，用已安装的 Python 启动：

```sh
python -m http.server 8000
```

然后打开 `http://localhost:8000`。这是电脑本机服务，不会自动把网站公开到互联网。不需要 Python 也可以先尝试双击 HTML。

## 上传源码，先保留为仓库

1. 登录你自己的 GitHub，创建一个仓库，建议名称 `BIOVISION-EDU`。
2. 在仓库中使用 **Add file → Upload files**，上传解压文件夹**里面**的文件与目录；分批上传也可以，但要保留目录层级。也可用 GitHub Desktop 将整个目录提交到仓库。
3. 根目录应当直接看到 `index.html`、`style.css`、`script.js`、`learning.js`、`viewer.js`，以及 `assets`、`data`、`vendor` 等目录。
4. 提交文件。仅保存源码时，到这里就完成了。

**不要把 ZIP 本身当成网站上传，也不要在仓库根目录再包一层 BIOVISION 文件夹。** 上传后先检查 `assets/models/respiratory-etc.blend` 等嵌套文件确实存在。

如果使用 GitHub 网页拖放大目录受阻，推荐用 GitHub Desktop 的本地仓库方式。项目不需要 npm 构建或 Git LFS；本包最大的单个文件远小于 GitHub 的普通文件上限。

## 以后决定提供可浏览网站时

这一步是发布操作，你可以在准备好后自行开启；本次没有代你开启。

在仓库 **Settings → Pages → Build and deployment** 中：

- Source：`Deploy from a branch`。
- Branch：`main`，目录选 `/(root)`。
- Save。以 GitHub 显示的实际发布地址为准。

根目录已包含 `.nojekyll`，使用相对路径；不需要域名或 API 密钥。项目站点地址格式通常为 `https://你的用户名.github.io/仓库名称/`，这只是地址格式，尚未替你创建真实链接。

**GitHub 仓库链接用于看源码；GitHub Pages 链接用于直接体验网站。** 单纯上传 HTML 到代码仓库不会自动变成可浏览的网页。

官网依据：

- [GitHub Pages 发布来源设置](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
- [创建 GitHub Pages 网站](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site)
- [上传文件到仓库](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository)

## 必须保留的资源

| 目录/文件 | 内容 |
| --- | --- |
| `data/` | 课程、题目、词汇数据 |
| `assets/images/` | 你的 logo 和角色图 |
| `assets/videos/` | 已上传的 ETC 短片 |
| `assets/models/` | Blender/GLB 模型及网页几何数据 |
| `vendor/` | 离线 Three.js 与许可证 |
| `docs/` | 网站下载入口对应的学习/上传文件 |
| 根目录 HTML/CSS/JS | 网站运行入口 |

`reference-design/` 是原设计参考，不是首页；`tools/` 是复现工具，不是运行依赖。上传完整包最省事。

## 以后补素材

参照 `ASSET_GAPS_CN.md`。把文件放进建议目录，再修改 `script.js` 对应的图片或视频占位。不要把资源路径改成你电脑的绝对路径。更新内容后保留题目和概念 ID，旧学习记录才能继续匹配。

## 学习记录

本地文件、localhost 与 GitHub Pages 属于不同地址，浏览器会分别保存进度。发布前在 **MyBio → Export progress** 下载 JSON，再在新地址的 **Import backup** 导入。这里保存的是本机数据，没有共享服务器。
