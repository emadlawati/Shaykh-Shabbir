# نص القرآن الكريم المعتمد في ملفات النحو والبلاغة

`quran_uthmani.json` هو نص **Tanzil Uthmani** كما هو، دون أي تغيير في الكلمات، منقول من مشروع «Quran Memorization» المحلي، وهو بدوره مثبَّت على `nuqayah/quran-text` (commit `37ba07d765ec3487a9b5852aded3e3b3ad2e322e`، SHA-256 `0a5926f8e27b8961e619f2d473db9c5466186ab2b56207c964a043336b174a7d`).

- شروط الاستعمال: [Tanzil terms of use](https://tanzil.net/docs/terms-of-use) — التوزيع حرفياً مع الإسناد، ودون تغيير النص.
- البسملة: الآية 1:1 مرقمة في الفاتحة، وفي بقية السور تُفصل البسملة عن الآية الأولى.
- البنية: `verses["سورة:آية"]` = نص الآية بالرسم العثماني.

كل آية في ملفات الجلسات تُكتب داخل `<span class="ayah" data-ref="س:آ">` وتُفحص حرفياً على هذا الملف بـ`python scripts/validate_sessions.py`. ويُستخرج النص بـ`python scripts/quran.py get 36:14`.
