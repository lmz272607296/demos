(() => {
  "use strict";

  const states = [...document.querySelectorAll(".demo-gif")].map((image) => ({
    image,
    button: image.closest("button"),
    status: image.closest("button").querySelector(".gif-status"),
    visible: false,
    paused: window.matchMedia("(prefers-reduced-motion: reduce)").matches || !!navigator.connection?.saveData,
    active: false,
    failed: false,
    loading: false,
  }));

  const update = (state) => {
    const active = state.visible && !state.paused && !document.hidden && !state.failed;
    if (active !== state.active) {
      state.active = active;
      state.loading = active;
      // GIFs have no native pause API. Restore the poster to stop offscreen decoding.
      state.image.src = active ? state.image.dataset.gif : state.image.dataset.poster;
    }
    state.button.setAttribute("aria-pressed", String(state.paused));
    state.button.setAttribute("aria-label", `${state.failed ? "重试加载" : state.paused ? "播放动图" : "暂停动图"}：${state.image.alt}`);
    state.button.classList.toggle("is-playing", active && !state.loading);
    state.status.textContent = state.failed ? "加载失败 · 点击重试或打开下方原视频" : state.loading ? "GIF 加载中…" : state.paused ? "点击播放 GIF" : active ? "点击暂停" : "等待播放";
  };

  states.forEach((state) => {
    state.button.addEventListener("click", () => {
      state.paused = state.failed ? false : !state.paused;
      state.failed = false;
      update(state);
    });
    state.image.addEventListener("load", () => {
      if (!state.active || state.image.getAttribute("src") !== state.image.dataset.gif) return;
      state.loading = false;
      update(state);
    });
    state.image.addEventListener("error", () => {
      if (!state.active) return;
      state.failed = true;
      update(state);
    });
    update(state);
  });

  if ("IntersectionObserver" in window) {
    const byImage = new Map(states.map((state) => [state.image, state]));
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(({ target, isIntersecting, intersectionRatio }) => {
        const state = byImage.get(target);
        state.visible = isIntersecting && intersectionRatio >= 0.1;
        update(state);
      });
    }, { threshold: [0, 0.1] });
    states.forEach(({ image }) => observer.observe(image));
  } else {
    states.forEach((state) => { state.visible = true; update(state); });
  }

  document.addEventListener("visibilitychange", () => states.forEach(update));
})();
