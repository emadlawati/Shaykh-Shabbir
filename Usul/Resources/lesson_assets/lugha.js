// التقييم الذاتي لتمارين جلسات النحو والبلاغة: بعد كشف الجواب يسجّل الطالب «أصبت» أو «أخطأت»،
// فيُحفظ ذلك محلياً، ويُعرض المجموع، ويمكن إعادة ما أخطأ فيه فقط.
(() => {
  "use strict";

  const lessonId = document.body.dataset.lesson || "lugha";
  const KEY = `shabbir_lugha_${lessonId}_scores`;
  const $ = (selector, root = document) => root.querySelector(selector);
  const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];

  function load() {
    try { return JSON.parse(localStorage.getItem(KEY) || "{}"); } catch (_) { return {}; }
  }

  function save(scores) {
    try { localStorage.setItem(KEY, JSON.stringify(scores)); } catch (_) { /* التخزين غير متاح */ }
  }

  function exercises() {
    return $$(".exercise").filter((item) => $("[data-reveal]", item));
  }

  function idOf(item) {
    return $("[data-reveal]", item).dataset.reveal;
  }

  function paint(item, value) {
    item.classList.toggle("is-right", value === 1);
    item.classList.toggle("is-wrong", value === 0);
    $$(".self-mark .btn", item).forEach((button) => {
      button.setAttribute("aria-pressed", String(Number(button.dataset.value) === value));
    });
  }

  function summary() {
    const scores = load();
    const all = exercises();
    const marked = all.filter((item) => idOf(item) in scores);
    const right = marked.filter((item) => scores[idOf(item)] === 1).length;
    const text = $("#score-text");
    if (text) {
      text.textContent = marked.length
        ? `التطبيقات: ${right} صحيحة من ${marked.length} مُقيَّمة • ${all.length} سؤالاً في الجلسة`
        : `التطبيقات: ${all.length} سؤالاً — اكشف الجواب ثم قيّم نفسك`;
    }
  }

  function init() {
    const scores = load();
    exercises().forEach((item) => {
      const reveal = $("[data-reveal]", item);
      const id = idOf(item);
      const box = document.createElement("span");
      box.className = "self-mark";
      box.hidden = !(id in scores);
      [[1, "✓ أصبت", "good"], [0, "✗ أخطأت", "bad"]].forEach(([value, label, kind]) => {
        const button = document.createElement("button");
        button.type = "button";
        button.className = `btn small ${kind}`;
        button.dataset.value = String(value);
        button.textContent = label;
        button.setAttribute("aria-pressed", "false");
        button.addEventListener("click", () => {
          const current = load();
          current[id] = value;
          save(current);
          paint(item, value);
          summary();
        });
        box.appendChild(button);
      });
      reveal.after(box);
      reveal.addEventListener("click", () => { box.hidden = false; });
      if (id in scores) paint(item, scores[id]);
    });

    $("#only-wrong")?.addEventListener("click", (event) => {
      const on = document.body.classList.toggle("only-wrong");
      event.currentTarget.textContent = on ? "أظهر كل الأسئلة" : "أعد ما أخطأت فيه فقط";
    });
    $("#reset-scores")?.addEventListener("click", () => {
      if (!window.confirm("مسح تقييم هذه الجلسة والبدء من جديد؟")) return;
      save({});
      exercises().forEach((item) => {
        paint(item, -1);
        $(".self-mark", item).hidden = true;
        const answer = document.getElementById(idOf(item));
        if (answer) answer.hidden = true;
        const reveal = $("[data-reveal]", item);
        reveal.textContent = "أظهر الجواب";
        reveal.setAttribute("aria-expanded", "false");
      });
      document.body.classList.remove("only-wrong");
      summary();
    });
    summary();
  }

  window.addEventListener("DOMContentLoaded", init);
})();
