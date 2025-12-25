# Conventions

> **Instructions:** Define your project's coding standards and conventions here. All agents should follow these patterns.

---

## File Structure

```
project/
├── docs/                    # Documentation
│   ├── _AGENTS.md          # Agent coordination
│   ├── _VISION.md          # Product vision
│   ├── _ROADMAP.md         # Product roadmap
│   ├── _ARCHITECTURE.md    # Technical decisions
│   └── _CONVENTIONS.md     # This file
├── src/                     # Source code
│   ├── components/         # [Describe structure]
│   ├── lib/                # [Describe structure]
│   └── ...
├── tests/                   # Test files
└── ...
```

---

## Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| **Files (components)** | [PascalCase / kebab-case] | `UserProfile.tsx` |
| **Files (utilities)** | [camelCase / kebab-case] | `formatDate.ts` |
| **Files (tests)** | [Pattern] | `UserProfile.test.tsx` |
| **Directories** | [Pattern] | `user-management/` |
| **Components** | [Pattern] | `UserProfileCard` |
| **Functions** | [Pattern] | `getUserById` |
| **Constants** | [Pattern] | `MAX_RETRY_COUNT` |
| **Types/Interfaces** | [Pattern] | `UserProfile` |

---

## Code Style

### General
- [Tab vs spaces, indent size]
- [Line length limit]
- [Trailing commas preference]
- [Quote style]

### TypeScript
- [Strict mode: yes/no]
- [Any types: allowed/forbidden]
- [Type vs Interface preference]

### Comments
- [When to comment]
- [Comment style]
- [Doc comment format]

---

## Git Workflow

### Branch Naming
```
[type]/[short-description]

Examples:
feature/user-authentication
fix/login-redirect-bug
docs/api-documentation
```

### Commit Messages
```
type(scope): description

Examples:
feat(auth): add Google OAuth login
fix(dashboard): correct date formatting
docs(readme): update installation steps
test(users): add profile update tests
```

**Types:** feat, fix, docs, test, refactor, style, chore

### Pull Requests
- [Required reviewers]
- [PR description template]
- [Merge strategy: squash/merge/rebase]

---

## Testing

### Test File Location
- [Co-located with source / separate directory]
- [Naming pattern]

### Test Structure
```
describe('[Unit/Component Name]', () => {
  describe('[method/behavior]', () => {
    it('should [expected behavior]', () => {
      // Arrange
      // Act
      // Assert
    });
  });
});
```

### Coverage Requirements
- [Minimum coverage percentage]
- [Critical paths that must be tested]

---

## Documentation

### Code Documentation
- [When to add doc comments]
- [Format for function documentation]

### Project Documentation
- [Where docs live]
- [When to update docs]

---

## Error Handling

### Error Messages
- [User-facing vs internal errors]
- [Logging requirements]

### Error Patterns
```
// Example pattern
try {
  // operation
} catch (error) {
  // how to handle
}
```

---

## Security

### Secrets
- [Never commit secrets]
- [How to handle environment variables]

### Input Validation
- [Where to validate]
- [What to validate]

### Data Access
- [Authorization patterns]
- [Data exposure rules]

---

## Performance

### Guidelines
- [Bundle size considerations]
- [Query optimization rules]
- [Caching strategy]

---

## Accessibility

### Requirements
- [WCAG level target]
- [Required attributes]
- [Testing approach]

---

## Review Checklist

Before submitting code:

- [ ] Follows naming conventions
- [ ] Has appropriate tests
- [ ] No TypeScript errors
- [ ] No linting errors
- [ ] Documentation updated if needed
- [ ] No secrets in code
- [ ] Accessible (if UI)

---

> **Maintenance:** All agents should follow these conventions. Update this document when patterns evolve.
