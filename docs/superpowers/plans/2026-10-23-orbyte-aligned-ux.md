# Orbyte-Aligned OrderGuard UX Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the OrderGuard MVP feel like a reusable Orbyte workspace module using the actual navigation, pending-action, search/filter, status and approval patterns observed in the participant demo platform.

**Architecture:** Keep the discrepancy engine, Trust Gate and approval services unchanged. Add a presentation adapter for pending-action counts/filtering, an Orbyte-aligned application shell, a searchable Supplier Checks page, and a separate Exception Report page. All organization/role integration remains explicitly simulated.

**Tech Stack:** Python, Flask, Jinja, Bootstrap, SQLite.

**Spec:** `docs/ORBYTE_PLATFORM_NOTE.md` plus participant-provided Orbyte screenshots from 23 October 2026.

## Global Constraints

- Do not claim live Orbyte API integration.
- Do not copy or store temporary Orbyte credentials.
- Preserve owner-only consequential approval and Trust Gate behavior.
- Keep synthetic competition data only.
- Keep OrderGuard branding while adopting compatible UX patterns rather than cloning proprietary UI exactly.

## Review Focus

- Empty case list remains usable.
- Search is case-insensitive and does not mutate data.
- Status filter supports all known OrderGuard statuses.
- Pending-action counts distinguish clarification from owner review.
- Navigation remains usable on narrow screens.

---

### Task 1: Presentation adapter

**Files:**
- Create: `src/orbyte_adapter.py`
- Create: `tests/test_orbyte_adapter.py`

**Produces:** pending-action counts and case filtering helpers.

- [ ] Add failing tests for pending counts, search and status filtering.
- [ ] Implement minimal pure helpers.
- [ ] Run unit tests.

### Task 2: Orbyte-aligned shell and dashboard

**Files:**
- Modify: `src/templates/base.html`
- Modify: `src/templates/dashboard.html`
- Modify: `src/static/style.css`
- Modify: `src/app.py`

- [ ] Add organization-context sidebar and Workspace > OrderGuard navigation.
- [ ] Add Pending Actions card with Clarify / Review / Approved categories.
- [ ] Preserve judge-demo scenarios and metrics below operational content.

### Task 3: Supplier Checks and Exception Report

**Files:**
- Create: `src/templates/checks.html`
- Create: `src/templates/reports.html`
- Modify: `src/app.py`

- [ ] Add GET `/checks` with query/status filtering.
- [ ] Add GET `/reports` using Supplier Exception Radar data.
- [ ] Keep Create Check as the primary action.

### Task 4: Documentation and verification

**Files:**
- Modify: `docs/ORBYTE_PLATFORM_NOTE.md`
- Modify: `README.md`

- [ ] Document observed Orbyte UX patterns separately from assumed integrations.
- [ ] Run full unit test suite through GitHub Actions.
