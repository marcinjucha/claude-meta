# Commit Message Structure - Template vs Natural Prose

Universal patterns for writing effective commit messages using Signal vs Noise and WHY > HOW principles.

---

## Anti-Pattern: Template with Sections

### Structure

```
<type>: <subject>

Business Impact:
- [Bullet point 1]
- [Bullet point 2]

Technical Scope:
- Layers: [Layer names]
- Files: [File list]
- Test Coverage: [Line counts]

Changes:
- [Component 1]: [What changed]
- [Component 2]: [What changed]

Implementation Details:
- [HOW implementation works]

Performance Impact:
- [Metrics or "N/A"]

Risk Assessment:
- Risk Level: [LOW/MEDIUM/HIGH]
- Breaking Changes: [YES/NO]
- Rollback Plan: [Description]
```

### Why This is Bad

**❌ Template sections add NOISE:**
- "Files:" → Git stat already shows
- "Test Coverage: +X lines" → Git diff --stat already shows
- "Changes:" list → Git diff already shows
- "Performance Impact:" → Often trivial or belongs in PR
- "Risk Assessment:" → Belongs in PR review template
- "Rollback Plan:" → Usually obvious ("revert commit")

**❌ HOW instead of WHY:**
- "Implementation Details:" section describes mechanics, not rationale
- Missing business context (why this approach chosen)
- Missing decision rationale (why this over alternatives)

**❌ Rigid structure prevents natural flow:**
- Forces information into boxes even when not relevant
- Encourages completeness over insight (fill every section)
- Reads like form-filling, not storytelling

---

## Recommended: Natural Prose with WHY Focus

### Structure

```
<type>: <subject>

[1-2 sentences describing affected areas/layers and WHY context. Max 500 chars.]
```

**Body constraints:**
- **Length:** 250-500 characters total
- **Structure:** 1-2 sentences covering all affected areas
- **Content:** Mention specific layers/areas changed (db, business logic, presentation, API, etc.)
- **Focus:** WHY context + area identification (not exhaustive HOW)

### Why This is Better

**✅ Natural flow:**
- Paragraphs tell a story with logical progression
- No forced sections to fill
- Emphasizes important information, skips obvious details

**✅ WHY-focused:**
- Explains business context (why feature/fix needed)
- Describes technical rationale (why this approach over alternatives)
- Provides bug context (why bug occurred, why fix correct)

**✅ Signal over Noise:**
- No file names (git shows)
- No line counts (git shows)
- No "Changes:" list (git shows)
- No risk levels (PR review concern)

---

## Transformation Example

### Before: Template Version

```
feat: Implement User Authentication with OAuth

Summary:
Add OAuth authentication flow.

Business Impact:
- Users can log in with third-party providers
- Reduces password management burden
- Improves security with delegated authentication

Technical Scope:
- Layers: Authentication, API, UI
- Files: AuthService.swift, LoginView.swift, TokenStorage.swift
- Dependencies: OAuthKit framework
- Test Coverage: +150 lines

Changes:
- AuthService: Implement OAuth flow with token exchange
- LoginView: Add OAuth provider buttons
- TokenStorage: Securely store access/refresh tokens
- Tests: Cover success, failure, and edge cases

Implementation Details:
- Use authorization code flow with PKCE
- Store tokens in keychain with biometric protection
- Refresh tokens 5 minutes before expiry

Performance Impact:
- OAuth flow: 2-3 seconds average
- Negligible impact on app launch

Risk Assessment:
- Risk Level: MEDIUM (new authentication path)
- Breaking Changes: NO (adds new option, doesn't remove existing)
- Rollback Plan: Revert commit, users fall back to password auth
```

### After: Natural Prose Version (Concise, 250-500 chars)

```
feat: Implement OAuth Authentication Flow

OAuth authentication required for third-party provider integration without
password storage. Updated authentication layer (AuthService), presentation
layer (LoginView), and token storage (keychain) with PKCE flow to prevent
authorization code interception. (252 chars)
```

### What Changed

