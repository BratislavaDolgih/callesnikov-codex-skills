<p align="center">
  <img src="./assets/header.png" alt="Callesnikov Codex Skills" width="100%">
</p>

<p align="center">
  <a href="./README.md"><img src="https://img.shields.io/badge/English-2563eb?style=for-the-badge" alt="English README"></a>
  <a href="./README_RU.md"><img src="https://img.shields.io/badge/%D0%A0%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B9-111827?style=for-the-badge" alt="Russian README"></a>
</p>

<p align="center">
  <a href="#skills"><img src="https://img.shields.io/badge/skills-16-2563eb?style=for-the-badge" alt="16 skills"></a>
  <a href="#install"><img src="https://img.shields.io/badge/install-agent--first-7c3aed?style=for-the-badge" alt="agent first install"></a>
  <a href="#principles"><img src="https://img.shields.io/badge/runtime-local--first-16a34a?style=for-the-badge" alt="local first"></a>
  <a href="#layout"><img src="https://img.shields.io/badge/platform-Windows--ready-111827?style=for-the-badge" alt="Windows ready"></a>
</p>

<h1 align="center">🪄 Callesnikov Codex Skills 💿</h1>

<p align="center">
  A personal collection of Codex skills for Windows: codebase research, interface design,
  local tools, evidence-backed verification, and workflows that avoid unnecessary cloud dependencies.
</p>

<p align="center">
  <a href="#overview"><img src="https://img.shields.io/badge/Overview-111827?style=for-the-badge" alt="Overview"></a>
  <a href="#install"><img src="https://img.shields.io/badge/Installation-111827?style=for-the-badge" alt="Installation"></a>
  <a href="#skills"><img src="https://img.shields.io/badge/Skills-2563eb?style=for-the-badge" alt="Skills"></a>
  <a href="#principles"><img src="https://img.shields.io/badge/Principles-111827?style=for-the-badge" alt="Principles"></a>
  <a href="#layout"><img src="https://img.shields.io/badge/Structure-111827?style=for-the-badge" alt="Repository structure"></a>
</p>

---

<a id="overview"></a>

## What's Inside

This repository contains 16 personal Codex skills whose names begin with `callesnikov-*`.
The collection covers recurring workflows ranging from codebase understanding, UX review, and parallel execution
to local work with documents, PDFs, Obsidian, QR codes, audio, YouTube, and ASCII media.
Dedicated skills also handle implementation verification, evidence-backed working instincts,
direct prose editing, animated Codex pets, and deliberate end-of-session audits.

Each skill's `SKILL.md` remains the source of truth for its behavior.
This README provides a map of the collection, its boundaries, and the recommended installation workflow.

What makes the collection practical:

- **Codex-first:** skills and adapters target Codex App architecture. Compatibility with other agents is preserved only where an upstream tool requires it.
- **Windows-ready:** commands, paths, and runtime expectations are prepared for a local Windows environment.
- **Agent-first:** workflows are designed to be used by the agent rather than assembled manually from fragments.
- **Local-first:** code, documents, audio, PDFs, QR codes, intermediate files, and runtime artifacts remain local unless a workflow needs an external source.
- **Clear boundaries:** research, design, execution, verification, and specialized tools remain separate responsibilities.

<a id="install"></a>

## Installation

The recommended way to install a skill is to ask Codex to do it from inside the agent.
Install the entire skill directory, not only its `SKILL.md`. A skill may also depend on neighboring
`scripts/`, `references/`, `agents/`, `tools/`, and other bundled assets.

Example request:

```text
Install the callesnikov-qrify skill from
https://github.com/BratislavaDolgih/callesnikov-codex-skills/tree/main/callesnikov-qrify
into my local Codex skills directory.
```

The equivalent manual layout is:

```text
%USERPROFILE%\.codex\skills\
  callesnikov-qrify\
    SKILL.md
    scripts\
    tools\
```

Restart or refresh the Codex session if the agent does not discover the newly installed skill immediately.

<a id="skills"></a>

## Skills

