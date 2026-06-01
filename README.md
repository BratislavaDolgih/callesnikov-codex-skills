<p align="center">
  <img src="./assets/header.png" alt="Callesnikov Codex Skills" width="100%">
</p>

<p align="center">
  <a href="#skills"><img src="https://img.shields.io/badge/skills-8-2563eb?style=for-the-badge" alt="8 skills"></a>
  <a href="#install"><img src="https://img.shields.io/badge/install-agent--first-7c3aed?style=for-the-badge" alt="agent first install"></a>
  <a href="#principles"><img src="https://img.shields.io/badge/runtime-local--first-16a34a?style=for-the-badge" alt="local first"></a>
  <a href="#layout"><img src="https://img.shields.io/badge/platform-Windows--ready-111827?style=for-the-badge" alt="Windows ready"></a>
</p>

<h1 align="center">🪄 Callesnikov Codex Skills 💿</h1>

<p align="center">
  Персональное ассорти Codex-навыков для Windows: локальные пайплайны,
  аккуратная работа с файлами, документами, медиа и контекстом, плюс немного инженерной магии без облачного фокуса.
</p>

<p align="center">
  <a href="#overview">Обзор</a> ·
  <a href="#install">Установка</a> ·
  <a href="#skills">Навыки</a> ·
  <a href="#principles">Принципы</a> ·
  <a href="#layout">Структура</a>
</p>

---

<a id="overview"></a>

## Что Внутри

Это витрина персональных навыков Codex, которые начинаются с `callesnikov-*`.
Каждый навык закрывает конкретный повторяемый сценарий: распарсить документ, бережно обслужить Obsidian-граф,
собрать или разрезать PDF, сгенерировать QR-код, подготовить длинное аудио к транскрибации,
сохранить YouTube-материал, подобрать интерфейсное движение или завершить длинную сессию без потери полезной памяти.

Источник истины по поведению каждого навыка остается в его `SKILL.md`.
README отвечает за другое: быстро показать состав коллекции, границы инструментов и правильный способ установки.

Что делает коллекцию практичной:

- **Windows-first:** команды, пути и runtime-ожидания адаптированы под локальную Windows-среду Codex.
- **Agent-first:** навыки рассчитаны на работу изнутри агента, а не на ручную возню с кусками инструкций.
- **Local-first:** документы, аудио, PDF, QR, промежуточные файлы и runtime-артефакты живут локально.
- **С понятными границами:** парсинг документов, PDF-хирургия, Obsidian-рефакторинг и скачивание медиа не смешаны в один мутный режим.

<a id="install"></a>

## Установка

Лучший способ установить отдельный навык — попросить Codex сделать это изнутри агента.
Скачивать нужно не один `SKILL.md`, а всю папку навыка целиком: вместе со `scripts/`, `references/`, `agents/`,
`tools/` и другими соседними артефактами, если они есть.

Пример запроса:

```text
Установи навык callesnikov-qrify из
https://github.com/BratislavaDolgih/callesnikov-codex-skills/tree/main/callesnikov-qrify
в мой локальный каталог навыков Codex.
```

Ручной вариант такой же по смыслу:

```text
%USERPROFILE%\.codex\skills\
  callesnikov-qrify\
    SKILL.md
    scripts\
    tools\
```

После установки перезапустите или обновите Codex-сессию, если агент не подхватил новый навык сразу.

<a id="skills"></a>

## Навыки

