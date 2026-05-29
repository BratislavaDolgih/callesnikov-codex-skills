# Obsidian Workflow Reference

Use this reference for broad or risky Obsidian vault work.

## Scope Discipline

Start from the narrowest useful scope. Prefer:

1. one note
2. one folder
3. one folder plus its attachment folder
4. whole vault only when the user asks for vault-wide maintenance

Exclude `.obsidian/`, `.git/`, plugin caches, generated exports, and backups unless the user explicitly asks to inspect them.

## Link Matching

Represent each link as:

- source file
- original token
- embed flag
- target path text
- heading fragment
- alias text
- code-block status

Resolve in this order:

1. exact Obsidian target path
2. exact basename
3. basename without extension
4. title after removing numeric prefixes such as `01.`, `1 -`, `001_`
5. title after removing leading marker characters that are part of the vault naming style

Only auto-repair when the result is unique and semantically obvious.

## Embeds

For `![[...]]`, support notes, images, PDFs, canvases, audio, video, and other attachments Obsidian can embed.

If `![[diagram.png]]` points to a unique `diagram.png`, leave it alone unless the user asked to normalize embed targets. If normalizing, prefer the style already dominant in the vault.

## Renames And Numbering Refactors

Before renaming:

1. list proposed file renames
2. list all link replacements
3. include incoming links if the rename affects existing references
4. check for basename collisions
5. ask for confirmation when the rename set is broad or ambiguous

After renaming:

1. update links preserving aliases and headings
2. audit the same scope
3. report exact changes

## Markdown Safety

Avoid changing:

- fenced code blocks
- quoted examples
- transcluded templates
- dataview queries
- callout syntax
- task status markers
- table alignment unless editing that table

When formatting, preserve the local style of headings, blank lines, lists, and callouts.

## Frontmatter Safety

Treat frontmatter as user-owned structured data. Preserve:

- unknown keys
- comments when possible
- aliases
- tags
- cssclasses
- created/modified fields
- plugin-specific fields

If YAML parsing is unavailable or risky, edit frontmatter by bounded text operations and validate the delimiters. Do not convert rich YAML into a lossy dictionary.

## Reporting

Use compact reports:

- Scope checked
- Files changed
- Replacements in `before -> after` form
- Remaining unresolved links
- Ambiguous candidates left untouched
- Encoding or line-ending risks

Avoid vague claims like "cleaned up links" without listing what changed.