| Skill | Scenario | What it does | Responsibility boundary |
|---|---|---|---|
| [`callesnikov-agent-summarizer`](https://github.com/BratislavaDolgih/callesnikov-codex-skills/tree/main/callesnikov-agent-summarizer) | End-of-session audit | Reviews a conversation before closing, archiving, deleting, or compacting it. Finds prompt, tool, and context anti-patterns, preserves useful operational memory, and prepares a direct handoff for the next task. | It does not replace the normal task response. Use it when a session needs to be closed or compressed deliberately. |
| [`callesnikov-ascii-video-fork`](https://github.com/BratislavaDolgih/callesnikov-codex-skills/tree/main/callesnikov-ascii-video-fork) | ASCII media | Plays video in the terminal, converts images into colored ASCII, and saves ASCII renders as PNG or MP4. Includes both the original project and an extended AI-assisted fork. | It is not a general media converter. Its scope is ASCII representation and the surrounding local workflow. |
| [`callesnikov-continuous-learning-v2`](https://github.com/BratislavaDolgih/callesnikov-codex-skills/tree/main/callesnikov-continuous-learning-v2) | Evidence-backed working instincts | Stores project-scoped instincts with confidence scores, imports and exports them, evolves mature patterns into skills, and controls promotion between project and global scope. | It does not learn from one accidental outcome or promote project-specific preferences without sufficient evidence. |
| [`callesnikov-design-checklist`](https://github.com/BratislavaDolgih/callesnikov-codex-skills/tree/main/callesnikov-design-checklist) | UX/UI quality gate | Applies Checklist Design while planning and reviewing screens, components, and user flows. Exposes missing states, weak copy, dead ends, unclear actions, and incomplete transitions. | Checklists provide questions for engineering judgment, not a universal product specification. |
| [`callesnikov-hatch-pet`](https://github.com/BratislavaDolgih/callesnikov-codex-skills/tree/main/callesnikov-hatch-pet) | Animated Codex pets | Creates, repairs, visually verifies, and packages v2 pets from concepts, brand cues, or references. Produces an 8x11 spritesheet with 9 animation rows and 16 look directions. | It does not accept an incomplete atlas as a finished package. Assembly requires deterministic and visual verification. |
| [`callesnikov-liteparse-forked`](https://github.com/BratislavaDolgih/callesnikov-codex-skills/tree/main/callesnikov-liteparse-forked) | Local document parsing | Processes PDF, DOCX, PPTX, XLSX, images, and OCR through LiteParse/lit. Extracts text, layout-aware JSON, bounding boxes, selected pages, screenshots, and batch results. | Use `callesnikov-pdf-wizard` to modify PDF files. This skill focuses on reading, OCR, and document structure. |
| [`callesnikov-obsidian-refactorer`](https://github.com/BratislavaDolgih/callesnikov-codex-skills/tree/main/callesnikov-obsidian-refactorer) | Safe Obsidian maintenance | Audits Markdown vaults, repairs wiki-links and embeds, preserves aliases, headings, and frontmatter, performs safe renames, refines notes, and exports Obsidian or Markdown content to PDF. | It does not damage the knowledge graph for cosmetic cleanup. It inspects the vault and link structure before making focused changes. |
| [`callesnikov-parallel-execution-optimizer`](https://github.com/BratislavaDolgih/callesnikov-codex-skills/tree/main/callesnikov-parallel-execution-optimizer) | Safe parallel execution | Builds a dependency graph, separates independent reading, research, and verification lanes, and merges their results through explicit checks. | It does not parallelize conflicting writes or dependent steps merely to appear faster. |
| [`callesnikov-pdf-wizard`](https://github.com/BratislavaDolgih/callesnikov-codex-skills/tree/main/callesnikov-pdf-wizard) | Local PDF surgery | Splits, merges, extracts, removes, replaces, inserts, reorders, rotates, and crops pages with `pypdf`. Also handles stamps, watermarks, metadata, encryption, forms, and attachments. | It is not intended for OCR or deep layout analysis. Use `callesnikov-liteparse-forked` for those tasks. |
| [`callesnikov-qrify`](https://github.com/BratislavaDolgih/callesnikov-codex-skills/tree/main/callesnikov-qrify) | Professional QR codes | Generates scan-safe PNG or SVG QR codes for links, text, Wi-Fi, vCard, and calendar payloads. Supports batches, high error correction, branded colors, gradients, quiet zones, and Windows-safe filenames. | It does not provide redirect hosting, analytics, payment dashboards, or live tracking. It generates files. |
| [`callesnikov-speech`](https://github.com/BratislavaDolgih/callesnikov-codex-skills/tree/main/callesnikov-speech) | Local audio transcription | Runs a staged `ffmpeg` and `whisper.cpp` pipeline: preflight, runtime and model bootstrap, long-audio splitting, directory preparation, chunk transcription, and TXT/SRT/JSON merging. | It does not skip pipeline stages. Verification and preparation come before transcription and merging. |
| [`callesnikov-stop-slop`](https://github.com/BratislavaDolgih/callesnikov-codex-skills/tree/main/callesnikov-stop-slop) | Direct prose editing | Removes predictable AI phrasing, filler, corporate jargon, passive voice, manufactured emphasis, and formulaic structure from prose and documentation. | It does not change facts or technical meaning to make writing sound more natural. |
| [`callesnikov-transitions`](https://github.com/BratislavaDolgih/callesnikov-codex-skills/tree/main/callesnikov-transitions) | UI motion reference | Helps select restrained motion for dropdowns, modals, panel reveals, page changes, badges, number updates, status feedback, avatar stacks, and icon swaps. Accounts for timing, utility, and `prefers-reduced-motion`. | It is a motion reference, not a separate animation framework. It helps select and describe transitions. |
| [`callesnikov-understand-anything-forked`](https://github.com/BratislavaDolgih/callesnikov-codex-skills/tree/main/callesnikov-understand-anything-forked) | Codebase and knowledge understanding | Builds knowledge graphs, explains files and modules, prepares onboarding, analyzes diffs and domain models, launches a dashboard, and adds cited external research when needed. | It starts with local code and graph evidence. External research is used only when local evidence is insufficient. |
| [`callesnikov-verification-loop`](https://github.com/BratislavaDolgih/callesnikov-codex-skills/tree/main/callesnikov-verification-loop) | Evidence-backed change verification | Derives quality gates from the repository, records a baseline, runs relevant build, test, lint, and smoke checks, and separates verified behavior from unverified claims. | It does not declare work ready because one test passed or replace evidence with a generic command list. |
| [`callesnikov-youtube-preserver`](https://github.com/BratislavaDolgih/callesnikov-codex-skills/tree/main/callesnikov-youtube-preserver) | YouTube video and audio preservation | Downloads YouTube media through a robust `yt-dlp` wrapper: MP4/WebM/MKV video, MP3/M4A/OPUS/WAV/FLAC audio, thumbnails, subtitles, metadata JSON, single-video defaults, and playlist opt-in. | It does not enable playlists without explicit intent or become a media manager. Its job is reliable preservation. |

## Quick Choice

| When you need to... | Use |
|---|---|
| Understand architecture, a diff, a domain, or a knowledge base | `callesnikov-understand-anything-forked` |
| Review a screen, component, or user flow with a UX/UI checklist | `callesnikov-design-checklist` |
| Prove that an implementation actually works | `callesnikov-verification-loop` |
| Accelerate a large task with independent parallel lanes | `callesnikov-parallel-execution-optimizer` |
| Preserve evidence-backed Codex working habits | `callesnikov-continuous-learning-v2` |
| Remove formulaic AI writing and corporate filler | `callesnikov-stop-slop` |
| Create or repair an animated v2 Codex pet | `callesnikov-hatch-pet` |
| Play or save images and video as ASCII media | `callesnikov-ascii-video-fork` |
| Extract text, tables, layout, or OCR from a document | `callesnikov-liteparse-forked` |
| Split, merge, rotate, or encrypt a PDF | `callesnikov-pdf-wizard` |
| Refine an Obsidian note or vault safely | `callesnikov-obsidian-refactorer` |
| Generate a QR code for a link, Wi-Fi, vCard, or payload batch | `callesnikov-qrify` |
| Prepare long audio for local transcription | `callesnikov-speech` |
| Preserve YouTube video, audio, subtitles, and metadata | `callesnikov-youtube-preserver` |
| Choose restrained motion for an interface | `callesnikov-transitions` |
| Close a long task without losing useful conclusions | `callesnikov-agent-summarizer` |

<a id="principles"></a>

## Principles

- **Evidence first:** inspect the actual files, repository, vault, runtime, or history before making changes.
- **No hidden destructive actions:** do not overwrite source files, notes, PDFs, or archives without explicit intent.
- **Narrow responsibility:** each skill solves one class of problems and hands adjacent work to the appropriate skill.
- **Repeatability over heroics:** recurring workflows belong in `scripts/`, `references/`, or explicit skill rules.
- **Inspectable local artifacts:** outputs, intermediate files, and runtime dependencies should remain understandable, verifiable, and portable.

<a id="layout"></a>

## Repository Structure

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

Temporary directories such as `downloads/`, `outputs/`, `tmp/`, and local runtime dependencies may appear inside a skill while it runs.
Document them in the relevant `SKILL.md`. Add them to this README only when they matter for installation or public understanding.

## Maintenance

When a skill changes, update its closest source of truth:

- `SKILL.md` - trigger rules, behavior, limitations, safety rules, and expected workflow;
- `scripts/` - repeatable mechanics that should be implemented in code rather than prompts;
- `references/` - detailed rules, upstream documentation, examples, edge cases, and quality notes;
- `agents/` - agent profiles and supporting configuration used by the skill;
- README files - the public map of the collection, including scope, installation, and responsibility boundaries.

---

<p align="center">
  Built for a Codex environment where local files, careful tools, and repeatable workflows matter.
</p>
