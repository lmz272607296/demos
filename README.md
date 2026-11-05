# Robotics demos · 李孟卓

这个仓库同时发布多份网页，使用 **URL 子目录**区分用途。GitHub Pages 从 `master` 分支的根目录发布；更新某个目录后，对应网页会自动部署。

| 网页 | 访问链接 | 入口文件 |
| --- | --- | --- |
| 访问学生申请 · 真机经验展示 | **https://lmz272607296.github.io/demos/email/** | `email/index.html` |
| GIF 审阅版 · 在线加载测试 | https://lmz272607296.github.io/demos/email/gif.html | `email/gif.html` |
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

## GIF 效果审阅

本地打开 `email/gif.html`，或启动上述预览服务后访问 http://localhost:8000/email/gif.html 。页面使用真实 GIF，保持全部 8 段演示的完整时长、正常播放速度及原有卡片布局。

在线审阅：https://lmz272607296.github.io/demos/email/gif.html 。测试首次加载时使用新的无痕会话，并分别尝试国内 Wi-Fi 和手机流量；完整加载后的循环流畅度不能代表首次访问的下载速度。

- 编码为 25 fps、最多 256 色，宽度最高 640 像素；每段标注尺寸和体积，提供原 MP4 和 GIF 链接以便比较。
- 动图进入视野后自动循环，离开视野或切换标签页时恢复静态封面，减少同时解码。点击画面暂停到封面，再次点击从头播放；减少动态效果 / 节省流量模式默认显示封面。
- 首轮 8 段 GIF 共约 452 MB，只适合先审阅效果，是否采用由审阅结果决定。B 站版本仍使用 `email/index.html`。
- 重建：在 `email/` 运行 `python build_gif_preview.py`；依赖 `imageio-ffmpeg`。脚本按当前 `index.html` 同步生成 `gif.html`，动图输出到 `assets/img/gif/`；`--force` 可强制重新转码。

## 申请页的 B 站视频加载

网页由 GitHub Pages 提供，8 个演示均使用 B 站外链播放器。简历通过申请邮件附上，两个网页版本均不再显示简历入口或卡片中的“B 站打开”链接。视频按页面从上到下、从左到右的顺序对应如下：

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

- iframe 使用 HTTPS、响应式尺寸和 `loading="lazy"`。
- 电脑端设置 `autoplay=false&muted=true&loop=false`，等待手动播放；手机端设置 `autoplay=true&muted=true&loop=true`，请求静音自动循环播放。两端均关闭弹幕、显示封面，使用 `true/false` 兼容 B 站移动播放器。
- `showcase.js` 根据设备 UA 设置参数后才赋值 iframe 的 `src`，避免电脑端先自动播放再被修改参数。缩窄电脑窗口不会切换到自动播放。禁用 JavaScript 时显示启用提示。
- 手机端自动播放仍受浏览器、低电量模式和 B 站实现影响。B 站桌面外链播放器忽略 `loop`，其控制栏无法由本站跨域隐藏。
- 视频清晰度、平台提示、控制按钮及片尾行为由 B 站提供；站点的原生 MP4 控制脚本无法控制跨域 iframe 的播放状态。

MP4 和封面保留在 `email/assets/video/web/`、`email/assets/img/web/`，用于生成 GIF、原片对照和动图暂停时的封面；B 站版不会直接加载这些视频。`email/optimize_media.py` 记录源文件映射和 H.264 / MP4、30 fps、`faststart` 转码参数，需要本地安装 `imageio-ffmpeg` 后运行。使用 `--force` 重新生成，使用 `--posters` 生成封面。
