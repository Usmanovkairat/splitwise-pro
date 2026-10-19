# Design system

## Reference direction
Use Linear (https://linear.app) for disciplined sidebar/navigation and dense information hierarchy, Ramp (https://ramp.com) for spending-card clarity, and Mercury (https://mercury.com) for restrained financial typography. These are inspiration references, not copied assets or brand identity. A dedicated detailed reference specification is used instead of claiming an unavailable Lovable/v0 session.

## Tokens
Warm off-white canvas `#f6f7f9`; white surfaces; dark navy text `#17212f`; muted slate `#667085`; border `#e5e9ef`; primary emerald `#087f5b`; pale emerald `#e8f6ef`; amber warning `#b45309`; red destructive `#b42318`. Maintain WCAG AA text contrast; never rely on color alone for owed/receivable states. System sans/Inter fallback; 14px body, 12px labels, 24–32px page titles. Monetary figures use tabular numerals.

Spacing follows 4px units: 8px compact gaps, 12/16px component spacing, 24px cards, 32px page gaps. Cards have 12–16px radius, subtle border and minimal shadow. Tables align amount columns right. Buttons have primary, secondary, ghost and destructive variants with consistent 40px desktop and 44px mobile touch targets.

## Layout and navigation
Desktop has persistent 232px sidebar, clear product mark, workspace label and Dashboard/Groups/Expenses/Balances/Settlements/Analytics navigation. Content uses fluid cards within a readable maximum width. Group context remains visible on details and forms. At 768px collapse sidebar into compact navigation; at 640px use single-column cards, stacked filters and horizontally scrollable data tables when necessary. At 1280px allow multi-column overview cards.

## States and interaction
Skeleton/loading label during async reads; actionable empty states with first-step button; inline field errors and alert feedback; success confirmation after mutations. Disable submitting controls while saving. Destructive operations require confirmation. Charts have textual totals and labels. Every form field has a programmatic label, visible keyboard focus, useful input mode and specific error message. Dialogs support escape, focus containment and return focus. Reduced-motion users avoid nonessential transitions. Test at desktop and 390px width with keyboard.
