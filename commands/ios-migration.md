---
description: "Migrate to TCA + Clean Architecture - Usage: /migration [file_path] [\"migration description\"]"
---

# Migrate to TCA + Clean Architecture

**Usage:** `/migration [file_path] [migration_type]`
**Example:** `/migration OldViewModel.swift ViewModel to TCA` or `/migration Store.swift extract Use Case`

Migrate legacy iOS code to TCA and Clean Architecture patterns:

**Legacy View Model → Modern Screen Logic:**
- Convert old observable pattern to modern state management
- Extract properties to proper state
- Convert methods to actions
- Migrate data subscriptions to modern effects
- Add proper dependency management
- Implement bindings for forms

**Direct API Calls → Data Layer:**
- Extract network calls to data layer
- Abstract data access behind interface
- Add local persistence if needed
- Return reactive data streams

**Business Logic → Proper Layer:**
- Extract validation to business layer
- Move data orchestration to business layer
- Create services if combining multiple data sources

**View Updates:**
- Update to modern SwiftUI patterns
- Simplify bindings
- Add proper action handling
- Remove business logic from views

**Testing Infrastructure:**
- Generate TestStore tests
- Create makeWithDeps factory
- Mock dependencies with testValue

**Preserves:**
- Existing functionality
- UI layout and design
- Business logic behavior

Provides step-by-step migration plan with before/after code examples.

> **Migration Patterns**: See Architecture Essentials and TCA Essentials in .cursor/rules for complete modern patterns and anti-patterns.

**Agent Used:** May invoke `tca-developer` and `ios-architect`.

## Usage
```
/migration [file_path] [migration_type]
```

## Parameters
- `file_path`: Path to the legacy file to migrate (required)
- `migration_type`: Optional specific migration (e.g., "ViewModel to TCA", "extract Use Case", "add Repository")
