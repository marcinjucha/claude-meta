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

[Paragraph 1: Business context - why this change matters]

[Paragraph 2: Technical decision with rationale - why this approach]

[Paragraph 3: Additional context - bug fixes, edge cases, constraints]

[Paragraph 4 (optional): Cross-cutting concerns - platform alignment, migration notes]
```

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

### After: Natural Prose Version

```
feat: Implement OAuth Authentication Flow

OAuth authentication required because third-party identity providers (Google,
Microsoft, etc.) don't expose passwords to apps. Delegating authentication to
providers improves security (no password storage/management) and reduces user
friction (single sign-on across services).

Authorization code flow with PKCE chosen over implicit flow because implicit
flow deprecated for security reasons (token exposure in browser history).
PKCE prevents authorization code interception without adding server-side
complexity.

Token refresh 5 minutes before expiry prevents authentication failures during
long-running operations. Without proactive refresh, operations spanning token
lifetime would fail mid-execution, forcing user to re-authenticate and lose
progress.

Keychain storage with biometric protection ensures tokens survive app
reinstalls while preventing unauthorized access. Access tokens in user
defaults or in-memory storage would expose credentials to backups or memory
dumps.
```

### What Changed

**Removed NOISE:**
- ❌ File names (git stat shows)
- ❌ Line counts (git diff --stat shows)
- ❌ "Changes:" list (git diff shows)
- ❌ Performance metrics (trivial, belongs in PR if critical)
- ❌ Risk assessment (PR review concern)

**Added SIGNAL:**
- ✅ Why OAuth needed (providers don't expose passwords)
- ✅ Why authorization code flow (implicit flow deprecated)
- ✅ Why PKCE (prevents code interception)
- ✅ Why proactive token refresh (prevents mid-operation failures)
- ✅ Why keychain with biometric (survives reinstall, prevents unauthorized access)

**Improved structure:**
- ✅ Natural paragraphs (business → technical → operational → security)
- ✅ WHY-focused (rationale, not mechanics)
- ✅ Non-obvious insights (not clear from reading code)

---

## Pattern: WHY-Focused Paragraphs

### Paragraph 1: Business Context

**What to include:**
- Why feature/fix needed from user/business perspective
- Problem being solved
- Impact if not addressed

**Template:**
```
[Feature/Fix name] [needed/required] because [business reason].
[Expanded context on user impact or business requirement].
```

**Example:**
```
OAuth authentication required because third-party identity providers don't
expose passwords to apps. Delegating authentication improves security (no
password storage) and reduces user friction (single sign-on).
```

### Paragraph 2: Technical Decision with Rationale

**What to include:**
- Technical approach chosen
- Why this approach over alternatives
- Trade-offs considered

**Template:**
```
[Technical approach] chosen over [alternative] because [rationale].
[Expanded context on trade-offs or constraints].
```

**Example:**
```
Authorization code flow with PKCE chosen over implicit flow because implicit
flow deprecated for security reasons (token exposure in browser history).
PKCE prevents authorization code interception without adding server-side
complexity.
```

### Paragraph 3: Operational/Bug Context

**What to include:**
- Bug root cause (if fixing bug)
- Edge cases handled
- Operational requirements (timing, caching, cleanup)

**Template:**
```
[Operational decision] prevents [problem]. Without [this approach],
[negative consequence].
```

**Example:**
```
Token refresh 5 minutes before expiry prevents authentication failures during
long-running operations. Without proactive refresh, operations spanning token
lifetime would fail mid-execution, forcing user re-authentication.
```

### Paragraph 4 (Optional): Cross-Cutting Concerns

**What to include:**
- Platform alignment (if applicable)
- Migration notes (if breaking change)
- Security considerations
- Performance implications (if significant)

**Template:**
```
[Implementation detail] ensures [quality attribute]. [Expanded context on
why this matters for maintainability/security/performance].
```

**Example:**
```
Keychain storage with biometric protection ensures tokens survive app
reinstalls while preventing unauthorized access. Access tokens in user
defaults would expose credentials to backups or memory dumps.
```

---

## Decision Framework: What to Include

### Always Include (SIGNAL)

✅ **Business context**
- Why feature/fix needed
- User/business impact
- Problem being solved

✅ **Technical rationale**
- Why this approach chosen
- Alternatives considered
- Trade-offs evaluated

✅ **Non-obvious decisions**
- Architecture choices requiring explanation
- Edge case handling
- Timing/sequencing requirements

✅ **Bug context (if applicable)**
- Root cause analysis
- Why bug occurred
- Why fix prevents recurrence

### Never Include (NOISE)

❌ **File names/paths**
- Git stat shows this

❌ **Line counts**
- Git diff --stat shows this

❌ **"Changes:" lists**
- Git diff shows exact changes

❌ **HOW implementation**
- Code shows implementation mechanics

❌ **Risk assessment**
- Belongs in PR review template

❌ **Rollback plans**
- Usually obvious (revert commit)

❌ **Performance metrics (unless critical)**
- Belongs in PR description or docs

### Consider Including (Context-Dependent)

⚠️ **Platform alignment**
- Include if coordinating across platforms
- Skip if platform-specific implementation

⚠️ **Migration notes**
- Include if breaking change
- Skip if backward compatible

⚠️ **Security implications**
- Include if security-critical decision
- Skip if standard secure practice

⚠️ **Performance implications**
- Include if significant impact (>10% change)
- Skip if negligible or optimization

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
