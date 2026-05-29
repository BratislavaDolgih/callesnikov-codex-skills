# AI Engineering Coach Rulebook For Codex

Use this reference when `callesnikov-agent-summarizer` needs a serious closing audit grounded in Microsoft AI Engineering Coach concepts.

Source basis for this adaptation:

- Microsoft AI Engineering Coach repository: `https://github.com/microsoft/AI-Engineering-Coach`
- Coach docs areas used conceptually: `docs/content/improve/anti-patterns.md`, `docs/content/improve/context-health.md`, `docs/content/improve/skill-finder.md`
- Coach rule catalog used conceptually: `src/core/rules/*.md`

This reference is self-contained. It does not require a local clone of AI Engineering Coach. If the user asks to refresh the rulebook later, re-check the upstream repository first and then update this file.

The original project is VS Code/Copilot-oriented. In Codex App, treat its measurements as an audit framework, not as guaranteed telemetry. Use visible conversation/tool evidence unless the user asks to inspect local logs.

## Coach Categories

Score qualitatively using the same five practice areas:

- `Prompt Quality`: specificity, file context, constraints, expected output, emotional clarity.
- `Session Hygiene`: thread length, drift, abandonment, cancellation loops, overwork patterns.
- `Code Review`: verification discipline, terminal safety, generated-code review, sandbox boundaries.
- `Tool Mastery`: using the right skill/tool/model for the job, avoiding tool bloat and premium waste.
- `Context Management`: context saturation, compaction risk, instruction bloat, source-of-truth hygiene.

Use verdicts `Healthy`, `Degraded`, or `Critical` instead of fake numeric scores unless real metrics are available.

## Finding Shape

Microsoft Coach findings are built around:

- `PROBLEM`: what was detected, with counts or concrete examples when available.
- `ACTION`: concrete recommendation.
- `Examples`: real examples from sessions.

Codex adaptation:

```text
Label: <rule name>
Problem: <what happened>
Evidence: <visible prompt/tool/file/command pattern>
Action: <how to fix next time>
Next prompt: <optional copy-ready wording>
```

## Rule Catalog Adapted To Codex

### Prompt Quality

- `Lazy Prompting`: short/vague requests without intent, constraints, target path, or output format. Fix by asking for artifact, scope, constraints, success criteria.
- `Missing File Context`: user references a file/repo/vault without path or artifact. Fix by asking for path or inspecting the workspace first.
- `Excessive File Context`: too many unrelated files/logs pulled into context. Fix with `rg`, targeted reads, summaries, and reference files.
- `Instruction Bloat`: always-on instructions or skill bodies become too large. Fix by moving details into `references/` and keeping `SKILL.md` lean.
- `Repeated Prompts`: same request pattern appears repeatedly. Fix by creating/extending a skill, script, or default prompt.
- `Verbose Output`: assistant answers with too much prose for a simple request. Fix with compact final answers and exact paths.
- `Verbose Prompt No Compression`: user provides long natural-language prompts where a structured brief would do. Fix with short templates.
- `Low Constraint Usage`: task lacks boundaries like no-delete, install location, output format, or verification. Fix by stating constraints upfront.
- `Context Engineering Gaps`: important project rules live only in chat. Fix by writing them to skills, AGENTS.md, scripts, or references.
- `Caps Lock / Frustration / Profanity`: emotion replaces constraints. Fix by translating frustration into failure condition plus next experiment.

### Session Hygiene

- `Mega Sessions`: one thread absorbs too many unrelated projects. Coach source suggests focused sessions around 15-25 messages; in Codex, use fresh threads after natural milestones.
- `Abandoned Sessions`: session stops without a handoff. Fix by writing done/open/next summary.
- `Session Drift`: topic changes before closure. Fix by checkpointing current task before switching.
- `Broken Flow State`: repeated interruptions/cancellations. Fix by narrowing one executable step.
- `High Cancellation`: user keeps stopping runs. Fix by starting with dry-runs and shorter tool passes.
- `Runaway Agent Loops`: repeated tool calls without new information. Fix by stating blocker, changing hypothesis, or asking for missing input.
- `Slow Responses`: task was made heavier than needed. Fix by using local source, targeted reads, or smaller scope.
- `Late-Night / Weekend Overwork`: if visible from timestamps, flag fatigue only gently and practically.

### Code Review And Safety

