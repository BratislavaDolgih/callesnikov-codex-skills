<p align="center">
  <img src="./assets/header.png" alt="Callesnikov Codex Skills" width="100%">
</p>

<p align="center">
  <a href="#skills"><img src="https://img.shields.io/badge/skills-16-2563eb?style=for-the-badge" alt="16 skills"></a>
  <a href="#install"><img src="https://img.shields.io/badge/install-agent--first-7c3aed?style=for-the-badge" alt="agent first install"></a>
  <a href="#principles"><img src="https://img.shields.io/badge/runtime-local--first-16a34a?style=for-the-badge" alt="local first"></a>
  <a href="#layout"><img src="https://img.shields.io/badge/platform-Windows--ready-111827?style=for-the-badge" alt="Windows ready"></a>
</p>

<h1 align="center">🪄 Callesnikov Codex Skills 💿</h1>

<p align="center">
  Персональная коллекция Codex-навыков для Windows: исследование кодовых баз,
  проектирование интерфейсов, локальные инструменты, проверка результата и работа без лишней облачной зависимости.
</p>

<p align="center">
  <a href="#overview"><img src="https://img.shields.io/badge/%D0%9E%D0%B1%D0%B7%D0%BE%D1%80-111827?style=for-the-badge" alt="Обзор"></a>
  <a href="#install"><img src="https://img.shields.io/badge/%D0%A3%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0-111827?style=for-the-badge" alt="Установка"></a>
  <a href="#skills"><img src="https://img.shields.io/badge/%D0%9D%D0%B0%D0%B2%D1%8B%D0%BA%D0%B8-2563eb?style=for-the-badge" alt="Навыки"></a>
  <a href="#principles"><img src="https://img.shields.io/badge/%D0%9F%D1%80%D0%B8%D0%BD%D1%86%D0%B8%D0%BF%D1%8B-111827?style=for-the-badge" alt="Принципы"></a>
  <a href="#layout"><img src="https://img.shields.io/badge/%D0%A1%D1%82%D1%80%D1%83%D0%BA%D1%82%D1%83%D1%80%D0%B0-111827?style=for-the-badge" alt="Структура"></a>
</p>

---

<a id="overview"></a>

## Что Внутри

Это витрина 16 персональных навыков Codex, которые начинаются с `callesnikov-*`.
Коллекция закрывает повторяемые сценарии от понимания кодовой базы, UX-проверки и параллельного выполнения
до локальной работы с документами, PDF, Obsidian, QR, аудио, YouTube и ASCII-медиа.
Отдельные навыки отвечают за проверку реализации, накопление подтверждённых рабочих привычек,
чистую редактуру текста, создание анимированных Codex-питомцев и осмысленное завершение длинных сессий.

Источник истины по поведению каждого навыка остается в его `SKILL.md`.
README отвечает за другое: быстро показать состав коллекции, границы инструментов и правильный способ установки.

Что делает коллекцию практичной:

