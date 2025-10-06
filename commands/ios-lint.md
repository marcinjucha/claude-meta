# Lint iOS + TCA Code Quality

Perform comprehensive code quality analysis for iOS/TCA code:

**TCA Code Quality:**
- State/Action/Reducer structure correctness
- Action naming conventions (descriptive, action-oriented)
- Effect patterns (proper cancellation, error handling)
- @Dependency usage (proper DependencyKey, makeWithDeps factory)
- Missing BindingReducer() when using @Bindable

**Swift/iOS Standards:**
- SwiftLint compliance (naming, structure, complexity)
- Design system compliance (Colors enum, .defaultFont(), L10n)
- Accessibility (VoiceOver labels, Dynamic Type)
- Memory safety (weak self, cancellation)

**Architecture Quality:**
- Layer separation (no layer skipping)
- Proper Use Case/Service/Repository usage
- Dependency flow (downward only)
- Single Responsibility Principle

**Code Smells:**
- Code duplication
- Complex functions (too many responsibilities)
- Hardcoded values (strings, colors, magic numbers)
- Missing error handling
- Force unwraps (!), implicitly unwrapped optionals

Provides specific improvements with code examples following project standards.

> **Quality Standards**: See .cursor/rules for complete guidelines:
> - Architecture Essentials (layer separation, SOLID principles)
> - TCA Essentials (TCA patterns and anti-patterns)
> - Localization Rules (L10n, Colors, .defaultFont())

**Agent Used:** May invoke `tca-developer`, `ios-architect`, or `ios-swiftui-designer`.

## Usage
```
/lint [file_path]
```

## Parameters
- `file_path`: Path to the file to analyze for code quality (required)