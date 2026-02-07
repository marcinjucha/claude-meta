# Why Over How - Content Quality Philosophy

**Purpose:** Ensure skill updates include context and rationale, not just implementation details. Every pattern needs WHY.

---

## Core Principle

**Priority:** WHY explanation > HOW implementation

Code syntax (HOW) is obvious to Claude. Context (WHY) is not.

**Without WHY:** Future developers don't understand importance → might remove or change pattern → reintroduce bugs

**With WHY:** Pattern becomes maintainable → developers understand consequences → pattern persists

---

## What is WHY?

**WHY includes:**

1. **Problem it solves** - What breaks without this pattern?
2. **Why approach chosen** - What alternatives were considered? Why rejected?
3. **Production impact** - Real incident, user complaint, measured numbers
4. **Consequences** - What happens if violated? (crash, memory leak, wrong data)

**WHY does NOT include:**

- Generic explanations (Claude knows)
- Syntax details (obvious)
- Architecture 101 (Claude knows)
- Time-sensitive info (version numbers, dates)

---

## Philosophy: Quality > Line Count

**Wrong approach:** Cut content to meet line count target

**Right approach:** Keep all critical WHY context, even if longer

**Sufficient > Comprehensive:**
- Focus on necessary WHY context, not exhaustive documentation
- 600 lines with sufficient WHY context > 300 lines missing critical information
- Signal-focused content matters more than brevity
- Line count is a guideline, not a constraint

---

## Pattern Transformation Examples

### Example 1: Resource Ownership

**❌ Without WHY (HOW only):**
```markdown
## Pattern: Resource in Component

Resource owned by LeafComponent:

\`\`\`pseudocode
struct LeafComponent {
    var resourceManager: ResourceController?
}
\`\`\`
```

**What's missing:** Why component? Why not root? What happens if wrong?

---

**✅ With WHY (Context + Impact):**
```markdown
## Pattern: Resource in Component (Not Root)

**Purpose:** Prevent memory leaks through proper ownership

**Why component ownership:**
- Leaf component knows navigation direction (forward vs back)
- Can use navigation state for conditional cleanup
- Root container can't distinguish navigation direction → always preserves resource

**Why NOT root:**
- Root container persists across entire flow
- Back navigation from child doesn't signal root to cleanup
- Result: Resource instance leaks on every back navigation

**Production impact:**
- Before fix: NMB leak per back navigation
- Symptom: Lower-end devices crashed after X navigations
- Root cause: Root container didn't know when to cleanup

**Implementation:**
\`\`\`pseudocode
struct LeafComponent {  // ← Leaf component, not root
    var resourceManager: ResourceController?

    onDisappear where isForwardNavigation:
        resourceManager.pause()  // Forward nav → preserve
        return

    onDisappear:
        resourceManager.dispose()  // Back nav → cleanup
        resourceManager = nil      // Release memory
        cancel(resourceSubscription)
}
\`\`\`

**Alternative considered:** Weak reference in root container
**Why rejected:** Framework doesn't provide reliable weak references to resource managers
```

**Value added by WHY:**
- Developer understands memory leak risk
- Developer won't move resource back to root (knows consequences)
- Alternative approach documented (rejected with reason)
- Production incident provides urgency

---

### Example 2: Service vs Component Pattern

**❌ Without WHY (HOW only):**
```markdown
## Service Pattern

Use Service when combining multiple data sources.

**Example:**
\`\`\`pseudocode
class DataCombinerService {
    let dataSource1: DataRepository
    let dataSource2: ContextRepository
}
\`\`\`
```

**What's missing:** Why combine? Why not orchestrator? What breaks if wrong?

---

