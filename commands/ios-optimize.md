# Optimize iOS + TCA Performance

Analyze iOS/TCA code for performance optimization:

**Screen Performance:**
- State efficiency (minimal state, computed properties)
- Effect optimization (proper cancellation, avoid duplicates)
- Data stream efficiency (combine, debounce, throttle)
- Collection updates optimization
- Reduce logic complexity (avoid heavy computations)

**SwiftUI Performance:**
- View rendering optimization (minimize body executions)
- Layout performance (avoid GeometryReader abuse)
- Image loading and caching
- List/ScrollView performance (LazyVStack, prefetching)

**iOS-Specific:**
- Main thread blocking (move work to background)
- Memory usage (reduce allocations, use value types)
- GRDB query optimization (indexes, batch operations)
- Network performance (request batching, caching)
- Startup time optimization

**General:**
- Algorithmic complexity (O(n²) → O(n log n))
- Memory leaks (retain cycles, uncanceled subscriptions)
- I/O operations (batch writes, async reads)

Provides specific optimizations with measurable improvements (FPS, memory, load time).

> **Performance Patterns**: See TCA Essentials and Critical Patterns in .cursor/rules for TCA-specific performance optimizations.

**Agent Used:** May invoke `tca-developer` for TCA-specific optimizations.

## Usage
```
/optimize [file_path] [performance_target]
```

## Parameters
- `file_path`: Path to the file to optimize (required)
- `performance_target`: Optional specific goal (e.g., "reduce load time", "fix scrolling jank")