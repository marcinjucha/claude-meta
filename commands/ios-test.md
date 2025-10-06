# Generate Tests for iOS + TCA

Automatically generate comprehensive tests for TCA features and Use Cases:

**Screen Tests:**
- Test setup with proper mocking
- State change validation
- Async behavior testing
- Action flow validation
- All dependencies mocked
- Timer and delayed effects testing
- Navigation testing

**Business Logic Tests:**
- Integration tests with real components where appropriate
- Reactive data flow testing
- Error handling scenarios
- Edge cases coverage

**Test Data:**
- Sample data generation
- Mocked dependencies
- Test helpers

**Best Practices:**
- Tests properly initialized
- All actions handled
- Proper test patterns followed
- No unnecessary test complexity

Generates complete, working tests ready to run.

**Agent Used:** May invoke `tca-developer` for TCA testing patterns.

## Usage
```
/test [file_path] [test_focus]
```

## Parameters
- `file_path`: Path to the file to generate tests for (required)
- `test_focus`: Optional specific test scenario (e.g., "happy path", "error handling", "edge cases")
