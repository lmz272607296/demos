"""Build full-length GIFs and gif.html: python -m pip install imageio-ffmpeg."""

import argparse
import html
import json
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import imageio_ffmpeg


ROOT = Path(__file__).resolve().parent
DESTINATION = ROOT / "assets/img/gif"
FPS = 25
# Match the displayed cards while retaining the complete action and playback speed.
CLIPS = [
    ("rotation-video", "inhand-rotation", 640, 360),
    ("simulation-video", "inhand-simulation", 640, 360),
    ("apple-video", "apple-grasp", 640, 360),
    ("grasp-video", "bottle-grasp", 640, 360),
    ("hand-video", "gesture-following", 640, 426),
    ("arm-video", "arm-teleoperation", 560, 448),
    ("eeg-video", "eeg-control", 640, 360),
    ("act-video", "chopsticks", 360, 640),
]


def encode(clip, force=False):
    identifier, name, width, height = clip
    source = ROOT / "assets/video/web" / f"{name}.mp4"
    destination = DESTINATION / f"{name}.gif"
    # Rebuild when either the source or the encoding recipe changes.
    if force or not destination.exists() or destination.stat().st_mtime < max(source.stat().st_mtime, Path(__file__).stat().st_mtime):
        temporary = destination.with_suffix(".partial.gif")
        graph = (
            f"[0:v]fps={FPS},scale={width}:{height}:flags=lanczos,setsar=1,split[frames][colors];"
            "[colors]palettegen=max_colors=256:stats_mode=diff[palette];"
            "[frames][palette]paletteuse=dither=bayer:bayer_scale=3:diff_mode=rectangle"
        )
        subprocess.run([
            imageio_ffmpeg.get_ffmpeg_exe(), "-hide_banner", "-loglevel", "error", "-y",
            "-i", str(source), "-filter_complex", graph, "-an", "-loop", "0",
            "-threads", "2", "-filter_complex_threads", "2", str(temporary),
        ], check=True)
        temporary.replace(destination)
    return {"id": identifier, "name": name, "width": width, "height": height,
            "fps": FPS, "bytes": destination.stat().st_size}


def build_page(results):
    # Keep the review page synchronized with the main page's copy and layout.
    page = (ROOT / "index.html").read_text(encoding="utf-8")
    page = page.replace("<title>", "<title>GIF 审阅版 · ", 1)
    page = page.replace('<body>', '<body data-media-mode="gif">', 1)
    page = page.replace(
        '  <script src="assets/showcase.js?v=20261105-media-review" defer></script>',
        '  <script src="assets/showcase.js?v=20261105-media-review" defer></script>\n'
        '  <script src="assets/gif-preview.js?v=20261105-media-review" defer></script>',
    )
    total_mb = sum(item["bytes"] for item in results) / 1_000_000
    banner = (
        '    <aside class="review-banner container" aria-label="GIF 审阅说明">\n'
        '      <div><strong>GIF 效果审阅</strong>'
        f'<p>完整时长 · {FPS} fps · 256 色 · 可见时自动循环；点击画面暂停 / 重播。'
        f'8 段合计 {total_mb:.1f} MB，首次加载需等待；可通过原 MP4 对照画质和流畅度。</p></div>\n'
        '      <a class="resume-link" href="index.html">查看 B 站版本 ↗</a>\n'
        '    </aside>\n'
    )
    page = page.replace('  <main id="main-content">\n', '  <main id="main-content">\n' + banner, 1)
    for item in results:
        identifier, name = item["id"], item["name"]
        pattern = rf'<iframe id="{re.escape(identifier)}"[^>]*></iframe>'
        match = re.search(pattern, page)
        if not match:
            raise ValueError(f"Missing source iframe: {identifier}")
        label = html.unescape(re.search(r'title="([^"]+)"', match[0])[1]).replace(" · B 站播放器", "")
        caption = re.search(r'aria-describedby="([^"]+)"', match[0])[1]
        poster = f"assets/img/web/{name}.webp"
        gif = f"assets/img/gif/{name}.gif"
        player = (
            f'<button class="gif-toggle" type="button" aria-label="暂停动图：{html.escape(label, quote=True)}" '
            f'aria-describedby="{caption}" aria-pressed="false">\n'
            f'                <img id="{identifier}" class="demo-gif" src="{poster}" data-poster="{poster}" '
            f'data-gif="{gif}" alt="{html.escape(label, quote=True)}" width="{item["width"]}" height="{item["height"]}" decoding="async">\n'
            '                <span class="gif-status" aria-live="polite">等待播放</span>\n'
            '              </button>'
        )
        page = page[:match.start()] + player + page[match.end():]
        # Replace the media links in this caption only; preserve the original Bilibili URL.
        caption_pattern = rf'(<figcaption\b[^>]*id="{caption}"[\s\S]*?<p class="media-links">)([\s\S]*?)(</p>)'
        links = (
            f'<a href="assets/video/web/{name}.mp4" target="_blank" rel="noopener">原 MP4 对照 ↗</a>'
            f'<a href="{gif}" target="_blank" rel="noopener">打开 GIF ↗</a>'
        )
        page, count = re.subn(caption_pattern, lambda m: m[1] + links + m[2] + m[3] + (
            f'\n              <p class="gif-details">GIF · {item["width"]} × {item["height"]} · {FPS} fps · '
            f'{item["bytes"] / 1_000_000:.2f} MB</p>'
        ), page, count=1)
        if count != 1:
            raise ValueError(f"Missing caption: {caption}")
    if "gif-preview.js" not in page or "<iframe" in page:
        raise ValueError("GIF page generation failed: check the main page template")
    (ROOT / "gif.html").write_text(page, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true", help="Rebuild all GIF assets")
    args = parser.parse_args()
    DESTINATION.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(lambda clip: encode(clip, args.force), CLIPS))
    build_page(results)
    print(json.dumps({"page": "gif.html", "clips": results, "total_MB": round(sum(item["bytes"] for item in results) / 1_000_000, 2)}, indent=2))


if __name__ == "__main__":
    main()