- **Codex-first:** навыки и адаптеры рассчитаны на архитектуру Codex App; совместимость с другими агентами сохраняется только там, где она нужна исходному инструменту.
- **Windows-ready:** команды, пути и runtime-ожидания проверяются для локальной Windows-среды.
- **Agent-first:** навыки рассчитаны на работу изнутри агента, а не на ручную возню с кусками инструкций.
- **Local-first:** код, документы, аудио, PDF, QR, промежуточные файлы и runtime-артефакты остаются локальными, пока сценарию не нужен внешний источник.
- **С понятными границами:** исследование, проектирование, исполнение, проверка и специализированные инструменты не смешаны в один режим.

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
| [`callesnikov-ascii-video-fork`](https://github.com/BratislavaDolgih/callesnikov-codex-skills/tree/main/callesnikov-ascii-video-fork) | ASCII-медиа | Проигрывает видео в терминале, превращает изображения в цветной ASCII и сохраняет ASCII-рендеры в PNG/MP4. Включает оригинальный проект и расширенный AI-assisted fork. | Не является универсальным медиаконвертером; отвечает за ASCII-представление и сопутствующий локальный workflow. |
| [`callesnikov-continuous-learning-v2`](https://github.com/BratislavaDolgih/callesnikov-codex-skills/tree/main/callesnikov-continuous-learning-v2) | Подтверждённые рабочие привычки | Хранит project-scoped instincts с confidence score, импортирует и экспортирует их, объединяет зрелые паттерны в навыки и контролирует перенос между проектами. | Не учится по одному случайному эпизоду и не переносит проектные предпочтения глобально без достаточных доказательств. |
| [`callesnikov-design-checklist`](https://github.com/BratislavaDolgih/callesnikov-codex-skills/tree/main/callesnikov-design-checklist) | UX/UI quality gate | Использует Checklist Design при проектировании и ревью экранов, компонентов и пользовательских потоков. Выявляет пропущенные состояния, слабый copy, тупики, неясные действия и незавершённые переходы. | Чек-листы служат вопросами для инженерного решения, а не универсальной спецификацией продукта. |
| [`callesnikov-hatch-pet`](https://github.com/BratislavaDolgih/callesnikov-codex-skills/tree/main/callesnikov-hatch-pet) | Анимированные питомцы Codex | Создаёт, чинит, визуально проверяет и упаковывает v2-питомцев из концепта, бренда или референсов. Собирает 8x11 spritesheet с 9 рядами анимаций и 16 направлениями взгляда. | Не принимает неполный atlas за готовый пакет; сборка проходит детерминированную и визуальную проверку. |
| [`callesnikov-liteparse-forked`](https://github.com/BratislavaDolgih/callesnikov-codex-skills/tree/main/callesnikov-liteparse-forked) | Локальный парсинг документов | Работает с PDF, DOCX, PPTX, XLSX, изображениями и OCR через LiteParse/lit. Извлекает текст, layout-aware JSON, bounding boxes, выбранные страницы, скриншоты и batch-результаты. | Для изменения самих PDF лучше использовать `callesnikov-pdf-wizard`; здесь фокус на чтении, OCR и структуре. |
| [`callesnikov-obsidian-refactorer`](https://github.com/BratislavaDolgih/callesnikov-codex-skills/tree/main/callesnikov-obsidian-refactorer) | Безопасная работа с Obsidian | Аудит Markdown-базы, ремонт wiki-links и embeds, сохранение aliases, headings и frontmatter, безопасные переименования, красивый рефактор заметок и экспорт Obsidian/Markdown в PDF. | Не ломает граф ради косметики; сначала анализирует vault и ссылки, потом предлагает или делает точечные правки. |
| [`callesnikov-parallel-execution-optimizer`](https://github.com/BratislavaDolgih/callesnikov-codex-skills/tree/main/callesnikov-parallel-execution-optimizer) | Безопасный параллелизм | Строит граф зависимостей, разделяет независимые чтения, исследования и проверки на параллельные линии, а результаты сводит через явную верификацию. | Не распараллеливает конфликтующие записи и зависимые шаги только ради видимой скорости. |
| [`callesnikov-pdf-wizard`](https://github.com/BratislavaDolgih/callesnikov-codex-skills/tree/main/callesnikov-pdf-wizard) | Локальная хирургия PDF | Разрезает, склеивает, извлекает, удаляет, заменяет, вставляет, переупорядочивает, поворачивает и кадрирует страницы через `pypdf`. Также умеет stamp/watermark, metadata, encrypt/decrypt, forms и attachments. | Не предназначен для OCR, глубокого парсинга и понимания layout; для этого есть `callesnikov-liteparse-forked`. |
| [`callesnikov-qrify`](https://github.com/BratislavaDolgih/callesnikov-codex-skills/tree/main/callesnikov-qrify) | Профессиональные QR-коды | Генерирует scan-safe PNG/SVG QR для ссылок, текста, Wi-Fi, vCard и calendar payload. Поддерживает batch, high error correction, брендовые цвета, градиенты, quiet zone и Windows-safe имена файлов. | Не управляет redirect-хостингом, аналитикой, платежными кабинетами и live-tracking; это генератор файлов. |
| [`callesnikov-speech`](https://github.com/BratislavaDolgih/callesnikov-codex-skills/tree/main/callesnikov-speech) | Локальная транскрибация аудио | Ведет пошаговый pipeline `ffmpeg` + `whisper.cpp`: preflight, bootstrap runtime/model, нарезка длинного аудио, подготовка папок, транскрибация чанков и склейка TXT/SRT/JSON. | Не перескакивает через стадии: сначала проверка и подготовка, затем транскрибация и merge. |
| [`callesnikov-stop-slop`](https://github.com/BratislavaDolgih/callesnikov-codex-skills/tree/main/callesnikov-stop-slop) | Чистая редактура текста | Убирает предсказуемые AI-формулировки, filler, канцелярит, пассивный залог, искусственное усиление и шаблонную структуру из прозы и документации. | Не меняет факты и технический смысл ради более живого звучания. |
| [`callesnikov-transitions`](https://github.com/BratislavaDolgih/callesnikov-codex-skills/tree/main/callesnikov-transitions) | Справочник UI-motion | Помогает выбрать tasteful motion для dropdown, modal, panel reveal, page changes, badges, number updates, success/error feedback, avatar stacks и icon swap. Учитывает скорость, практичность и `prefers-reduced-motion`. | Это motion-reference, а не отдельный animation framework; он помогает выбрать и описать переходы. |
| [`callesnikov-understand-anything-forked`](https://github.com/BratislavaDolgih/callesnikov-codex-skills/tree/main/callesnikov-understand-anything-forked) | Понимание кодовых баз и знаний | Строит knowledge graph, объясняет файлы и модули, готовит onboarding, анализирует diff и доменную модель, запускает dashboard и при необходимости добавляет внешнее исследование с источниками. | Сначала опирается на локальный код и граф; внешний research включается, когда локальных доказательств недостаточно. |
| [`callesnikov-verification-loop`](https://github.com/BratislavaDolgih/callesnikov-codex-skills/tree/main/callesnikov-verification-loop) | Доказательная проверка изменений | Выводит quality gates из самого репозитория, фиксирует baseline, запускает релевантные build/test/lint/smoke-проверки и отделяет подтверждённое от непроверенного. | Не объявляет работу готовой по одному зелёному тесту и не подменяет доказательства общим списком команд. |
| [`callesnikov-youtube-preserver`](https://github.com/BratislavaDolgih/callesnikov-codex-skills/tree/main/callesnikov-youtube-preserver) | Сохранение YouTube-видео и аудио | Скачивает YouTube-материалы через robust-обертку над `yt-dlp`: MP4/WebM/MKV, MP3/M4A/OPUS/WAV/FLAC, thumbnails, subtitles, metadata JSON, single-video default и playlist opt-in. | Не включает playlist без явного согласия и не превращается в медиаменеджер; цель — надежно сохранить нужный материал. |

## Быстрый Выбор

| Если нужно... | Берите |
|---|---|
| Разобраться в архитектуре, diff, домене или knowledge base | `callesnikov-understand-anything-forked` |
| Проверить экран, компонент или пользовательский поток по UX/UI-чек-листу | `callesnikov-design-checklist` |
| Доказать, что реализация действительно работает | `callesnikov-verification-loop` |
| Ускорить большую задачу независимыми параллельными линиями | `callesnikov-parallel-execution-optimizer` |
| Сохранить подтверждённые проектные привычки Codex | `callesnikov-continuous-learning-v2` |
| Убрать из текста шаблонный AI-стиль и канцелярит | `callesnikov-stop-slop` |
| Создать или починить анимированного v2-питомца Codex | `callesnikov-hatch-pet` |
| Проиграть или сохранить фото и видео в ASCII-виде | `callesnikov-ascii-video-fork` |
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
  callesnikov-ascii-video-fork/
    SKILL.md
    agents/
    fork/
    repository/
  callesnikov-continuous-learning-v2/
    SKILL.md
    agents/
    hooks/
    scripts/
  callesnikov-design-checklist/
    SKILL.md
    agents/
    references/
  callesnikov-hatch-pet/
    SKILL.md
    agents/
    references/
    scripts/
    tests/
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
  callesnikov-parallel-execution-optimizer/
    SKILL.md
    agents/
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
  callesnikov-stop-slop/
    SKILL.md
    agents/
    references/
  callesnikov-transitions/
    SKILL.md
    agents/
  callesnikov-understand-anything-forked/
    SKILL.md
    agents/
    scripts/
    understand-anything-plugin/
  callesnikov-verification-loop/
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
