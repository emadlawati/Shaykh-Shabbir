(() => {
  "use strict";

  const lessonId = document.body.dataset.lesson || "01";
  const prefix = `shabbir_usul_lesson_${lessonId}`;
  const SOURCES = window.LESSON_SOURCES || window.LESSON01_SOURCES || {};
  const SOURCE_ORDER = window.LESSON_SOURCE_ORDER || window.LESSON01_SOURCE_ORDER || Object.keys(SOURCES);
  const LABELS = window.LESSON_LABELS || window.LESSON01_LABELS;
  const KEYS = {
    theme: "shabbir_usul_theme",
    notes: `${prefix}_unified_notes`,
    tasks: `${prefix}_tasks`,
    errors: `${prefix}_error_log`,
    reviews: `${prefix}_review_dates`,
    tab: `${prefix}_active_tab`
  };

  const $ = (selector, root = document) => root.querySelector(selector);
  const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];

  function setTheme(theme) {
    document.documentElement.dataset.theme = theme;
    localStorage.setItem(KEYS.theme, theme);
    const label = $("#theme-label");
    if (label) label.textContent = theme === "dark" ? "النمط الفاتح" : "النمط الداكن";
  }

  function initTheme() {
    const saved = localStorage.getItem(KEYS.theme);
    const preferred = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
    setTheme(saved === "dark" || saved === "light" ? saved : preferred);
  }

  function activateTab(id, focus = false) {
    const button = $(`[data-tab="${id}"]`);
    const panel = $(`#panel-${id}`);
    if (!button || !panel) return;
    $$("[data-tab]").forEach((item) => item.setAttribute("aria-selected", String(item === button)));
    $$(".panel").forEach((item) => { item.hidden = item !== panel; });
    localStorage.setItem(KEYS.tab, id);
    history.replaceState(null, "", `#${id}`);
    if (focus) panel.focus({ preventScroll: true });
  }

  function loadTasks() {
    let saved = {};
    try { saved = JSON.parse(localStorage.getItem(KEYS.tasks) || "{}"); } catch (_) { saved = {}; }
    $$(".task-check").forEach((box) => {
      if (Object.prototype.hasOwnProperty.call(saved, box.id)) box.checked = Boolean(saved[box.id]);
    });
    updateProgress(false);
  }

  function updateProgress(save = true) {
    const boxes = $$(".task-check");
    const state = {};
    let complete = 0;
    boxes.forEach((box) => {
      state[box.id] = box.checked;
      if (box.checked) complete += 1;
    });
    if (save) localStorage.setItem(KEYS.tasks, JSON.stringify(state));
    const percent = boxes.length ? Math.round((complete / boxes.length) * 100) : 0;
    const text = $("#progress-text");
    const bar = $("#progress-fill");
    if (text) text.textContent = `${complete} من ${boxes.length} • ${percent}٪`;
    if (bar) bar.style.width = `${percent}%`;
  }

  function bindSavedText(selector, key) {
    const field = $(selector);
    if (!field) return;
    const saved = localStorage.getItem(key);
    if (saved !== null) field.value = saved;
    const count = $(`${selector}-count`);
    const persist = () => {
      localStorage.setItem(key, field.value);
      if (count) count.textContent = `${field.value.length} حرف`;
      const status = $("#save-status");
      if (status) {
        status.textContent = "حُفظ تلقائياً";
        clearTimeout(persist.timer);
        persist.timer = setTimeout(() => { status.textContent = ""; }, 1200);
      }
    };
    field.addEventListener("input", persist);
    if (count) count.textContent = `${field.value.length} حرف`;
  }

  function loadReviewDates() {
    let saved = {};
    try { saved = JSON.parse(localStorage.getItem(KEYS.reviews) || "{}"); } catch (_) { saved = {}; }
    $$("[data-review-date]").forEach((input) => {
      if (saved[input.id]) input.value = saved[input.id];
      input.addEventListener("change", () => {
        const current = {};
        $$("[data-review-date]").forEach((item) => { current[item.id] = item.value; });
        localStorage.setItem(KEYS.reviews, JSON.stringify(current));
      });
    });
  }

  function openSource(id) {
    const source = SOURCES[id];
    if (!source) return;
    $("#source-title").textContent = source.book;
    $("#source-author").textContent = source.author;
    $("#source-kind").textContent = LABELS.content_kind[source.content_kind];
    $("#source-verification").textContent = LABELS.verification[source.verification];
    $("#source-text").textContent = source.text;
    $("#source-context").textContent = source.context;
    const provenance = $("#source-provenance");
    provenance.innerHTML = "";
    [
      ["الطبعة", source.edition],
      ["الجزء", source.volume],
      ["الصفحة المطبوعة", source.printed_page],
      ["صفحة المسح/البيانات", source.scan_or_database_page]
    ].forEach(([label, value]) => {
      if (!value) return;
      const dt = document.createElement("dt");
      const dd = document.createElement("dd");
      dt.textContent = label;
      dd.textContent = value;
      provenance.append(dt, dd);
    });
    const link = $("#source-link");
    if (source.file) {
      link.href = source.file + (source.pdf_page ? `#page=${source.pdf_page}` : "");
      link.hidden = false;
    } else {
      link.hidden = true;
    }
    $("#source-overlay").classList.add("open");
    $("#source-drawer").classList.add("open");
    $("#source-drawer").setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
    $("#source-close").focus();
  }

  function closeSource() {
    $("#source-overlay").classList.remove("open");
    $("#source-drawer").classList.remove("open");
    $("#source-drawer").setAttribute("aria-hidden", "true");
    document.body.style.overflow = "";
  }

  function renderSources() {
    const container = $("#source-list");
    if (!container || !Object.keys(SOURCES).length) return;
    SOURCE_ORDER.forEach((id) => {
      const source = SOURCES[id];
      const item = document.createElement("article");
      item.className = "source-item";
      item.dataset.layer = source.layer;
      const h = document.createElement("h3");
      h.textContent = source.book;
      const meta = document.createElement("div");
      meta.className = "source-meta";
      meta.textContent = `${source.author} • ${source.printed_page || source.scan_or_database_page}`;
      const row = document.createElement("div");
      row.className = "meta-row";
      const layer = document.createElement("span");
      layer.className = `pill ${source.layer}`;
      layer.textContent = source.layer === "core" ? "الطبقة الأساسية" : source.layer === "advanced" ? "الطبقة المتقدمة" : "تطبيق";
      const kind = document.createElement("span");
      kind.className = "pill";
      kind.textContent = LABELS.content_kind[source.content_kind];
      const verification = document.createElement("span");
      verification.className = "pill verified";
      verification.textContent = LABELS.verification[source.verification];
      const button = document.createElement("button");
      button.className = "btn small";
      button.type = "button";
      button.textContent = "قراءة المقتطف";
      button.addEventListener("click", () => openSource(id));
      row.append(layer, kind, verification, button);
      item.append(h, meta, row);
      container.appendChild(item);
    });
  }

  function filterSources(filter) {
    $$("[data-source-filter]").forEach((button) => {
      button.classList.toggle("primary", button.dataset.sourceFilter === filter);
    });
    $$("#source-list .source-item").forEach((item) => {
      item.hidden = filter !== "all" && item.dataset.layer !== filter;
    });
  }

  function copyText(text) {
    if (navigator.clipboard) return navigator.clipboard.writeText(text);
    const area = document.createElement("textarea");
    area.value = text;
    document.body.appendChild(area);
    area.select();
    document.execCommand("copy");
    area.remove();
    return Promise.resolve();
  }

  function init() {
    initTheme();
    renderSources();
    loadTasks();
    bindSavedText("#notes-unified", KEYS.notes);
    bindSavedText("#error-log", KEYS.errors);
    loadReviewDates();

    $$("[data-tab]").forEach((button) => button.addEventListener("click", () => activateTab(button.dataset.tab, true)));
    const hash = location.hash.replace("#", "");
    const savedTab = localStorage.getItem(KEYS.tab);
    activateTab($( `[data-tab="${hash}"]`) ? hash : ($( `[data-tab="${savedTab}"]`) ? savedTab : "orientation"));

    $("#theme-toggle")?.addEventListener("click", () => setTheme(document.documentElement.dataset.theme === "dark" ? "light" : "dark"));
    $$(".task-check").forEach((box) => box.addEventListener("change", () => updateProgress(true)));
    $$('[data-reveal]').forEach((button) => button.addEventListener("click", () => {
      const answer = document.getElementById(button.dataset.reveal);
      const willShow = answer.hidden;
      answer.hidden = !willShow;
      button.textContent = willShow ? "إخفاء الجواب" : "أظهر الجواب";
      button.setAttribute("aria-expanded", String(willShow));
    }));
    $$(".flashcard").forEach((card) => card.addEventListener("click", () => {
      const answer = $(".back", card);
      answer.hidden = !answer.hidden;
      card.setAttribute("aria-expanded", String(!answer.hidden));
    }));
    $$('[data-source]').forEach((button) => button.addEventListener("click", () => openSource(button.dataset.source)));
    $$('[data-source-filter]').forEach((button) => button.addEventListener("click", () => filterSources(button.dataset.sourceFilter)));
    $("#source-close")?.addEventListener("click", closeSource);
    $("#source-overlay")?.addEventListener("click", closeSource);
    $("#source-copy")?.addEventListener("click", () => copyText($("#source-text").textContent));
    $("#copy-notes")?.addEventListener("click", () => copyText($("#notes-unified").value));
    $("#print-lesson")?.addEventListener("click", () => window.print());

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") closeSource();
      if (/^[1-7]$/.test(event.key) && !/INPUT|TEXTAREA/.test(document.activeElement.tagName)) {
        const button = $$("[data-tab]")[Number(event.key) - 1];
        if (button) activateTab(button.dataset.tab, true);
      }
    });
  }

  window.addEventListener("DOMContentLoaded", init);
})();
