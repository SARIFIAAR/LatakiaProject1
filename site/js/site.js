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
  var night = document.getElementById("heroNight");
  var dayLabel = document.getElementById("dayNightLabel");

  gsap.timeline({
    scrollTrigger: {
      trigger: ".hero",
      start: "top top",
      end: "bottom top",
      scrub: 0.6,
      onUpdate: function (self) {
        dayLabel.textContent = self.progress > 0.55 ? "Night" : "Day";
      }
    }
  })
    .to(night, { opacity: 1, ease: "none" }, 0)
    .to(".hero-inner", { y: -70, opacity: 0.15, ease: "none" }, 0)
    .to(".hero-img", { scale: 1.09, ease: "none" }, 0);

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
  gsap.utils.toArray(".pass-text p, .spec, .fig-note, .model-note").forEach(function (el) {
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
  (function () {
    var tabs = document.querySelectorAll(".plan-tabs button");
    var panes = document.querySelectorAll(".plan");
    var keyEl = document.getElementById("planKey");
    if (!tabs.length || !keyEl) return;

    var KEYS = {
      ground: [
        ["Frontage", "10.70 m", ""],
        ["Depth", "21.50 m", ""],
        ["Passage", "2.50 m", "clear width"],
        ["Shopfronts", "3.70 m", "each, to the street"],
        ["Front shops", "7.10 m", "deep"]
      ],
      typical: [
        ["Street", "49 m²", "الشارع"],
        ["Street corner", "40 m²", "زاوية الشارع"],
        ["Back corner", "44 m²", "الزاوية الخلفية"],
        ["Back", "44 m²", "الخلفي"],
        ["Stair and core", "15 m²", "الدرج"]
      ]
    };

    function paint(name) {
      keyEl.innerHTML = KEYS[name].map(function (k) {
        return "<div><dt>" + k[0] + "</dt><dd>" + k[1] +
               (k[2] ? "<small>" + k[2] + "</small>" : "") + "</dd></div>";
      }).join("");
      if (!reduce) {
        gsap.from(keyEl.children, { y: 14, opacity: 0, duration: 0.6,
                                    ease: "power3.out", stagger: 0.045 });
      }
    }

    function show(name) {
      tabs.forEach(function (t) { t.setAttribute("aria-selected", String(t.dataset.plan === name)); });
      panes.forEach(function (p) { p.classList.toggle("is-on", p.dataset.plan === name); });
      paint(name);
    }

    tabs.forEach(function (t) {
      t.addEventListener("click", function () { show(t.dataset.plan); });
      t.addEventListener("keydown", function (e) {
        if (e.key !== "ArrowRight" && e.key !== "ArrowLeft") return;
        e.preventDefault();
        var list = Array.prototype.slice.call(tabs);
        var next = list[(list.indexOf(t) + (e.key === "ArrowRight" ? 1 : list.length - 1)) % list.length];
        next.focus(); show(next.dataset.plan);
      });
    });

    paint("ground");
    gsap.from(".plan-stage", {
      scrollTrigger: { trigger: ".plans", start: "top 84%" },
      y: 30, opacity: 0, duration: 1.0, ease: "power3.out"
    });
    gsap.from(".plan-tabs button", {
      scrollTrigger: { trigger: ".plans", start: "top 88%" },
      y: 16, opacity: 0, duration: 0.7, ease: "power3.out", stagger: 0.08
    });
  })();

  /* ============================== THE MODEL ============================= */
  var canvas = document.getElementById("scene");
  if (!canvas || !window.THREE) return;

  var W = 10.70, D = 21.50, H = 12.00, GF = 5.00, WALL = 0.35;
  var SL0 = 0.20, SL1 = 3.90, PS0 = 4.10, PS1 = 6.60, SR0 = 6.80, SR1 = 10.50;
  var WIN = [1.34, 4.01, 6.69, 9.36], WW = 1.05, WH = 1.90, S1 = 5.65, S2 = 8.65;

  var renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.outputEncoding = THREE.sRGBEncoding;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.1;

  var scene = new THREE.Scene();
  var camera = new THREE.PerspectiveCamera(40, 1, 0.1, 400);
  var group = new THREE.Group();
  scene.add(group);

  var limestone = new THREE.MeshStandardMaterial({ color: 0xe6dbc2, roughness: 0.94 });
  var warm      = new THREE.MeshStandardMaterial({ color: 0xefe6d0, roughness: 0.9 });
  var darkStone = new THREE.MeshStandardMaterial({ color: 0x6f6656, roughness: 0.9 });
  var glassM    = new THREE.MeshStandardMaterial({ color: 0x2a3a46, roughness: 0.2, metalness: 0.5,
                                                   emissive: 0xffc98a, emissiveIntensity: 0.55 });
  var timberM   = new THREE.MeshStandardMaterial({ color: 0x5a3f2d, roughness: 0.72 });

  function box(w, h, d, m, x, y, z) {
    var mesh = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), m);
    mesh.position.set(x, y, z); mesh.castShadow = true; mesh.receiveShadow = true;
    group.add(mesh); return mesh;
  }

  /* facade with real openings */
  var shape = new THREE.Shape();
  shape.moveTo(0, 0); shape.lineTo(W, 0); shape.lineTo(W, H); shape.lineTo(0, H); shape.lineTo(0, 0);

  function segHole(x0, x1) {
    var p = new THREE.Path(), spr = 3.40, rise = 0.80, s = x1 - x0;
    var R = (s * s / 4 + rise * rise) / (2 * rise), cx = (x0 + x1) / 2, cy = spr + rise - R;
    p.moveTo(x0, 0); p.lineTo(x0, spr);
    var a0 = Math.atan2(spr - cy, x0 - cx), a1 = Math.atan2(spr - cy, x1 - cx);
    if (a0 < a1) a0 += Math.PI * 2;
    for (var i = 0; i <= 24; i++) {
      var t = a0 + (a1 - a0) * (i / 24);
      p.lineTo(cx + R * Math.cos(t), cy + R * Math.sin(t));
    }
    p.lineTo(x1, 0); p.lineTo(x0, 0); return p;
  }
  shape.holes.push(segHole(SL0, SL1));
  shape.holes.push(segHole(SR0, SR1));

  (function () {                                   /* pointed horseshoe */
    var p = new THREE.Path(), cx = (PS0 + PS1) / 2, a = (PS1 - PS0) / 2, spr = 3.00, Hh = 1.80, n = 34;
    var R = [], i, u, f;
    for (i = n; i >= 0; i--) {
      u = i / n; f = Math.pow(1 - u, 0.60) + 0.22 * Math.sin(Math.PI * Math.pow(u, 0.75));
      R.push([cx + a * f, spr + u * Hh]);
    }
    p.moveTo(PS0, 0); p.lineTo(PS0, spr);
    for (i = R.length - 1; i >= 0; i--) p.lineTo(2 * cx - R[i][0], R[i][1]);
    for (i = 0; i < R.length; i++) p.lineTo(R[i][0], R[i][1]);
    p.lineTo(PS1, 0); p.lineTo(PS0, 0);
    shape.holes.push(p);
  })();

  WIN.forEach(function (c) {
    [S1, S2].forEach(function (s) {
      var p = new THREE.Path();
      p.moveTo(c - WW / 2, s); p.lineTo(c + WW / 2, s);
      p.lineTo(c + WW / 2, s + WH); p.lineTo(c - WW / 2, s + WH); p.lineTo(c - WW / 2, s);
      shape.holes.push(p);
    });
  });

  var facade = new THREE.Mesh(new THREE.ExtrudeGeometry(shape, { depth: WALL, bevelEnabled: false }), limestone);
  facade.castShadow = facade.receiveShadow = true;
  group.add(facade);

  /* mass: open passage between two ground-floor wings */
  var dz = D - WALL, zc = -dz / 2;
  box(PS0, GF, dz, darkStone, PS0 / 2, GF / 2, zc);
  box(W - PS1, GF, dz, darkStone, (PS1 + W) / 2, GF / 2, zc);
  box(W, H - GF, dz, darkStone, W / 2, GF + (H - GF) / 2, zc);
  box(W + 0.10, 0.30, D, darkStone, W / 2, H + 0.15, -D / 2 + WALL);

  /* openings dressed */
  WIN.forEach(function (c) {
    [S1, S2].forEach(function (s) {
      box(WW - 0.05, WH - 0.05, 0.05, glassM, c, s + WH / 2, -0.02);
      box(WW + 0.44, 0.10, 0.20, warm, c, s - 0.05, WALL - 0.02);
      box(WW + 0.24, 0.14, 0.18, warm, c, s + WH + 0.08, WALL - 0.01);
      box(0.20, 0.26, 0.22, warm, c, s + WH + 0.12, WALL + 0.02);
      [-1, 1].forEach(function (sd) {
        box(0.40, WH - 0.04, 0.06, timberM, c + sd * (WW / 2 + 0.21), s + WH / 2, WALL + 0.04);
      });
    });
  });
  box(3.60, 4.15, 0.06, glassM, (SL0 + SL1) / 2, 2.10, -0.02);
  box(3.60, 4.15, 0.06, glassM, (SR0 + SR1) / 2, 2.10, -0.02);

  /* ablaq ring on the entrance */
  (function () {
    var cx = (PS0 + PS1) / 2, a = (PS1 + 0.17 - PS0) / 2, spr = 3.00, Hh = 1.80, n = 13, i, pts = [];
    for (i = n; i >= 0; i--) {
      var u = i / n, f = Math.pow(1 - u, 0.60) + 0.22 * Math.sin(Math.PI * Math.pow(u, 0.75));
      pts.push([cx + a * f, spr + u * Hh]);
    }
    function ring(list, flip) {
      for (var k = 0; k < list.length - 1; k++) {
        var ax = list[k][0], ay = list[k][1], bx = list[k + 1][0], by = list[k + 1][1];
        var m = new THREE.Mesh(new THREE.BoxGeometry(Math.hypot(bx - ax, by - ay) * 1.08, 0.34, 0.30),
                               (k % 2 ? (flip ? warm : darkStone) : (flip ? darkStone : warm)));
        m.position.set((ax + bx) / 2, (ay + by) / 2, WALL + 0.06);
        m.rotation.z = Math.atan2(by - ay, bx - ax);
        m.castShadow = true; group.add(m);
      }
    }
    ring(pts.slice().reverse(), false);
    ring(pts.map(function (p) { return [2 * cx - p[0], p[1]]; }), true);
  })();

  /* plinth, string course, stepped cornice, parapet, name panel */
  box(W + 0.14, 0.40, WALL + 0.14, darkStone, W / 2, 0.20, WALL / 2 + 0.03);
  box(W + 0.20, 0.26, WALL + 0.20, warm, W / 2, GF + 0.13, WALL / 2 + 0.05);
  box(W + 0.24, 0.10, WALL + 0.24, warm, W / 2, 11.06, WALL / 2 + 0.07);
  box(W + 0.40, 0.16, WALL + 0.42, warm, W / 2, 11.42, WALL / 2 + 0.17);
  box(W, 0.60, WALL, limestone, W / 2, 11.75, WALL / 2);
  box(2.90, 0.62, WALL + 0.16, limestone, W / 2, 12.32, WALL / 2 + 0.04);
  box(3.10, 0.14, WALL + 0.26, warm, W / 2, 12.63, WALL / 2 + 0.07);
  var rose = new THREE.Mesh(new THREE.CylinderGeometry(0.20, 0.20, 0.10, 24), warm);
  rose.rotation.x = Math.PI / 2; rose.position.set(W / 2, 12.28, WALL + 0.12);
  group.add(rose);

  /* balcony */
  box(3.60, 0.14, 0.55, warm, W / 2, 5.62, WALL + 0.275);
  for (var b = 0; b <= 20; b++) box(0.035, 0.90, 0.035, darkStone, 3.65 + b * 3.4 / 20, 6.09, WALL + 0.52);
  box(3.70, 0.08, 0.10, darkStone, W / 2, 6.54, WALL + 0.52);

  /* corner quoins */
  for (var q = 0.42; q < H - 0.42; q += 0.84) {
    box(0.44, 0.42, WALL + 0.08, warm, 0.22, q + 0.21, WALL / 2 + 0.02);
    box(0.44, 0.42, WALL + 0.08, warm, W - 0.22, q + 0.21, WALL / 2 + 0.02);
  }

  /* ground plane */
  var ground = new THREE.Mesh(new THREE.PlaneGeometry(240, 240),
                              new THREE.MeshStandardMaterial({ color: 0x2a3340, roughness: 1 }));
  ground.rotation.x = -Math.PI / 2; ground.receiveShadow = true;
  ground.position.set(W / 2, 0, -D / 2); group.add(ground);

  /* light */
  scene.add(new THREE.HemisphereLight(0x9fbdd4, 0x3a3a35, 0.75));
  var key = new THREE.DirectionalLight(0xffe9cc, 2.0);
  key.position.set(-16, 24, 26); key.castShadow = true;
  key.shadow.mapSize.set(2048, 2048);
  var c = key.shadow.camera; c.left = -22; c.right = 22; c.top = 26; c.bottom = -6; c.far = 110;
  scene.add(key);
  scene.add(new THREE.DirectionalLight(0x9ab6d0, 0.45).translateX(20));

  group.position.set(-W / 2, -5.6, D / 2 - 3);

  /* camera: scroll orbits it, drag overrides */
  var orbit = { th: -0.42, ph: 1.28, r: 37 };
  var drag = null, manual = false;
  function place() {
    camera.position.set(
      orbit.r * Math.sin(orbit.ph) * Math.sin(orbit.th),
      orbit.r * Math.cos(orbit.ph),
      orbit.r * Math.sin(orbit.ph) * Math.cos(orbit.th));
    camera.lookAt(0, 0.4, 0);
  }
  canvas.addEventListener("pointerdown", function (e) {
    drag = { x: e.clientX, y: e.clientY }; manual = true;
    canvas.setPointerCapture(e.pointerId);
  });
  canvas.addEventListener("pointermove", function (e) {
    if (!drag) return;
    orbit.th -= (e.clientX - drag.x) * 0.006;
    orbit.ph = Math.max(0.45, Math.min(1.52, orbit.ph - (e.clientY - drag.y) * 0.004));
    drag.x = e.clientX; drag.y = e.clientY; place();
  });
  ["pointerup", "pointercancel"].forEach(function (t) {
    canvas.addEventListener(t, function () { drag = null; });
  });

  ScrollTrigger.create({
    trigger: ".model", start: "top bottom", end: "bottom top", scrub: 1,
    onUpdate: function (self) {
      if (manual) return;
      orbit.th = -0.78 + self.progress * 1.35;
      orbit.ph = 1.34 - self.progress * 0.19;
      orbit.r  = 39 - self.progress * 5;
      place();
    }
  });

  function resize() {
    var w = canvas.clientWidth, h = canvas.clientHeight;
    if (!w || !h) return;
    renderer.setSize(w, h, false);
    camera.aspect = w / h; camera.updateProjectionMatrix();
  }
  window.addEventListener("resize", resize);
  ScrollTrigger.addEventListener("refresh", resize);
  resize(); place();
  // the canvas has no measured size on the first pass, which would leave the camera
  // at aspect 1 and the building cropped — re-measure once layout has settled
  requestAnimationFrame(function () { resize(); place(); });
  window.addEventListener("load", function () { resize(); place(); ScrollTrigger.refresh(); });

  var visible = true;
  new IntersectionObserver(function (es) { visible = es[0].isIntersecting; },
                           { rootMargin: "150px" }).observe(canvas);
  (function loop() {
    if (visible) renderer.render(scene, camera);
    requestAnimationFrame(loop);
  })();
})();