**✅ With WHY (Context + Impact):**
```markdown
## Service Pattern: Combining Data Sources

**Purpose:** Break circular dependencies between data sources

**Why Service (not Orchestrator):**
- Orchestrator CAN'T directly depend on 3+ data sources (architecture rule)
- Data sources CAN'T depend on other data sources (creates cycles)
- Service CAN combine any data sources (designed for multi-source coordination)

**Problem it solves:**
DataRepository needs context history → must depend on ContextRepository
ContextRepository needs data context → must depend on DataRepository
→ Circular dependency → initialization crash

**Why circular dependency crashes:**
Language initializers require all dependencies resolved before use
Circular dependency = infinite loop during initialization
App crashes at startup (100% crash rate in version X)

**Solution:**
Service combines both data sources (breaks cycle):

\`\`\`pseudocode
class DataCombinerService {
    inject dataRepository: DataRepository
    inject contextRepository: ContextRepository

    // Combines data from both (no circular dependency)
    function getDataWithContext(id: String) -> Observable<DataWithContext> {
        return combine(
            dataRepository.getData(id),
            contextRepository.getContext(id)
        ).map { data, context ->
            DataWithContext(data: data, status: context.status)
        }
    }
}
\`\`\`

**Production incident - version X:**
- DataRepository → ContextRepository dependency added
- App crashed at startup (100% crash rate)
- Root cause: Circular dependency during initialization
- Fix: Created DataCombinerService to break cycle
- Result: 0% crash rate after fix

**Alternative considered:** Event-based communication between repositories
**Why rejected:** Complex, harder to test, same data needs reactive stream
```

**Value added by WHY:**
- Developer understands circular dependency risk
- Developer knows when to create Service (3+ sources, prevent cycles)
- Production incident shows real consequences
- Alternative documented with rejection reason

---

### Example 3: Spatial Tolerance Parameter

**❌ Without WHY (HOW only):**
```markdown
## Spatial Processing

Use Xcm tolerance for deduplication.

\`\`\`pseudocode
let tolerance = X_CM
\`\`\`
```

**What's missing:** Why Xcm? What happens if too small? Too large?

---

**✅ With WHY (Context + Impact):**
```markdown
## Spatial Deduplication (Xcm Tolerance)

**Purpose:** Prevent same physical entity from creating multiple detections

**Why Xcm tolerance:**
- Sensor has ±Ycm noise per measurement
- Same entity detected at slightly different positions each frame
- Without tolerance: Same entity creates N detections (noise causes duplicates)
- Too small (< Ycm): Noise alone creates duplicates
- Too large (> Zcm): Different entities merged incorrectly

**Why Xcm specifically:**
- Xcm = 3× sensor noise (±Ycm) → compensates for measurement variance
- Allows slight movement between frames
- Tested range: Acm-Bcm
- Acm: Still showed duplicates (2-3 per entity)
- Xcm: Correct deduplication (N unique from N physical)
- Bcm: Merged different entities (M unique from N physical)

**Production validation - version Y:**
- Without deduplication: Large number entries from N physical entities
- With Xcm tolerance: N unique entries (correct!)
- User complaints: "too many duplicates" → resolved

**Implementation:**
\`\`\`pseudocode
// Check if detection is near existing entry
function isNear(location: Vector3, tolerance: Float = X_CM) -> Bool {
    let distance = calculateDistance(self.location, location)
    return distance < tolerance
}

// Deduplicate during ingestion
if let existing = existingEntry(near: detection.location) {
    existing.locations.append(detection.location)  // Update existing
} else {
    entries.append(detection)  // Truly new entity
}
\`\`\`

**Performance impact:**
- Without: Large number entries → UI laggy
- With: N entries → UI smooth
- Frame rate: X FPS → Y FPS (fewer render calls)

**Tuning guide:**
- Small entities (< Acm spacing): A-Bcm tolerance
- Standard entities (B-Ccm spacing): Xcm tolerance (default)
- Large entities (> Ccm spacing): C-Dcm tolerance

**Alternative considered:** Advanced filtering algorithm for position stability
**Why rejected:** Complexity not justified (Xcm tolerance sufficient for requirements)
```

