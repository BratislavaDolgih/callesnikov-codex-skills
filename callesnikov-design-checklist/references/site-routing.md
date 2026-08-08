# Checklist Design routing

Use this reference to choose a small, relevant set of live pages from <https://www.checklist.design/>. The site currently organizes its catalog into five product layers. Treat the routes and examples as navigation aids; confirm live content before relying on it.

## Route by design question

| Question | Section | Base route | Typical targets |
| --- | --- | --- | --- |
| What should this mobile screen or native interaction contain? | Mobile app | `/mobile` | onboarding, login, paywall, checkout, search, camera, settings, tab navigation |
| What should this application workspace or account area contain? | Web app | `/web-app` | admin panel, billing, empty state, notifications, user management, chat, API keys |
| What should this public-facing page contain? | Website | `/website` | pricing, features, contact, FAQ, security, privacy, careers, 404 |
| How should this reusable UI control behave? | Design system | `/design-system` | button, input field, modal, toast, loading, tabs, toggle, typography, tokens |
| What should happen across several states or screens? | Flows | `/flows` | uploading media, submitting a form, resetting a password, deleting an account, saving changes |

Open `/browse` when the target is unclear or a known route fails. Use the site's search for synonyms. Do not sweep the whole catalog.

## Selection order

1. Start with the user's goal, not the visible component.
2. Choose the primary page for the artifact being built or reviewed.
3. Add the flow page when success, failure, cancellation, or recovery spans multiple states.
4. Add a design-system page only for a component whose behavior materially affects the flow.
5. Follow a page's **Related** links when they reveal a real dependency.

Examples:

- Mobile paywall: primary `/mobile/paywall`; consider `/mobile/billing` and `/flows/making-a-payment` only if purchase behavior is in scope.
- Upload screen: primary `/flows/uploading-media`; consider `/design-system/loading`, `/design-system/toast`, and `/design-system/modal` when those controls exist.
- Empty project list: primary `/web-app/empty-state`; consider onboarding or search only when the state leads into those flows.
- Button implementation: primary `/design-system/button`; include the surrounding screen or flow because button quality depends on context and consequence.

## What to inspect on a checklist page

- The introductory definition: clarifies the intended scope.
- Checklist items: names the expected decisions or states.
- Item explanations: gives the reason and often the failure mode.
- **Documentation**: supplies visual or structural examples when available.
- **Related** pages: exposes nearby components and flows.
- Export controls: useful only when the user asks for a checklist formatted for a work-management tool.

## Source boundaries

- Link to the exact pages used.
- Paraphrase guidance and adapt it to the product.
- Do not reproduce the entire catalog or large portions of a page.
- Do not treat Checklist Design as official Apple, Google, web-standard, accessibility, legal, or security guidance.
- For platform-specific or high-risk behavior, verify against current primary sources in addition to this site.
