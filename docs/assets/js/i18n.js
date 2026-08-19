/*
 * Tiny client-side i18n loader for the PSNee static site.
 * - Detects a default language from localStorage, then navigator.language.
 * - Fetches assets/i18n/<lang>.json and applies it to every [data-i18n] node.
 * - data-i18n="a.b.c" sets textContent from the nested JSON key "a.b.c".
 * - data-i18n-html="a.b.c" sets innerHTML instead (for strings with <strong>/<a> etc).
 * - Arrays at a key render <li> items into the element (used for tips/steps lists).
 * - data-i18n-attr="title:a.b.c|alt:d.e.f" translates element attributes.
 */
(function () {
  var SUPPORTED = ["en", "pt", "es"];
  var DEFAULT_LANG = "en";
  var STORAGE_KEY = "psnee-lang";

  function assetsRoot() {
    var el = document.currentScript || document.querySelector('script[src*="i18n.js"]');
    var src = el ? el.getAttribute("src") : "assets/js/i18n.js";
    return src.replace(/js\/i18n\.js$/, "");
  }

  var ROOT = assetsRoot();

  function detectLang() {
    var stored = null;
    try { stored = localStorage.getItem(STORAGE_KEY); } catch (e) {}
    if (stored && SUPPORTED.indexOf(stored) !== -1) return stored;

    var candidates = (navigator.languages && navigator.languages.length)
      ? navigator.languages
      : [navigator.language || navigator.userLanguage || DEFAULT_LANG];

    for (var i = 0; i < candidates.length; i++) {
      var code = String(candidates[i]).toLowerCase().slice(0, 2);
      if (SUPPORTED.indexOf(code) !== -1) return code;
    }
    return DEFAULT_LANG;
  }

  function getByPath(obj, path) {
    var parts = path.split(".");
    var cur = obj;
    for (var i = 0; i < parts.length; i++) {
      if (cur == null) return undefined;
      cur = cur[parts[i]];
    }
    return cur;
  }

  function applyTranslations(dict) {
    document.querySelectorAll("[data-i18n]").forEach(function (node) {
      var key = node.getAttribute("data-i18n");
      var val = getByPath(dict, key);
      if (val === undefined) return;
      if (Array.isArray(val)) {
        node.innerHTML = val.map(function (item) { return "<li>" + item + "</li>"; }).join("");
      } else {
        node.textContent = val;
      }
    });

    document.querySelectorAll("[data-i18n-html]").forEach(function (node) {
      var key = node.getAttribute("data-i18n-html");
      var val = getByPath(dict, key);
      if (val !== undefined) node.innerHTML = val;
    });

    document.querySelectorAll("[data-i18n-attr]").forEach(function (node) {
      var spec = node.getAttribute("data-i18n-attr");
      spec.split("|").forEach(function (pair) {
        var idx = pair.indexOf(":");
        if (idx === -1) return;
        var attr = pair.slice(0, idx).trim();
        var key = pair.slice(idx + 1).trim();
        var val = getByPath(dict, key);
        if (val !== undefined) node.setAttribute(attr, val);
      });
    });

    var titleKey = document.body.getAttribute("data-i18n-title");
    if (titleKey) {
      var titleVal = getByPath(dict, titleKey);
      var suffix = getByPath(dict, "meta.title_suffix");
      if (titleVal !== undefined) {
        document.title = suffix ? titleVal + " — " + suffix : titleVal;
      }
    }
  }

  function updateSwitcherUI(lang) {
    document.querySelectorAll(".lang-switch button").forEach(function (btn) {
      btn.classList.toggle("active", btn.getAttribute("data-lang") === lang);
    });
    document.documentElement.setAttribute("lang", lang);
  }

  var cache = {};

  function loadLang(lang) {
    if (cache[lang]) return Promise.resolve(cache[lang]);
    return fetch(ROOT + "i18n/" + lang + ".json")
      .then(function (res) { return res.json(); })
      .then(function (json) {
        cache[lang] = json;
        return json;
      });
  }

  function setLang(lang) {
    if (SUPPORTED.indexOf(lang) === -1) lang = DEFAULT_LANG;
    try { localStorage.setItem(STORAGE_KEY, lang); } catch (e) {}
    return loadLang(lang).then(function (dict) {
      applyTranslations(dict);
      updateSwitcherUI(lang);
    }).catch(function (err) {
      console.error("PSNee i18n: failed to load language " + lang, err);
    });
  }

  // On page load, the browser jumps to any #hash in the URL before the
  // translated text (and images) have finished loading, while the page is
  // still short/empty — so it lands in the wrong place. Once real content is
  // in and laid out, re-issue the scroll so it lands on the actual target.
  function fixHashScroll() {
    if (!window.location.hash) return;
    var id = decodeURIComponent(window.location.hash.slice(1));
    var el = document.getElementById(id);
    if (!el) return;
    // Force an instant jump for this correction, regardless of the site's
    // smooth-scroll CSS — this is fixing an already-wrong position, not
    // animating a user-initiated navigation, and an animated scrollIntoView
    // can stall entirely if the tab isn't focused/visible at that instant.
    var root = document.documentElement;
    var prevBehavior = root.style.scrollBehavior;
    root.style.scrollBehavior = "auto";
    el.scrollIntoView({ block: "start" });
    root.style.scrollBehavior = prevBehavior;
  }

  window.psneeI18n = { setLang: setLang, detectLang: detectLang };

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".lang-switch button").forEach(function (btn) {
      btn.addEventListener("click", function () {
        setLang(btn.getAttribute("data-lang"));
      });
    });

    var toggle = document.querySelector(".nav-toggle");
    var links = document.querySelector(".nav-links");
    if (toggle && links) {
      toggle.addEventListener("click", function () {
        links.classList.toggle("open");
      });
    }

    setLang(detectLang()).then(function () {
      requestAnimationFrame(fixHashScroll);
    });
    // Images finishing (board/BIOS photos) can also grow the page after the
    // text-driven fix above already ran — correct once more when they're in.
    window.addEventListener("load", fixHashScroll);
  });
})();
