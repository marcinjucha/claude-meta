# Run iOS Tests with DerivedData Cache

Run specific tests or entire test suite while preserving DerivedData for fast compilation:

**Test Execution:**
- Run specific test file by name
- Run specific test class
- Run specific test method
- Run all tests in target
- Preserves DerivedData (no clean build)
- Shows only relevant test output

**DerivedData Optimization:**
- Uses existing build cache (no clean)
- Fast incremental compilation
- Minimal rebuild time
- Preserves previous test builds

**Output:**
- Test results (pass/fail)
- Execution time per test
- Failure details with file:line
- Summary statistics

**Examples:**
```bash
# Run specific test file
/run-tests RouteListFeatureTests

# Run specific test class
/run-tests RouteListFeatureTests.RouteListFeatureTests

# Run specific test method
/run-tests RouteListFeatureTests.testLoadRoutesSuccess

# Run all tests
/run-tests
```

**Performance:**
- First run: ~30-60s (full build)
- Subsequent runs: ~5-10s (incremental)
- No DerivedData clean = faster iterations

## Usage
```
/run-tests [test_filter]
```

## Parameters
- `test_filter`: Optional test name filter (file, class, or method name)
  - Examples: "RouteListFeatureTests", "testLoadRoutesSuccess", "RouteList"
  - If omitted, runs all tests
