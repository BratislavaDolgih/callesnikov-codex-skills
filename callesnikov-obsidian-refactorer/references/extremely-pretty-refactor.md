# Extremely Pretty Refactor

Use this Obsidian Refactorer mini-skill when the user explicitly asks for `Крайне привлекательный рефактор заметки`, an attractive lecture refactor, a quick attractive note refactor, mass refactor of existing note text, or gives matching formatting rules for Markdown lecture cleanup.

## Core Reaction

Treat the task as **format-preserving, content-preserving refactor**, not rewriting.

Do not fully transform the author's text into a new voice. Preserve the author's content, order, terminology, examples, and logical flow. Edit wording only when:

- a phrase is unfinished;
- an abbreviation is too broken to read;
- grammar blocks comprehension;
- the connection between adjacent sentences is lost;
- a definition, formula, or list item needs formatting to become readable.

Do not shorten existing text. Do not expand it unless a missing connective phrase or obvious abbreviation must be restored for comprehension.

## Safety Before Refactor

Keep the normal Callesnikov Obsidian Refactorer rules active:

1. Inspect the exact note first.
2. Preserve frontmatter, aliases, wiki-links, embeds, headings, block references, and code fences.
3. Avoid broad structure changes.
4. Validate the same scope after editing.
5. Apply agent-owned properties according to `properties-rules.md` when the note is edited.

For mass refactors, split work by folder/note batch, run audit before and after each batch, and report what was changed. Do not do uncontrolled whole-vault style rewrites.

## Default Refactor Theme

Use this as the default visual/structural theme unless the user gives another theme.

1. Rename the lecture note only when the user asks for lecture-title normalization. Use the format `ЛК-<NUMBER>; <GENERAL TITLE OF LECTURE>` and check incoming/outgoing links before renaming.
2. Format each main point as a level-two Markdown heading: `##`.
3. Format each subpoint inside a main point as a level-four Markdown heading: `####`.
4. Use Obsidian callouts by meaning, combining adjacent definition/explanation/nuance material into the most precise callout type when it improves readability:
   - `abstract`: for definitions, using `>[!abstract] ==<DEFINITION>== — <DESCRIPTION>`.
   - `info`: for explanations and clarifying notes; sometimes also for definitions when the text is explanatory rather than formal.
   - `warning`: for nuances, caveats, traps, exceptions, and fragile distinctions.
5. Replace mathematical Unicode symbols with matching LaTeX notation where practical, for example `Θ` -> `\Theta`, `Γ` -> `\Gamma`, `δ` -> `\delta`, `λ` -> `\lambda`, `α` -> `\alpha`, `≤` -> `\leq`, `∈` -> `\in`.
6. Put standalone definitions, sets, transition rules, and formulas written in LaTeX notation into display math blocks: `$$...$$`.
7. Put inline calculations, symbols, and explanatory math fragments into single-dollar inline math: `$...$`.
8. For numbered lists, make only the sentence or title of the numbered item bold italic, for example `1. ***...***`; put the explanatory text below the numbered item without repeating the number.

## What To Report

Final response must state:

- final path of the edited note;
- whether the note was renamed;
- which default theme rules were applied;
- whether agent properties were added/updated;
- content-level corrections made deliberately;
- unresolved links, ambiguous embeds, or formatting risks left untouched.
