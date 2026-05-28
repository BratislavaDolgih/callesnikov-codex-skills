# Obsidian Properties Rules

Read this reference before adding or updating agent-owned Obsidian properties in a note.

When Codex edits the content, structure, links, embeds, or formatting of a Markdown note, add or update the Codex-owned properties block. Treat it as a small audit clamp (`клемма`) that marks the note as touched and explains what changed. Do not skip this metadata merely because the edit feels small.

Use this exact schema:

```yaml
agent: Codex
agent_action: "Аккуратное редактирование"
agent_summary: "Кратко что изменено"
modified_at: "YYYY-MM-DD"
```

Field rules:

- `agent` identifies the agent or model that created or updated the properties block.
- `agent_action` is a short Russian title for the agent action.
- `agent_summary` is a concise Russian summary of the concrete note changes: what was added, removed, edited, repaired, or refactored.
- `modified_at` is the calendar date when the change happened, formatted as `YYYY-MM-DD`.

Preservation rules:

- Preserve existing user-authored Obsidian properties whenever possible.
- Do not overwrite user metadata to make the block look cleaner.
- If existing agent-owned fields were previously written by Codex, update those fields to describe the current change instead of adding duplicates.
- If the existing properties block contains only user metadata, append the Codex-owned fields after the preserved user fields when the note itself was edited.
- If a note has no properties block and Codex edits the note, create valid YAML frontmatter at the top of the note.
- If the task is read-only audit, planning, export-only, or PDF generation that does not modify the source `.md`, do not add or update note properties.
- If the user explicitly forbids metadata changes for a particular edit, obey the user and mention that the audit clamp was intentionally not written.
- Keep the frontmatter parseable by Obsidian.
- Do not replace `modified_at` with `agent_modified` or other date-field variants.

Good default values:

- `agent_action`: short action label, for example `"Крайне привлекательный рефактор"`, `"Ремонт wiki-ссылок"`, `"Аккуратное редактирование"`, `"Обновление структуры заметки"`.
- `agent_summary`: one concise sentence in Russian describing concrete changes, not generic praise.
- `modified_at`: current local date in `YYYY-MM-DD`.
