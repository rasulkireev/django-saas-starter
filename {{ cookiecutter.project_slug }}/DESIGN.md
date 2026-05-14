---
version: alpha
name: "{{ cookiecutter.project_name }}"
description: "Default SaaS design system for {{ cookiecutter.project_name }}. Replace these tokens and notes as the product identity matures."
colors:
  primary: "#15803D"
  primary-hover: "#166534"
  primary-soft: "#DCFCE7"
  secondary: "#0F172A"
  secondary-soft: "#E2E8F0"
  accent: "#2563EB"
  neutral: "#F8FAFC"
  surface: "#FFFFFF"
  surface-muted: "#F1F5F9"
  surface-dark: "#020617"
  border: "#E2E8F0"
  border-dark: "#1E293B"
  text: "#0F172A"
  text-muted: "#475569"
  text-inverse: "#FFFFFF"
  success: "#166534"
  warning: "#F59E0B"
  danger: "#DC2626"
typography:
  headline-display:
    fontFamily: Inter, ui-sans-serif, system-ui, sans-serif
    fontSize: 60px
    fontWeight: 800
    lineHeight: 1
    letterSpacing: -0.04em
  headline-lg:
    fontFamily: Inter, ui-sans-serif, system-ui, sans-serif
    fontSize: 48px
    fontWeight: 800
    lineHeight: 1.05
    letterSpacing: -0.035em
  headline-md:
    fontFamily: Inter, ui-sans-serif, system-ui, sans-serif
    fontSize: 30px
    fontWeight: 750
    lineHeight: 1.15
    letterSpacing: -0.025em
  headline-sm:
    fontFamily: Inter, ui-sans-serif, system-ui, sans-serif
    fontSize: 24px
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: -0.015em
  body-lg:
    fontFamily: Inter, ui-sans-serif, system-ui, sans-serif
    fontSize: 18px
    fontWeight: 400
    lineHeight: 1.65
  body-md:
    fontFamily: Inter, ui-sans-serif, system-ui, sans-serif
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.65
  body-sm:
    fontFamily: Inter, ui-sans-serif, system-ui, sans-serif
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.55
  label-md:
    fontFamily: Inter, ui-sans-serif, system-ui, sans-serif
    fontSize: 14px
    fontWeight: 650
    lineHeight: 1.3
  label-caps:
    fontFamily: Inter, ui-sans-serif, system-ui, sans-serif
    fontSize: 12px
    fontWeight: 700
    lineHeight: 1
    letterSpacing: 0.14em
  code-sm:
    fontFamily: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace
    fontSize: 13px
    fontWeight: 500
    lineHeight: 1.6
rounded:
  none: 0px
  sm: 6px
  md: 10px
  lg: 14px
  xl: 20px
  full: 9999px
spacing:
  xs: 4px
  sm: 8px
  control: 12px
  md: 16px
  lg: 24px
  xl: 32px
  2xl: 48px
  3xl: 64px
  section-y: 96px
  page-x: 24px
  container: 1200px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.text-inverse}"
    typography: "{typography.label-md}"
    rounded: "{rounded.full}"
    padding: "{spacing.control}"
  button-primary-hover:
    backgroundColor: "{colors.primary-hover}"
    textColor: "{colors.text-inverse}"
  button-secondary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.secondary}"
    typography: "{typography.label-md}"
    rounded: "{rounded.full}"
    padding: "{spacing.control}"
  button-danger:
    backgroundColor: "{colors.danger}"
    textColor: "{colors.text-inverse}"
    typography: "{typography.label-md}"
    rounded: "{rounded.full}"
    padding: "{spacing.control}"
  card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text}"
    rounded: "{rounded.xl}"
    padding: 24px
  card-muted:
    backgroundColor: "{colors.surface-muted}"
    textColor: "{colors.text}"
    rounded: "{rounded.xl}"
    padding: 24px
  app-shell:
    backgroundColor: "{colors.neutral}"
    textColor: "{colors.text}"
  nav:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text}"
    rounded: "{rounded.full}"
  input:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text}"
    rounded: "{rounded.md}"
    padding: "{spacing.control}"
  badge-success:
    backgroundColor: "{colors.primary-soft}"
    textColor: "{colors.success}"
    typography: "{typography.label-caps}"
    rounded: "{rounded.full}"
    padding: 8px
  badge-warning:
    backgroundColor: "{colors.warning}"
    textColor: "{colors.surface-dark}"
    typography: "{typography.label-caps}"
    rounded: "{rounded.full}"
    padding: 8px
  badge-neutral:
    backgroundColor: "{colors.secondary-soft}"
    textColor: "{colors.secondary}"
    typography: "{typography.label-caps}"
    rounded: "{rounded.full}"
    padding: 8px
  link:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.accent}"
    typography: "{typography.body-md}"
  divider-light:
    backgroundColor: "{colors.border}"
    height: 1px
  divider-dark:
    backgroundColor: "{colors.border-dark}"
    height: 1px
  muted-copy:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text-muted}"
    typography: "{typography.body-sm}"
