<p align="center">
  <img src="./assets/header.png" alt="Callesnikov Codex Skills" width="100%">
</p>

<p align="center">
  <a href="#skills"><img src="https://img.shields.io/badge/skills-7-2563eb?style=for-the-badge" alt="7 skills"></a>
  <a href="#principles"><img src="https://img.shields.io/badge/runtime-local--first-16a34a?style=for-the-badge" alt="local first"></a>
  <a href="#skills"><img src="https://img.shields.io/badge/README-GitHub--ready-111827?style=for-the-badge" alt="GitHub ready"></a>
</p>

<h1 align="center">🪄 Callesnikov Codex Skills 💿</h1>

<p align="center">
  Персональное ассорти навыков Codex: разработанные и дополненные рабочие сценарии,
  собранные под Windows, локальные пайплайны и маленькие автоматизации с характером.
</p>

---

## Что Внутри

Это витрина для навыков Codex, которые начинаются с `callesnikov-*`.
Каждый навык сделан под конкретный повторяемый сценарий: разобрать документ,
защитить Obsidian-граф, подготовить транскрибацию, сохранить YouTube-материал,
подобрать аккуратное движение в интерфейсе или закрыть длинную сессию без потери полезной памяти.

Источник истины по поведению каждого навыка остается в его `SKILL.md`.
Этот README нужен как красивая GitHub-страница: быстро понять, что есть в коллекции и зачем оно нужно.

Чтобы установить отдельный навык, попросите Codex изнутри агента скачать или скопировать соответствующую папку
из этого репозитория в локальный каталог `skills`. Важна именно папка целиком: `SKILL.md`, `scripts/`,
`references/`, `tools/` и другие соседние артефакты должны переехать вместе с ней.

<a id="skills"></a>

## Навыки

| Навык | Зачем нужен | Что делает |
|---|---|---|
| [`callesnikov-agent-summarizer`](https://github.com/BratislavaDolgih/callesnikov-codex-skills/tree/main/callesnikov-agent-summarizer) | Финальный аудит диалога | Проверяет сессию перед закрытием, архивированием, удалением или компакцией. Ищет анти-паттерны в промптах, инструментах и управлении контекстом, сохраняет полезную операционную память, предлагает кандидатов в новые навыки и пишет жесткий handoff для следующего чата. |
| [`callesnikov-liteparse-forked`](https://github.com/BratislavaDolgih/callesnikov-codex-skills/tree/main/callesnikov-liteparse-forked) | Локальный парсинг документов | Работает с PDF и другими документами через LiteParse. Извлекает текст, JSON со структурой, bounding boxes, OCR, выбранные страницы, скриншоты страниц и batch-результаты, при этом не трогает исходные файлы. |
| [`callesnikov-obsidian-refactorer`](https://github.com/BratislavaDolgih/callesnikov-codex-skills/tree/main/callesnikov-obsidian-refactorer) | Безопасная работа с Obsidian | Аккуратно обслуживает Obsidian vault и Markdown-базу: аудит заметок, ремонт wiki-links и embeds, сохранение алиасов, headings, frontmatter, безопасные переименования, красивый рефактор заметок и экспорт Markdown/Obsidian в PDF. |
| [`callesnikov-qrify`](https://github.com/BratislavaDolgih/callesnikov-codex-skills/tree/main/callesnikov-qrify) | Генерация QR-кодов | Создает scan-safe QR-коды в PNG или SVG: ссылки, текст, Wi-Fi, vCard, календарные payload, batch-режим, брендовые цвета, градиенты и Windows-safe имена файлов. Держит вывод в текущей рабочей папке, а не внутри навыка. |
| [`callesnikov-speech`](https://github.com/BratislavaDolgih/callesnikov-codex-skills/tree/main/callesnikov-speech) | Локальная транскрибация длинного аудио | Ведет пошаговый пайплайн `ffmpeg` + `whisper.cpp`: preflight, нарезка аудио на чанки, подготовка папок, транскрибация чанков и склейка текстов. Все runtime-активы держит внутри папки навыка. |
| [`callesnikov-transitions`](https://github.com/BratislavaDolgih/callesnikov-codex-skills/tree/main/callesnikov-transitions) | Справочник аккуратных UI-переходов | Помогает выбирать motion для интерфейсов: dropdown, modal, panel reveal, смена чисел, badges, success/error-состояния, icon swap и переходы между страницами. Держит стиль практичным, быстрым и совместимым с `prefers-reduced-motion`. |
| [`callesnikov-youtube-preserver`](https://github.com/BratislavaDolgih/callesnikov-codex-skills/tree/main/callesnikov-youtube-preserver) | Сохранение YouTube-видео и аудио | Скачивает YouTube-материалы через обертку над `yt-dlp`. Поддерживает качество, аудиоформаты, thumbnail, subtitles, metadata JSON, opt-in для playlist, retries и Windows-safe имена файлов. |

<a id="principles"></a>

## Принципы

- **Local-first:** инструменты, runtime, модели, outputs и вспомогательные файлы живут локально и предсказуемо.
- **Без скрытых разрушительных действий:** исходники, vault, PDF и архивы не перезаписываются без явного намерения.
- **Узкий фокус:** каждый навык решает один повторяемый класс задач, а не превращается в расплывчатый режим на все случаи.
- **Сначала доказательства:** перед правками Codex должен посмотреть реальные файлы, структуру, vault или runtime.
- **Память в артефактах:** повторяющиеся сценарии стоит переносить в scripts, references или правила навыка, а не оставлять только в истории чата.

## Рекомендуемая Структура

```text
skills/
  callesnikov-agent-summarizer/
    SKILL.md
    references/
  callesnikov-liteparse-forked/
    SKILL.md
    scripts/
    references/
    tools/
  callesnikov-obsidian-refactorer/
    SKILL.md
    scripts/
    references/
  callesnikov-qrify/
    SKILL.md
    agents/
    scripts/
    tools/
  callesnikov-speech/
    SKILL.md
    scripts/
    runtime/
  callesnikov-transitions/
    SKILL.md
  callesnikov-youtube-preserver/
    SKILL.md
    scripts/
```

## Улучшение Навыков

Когда навык усиливается, лучше обновлять ближайший источник истины:

- `SKILL.md` для поведения, trigger rules и ограничений;
- `scripts/`, если workflow стал повторяемым;
- `references/`, если появились длинные правила, upstream-доки или примеры;
- README, только если меняется публичная карта коллекции.

---

<p align="center">
  Собрано для Codex-среды, где локальные файлы, аккуратные инструменты и повторяемые workflows действительно важны.
</p>
