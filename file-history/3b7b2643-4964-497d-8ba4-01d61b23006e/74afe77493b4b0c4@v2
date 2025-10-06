# Trace Data Flow Through Layers

Analyze how data flows through Clean Architecture layers:

**Data Flow Analysis:**
- View → TCA Store → Use Case → Service → Repository → Database/API
- Complete dependency chain visualization
- Layer responsibility mapping
- Data transformation points

**Architecture Validation:**
- Verify proper layer separation
- Detect layer skipping (Presentation → Data)
- Identify dependency cycles
- Check Repository → Repository dependencies

**Performance Insights:**
- Find redundant data fetches
- Identify N+1 query problems
- Spot inefficient Publishers chains
- Detect unnecessary state updates

**Dependency Graph:**
- Which Use Cases depend on which Services
- Which Services combine which Repositories
- Which Repositories access which data sources
- External dependencies (API, Database, FileSystem)

**Use Cases:**
- Understanding complex features (onboarding new developers)
- Debugging data flow issues (data not updating)
- Architecture review (finding violations)
- Performance investigation (slow screens)

Provides visual representation and detailed explanation of complete data flow.

**Agent Used:** May invoke `ios-architect` for architecture analysis.

## Usage
```
/trace [file_path] [focus]
```

## Parameters
- `file_path`: Path to the file to trace (required, usually a View or Store)
- `focus`: Optional specific concern (e.g., "route data", "user authentication", "performance")