- `Auto-Approve Terminal`: terminal/network/destructive commands happen without appropriate approval or sandbox. Fix by dry-run, local scope, approval, and exact paths.
- `Copy-Paste Blindness`: generated code/commands accepted without verification. Fix by running help, tests, preflight, or reading outputs.
- `No Devcontainer`: project lacks isolated runtime when risky commands are needed. In Codex, mention sandbox/worktree/root boundaries instead of VS Code devcontainers when relevant.
- `Speed Accept`: too much trust in generated edits. Fix by diff review and focused tests.
- `Tunnel Vision`: Codex pursues first approach despite failures. Fix by alternative tactic after repeated failure.
- `Vibe Coding`: broad coding by feel, unclear acceptance criteria. Fix by artifact-first prompt plus verification.
- `YOLO Mode`: destructive/global install/mass rewrite without boundaries. Fix with no-delete rules, dry-run, scoped paths, and backups/git state.

### Tool Mastery

- `Agentic No Tools`: using chat-only answers when local inspection is needed. Fix by inspecting relevant files/commands.
- `Agent Mode For Asks`: using heavy workspace/tool flow for trivial factual questions. Fix by direct answer.
- `Auto Avoidance`: user or Codex avoids useful automation/scripts. Fix by scripting repeated mechanical work.
- `Cache Hit Starvation`: repeated work misses reusable artifacts. Fix by recording paths, commands, and outputs.
- `MCP Tool Bloat`: too many tools in one request. Fix by one primary path plus one fallback.
- `Model Overreliance`: assuming model intelligence replaces verification. Fix by evidence-first checks.
- `No Custom Instructions`: recurring rules are not codified. In Codex, convert to skills/AGENTS.md/references.
- `No Plan Mode`: broad/high-risk tasks start without a small plan. In Codex, present a short plan for multi-step edits.
- `No Skills`: repeated manual workflow despite an available skill. Fix by invoking the skill explicitly.
- `Premium For Lookup Questions` / `Premium Waste`: expensive model/context use for simple or local-source tasks. Fix by direct command, local docs, or shorter answer.
- `Reasoning Effort Overuse`: deep analysis for already-decided work. Fix by execute-and-verify.

### Context Management

- `Context Window Saturation`: long thread approaches compaction. Fix by closing with a handoff and starting fresh.
- `Compaction Storms`: frequent automatic compactions. Fix by manual summaries at milestones.
- `Runaway Growth`: context grows without closure. Fix by slicing work and preserving only current task facts.
- `Low Signal-To-Noise`: banter/log dumps drown reusable facts. Fix by writing decisions into files and keeping final summaries tight.
- `Stale Source Of Truth`: paths/version/status changed but skill or summary was not updated. Fix by rechecking and patching metadata.

## Context Health For Codex App

Assess two tabs conceptually:

### Context Quality

Adapt the Coach signals to Codex:

- Context files: `AGENTS.md`, repo docs, local project instructions.
- Custom skills: relevant skills in `C:\Users\User333\.codex\skills`.
- Custom agents/plugins: available Codex plugins/MCP servers/apps.
- Prompt templates: recurring copy-ready prompts in skills or references.
- Hooks/preflight: scripts that verify runtime readiness.
- Sandbox/runtime: workspace-write roots, local installs, no global writes unless approved.
- MCP/tool config: whether the needed tools exist and are not bloated.
- Context freshness: whether paths, versions, display names, and install status were rechecked.

### Context Management

Use visible proxies when exact metrics are unavailable:

- thread length and number of topic shifts;
- repeated file reads or repeated failed commands;
- whether compaction already happened;
- amount of stale chat-only state;
- number of unrelated domains in one thread;
- whether the final handoff is enough to start a new session without rereading everything.

## Skill Finder For Codex

Surface opportunities when similar prompts repeat across this session or visible history:

- same file family: PDF, audio, YouTube, Obsidian, frontend motion, browser testing;
- same command chain or preflight;
- same “how should I ask you?” confusion;
- same metadata/display-name repair;
- same safety rule: do not delete, local install only, dry-run first;
- same final report format.

Prefer `Extend existing: <skill>` over new skills when a skill already owns the domain.

For each candidate include:

- repetition evidence;
- trigger phrase;
- core workflow;
- whether it belongs in `SKILL.md`, `references/`, or `scripts/`;
- priority.

## Token Diet Heuristics

Call out expensive moves only when backed by evidence:

- browsing when local source was available;
- reading whole files when `rg` or a narrow snippet would do;
- installing dependencies before proving a use case;
- overlong answers after tiny factual questions;
- one giant session for many unrelated domains;
- tool loops without new hypothesis;
- skill creation when a reference patch would be enough.

Always give a replacement:

```text
Next time say: "<shorter prompt>"
Use skill: "$skill-name"
Start fresh with handoff: "<handoff>"
Run first: "<preflight command>"
```
