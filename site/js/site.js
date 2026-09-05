/* ==========================================================================
   Khan Murjan — Latakia
   GSAP + ScrollTrigger for the scroll work, Lenis for the scroll itself,
   Three.js for the model. No build step: everything here runs as-is.
   ========================================================================== */
(function () {
  "use strict";

  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var hasGSAP = !!(window.gsap && window.ScrollTrigger);
  if (hasGSAP) gsap.registerPlugin(ScrollTrigger);

  /* ---------------------------------------------------- smooth scroll --- */
  var lenis = null;
  if (window.Lenis && !reduce) {
    lenis = new Lenis({ duration: 1.05, smoothWheel: true, lerp: 0.09 });
    lenis.on("scroll", function () {
      if (hasGSAP) ScrollTrigger.update();
      navState();                                  // Lenis suppresses the native scroll event
    });
    gsapTicker();
    document.documentElement.classList.add("lenis");
  }
  function gsapTicker() {
    if (!hasGSAP) { requestAnimationFrame(function raf(t){ lenis.raf(t); requestAnimationFrame(raf); }); return; }
    gsap.ticker.add(function (time) { lenis.raf(time * 1000); });
    gsap.ticker.lagSmoothing(0);
  }
  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener("click", function (e) {
      var el = document.querySelector(a.getAttribute("href"));
      if (!el) return;
      e.preventDefault();
      if (lenis) lenis.scrollTo(el, { offset: -10 });
      else el.scrollIntoView({ behavior: reduce ? "auto" : "smooth" });
    });
  });

  /* ----------------------------------------------------------- header --- */
  var nav = document.getElementById("nav");
  var hero = document.querySelector(".hero");
  function navState() {
    // solid as soon as the hero has left, so the light text never sits on the cream
    var y = window.scrollY || document.documentElement.scrollTop || 0;
    nav.classList.toggle("is-solid", y > hero.offsetHeight - 90);
  }
  window.addEventListener("scroll", navState, { passive: true });
  window.addEventListener("resize", navState);
  navState();

  // deep links: Lenis owns the scroll position, so the browser's own hash jump is lost
  if (location.hash) {
    var deep = document.querySelector(location.hash);
    if (deep) requestAnimationFrame(function () {
      setTimeout(function () {
        if (lenis) lenis.scrollTo(deep, { immediate: true, offset: -10 });
        else deep.scrollIntoView();
        navState();
      }, 60);
    });
  }

  if (!hasGSAP) { document.body.classList.add("no-js"); return; }

  // ScrollTrigger owns the header state: reading window.scrollY is unreliable while
  // Lenis is driving, and a transparent header over the cream sections is unreadable
  ScrollTrigger.create({
    trigger: ".hero",
    start: "bottom top+=90",
    onEnter:     function () { nav.classList.add("is-solid"); },
    onLeaveBack: function () { nav.classList.remove("is-solid"); }
  });

  /* ------------------------------------------- hero: day becomes night --- */
  // Two phases across one pin. First the facade grows until it meets the edges
  // of the frame, then — and only then — day turns to night.
  var night = document.getElementById("heroNight");
  var dayLabel = document.getElementById("dayNightLabel");
  var dayBar = document.getElementById("dayNightBar");
  var frame = document.querySelector(".hero-frame");

  // how far the contained image has to grow to fill the hero's height
  function growTo() {
    var h = document.querySelector(".hero").getBoundingClientRect().height;
    var f = frame.getBoundingClientRect().height;
    return f > 0 ? Math.min(2.4, Math.max(1.05, (h / f) * 1.02)) : 1.6;
  }
  var grow = growTo();

  var heroTl = gsap.timeline({
    scrollTrigger: {
      trigger: ".hero",
      start: "top top",
      end: "+=220%",
      pin: true,
      pinSpacing: true,
      scrub: 0.55,
      anticipatePin: 1,
      invalidateOnRefresh: true,
      onRefresh: function () { grow = growTo(); },
      onUpdate: function (self) {
        var p = self.progress;
        dayLabel.textContent = p < 0.46 ? "Day" : p < 0.78 ? "Dusk" : "Night";
        if (dayBar) dayBar.style.width = (p * 100).toFixed(1) + "%";
      }
    }
  });

  heroTl
    // phase one — the facade grows to the edges
    .to(frame,          { scale: function () { return grow; }, duration: 0.46, ease: "power1.inOut" }, 0)
    .to(".hero-bg",     { opacity: 0, duration: 0.40, ease: "none" }, 0)
    // phase two — night falls on the filled frame
    .to(night,          { opacity: 1, duration: 0.30, ease: "power1.inOut" }, 0.48)
    .to(".hero-veil",   { opacity: 1.25, duration: 0.30, ease: "none" }, 0.48)
    // then let the words go
    .to(".hero-inner",  { y: -46, opacity: 0, duration: 0.16, ease: "power2.in" }, 0.84)
    .to(".hero-foot",   { opacity: 0, duration: 0.14, ease: "none" }, 0.88);

  /* ------------------------------------------------------ hero intro --- */
  var intro = gsap.timeline({ delay: 0.15 });
  intro
    .to(".hero .eyebrow", { opacity: 1, y: 0, duration: 0.9, ease: "power3.out" })
    .to(".wm-line > span", { y: "0%", duration: 1.15, ease: "expo.out" }, "-=0.55")
    .to(".wm-sub > span", { y: "0%", duration: 1.05, ease: "expo.out" }, "-=0.85")
    .to(".hero-tag", { opacity: 1, y: 0, duration: 0.85, ease: "power3.out" }, "-=0.65")
    .to(".hero .rule", { scaleX: 1, duration: 1.1, ease: "power2.inOut" }, "-=0.6")
    .to(".hero-creed", { opacity: 1, y: 0, duration: 0.85, ease: "power3.out" }, "-=0.75");

  /* ------------------------------------------- statement, word by word --- */
  var lede = document.querySelector(".lede");
  if (lede) {
    lede.innerHTML = lede.textContent.trim().split(/\s+/).map(function (w) {
      return '<span class="word"><span>' + w + "</span></span>";
    }).join(" ");
    gsap.from(".lede .word > span", {
      scrollTrigger: { trigger: ".statement", start: "top 74%" },
      yPercent: 108, duration: 1.0, ease: "expo.out", stagger: 0.022
    });
  }

  /* ---------------------------------------------------- section heads --- */
  gsap.utils.toArray(".section-head").forEach(function (h) {
    gsap.from(h.children, {
      scrollTrigger: { trigger: h, start: "top 86%" },
      y: 26, opacity: 0, duration: 0.9, ease: "power3.out", stagger: 0.08
    });
    gsap.from(h, {
      scrollTrigger: { trigger: h, start: "top 86%" },
      "--x": 0, duration: 1
    });
  });

  /* -------------------------------------------------------- counters --- */
  gsap.utils.toArray(".fig").forEach(function (el) {
    var target = parseFloat(el.dataset.count);
    var dec = parseInt(el.dataset.dec, 10) || 0;
    // show the real figure straight away: if the trigger never fires — deep link,
    // fast scroll, reduced motion — the number is still correct, never a stuck 0
    el.textContent = target.toFixed(dec);
    if (reduce) return;
    ScrollTrigger.create({
      trigger: el, start: "top 88%", once: true,
      onEnter: function () {
        var obj = { v: 0 };
        gsap.to(obj, {
          v: target, duration: 1.7, ease: "power2.out",
          onUpdate: function () { el.textContent = obj.v.toFixed(dec); },
          onComplete: function () { el.textContent = target.toFixed(dec); }
        });
      }
    });
  });
  gsap.from(".fig-grid li", {
    scrollTrigger: { trigger: ".fig-grid", start: "top 84%" },
    y: 26, opacity: 0, duration: 0.85, ease: "power3.out", stagger: 0.06
  });

  /* --------------------------------------------------------- parallax --- */
  gsap.utils.toArray("[data-parallax]").forEach(function (el) {
    var amt = parseFloat(el.dataset.parallax) || 0.12;
    gsap.fromTo(el, { yPercent: -amt * 100 * 0.5 }, {
      yPercent: amt * 100 * 0.5, ease: "none",
      scrollTrigger: { trigger: el.parentElement, start: "top bottom", end: "bottom top", scrub: true }
    });
  });

  /* ------------------------------------------------- general reveals --- */
  gsap.utils.toArray(".pass-text p, .shop-text p, .spec, .fig-note").forEach(function (el) {
    gsap.from(el, {
      scrollTrigger: { trigger: el, start: "top 88%" },
      y: 24, opacity: 0, duration: 0.9, ease: "power3.out"
    });
  });
  gsap.from(".tile", {
    scrollTrigger: { trigger: ".tiles", start: "top 82%" },
    y: 46, opacity: 0, duration: 1.0, ease: "power3.out", stagger: 0.09
  });
  gsap.utils.toArray(".floor-row").forEach(function (row) {
    gsap.from(row.children, {
      scrollTrigger: { trigger: row, start: "top 86%" },
      y: 24, opacity: 0, duration: 0.85, ease: "power3.out", stagger: 0.07
    });
  });
  gsap.from(".foot > div", {
    scrollTrigger: { trigger: ".foot", start: "top 88%" },
    y: 30, opacity: 0, duration: 0.95, ease: "power3.out", stagger: 0.1
  });

  /* ----------------------------------------------------- floor plans --- */
  gsap.utils.toArray(".plan-block").forEach(function (blk) {
    gsap.from(blk.querySelector(".plan-title"), {
      scrollTrigger: { trigger: blk, start: "top 88%" },
      y: 18, opacity: 0, duration: 0.8, ease: "power3.out"
    });
    gsap.from(blk.querySelector(".plan-stage"), {
      scrollTrigger: { trigger: blk, start: "top 84%" },
      y: 30, opacity: 0, duration: 1.0, ease: "power3.out"
    });
    gsap.from(blk.querySelectorAll(".plan-key > div"), {
      scrollTrigger: { trigger: blk.querySelector(".plan-key"), start: "top 92%" },
      y: 14, opacity: 0, duration: 0.65, ease: "power3.out", stagger: 0.05
    });
  });


})();
