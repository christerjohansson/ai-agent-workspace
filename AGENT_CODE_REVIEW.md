# AI Agent Instructions: Code Review Best Practices

## Overview
This document provides guidelines for AI agents performing code review tasks on web applications. Code review is critical for maintaining code quality, knowledge sharing, and preventing bugs.

## Code Review Process

### 1. Pre-Review Setup

```bash
# Fetch latest changes
git fetch origin

# Create review branch
git checkout -b review/feature-name

# Install dependencies
npm install
```

### 2. Review Checklist

#### Code Quality
- [ ] Code follows project style guide
- [ ] No console.log or debug statements left in code
- [ ] No hardcoded values (use environment variables)
- [ ] DRY principle applied (no code duplication)
- [ ] Proper error handling implemented
- [ ] Comments explain "why", not "what"

#### TypeScript/JavaScript
- [ ] TypeScript types are correctly defined
- [ ] No `any` types without justification
- [ ] Interfaces/types are properly exported
- [ ] Import statements are organized
- [ ] Naming conventions are consistent
- [ ] Functions are properly documented with JSDoc

#### React Best Practices
- [ ] Components are properly memoized if needed
- [ ] Props are typed with TypeScript
- [ ] Hooks are used correctly (dependencies, cleanup)
- [ ] No unnecessary re-renders
- [ ] Component composition is logical
- [ ] State management is appropriate

#### Testing
- [ ] Unit tests cover critical paths
- [ ] Test coverage is adequate (>80% target)
- [ ] Tests are descriptive and maintainable
- [ ] Edge cases are tested

#### Performance
- [ ] No performance regressions
- [ ] Images are optimized
- [ ] Large bundles are code-split
- [ ] Database queries are efficient
- [ ] No memory leaks

#### Security
- [ ] No SQL injection vulnerabilities
- [ ] Input is validated and sanitized
- [ ] Sensitive data is not logged
- [ ] Authentication/authorization is correct
- [ ] CORS headers are properly configured
- [ ] Dependencies have no known vulnerabilities

#### Accessibility (A11y)
- [ ] Semantic HTML is used
- [ ] ARIA labels are appropriate
- [ ] Keyboard navigation works
- [ ] Color contrast meets WCAG standards
- [ ] Forms are properly labeled

### 3. Review Commands

```bash
# View changes
git diff origin/main...HEAD

# View commit history
git log --oneline origin/main...HEAD

# Run linting
npm run lint
npm run lint -- --fix

# Run type checking
npm run type-check

# Run tests
npm run test
npm run test -- --coverage

# Build check
npm run build

# Performance check (if available)
npm run analyze
```

### 4. Review Comment Templates

#### Suggestion (Non-blocking)
```
💡 Suggestion: Consider using [approach] instead of [current approach]
Reason: [brief explanation]
Example: [code snippet if helpful]
```

#### Issue (Must fix)
```
⚠️ Issue: [Problem description]
Impact: [Why this matters]
Solution: [How to fix]
Reference: [Link to docs/issue if applicable]
```

#### Question
```
❓ Question: [Ask for clarification]
Context: [Why you're asking]
```

### 5. Approval Criteria

**Approve when:**
- ✅ All critical issues are resolved
- ✅ Code follows style guide
- ✅ Tests pass and coverage is adequate
- ✅ No performance regressions
- ✅ Documentation is updated
- ✅ Security concerns are addressed

**Request Changes when:**
- ❌ Critical bugs or security issues exist
- ❌ Code quality standards not met
- ❌ Tests are failing or inadequate
- ❌ TypeScript types are missing/incorrect
- ❌ Documentation is incomplete

## Automated Review Tools

### Pre-commit Hooks
```bash
npm install husky lint-staged --save-dev
npx husky install
npx husky add .husky/pre-commit "npm run lint-staged"
```

### GitHub Actions for CI/CD
```yaml
# .github/workflows/review.yml
name: Code Review

on: [pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm ci
      - run: npm run lint
      - run: npm run type-check
      - run: npm test
      - run: npm run build
```

## Common Issues and Fixes

### Issue: Large Functions
**Fix**: Break into smaller, testable functions
```typescript
// ❌ Before
function processUserData(user) {
  // 50 lines of logic
}

// ✅ After
function validateUser(user): boolean { }
function transformUserData(user): User { }
function saveUserToDatabase(user): Promise<void> { }
```

### Issue: Missing Error Handling
```typescript
// ❌ Before
const data = await fetch(url);

// ✅ After
try {
  const response = await fetch(url);
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  const data = await response.json();
} catch (error) {
  logger.error('Failed to fetch data:', error);
  throw error;
}
```

### Issue: Prop Drilling
```typescript
// ❌ Before - Props passed through multiple components
<GrandParent theme={theme} />
  <Parent theme={theme} />
    <Child theme={theme} />

// ✅ After - Use Context API
<ThemeProvider>
  <GrandParent />
    <Parent />
      <Child />
</ThemeProvider>
```

### Issue: Missing TypeScript Types
```typescript
// ❌ Before
const handleSubmit = (e) => { }
const user = { name: 'John', age: 30 };

// ✅ After
interface User {
  name: string;
  age: number;
}

const handleSubmit = (e: React.FormEvent<HTMLFormElement>): void => { }
const user: User = { name: 'John', age: 30 };
```

## Review Performance Benchmarks

- **Small PR** (< 200 lines): 15-30 minutes
- **Medium PR** (200-500 lines): 30-60 minutes
- **Large PR** (> 500 lines): 1-2 hours (consider requesting smaller PRs)

## Documentation for Reviewers

Update documentation when reviewing:
- [ ] README updated if needed
- [ ] API docs reflect changes
- [ ] Component Storybook stories updated
- [ ] Comments explain complex logic
- [ ] Changelog entry added

---

**Last Updated**: December 10, 2025
