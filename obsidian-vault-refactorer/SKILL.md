---
name: obsidian-vault-refactorer
description: Use this skill for professional, conservative work with a local Obsidian vault or knowledge-base repository: auditing Markdown notes, checking UTF-8 encoding, repairing wiki-links and embeds, preserving aliases/headings/frontmatter, planning safe renames or numbering refactors, validating changes, and reporting exact replacements without damaging the existing note graph.
---

# Obsidian Vault Refactorer

Use this skill when working in a local Obsidian vault where correctness matters more than speed.

Default to careful, reversible work: inspect first, edit narrowly, validate the same scope, and report exact changes.

## First Move

1. Identify the vault root and the exact requested scope: whole vault, folder, note set, or one note.
2. Inspect the repository state before editing:
   - `git status --short` when the vault is a Git repository
   - file encoding and line-ending risks
   - existing Obsidian structure, especially `.obsidian/`, attachments, canvases, PDFs, and hub notes
3. Run an audit before broad edits:

```powershell
python "C:\Users\User333\.codex\skills\obsidian-vault-refactorer\scripts\obsidian_audit.py" "C:\path\to\vault" --scope "Folder Or Note"
```

Use the audit as evidence, not as permission to rewrite everything.

## Operating Rules

- Preserve vault structure unless the user explicitly asks for moves, renames, merges, or deletions.
- Prefer folder-by-folder repair over whole-vault rewrites.
- Scan outgoing links by default. Inspect incoming links only when asked or when planning a rename/move.
- Treat `[[wiki-links]]` and `![[embeds]]` as first-class graph edges.
- Preserve `[[target|alias]]`, `[[target#heading]]`, and `[[target#heading|alias]]`.
- Leave unresolved or ambiguous links unchanged unless there is one confident target.
- Never delete unresolved links just because they are broken.
- Avoid editing text inside fenced code blocks unless the user asks to update examples.
- Keep Markdown and YAML frontmatter readable for Obsidian and humans.
- Preserve user-authored frontmatter. Add agent fields only when creating a note or when the user approved metadata updates.

## Editing Workflow

1. Build an index of existing note and attachment basenames across the vault.
2. Compare link targets against existing basenames and path-like targets.
3. Apply only confident repairs:
   - exact basename match wins
   - renumbered title match can be used when it resolves to one candidate
   - extension cleanup for embeds can be used when the basename is unique
4. For planned renames or numbering refactors, make a dry-run replacement list before editing.
5. Edit with the smallest diff that solves the request.
6. Re-run audit on the same scope.
7. Report:
   - checked scope
   - files changed
   - exact `before -> after` replacements
   - unresolved or intentionally untouched items

## Encoding And File Hygiene

Use UTF-8 without BOM for Markdown whenever possible. Before editing, check for:

- decode failures
- UTF-8 BOM
- mixed CRLF/LF line endings
- accidental binary files in note scopes
- malformed YAML frontmatter boundaries

Do not normalize line endings or encoding across many files unless the user asked for that maintenance pass.

## Frontmatter

When adding or updating agent metadata, keep it concise and Russian-readable:

```yaml
agent: Codex
agent_action: "Аккуратное редактирование"
agent_scope: "Папка или заметка"
agent_summary: "Кратко что изменено"
agent_modified: "YYYY-MM-DD"
```

Preserve existing properties and ordering where practical. Do not overwrite user-authored fields without permission.

## Deeper Guidance

Read `references/obsidian-workflow.md` when the task involves:

- renaming or renumbering notes
- repairing many links or embeds
- changing frontmatter in existing notes
- checking hub notes, indexes, roadmaps, maps of content, or dashboards
- making a maintenance report for the vault

## Useful Commands

Audit a whole vault:

```powershell
python "C:\Users\User333\.codex\skills\obsidian-vault-refactorer\scripts\obsidian_audit.py" "C:\path\to\vault"
```

Audit a folder or note:

```powershell
python "C:\Users\User333\.codex\skills\obsidian-vault-refactorer\scripts\obsidian_audit.py" "C:\path\to\vault" --scope "Knowledge/Folder"
```

Write a Markdown report:

```powershell
python "C:\Users\User333\.codex\skills\obsidian-vault-refactorer\scripts\obsidian_audit.py" "C:\path\to\vault" --format markdown --output audit.md
```
