# 修改内容与接入新素材

## 改课程和题目

`data/curriculum.json` 是易读数据；网页离线打开时读取 `data/curriculum.js`。两者内容要一致。建议修改 `tools/build_curriculum.py` 中的课程文字，再运行：

```sh
python tools/build_curriculum.py
```

每个概念有唯一 `id`、章节、五问、关键点、步骤、易错点、账目表和模型名。每题包含 `id`、`lesson`、`level`、`prompt`、四个 `options`、从 **0** 开始的正确 `answer` 索引与解析。保留已有 ID，避免已保存进度失配。

## 接入图片或动画

`script.js` 中 `study()` 生成课程页面，`renderStep()` 生成分步讲解，`home()` / `gallery()` 生成入口。搜索占位标题，如 `Personified animation` 或 `Lesson illustration`，替换对应的 `placeholder()` 调用：

```html
<img src="assets/images/lessons/etc.png" alt="Explain what the illustration shows">
<video src="assets/videos/lectures/etc.mp4" controls preload="metadata"></video>
```

使用相对路径，文件名大小写保持一致。保留未完成提示，直到确有最终素材。新增模型先修改 Blender 配方并导出，同步 `model-data.js` 后才能在网页显示。

## 本机数据格式

浏览器 localStorage 键：`biovision-energetics-v1`。包含显示名、完成概念、访问概念、笔记、收藏、标签、题目记录、测验历史和讨论草稿。MyBio 的 JSON 导入会替换当前记录；请先导出旧备份。不会向远程服务发送数据。
