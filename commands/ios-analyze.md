---
description: "Analyze iOS + TCA Code - Usage: /analyze [file_path] [explain|debug|lint] [\"concern text\"]"
---

# Analyze iOS + TCA Code

**Usage:** `/analyze [file_path] [mode] [focus]`
**Modes:** `explain` (default) | `debug` | `lint`

Analyze iOS/TCA code with three analysis modes:

## Modes

### explain (default)
Explain code structure and implementation:
- Screen logic (state, actions, business logic, dependencies)
- Code organization (layers, services, data access)
- Implementation details (SwiftUI, async/await, publishers)
- Design system usage (Colors, L10n, .defaultFont())

### debug
Find and fix bugs:
- View not updating when state changes
- Actions not triggering
- Crashes (dependencies, nil values, threading)
- Memory leaks (retain cycles, uncanceled subscriptions)
- Navigation issues
- Race conditions in async code
- Error handling gaps

### lint
Check code quality:
- TCA patterns (State/Action/Reducer structure, @Dependency usage)
- Swift/iOS standards (SwiftLint, design system, accessibility)
- Architecture quality (layer separation, SOLID principles)
- Code smells (duplication, complexity, hardcoded values)
- Missing error handling, force unwraps

## Usage
```
/analyze [file_path] [mode] [focus]
```

## Parameters
- `file_path`: Path to file (required)
- `mode`: Analysis mode - `explain` | `debug` | `lint` (default: explain)
- `focus`: Optional specific concern (e.g., "state updates", "memory leaks", "design system")

## Examples
```
/analyze HomeStore.swift                    # Explain code (default)
/analyze HomeStore.swift explain            # Explain structure
/analyze HomeStore.swift debug              # Find bugs
/analyze HomeStore.swift lint               # Check quality
/analyze HomeStore.swift debug "state not updating"
/analyze HomeView.swift lint "design system"
```

## Output

**explain mode:**
Clear explanations suitable for code reviews, onboarding, documentation.

**debug mode:**
Specific debugging steps, breakpoint suggestions, and fixes with code examples.

**lint mode:**
Specific improvements with before/after examples following project standards.

> **Pattern Reference**: See .cursor/rules for detailed patterns (Architecture Essentials, TCA Essentials, Critical Patterns, Localization Rules, TCA Testing Best Practices).

**Agent Used:** May invoke `tca-developer`, `ios-architect`, or `ios-swiftui-designer` depending on mode and context.
