# Design system

## Reference direction
Use Linear (https://linear.app) for disciplined sidebar/navigation and dense information hierarchy, Ramp (https://ramp.com) for spending-card clarity, and Mercury (https://mercury.com) for restrained financial typography. These are inspiration references, not copied assets or brand identity. A dedicated detailed reference specification is used instead of claiming an unavailable Lovable/v0 session.

## Tokens
Implemented tokens live in `frontend/src/styles.css`: warm canvas `#f7f8f4`; white surfaces; dark text `#253c34`; navy sidebar `#152d2b`; emerald `#237e60`; border `#e6eae2`. After observed contrast defect#41, semantic muted normal text uses `#586b5f` on light surfaces and sidebar-muted `#a5b9af` on navy. Negative balances use `#9b5138`; error text uses `#8b5134`. These changes preserve the warm fintech identity while strengthening small-label readability; independent browser ratio verification is recorded in QA, not assumed from token names.

Maintain WCAG AA normal-text contrast>=4.5 on actual backgrounds; never rely on color alone for owed/receivable or success/error states. Use Inter/system sans at14px base, compact labels, serif display headings and tabular monetary figures. Large headings and restrained chart colors establish hierarchy without pale essential labels.

Spacing follows 4px units: 8px compact gaps, 12/16px component spacing, 24px cards, 32px page gaps. Cards have 12–16px radius, subtle border and minimal shadow. Tables align amount columns right. Buttons have primary, secondary, ghost and destructive variants with consistent 40px desktop and 44px mobile touch targets.

## Layout and navigation
Desktop has a persistent242px sidebar, clear product mark, workspace label and Overview/Groups/Expenses/Balances/Settlements/Analytics navigation. Content uses fluid cards within a readable maximum width. Group context remains visible on details and forms. Responsive CSS collapses navigation and stacks content on narrow screens; data tables may scroll inside their own positioned container, never extend the entire document. Verify the actual390px viewport rather than relying on breakpoint names. Desktop cards and charts use multi-column space where available.

Implemented breakpoints:1500px and wider expands desktop space;1150px and narrower reduces dense layouts;850px and narrower collapses sidebar/navigation and page structures;640px and narrower stacks compact mobile content, controls and dialogs. The exact per-component behavior is defined by the stylesheet's media rules and covered by390px browser regression.

## States and interaction
Skeleton/loading label during async reads; actionable empty states with first-step button; inline field errors and alert feedback; success confirmation after mutations. Disable submitting controls while saving. Destructive operations require confirmation. Charts have textual totals and labels. Every form field has a programmatic label, visible keyboard focus, useful input mode and specific error message. Dialogs support Escape, initial focus, focus containment and return focus to the connected visible invoking control; if that control disappears after mutation, choose a sensible surviving page control. Mutation errors stay inside the active modal accessibility tree. Reduced-motion users avoid nonessential transitions. Test desktop and390px width with keyboard; independent regressions#34/#35/#40/#41 cover observed failures rather than claiming blanket accessibility certification.
