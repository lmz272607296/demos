# Robotics demos · 李孟卓

这个仓库同时发布多份网页，使用 **URL 子目录**区分用途。GitHub Pages 从 `master` 分支的根目录发布；更新某个目录后，对应网页会自动部署。

| 网页 | 访问链接 | 入口文件 |
| --- | --- | --- |
| 访问学生申请 · 真机经验展示 | **https://lmz272607296.github.io/demos/email/** | `email/index.html` |
| 筷子操作项目 · 中文 | https://lmz272607296.github.io/demos/ | `index.html` → `index_cn.html` |
| 筷子操作项目 · English | https://lmz272607296.github.io/demos/index_en.html | `index_en.html` |

仓库：https://github.com/lmz272607296/demos

## 本地预览

在仓库根目录运行：

```bash
python -m http.server 8000
```

打开 http://localhost:8000/email/ 查看申请展示页，或 http://localhost:8000/ 查看筷子项目页。

## 更新发布

先用 `git status` 检查改动，只暂存需要发布的文件，然后提交并推送到 `origin master`。GitHub Pages 的发布进度可在仓库 Actions 中查看。

Pages 设置：https://github.com/lmz272607296/demos/settings/pages

发布来源：`Deploy from a branch` → `master` → `/(root)`。

## 申请页的视频加载

- 完整演示使用 H.264 / MP4、30 fps，兼容常见桌面和手机浏览器；静音演示不携带音轨。
- `faststart` 将播放索引放在文件开头，支持边下载边播放；重新编码的视频关键帧间隔最长约 2 秒。脑电视频复用已有的精简版，避免二次有损压缩。
- 视频先展示 WebP 封面，接近视野时预读元数据，进入视野后静音播放；离开视野或切换标签页时暂停。
- 用户手动暂停后保持暂停。系统减少动态效果或浏览器省流量设置开启时，由用户点击播放。
- 不启用 JavaScript 时，仍可使用浏览器原生播放控件。
- 申请页发布资源位于 `email/assets/video/web/`、`email/assets/img/web/`，简历位于 `email/assets/resume.pdf`。

`email/optimize_media.py` 记录了完整视频的源文件映射和转码参数，需要本地安装 `imageio-ffmpeg` 后运行。双臂原始素材位于本地 `program/static/videos/piper_arm.mp4`，脑电精简版位于本地 `email/assets/video/eeg-control.mp4`，需要保留这些文件才能重新生成发布资源。使用 `--force` 可重新生成已有视频。

媒体直接由 GitHub Pages 提供，视频使用普通 Git 文件。Git LFS 不适合作为 GitHub Pages 的视频发布方式。实际访问速度仍取决于访问者到 GitHub Pages 的网络连接。
