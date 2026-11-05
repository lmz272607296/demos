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

网页和简历由 GitHub Pages 提供，8 个演示均使用 B 站外链播放器。视频按页面从上到下、从左到右的顺序对应如下：

| 演示 | B 站 BV 号 |
| --- | --- |
| 方块手内旋转 · 真机 | `BV1N84b68EYZ` |
| 方块手内旋转 · 仿真 | `BV19V4b6gEjd` |
| 视觉引导抓取 · 苹果 | `BV1cZ4t6HEh2` |
| 视觉引导抓取 · 瓶子 | `BV1nZ4t6HEif` |
| 灵巧手手势跟随 | `BV1cZ4t6HEjx` |
| 双臂 VR 遥操作 | `BV1cZ4t6HEh5` |
| 脑电指令控制机械臂 | `BV1cZ4t6HEgQ` |
| 筷子夹取 · 真机实录 | `BV1FZ4t6HEyu` |

- iframe 使用 HTTPS、响应式尺寸和 `loading="lazy"`，各卡片提供对应的 B 站原视频链接。
- 参数统一设置为 `autoplay=true&muted=true&loop=true&danmaku=false&danmakuClosed=true`；使用 `true/false` 兼容 B 站移动播放器，并通过 iframe 的 `allow` 开放自动播放、全屏和画中画权限。
- 已验证桌面与 Android 模式下可静音自动播放，实际行为仍受浏览器策略影响。B 站桌面外链播放器忽略 `loop`，移动播放器支持循环。
- 视频清晰度、平台提示、控制按钮及片尾行为由 B 站提供；站点的原生 MP4 控制脚本无法控制跨域 iframe 的播放状态。
- 简历位于 `email/assets/resume.pdf`，更新时同步修改 HTML 中的 `?v=` 版本参数。

历史 MP4 和封面保留在 `email/assets/video/web/`、`email/assets/img/web/`。`email/optimize_media.py` 记录源文件映射和 H.264 / MP4、30 fps、`faststart` 转码参数，需要本地安装 `imageio-ffmpeg` 后运行。使用 `--force` 重新生成，使用 `--posters` 生成封面；这些文件不再由申请页播放器直接加载。
