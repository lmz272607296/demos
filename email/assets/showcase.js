(() => {
  "use strict";

  // Match mobile devices, rather than viewport width: a narrow desktop window
  // must still wait for a click. Bilibili redirects mobile UAs to its loop-capable player.
  const mobilePlayer = /AppleWebKit.*Mobile/i.test(navigator.userAgent)
    && !/Domono/i.test(navigator.userAgent);
  document.querySelectorAll(".video-shell iframe[data-src]").forEach((iframe) => {
    const url = new URL(iframe.dataset.src);
    url.searchParams.set("autoplay", String(mobilePlayer));
    url.searchParams.set("muted", "true");
    url.searchParams.set("loop", String(mobilePlayer));
    url.searchParams.set("poster", "true");
    // Assign src only after selecting the policy, avoiding an initial autoplay request.
    iframe.src = url.href;
  });

  const videos = [...document.querySelectorAll(".video-shell video")];
  const visibleVideos = new Set();
  const pausedByUser = new WeakSet();
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  const connection = navigator.connection;
  let gestureFallbackAttached = false;

  const canAutoplay = () => !reducedMotion.matches && !connection?.saveData;

  const playVisible = () => {
    if (document.hidden || !canAutoplay()) return;
    visibleVideos.forEach((video) => {
      if (!pausedByUser.has(video)) playVideo(video);
    });
  };

  const attachGestureFallback = () => {
    if (gestureFallbackAttached) return;
    gestureFallbackAttached = true;
    const retry = (event) => {
      // A click on native controls belongs to the viewer, including pause clicks.
      if (event.target.closest("video")) return;
      document.removeEventListener("pointerdown", retry);
      document.removeEventListener("keydown", retry);
      gestureFallbackAttached = false;
      playVisible();
    };
    document.addEventListener("pointerdown", retry, { passive: true });
    document.addEventListener("keydown", retry);
  };

  const playVideo = (video) => {
    const playback = video.play();
    if (!playback) return;

    playback.catch((error) => {
      if (error.name === "NotAllowedError") {
        attachGestureFallback();
      }
    });
  };

  for (const video of videos) {
    const card = video.closest(".demo-card");
    const errorMessage = card.querySelector(".media-error");

    const showError = () => {
      if (errorMessage) errorMessage.hidden = false;
    };

    video.addEventListener("playing", () => {
      if (errorMessage) errorMessage.hidden = true;
    });
    video.addEventListener("pause", () => {
      if (visibleVideos.has(video) && !document.hidden) pausedByUser.add(video);
    });
    video.addEventListener("play", () => pausedByUser.delete(video));
    video.addEventListener("error", showError);
    video.querySelector("source").addEventListener("error", showError);
  }

  if ("IntersectionObserver" in window) {
    // Warm the MP4 metadata shortly before a clip enters the viewport.
    // Without JavaScript, preload=none and native controls still allow playback.
    const prepareObserver = new IntersectionObserver((entries) => {
      entries.forEach(({ target: video, isIntersecting }) => {
        if (!isIntersecting) return;
        if (!connection?.saveData) video.preload = "metadata";
        prepareObserver.unobserve(video);
      });
    }, { rootMargin: "240px 0px" });

    const playbackObserver = new IntersectionObserver((entries) => {
      entries.forEach(({ target: video, isIntersecting, intersectionRatio }) => {
        if (isIntersecting && intersectionRatio >= 0.15) {
          visibleVideos.add(video);
        } else {
          visibleVideos.delete(video);
          video.pause();
        }
      });
      playVisible();
    }, { threshold: [0, 0.15] });

    videos.forEach((video) => {
      prepareObserver.observe(video);
      playbackObserver.observe(video);
    });
  }

  window.addEventListener("pageshow", playVisible);

  document.addEventListener("visibilitychange", () => {
    if (document.hidden) videos.forEach((video) => video.pause());
    else playVisible();
  });

  const links = [...document.querySelectorAll(".nav-links a")];
  const sections = links.map((link) => document.querySelector(link.hash));
  let scheduled = false;

  const updateNavigation = () => {
    const threshold = Math.max(140, window.innerHeight * 0.32);
    let active = -1;
    sections.forEach((section, index) => {
      if (section.getBoundingClientRect().top <= threshold) active = index;
    });
    links.forEach((link, index) => {
      if (index === active) link.setAttribute("aria-current", "location");
      else link.removeAttribute("aria-current");
    });
    scheduled = false;
  };

  const scheduleNavigation = () => {
    if (!scheduled) {
      scheduled = true;
      window.requestAnimationFrame(updateNavigation);
    }
  };

  window.addEventListener("scroll", scheduleNavigation, { passive: true });
  window.addEventListener("resize", scheduleNavigation);
  window.addEventListener("pageshow", scheduleNavigation);
  updateNavigation();
})();
