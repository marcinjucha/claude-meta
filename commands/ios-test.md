---
description: "Generate Tests for iOS + TCA - Usage: /test [file_path] [\"scenario description\"]"
---

# Generate Tests for iOS + TCA

**Usage:** `/test [file_path] [test_focus]`
**Example:** `/test HomeStore.swift` or `/test HomeStore.swift error handling`

**Core Philosophy:** Generate **high-quality, maintainable tests** focused on business value. Test quality > test quantity.

## 🎯 Test Prioritization (MANDATORY)

**Before generating tests, ask:**
1. What are the **critical user journeys** in this code?
2. What **errors** do users actually encounter?
3. Which edge cases **caused bugs before**?

**Generate tests in this order:**

**P0 (MUST) - Critical User Journeys**
- Complete flow from user action to business outcome
- Examples: Login success, Route capture + upload, Offline data loading

**P1 (SHOULD) - Error Handling**
- Only errors users encounter: network failures, invalid input
- Skip theoretical errors that never happen

**P2 (CONSIDER) - Edge Cases**
- ONLY if justified (caused bugs OR non-trivial logic >3 conditions)
- Ask user if edge cases are needed before generating

**P3 (SKIP) - Low Value Tests**
- Don't generate tests for: trivial computed properties, framework bindings, obvious logic

## Generated Test Structure

**Business Integration Tests (PRIORITIZE THESE):**
- Real repositories/services (higher business value)
- Mock only external dependencies (API, FileSystem)
- Test complete business scenarios
- Test data flow between layers

**Presentation Tests (Generate ONLY for TCA-specific logic):**
- Mock all dependencies
- Test UI behavior not covered by integration tests
- Skip if integration tests cover the scenario

**Test Data:**
- Use `.sample()` extensions
- Generate mocks/spies only when needed
- Keep test data minimal and focused

## ❌ DON'T Generate Tests For

- Trivial computed properties without logic
- SwiftUI framework bindings
- Obvious getters/setters
- Implementation details (method calls)
- Loading spinner visibility (unless caused bugs)

## ✅ DO Generate Tests For

- Complete user journeys with business outcomes
- Critical error handling (network, upload failures)
- Non-trivial edge cases (if justified)
- Business logic flow between layers

> **Testing Patterns**: See TCA Testing Best Practices in .cursor/rules for comprehensive testing patterns, pitfalls, and debugging strategies.

**Agent Used:** May invoke `ios-testing-specialist` agent for comprehensive test generation.

## 🚨 Critical Instructions for Agent

When generating tests:

1. **Ask First**: "Which scenarios are critical for this feature from business perspective?"
2. **Prioritize**: Start with P0 (critical journeys), then P1 (errors), ask before P2 (edge cases)
3. **Skip Low-Value**: Don't generate tests for trivial logic, framework code, or obvious behavior
4. **Focus on Outcomes**: Test business outcomes, not implementation details
5. **Integration > Presentation**: Prioritize business integration tests over isolated presentation tests
6. **Justify Edge Cases**: Before generating edge case test, explain why it's needed

**Example Good Test:**
```swift
func testUserCompletesRouteCaptureAndUploadSucceeds() async {
    // Tests complete user journey with business outcome
}
```

**Example Bad Test (DON'T GENERATE):**
```swift
func testButtonTapSendsAction() async {
    // Too granular, no business value
}
```

## Usage
```
/test [file_path] [test_focus]
```

## Parameters
- `file_path`: Path to the file to generate tests for (required)
- `test_focus`: Optional specific test scenario (e.g., "happy path", "error handling", "edge cases")