**Removed NOISE:**
- ❌ File names (git stat shows)
- ❌ Line counts (git diff --stat shows)
- ❌ "Changes:" list (git diff shows)
- ❌ Performance metrics (trivial, belongs in PR if critical)
- ❌ Risk assessment (PR review concern)
- ❌ Verbose explanations (reduced from 4 paragraphs to 2 sentences)

**Added SIGNAL:**
- ✅ Why OAuth needed (providers don't expose passwords)
- ✅ Specific areas/layers affected (authentication, presentation, token storage)
- ✅ Why PKCE (prevents code interception)
- ✅ Concise WHY context within 250-500 char limit

**Improved structure:**
- ✅ Concise 1-2 sentences (252 chars vs 600+ chars)
- ✅ Area/layer identification (AuthService, LoginView, keychain)
- ✅ WHY-focused (rationale, not mechanics)
- ✅ Sufficient context without verbose explanations

---

## Pattern: Concise Body (1-2 Sentences, 250-500 chars)

### Goal

Pack WHY context + area identification into 1-2 sentences within 250-500 character limit.

### Structure Options

**Option 1: Single sentence (single area or tightly related areas):**
```
[Business WHY]. [Technical approach with areas mentioned] [to achieve outcome].
```

**Option 2: Two sentences (multiple areas or complex change):**
```
[Business WHY or problem statement]. [Technical approach] [area 1], [area 2],
and [area 3] [to achieve outcome or rationale].
```

### Examples by Change Type

**Feature (multiple areas):**
```
OAuth authentication required for third-party provider integration without
password storage. Updated authentication layer (AuthService), presentation
layer (LoginView), and token storage (keychain) with PKCE flow to prevent
authorization code interception. (252 chars)
```

**Bug fix (single area):**
```
Row-level security policy queried same table it protected, causing infinite
recursion. Updated policy logic to use cached role check instead of
re-querying user_roles table. (188 chars)
```

**Refactor (multiple areas, two sentences):**
```
600-line UploadService mixed business logic, file validation, and API calls.
Extracted validation layer (FileValidator), storage layer (S3Adapter), and
business logic (UploadOrchestrator) to separate concerns and enable
independent testing. (276 chars)
```

**Performance optimization (specific areas):**
```
N+1 queries in activity feed caused 3-second load times. Added eager loading
in FeedRepository and query result caching in ActivityService to reduce
database roundtrips from 50+ to 3. (187 chars)
```

### Template Patterns

**Business WHY + Technical approach + Areas:**
```
[Feature/fix name] [required/needed] because [business reason]. [Updated/Added/
Modified] [layer/area 1] ([Component]), [layer/area 2] ([Component]), and
[layer/area 3] ([Component]) [with/using] [technical approach] to [outcome].
```

**Problem statement + Solution with areas:**
```
[Problem description with impact]. [Updated/Fixed/Extracted] [technical
approach] in [layer/area 1] ([Component]) and [layer/area 2] ([Component])
[to achieve outcome or prevent issue].
```

### Area/Layer Naming

**Common layers to mention:**
- **Database:** db layer, schema, migration, RLS policy, query logic
- **Business logic:** service layer, domain logic, orchestrator, validator
- **Presentation:** UI layer, view, component, screen
- **API:** endpoint, controller, route handler, middleware
- **Storage:** file storage, cache layer, token storage, session store
- **Integration:** external API client, webhook handler, third-party adapter

**Format:** `[layer/area] ([specific component if helpful])`

**Examples:**
- "authentication layer (AuthService)"
- "database schema (user_roles table)"
- "presentation layer (LoginView)"
- "API endpoints (/oauth/callback)"
- "business logic (UploadOrchestrator)"

---

## Decision Framework: What to Include (Within 250-500 chars)

### Always Include (SIGNAL)

✅ **Business context (condensed)**
- Why feature/fix needed (1 clause)
- Problem being solved (brief)

✅ **Affected areas/layers**
- Which layers/components changed
- Format: `[layer] ([Component])`
- Examples: "authentication layer (AuthService)", "database schema (users table)"

✅ **Technical rationale (condensed)**
- Why this approach (brief phrase)
- Key decision rationale (not exhaustive)

✅ **Bug context (if applicable, brief)**
- Root cause (1 clause)
- Why fix prevents recurrence

### Never Include (NOISE)

❌ **File names/paths**
- Git stat shows this

❌ **Line counts**
- Git diff --stat shows this

❌ **"Changes:" lists**
- Git diff shows exact changes

❌ **HOW implementation (exhaustive)**
- Code shows implementation mechanics
- Brief technical approach OK if non-obvious

❌ **Risk assessment**
- Belongs in PR review template

❌ **Rollback plans**
- Usually obvious (revert commit)

❌ **Performance metrics**
- Belongs in PR description (unless critical context)

❌ **Verbose explanations**
- 250-500 char limit forces brevity

### Prioritization Within 500-Char Limit

**Priority 1 (Must have):**
1. Business WHY (1 sentence or clause)
2. Affected areas/layers (components list)

**Priority 2 (Should have if space):**
3. Technical rationale (brief phrase)
4. Key outcome or prevention (brief phrase)

**Priority 3 (Nice to have if space):**
5. Edge case handling (if critical)
6. Platform alignment note (if coordinating)

**Strategy:** Start with Priority 1, add Priority 2, check char count, add Priority 3 only if under 400 chars.

---

## 3-Question Filter Application

Before including any information, ask:

1. **Actionable?** Can future developer act on this when debugging?
2. **Impactful?** Would lack of this cause confusion or wrong decisions?
3. **Non-Obvious?** Is this insight non-trivial?

**If NO to all three → Remove it (NOISE)**

### Example: File Names

- Actionable? ❌ (Git stat provides file list)
- Impactful? ❌ (No confusion from missing this)
- Non-Obvious? ❌ (Trivial information)
→ **Remove**

### Example: Technical Rationale

- Actionable? ✅ (Future dev understands why approach chosen)
- Impactful? ✅ (Without rationale, might choose wrong approach in similar situation)
- Non-Obvious? ✅ (Not obvious why this over alternatives)
→ **Include**

---

## Key Principles

1. **Natural prose > Template sections** - Tell a story, don't fill a form
2. **WHY > HOW** - Explain rationale, not implementation mechanics
3. **SIGNAL > NOISE** - Non-obvious insights, not git-redundant info
4. **Context > Status** - Business/technical context, not current state
5. **Paragraphs flow logically** - Business → Technical → Operational → Cross-cutting

---

## Common Mistakes

### Mistake 1: Listing Files in Message

❌ Bad:
```
Files:
- AuthService.swift
- LoginView.swift
- TokenStorage.swift
```

✅ Fix: Remove file list (git stat shows this)

### Mistake 2: "Changes:" List

❌ Bad:
```
Changes:
- AuthService: Add OAuth flow
- LoginView: Add provider buttons
- TokenStorage: Store tokens
```

✅ Fix: Remove "Changes:" list (git diff shows exact changes)

### Mistake 3: HOW Instead of WHY

❌ Bad:
```
Implementation:
- Use authorization code flow
- Store tokens in keychain
- Refresh every 55 minutes
```

✅ Fix: Explain WHY (why authorization code, why keychain, why 55min)

### Mistake 4: Risk Assessment in Message

❌ Bad:
```
Risk Level: MEDIUM
Breaking Changes: NO
Rollback Plan: Revert commit
```

✅ Fix: Remove risk assessment (belongs in PR template)

### Mistake 5: Template Sections for Completeness

❌ Bad:
```
Performance Impact: N/A
```

✅ Fix: Skip section entirely if not applicable (don't fill for completeness)

---

## Summary

**Template approach:**
- Rigid structure
- Forces completeness over insight
- Mixes SIGNAL with NOISE
- HOW-focused

**Natural prose approach:**
- Logical flow
- Emphasizes important information
- Pure SIGNAL (no NOISE)
- WHY-focused

**Use natural prose with WHY focus for effective commit messages.**