**Value added by WHY:**
- Developer understands why Xcm (not arbitrary)
- Developer knows testing was done (range exploration)
- Production incident shows real user complaints
- Performance impact measured
- Tuning guide for different scenarios
- Alternative documented with rejection reason

---

## When to Include WHY

**Always include WHY for:**

1. **Non-obvious patterns** - Anything that might seem arbitrary or unusual
2. **Production bugs** - Every anti-pattern needs incident context
3. **Thresholds/numbers** - Why this specific value? What happens if different?
4. **Design decisions** - Why this approach over alternatives?
5. **Architecture rules** - Why this layer? Why not another?

**Example triggers:**
- "Why is resource in component, not root?"
- "Why Xcm tolerance specifically?"
- "Why Service instead of Orchestrator?"
- "Why sharing mechanism on this stream?"
- "Why N-second time window?"

---

## Structure Template

**Standard WHY structure for patterns:**

```markdown
## Pattern: [Name]

**Purpose:** [One sentence - what problem does this solve?]

**Why [approach]:**
- [Reason 1 - technical constraint]
- [Reason 2 - architecture rule]
- [Reason 3 - production requirement]

**Why NOT [alternative]:**
- [Why alternative A fails]
- [Why alternative B inadequate]

**Production impact:**
- Before fix: [Symptom, numbers, user complaints]
- After fix: [Improvement, metrics]
- Root cause: [Technical explanation]

**Implementation:**
\`\`\`pseudocode
[Code example with inline comments explaining critical parts]
\`\`\`

**Alternative considered:** [Other approach]
**Why rejected:** [Reason]
```

---

## Anti-Pattern: Missing WHY

**Common mistake:** Pattern documented without context

**Example:**
```markdown
❌ BAD (no WHY):
## Memory Management
Use weak references instead of strong references.

✅ GOOD (includes WHY):
## Memory Management: Weak Reference Pattern

**Purpose:** Prevent retain cycles in subscription chains

**Why weak references:**
Standard strong capture creates cycle if publisher stored in same object
→ Memory leak (objects never deallocated)

**Production impact - version X:**
- Strong capture caused NMB leak per session
- Memory grew continuously during operation
- Lower-end devices ran out of memory after N minutes

**Implementation:**
\`\`\`pseudocode
// ❌ WRONG - Strong capture
stream.subscribe { self in
    self.handle(value)  // self retained by closure, closure retained by self → cycle
}

// ✅ CORRECT - Weak capture
stream.subscribeWeak(target: self) { strongSelf, value in
    strongSelf.handle(value)  // utility handles weak→strong conversion
}
\`\`\`

**Alternative considered:** Manual weak capture with guard
**Why rejected:** Easy to forget guard, utility enforces pattern
```

---

## Quick Checklist

**Before finalizing skill update, verify:**

- [ ] Every pattern includes **Purpose** (what problem solved)
- [ ] Non-obvious choices include **Why [approach]** (reason for design)
- [ ] Alternatives documented with **Why rejected** (show thinking)
- [ ] Production incidents include **Impact** (numbers, symptoms, complaints)
- [ ] Numbers/thresholds include **Why this value** (testing range, reasoning)
- [ ] Anti-patterns include **Production context** (when it happened, how fixed)

---

## Remember

**Signal = WHY-focused content**
- Claude knows HOW to write code in most languages
- Claude doesn't know WHY your project chose specific patterns
- Production context is ALWAYS valuable (incidents, bugs, complaints)
- Complete WHY context > brevity

**Quality First:**
- 600 lines with complete WHY > 300 lines missing context
- Better to include full explanation than cut for line count
- Every "Why not?" is valuable (shows alternatives considered)

**Future-proof:**
- Pattern with WHY survives refactoring (devs understand importance)
- Pattern without WHY gets removed (seems arbitrary)
- Production context prevents regression (nobody wants to reintroduce bug)