---

# {{ cookiecutter.project_name }} Design System

## Overview

This file is the project-level design source of truth for humans and AI coding agents. It follows the public Google Labs Code [`DESIGN.md`](https://github.com/google-labs-code/design.md) alpha format: YAML design tokens first, then markdown guidance explaining how to apply them.

The default style is intentionally generic for a modern Django SaaS product: clean, trustworthy, accessible, and easy to customize after generation. Treat this as a starting point, not a permanent brand identity.

When the product direction is clearer, update this file before making broad UI changes. Keep the tokens and prose aligned so different agents and tools produce consistent interfaces.

## Colors

The default palette uses practical SaaS neutrals with one confident primary color.

- **Primary (#15803D):** Main action color for CTAs, selected states, success-adjacent highlights, and the most important conversion path.
- **Secondary (#0F172A):** Deep slate for headlines, app chrome, and high-contrast UI surfaces.
- **Accent (#2563EB):** Secondary action/link color. Use it for navigation emphasis and informational affordances, not the main conversion path.
- **Neutral/Surface (#F8FAFC / #FFFFFF / #F1F5F9):** Light surfaces for pages, cards, forms, dashboards, and marketing sections.
- **Semantic colors:** Green for success, amber for warning, red for destructive or error states.

If your generated project needs a different brand, start by changing `primary`, `primary-hover`, `primary-soft`, and `accent`, then review button, badge, and link components.

## Typography

Use a system sans-serif stack for speed, reliability, and low setup friction. Add a brand font later only if it improves the product enough to justify the dependency.

- **Headlines:** Bold, slightly tight tracking for landing pages, docs intros, and major empty states.
- **Body:** 16px default with generous line height for readable forms, settings pages, docs, and dashboards.
- **Labels:** Medium-weight labels for form controls and action buttons.
- **Caps labels:** Use sparingly for section eyebrows, small status badges, and metadata.
- **Code:** Monospace for API examples, environment variables, commands, tokens, and identifiers.

## Layout

Use simple responsive layouts that work well for server-rendered Django pages.

- Keep page content inside a centered max-width container (`1200px`) with `24px` mobile-safe horizontal padding.
- Use generous vertical rhythm on marketing pages and tighter spacing in authenticated app screens.
- Prefer boring, predictable grids: single column on mobile, 2-column feature areas, 3-column card groups when content is symmetrical.
- Forms should be narrow enough to scan comfortably. Dashboards can use wider containers, but avoid dense data walls without hierarchy.
- Design empty, loading, error, and success states as first-class UI, not afterthoughts.

## Elevation & Depth

Depth should come from borders, spacing, and subtle shadows.

- Default cards use light backgrounds, clear borders, and rounded corners.
- Use shadows only for overlays, menus, modals, and important hover states.
- Dark surfaces are reserved for headers, footers, code examples, and high-contrast hero sections.
- Avoid heavy glassmorphism, noisy gradients, and decorative effects that make forms or tables harder to read.

## Shapes

The default shape language is friendly but restrained.

- Use pill buttons for primary actions and navigation CTAs.
- Use `10px`–`20px` radius for inputs, cards, panels, and modal containers.
- Use full-radius badges for status labels.
- Keep radius choices consistent within each screen; inconsistency makes generated products feel stitched together.

## Components

- **Primary button:** Primary background, white text, pill radius, medium-bold label. Use for the single most important action in a section.
- **Secondary button:** White or muted background, slate text, border when needed. Use for navigation, cancel, and lower-priority actions.
- **Danger button:** Red background, white text. Use only for irreversible destructive actions and pair with confirmation UI.
- **Cards:** White/muted surfaces with rounded corners and borders. Keep one clear purpose per card.
- **Forms:** Visible labels, clear helper/error text, high-contrast focus rings, and full-width controls on mobile.
- **Navigation:** Simple top nav with clear product name, primary links, auth/account actions, and accessible mobile behavior.
- **Tables/lists:** Prioritize scanability: sticky or repeated context where needed, muted metadata, and explicit empty states.
- **Docs/code blocks:** Monospace code, copyable commands when possible, and examples that match the generated project structure.

## Do's and Don'ts

- Do update this file when the brand, UI conventions, or component rules change.
- Do keep YAML tokens and markdown descriptions consistent.
- Do preserve WCAG AA contrast for text, buttons, alerts, and form states.
- Do design for both anonymous marketing pages and authenticated SaaS app screens.
- Do keep guidance agent-neutral: useful to humans, Codex, Claude Code, Cursor, and any future coding tool.
- Don't hard-code maintainer names, domains, or one project's positioning into reusable UI guidance.
- Don't introduce a new font, color, radius, or shadow style for a single screen without updating the design system.
- Don't make AI-agent instructions vendor-specific; use plain project conventions and file paths.
- Don't let generated pages depend on remote design assets unless the project explicitly adds them.
