# Design review framework

Use this reference to convert selected Checklist Design guidance into decisions, implementation work, and verification.

## Design mode

For a new or changing feature, produce a compact specification:

1. **User goal**: what the user is trying to finish.
2. **Entry and exit**: how the flow starts, succeeds, cancels, and returns.
3. **Required content and actions**: only what supports the goal.
4. **State matrix**: applicable states and transitions.
5. **Acceptance criteria**: observable outcomes.
6. **Open decisions**: unresolved product choices, separated from implementation facts.

Consider these state families when relevant:

- initial, active, pressed, selected, focused, and disabled;
- loading, progress, success, empty, no-results, and failure;
- offline, timeout, retry, cancellation, and partial completion;
- first use, returning use, restored session, and restored purchase;
- permission unknown, denied, permanently denied, and granted;
- keyboard visible, back navigation, rotation or resize, and interrupted app lifecycle.

Do not force every state into every feature. Include a state only when the system can actually enter it.

## Audit mode

Use these statuses:

| Status | Meaning |
| --- | --- |
| `Pass` | The artifact visibly or demonstrably satisfies the item. |
| `Partial` | The behavior exists but misses an important case or quality threshold. |
| `Missing` | The relevant behavior is absent or contradicted by evidence. |
| `N/A` | The item does not apply; state the product reason. |
| `Unknown` | Available evidence cannot establish the result. |

For every `Partial`, `Missing`, or important `Unknown`, record:

- **Evidence**: file, component, screenshot, runtime behavior, requirement, or missing artifact.
- **Consequence**: what the user cannot understand, complete, recover from, or trust.
- **Fix**: the smallest product-appropriate change.
- **Acceptance criterion**: a behavior that can be observed or tested.
- **Source**: exact Checklist Design page when the finding came from it.

## Priority

Rank findings by consequence:

- **Blocker**: prevents completion, causes data or money risk, traps the user, or violates a hard platform requirement.
- **High**: causes frequent confusion, inaccessible interaction, lost progress, or unrecoverable failure.
- **Medium**: weakens clarity, feedback, consistency, or efficiency without blocking the goal.
- **Polish**: improves refinement after functional and accessibility issues are addressed.

Do not inflate cosmetic preferences into blockers.

## Acceptance criteria style

Write criteria as observable behavior:

- Weak: "The error state should look good."
- Strong: "After a failed upload, the file remains visible, shows the failure reason, and offers Retry and Remove actions without discarding successful files."

- Weak: "The button should be accessible."
- Strong: "The primary action has an accessible name, visible keyboard focus, a disabled explanation when submission is unavailable, and no duplicate submission while loading."

## Recommended audit output

Start with the verdict and highest-impact findings. Use a table only when three or more items benefit from comparison.

```markdown
Verdict: [one sentence]

| Priority | Status | Area | Evidence and consequence | Recommended change |
| --- | --- | --- | --- | --- |
| High | Missing | Upload recovery | Failed files disappear, so users cannot retry | Preserve each failed item and expose Retry/Remove |

Acceptance criteria:
- [Observable behavior]

Sources:
- [Checklist name](exact URL)

Unverified:
- [Device, state, or artifact that was not checked]
```

For implementation work, replace the generic recommendation column with the actual changed files and verification result.