| Навык | Сценарий | Что делает | Граница ответственности |
|---|---|---|---|
| [`callesnikov-agent-summarizer`](https://github.com/BratislavaDolgih/callesnikov-codex-skills/tree/main/callesnikov-agent-summarizer) | Финальный аудит сессии | Проверяет диалог перед закрытием, архивированием, удалением или компакцией. Ищет анти-паттерны в промптах, инструментах и контексте, сохраняет полезную операционную память и пишет жесткий handoff для следующего чата. | Не заменяет обычный ответ по задаче; включается, когда нужно осмысленно завершить или сжать сессию. |
| [`callesnikov-liteparse-forked`](https://github.com/BratislavaDolgih/callesnikov-codex-skills/tree/main/callesnikov-liteparse-forked) | Локальный парсинг документов | Работает с PDF, DOCX, PPTX, XLSX, изображениями и OCR через LiteParse/lit. Извлекает текст, layout-aware JSON, bounding boxes, выбранные страницы, скриншоты и batch-результаты. | Для изменения самих PDF лучше использовать `callesnikov-pdf-wizard`; здесь фокус на чтении, OCR и структуре. |
| [`callesnikov-obsidian-refactorer`](https://github.com/BratislavaDolgih/callesnikov-codex-skills/tree/main/callesnikov-obsidian-refactorer) | Безопасная работа с Obsidian | Аудит Markdown-базы, ремонт wiki-links и embeds, сохранение aliases, headings и frontmatter, безопасные переименования, красивый рефактор заметок и экспорт Obsidian/Markdown в PDF. | Не ломает граф ради косметики; сначала анализирует vault и ссылки, потом предлагает или делает точечные правки. |
| [`callesnikov-pdf-wizard`](https://github.com/BratislavaDolgih/callesnikov-codex-skills/tree/main/callesnikov-pdf-wizard) | Локальная хирургия PDF | Разрезает, склеивает, извлекает, удаляет, заменяет, вставляет, переупорядочивает, поворачивает и кадрирует страницы через `pypdf`. Также умеет stamp/watermark, metadata, encrypt/decrypt, forms и attachments. | Не предназначен для OCR, глубокого парсинга и понимания layout; для этого есть `callesnikov-liteparse-forked`. |
| [`callesnikov-qrify`](https://github.com/BratislavaDolgih/callesnikov-codex-skills/tree/main/callesnikov-qrify) | Профессиональные QR-коды | Генерирует scan-safe PNG/SVG QR для ссылок, текста, Wi-Fi, vCard и calendar payload. Поддерживает batch, high error correction, брендовые цвета, градиенты, quiet zone и Windows-safe имена файлов. | Не управляет redirect-хостингом, аналитикой, платежными кабинетами и live-tracking; это генератор файлов. |
| [`callesnikov-speech`](https://github.com/BratislavaDolgih/callesnikov-codex-skills/tree/main/callesnikov-speech) | Локальная транскрибация аудио | Ведет пошаговый pipeline `ffmpeg` + `whisper.cpp`: preflight, bootstrap runtime/model, нарезка длинного аудио, подготовка папок, транскрибация чанков и склейка TXT/SRT/JSON. | Не перескакивает через стадии: сначала проверка и подготовка, затем транскрибация и merge. |
| [`callesnikov-transitions`](https://github.com/BratislavaDolgih/callesnikov-codex-skills/tree/main/callesnikov-transitions) | Справочник UI-motion | Помогает выбрать tasteful motion для dropdown, modal, panel reveal, page changes, badges, number updates, success/error feedback, avatar stacks и icon swap. Учитывает скорость, практичность и `prefers-reduced-motion`. | Это motion-reference, а не отдельный animation framework; он помогает выбрать и описать переходы. |
| [`callesnikov-youtube-preserver`](https://github.com/BratislavaDolgih/callesnikov-codex-skills/tree/main/callesnikov-youtube-preserver) | Сохранение YouTube-видео и аудио | Скачивает YouTube-материалы через robust-обертку над `yt-dlp`: MP4/WebM/MKV, MP3/M4A/OPUS/WAV/FLAC, thumbnails, subtitles, metadata JSON, single-video default и playlist opt-in. | Не включает playlist без явного согласия и не превращается в медиаменеджер; цель — надежно сохранить нужный материал. |

## Быстрый Выбор

| Если нужно... | Берите |
|---|---|
| Достать текст, таблицы, layout или OCR из документа | `callesnikov-liteparse-forked` |
| Разрезать, склеить, повернуть или зашифровать PDF | `callesnikov-pdf-wizard` |
| Привести Obsidian-заметку или vault в порядок | `callesnikov-obsidian-refactorer` |
| Сделать QR для ссылки, Wi-Fi, vCard или пачки payload | `callesnikov-qrify` |
| Подготовить длинное аудио к локальной расшифровке | `callesnikov-speech` |
| Сохранить YouTube-видео, аудио, субтитры и метаданные | `callesnikov-youtube-preserver` |
| Подобрать аккуратную анимацию для интерфейса | `callesnikov-transitions` |
| Закрыть длинный чат без потери выводов и уроков | `callesnikov-agent-summarizer` |

<a id="principles"></a>

## Принципы

- **Сначала доказательства:** перед правками агент смотрит реальные файлы, структуру, vault, runtime или историю.
- **Никаких скрытых разрушительных действий:** исходники, заметки, PDF и архивы не перезаписываются без явного намерения.
- **Узкий фокус:** каждый навык решает один класс задач и честно отдает соседние сценарии другому навыку.
- **Повторяемость вместо героизма:** если workflow повторяется, он переезжает в `scripts/`, `references/` или правила навыка.
- **Локальные артефакты важнее магии:** outputs, промежуточные файлы и runtime-зависимости должны быть понятны, проверяемы и переносимы.

<a id="layout"></a>

## Структура Репозитория

```text
skills/
  assets/
    header.png
  callesnikov-agent-summarizer/
    SKILL.md
    agents/
    references/
  callesnikov-liteparse-forked/
    SKILL.md
    agents/
    references/
    scripts/
    tools/
  callesnikov-obsidian-refactorer/
    SKILL.md
    agents/
    references/
    scripts/
  callesnikov-pdf-wizard/
    SKILL.md
    agents/
    scripts/
  callesnikov-qrify/
    SKILL.md
    agents/
    scripts/
    tools/
  callesnikov-speech/
    SKILL.md
    agents/
    scripts/
  callesnikov-transitions/
    SKILL.md
    agents/
  callesnikov-youtube-preserver/
    SKILL.md
    agents/
    scripts/
```

Временные каталоги вроде `downloads/`, `outputs/`, `tmp/` или локальные runtime-зависимости могут появляться внутри конкретных навыков во время работы.
Их стоит описывать в `SKILL.md`, а в README выносить только тогда, когда это важно для установки или публичного понимания коллекции.

## Сопровождение

Когда навык усиливается, обновляйте ближайший источник истины:

- `SKILL.md` — trigger rules, поведение, ограничения, safety-правила и ожидаемый workflow;
- `scripts/` — повторяемая механика, которую лучше выполнять кодом, а не промптом;
- `references/` — длинные правила, upstream-доки, примеры, edge cases и заметки по качеству;
- `agents/` — агентские профили или вспомогательная конфигурация, если навык ее использует;
- README — публичная карта коллекции: состав, назначение, установка и границы.

---

<p align="center">
  Собрано для Codex-среды, где локальные файлы, аккуратные инструменты и повторяемые workflows действительно важны.
</p>
