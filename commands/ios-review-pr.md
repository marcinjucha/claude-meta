---
description: "Pull Request Readiness Check - Usage: /review-pr [file_or_directory_path]"
---

# Pull Request Readiness Check

**Usage:** `/review-pr [file_or_directory_path]`
**Example:** `/review-pr DigitalShelf/Screens/Home/` or `/review-pr HomeStore.swift`

Comprehensive pre-PR validation combining quality, architecture, and testing checks:

**Code Quality:**
- SwiftFormat compliance
- SwiftLint warnings/errors
- No TODO/FIXME comments in production code
- No commented-out code blocks
- No debug print statements

**Screen Logic:**
- State properly set up and observable
- Bindings working correctly
- Actions well organized
- Effects properly canceled
- No dependency crashes

**Code Organization:**
- Logic in the right layer (views → business logic → data → models)
- No circular dependencies between data layers
- Business logic properly separated
- Views don't contain business logic

**Design System:**
- Uses Colors enum (not hardcoded colors)
- Uses L10n constants (no hardcoded strings)
- Uses .defaultFont() (not .system(size:))
- Has accessibility labels

**Testing:**
- Tests exist for new features
- Tests pass locally
- Test coverage adequate

**Documentation:**
- Public APIs documented
- Complex logic has WHY comments

Provides actionable checklist of issues to fix before creating PR.

> **Review Guidelines**: See .cursor/rules for complete checklists:
> - Architecture Essentials (code organization, comments)
> - Critical Patterns (safety rules, common pitfalls)
> - TCA Essentials (TCA best practices)
> - Localization Rules (design system compliance)
> - TCA Testing Best Practices (testing quality)

**Agent Used:** May invoke `tca-developer`, `ios-architect`, and `ios-swiftui-designer`.

## Usage
```
/review-pr [file_or_directory_path]
```

## Parameters
- `file_or_directory_path`: Path to file or directory to review (required)
