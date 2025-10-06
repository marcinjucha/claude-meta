# Refactor iOS + TCA Architecture

Analyze code for refactoring opportunities in iOS/TCA context:

**Screen Logic Refactoring:**
- Improve action organization
- Extract smaller sub-features
- Simplify complex logic (split into smaller pieces)
- Improve async patterns
- Add proper dependency management
- Implement proper navigation

**Code Organization Refactoring:**
- Extract business logic from screens
- Create services to prevent circular dependencies
- Move logic to appropriate layers
- Split large components
- Improve separation of concerns

**Code Quality Refactoring:**
- Eliminate code duplication (extract helpers, extensions)
- Break down complex functions (single responsibility)
- Extract magic numbers/strings (constants, enums)
- Improve naming (descriptive, intention-revealing)
- Add error handling (Result types, proper throws)

**SwiftUI Refactoring:**
- Extract view components (reusable views)
- Apply design system (Colors, L10n, .defaultFont())
- Add accessibility support
- Improve layout structure

Provides specific refactoring steps with before/after examples following project patterns.

> **Refactoring Patterns**: See Architecture Essentials and Critical Patterns in .cursor/rules for detailed refactoring guidelines and anti-patterns.

**Agent Used:** May invoke `tca-developer`, `ios-architect`, or `ios-swiftui-designer`.

## Usage
```
/refactor [file_path] [refactor_goal]
```

## Parameters
- `file_path`: Path to the file to refactor (required)
- `refactor_goal`: Optional specific objective (e.g., "extract use case", "split reducer", "improve actions")