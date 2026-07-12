# Dexterous Chopstick Manipulation

Bilingual project page for dexterous-hand chopstick manipulation, covering real-world data collection, ACT imitation learning, RL simulation data generation, and the long-term VLA route.

## Local Preview

Run from this directory:

```bash
python3 -m http.server 8000
```

Open `http://localhost:8000/`. The root page defaults to Chinese; the language switch opens the English version.

## Publish With The Existing GitHub Repository

This checkout is already connected to `https://github.com/Aurora-0419/Dexterous-Hand-Project.git` on branch `master`. If `Aurora-0419` is your GitHub account, run:

```bash
git add README.md index.html index_cn.html index_en.html \
  static/css/index.css static/js/index.js \
  static/images/favicon.ico static/images/wonderful.jpg \
  static/images/rll.png static/images/vla_pipeline.png \
  static/videos/carousel1.mp4 static/videos/follow_final.mp4 \
  "static/videos/瓶子抓取.mp4" "static/videos/水果抓取.mp4" \
  "static/videos/ACT筷子.mp4"
git commit -m "feat: publish dexterous hand project page"
git push origin master
```

Then:

1. Open `https://github.com/Aurora-0419/Dexterous-Hand-Project/settings/pages` while signed in.
2. Under `Build and deployment`, select `Deploy from a branch`.
3. Select branch `master`, folder `/(root)`, then click `Save`.
4. After deployment finishes, open `https://aurora-0419.github.io/Dexterous-Hand-Project/`.

If `Aurora-0419` is not your account, create an empty public repository under your own account and replace the remote before pushing:

```bash
git remote set-url origin https://github.com/USERNAME/REPOSITORY.git
git push -u origin master
```

The resulting URL will be `https://USERNAME.github.io/REPOSITORY/` after enabling Pages from `master` and `/(root)`.

GitHub rejects ordinary Git files of 100 MB or more. Keep each video below that limit or move large media to an external host or Git LFS before publishing.
