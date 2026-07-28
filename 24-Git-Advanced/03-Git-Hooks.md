# Git Hooks

[![Category: Reference](https://img.shields.io/badge/category-Reference-808080)](.)

 occur (commit, push, merge, etc.). They allow you to enforce policies, automate tasks, and integrate with other tools.

## Why Do We Need It?

- **Code quality**: Automatically lint, format, and test code before commits
- **Enforce policies**: Ensure commit messages follow conventions
- **Automation**: Run tests, deployments, notifications
- **Security**: Prevent secrets from being committed
- **Consistency**: Ensure team standards are followed

## How It Works
Git hooks are stored in `.git/hooks/` and are executed by Git during specific events:

### Git Hooks Flow

```text
┌─────────────────────────────────────────────────────────────────┐
│                    Git Hooks Execution Flow                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Client-Side Hooks                                               │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────────┐ │
│  │  pre-commit │───▶│  commit-msg │───▶│  post-commit        │ │
│  │  (lint)     │    │  (validate) │    │  (notify)           │ │
│  └─────────────┘    └─────────────┘    └─────────────────────┘ │
│                                                                 │
│  Server-Side Hooks                                               │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────────┐ │
│  │  pre-receive│───▶│  update     │───▶│  post-receive       │ │
│  │  (validate) │    │  (per branch│    │  (deploy/notify)    │ │
│  └─────────────┘    └─────────────┘    └─────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘

```

## Code Examples

### Pre-commit Hook

```bash
#!/bin/sh
# .git/hooks/pre-commit

# Run linter
echo "Running linter..."
npm run lint

# Check if linting failed
if [ $? -ne 0 ]; then
  echo "Linting failed. Commit aborted."
  exit 1
fi

# Run tests
echo "Running tests..."
npm test

# Check if tests failed
if [ $? -ne 0 ]; then
  echo "Tests failed. Commit aborted."
  exit 1
fi

echo "All checks passed!"
exit 0

```

### Commit-msg Hook

```bash
#!/bin/sh
# .git/hooks/commit-msg

# Validate commit message format
commit_msg=$(cat "$1")

# Check for conventional commits format
pattern="^(feat|fix|docs|style|refactor|test|chore|ci|build|perf)(\(.+\))?: .{1,72}"

if ! echo "$commit_msg" | grep -qE "$pattern"; then
  echo "ERROR: Commit message does not follow Conventional Commits format."
  echo "Expected: type(scope): description"
  echo "Example: feat(auth): add login functionality"
  exit 1
fi

# Check for length
if [ ${#commit_msg} -gt 100 ]; then
  echo "ERROR: Commit message too long (max 100 characters)."
  exit 1
fi

exit 0

```

### Pre-push Hook

```bash
#!/bin/sh
# .git/hooks/pre-push

# Run tests before push
echo "Running tests before push..."
npm test

if [ $? -ne 0 ]; then
  echo "Tests failed. Push aborted."
  exit 1
fi

# Check for secrets
echo "Checking for secrets..."
if grep -rE "(password|secret|api_key|token)" . --include="*.{js,ts,jsx,tsx,json,env}"; then
  echo "ERROR: Potential secrets found in code."
  exit 1
fi

exit 0

```

### Post-merge Hook

```bash
#!/bin/sh
# .git/hooks/post-merge

# Install dependencies after merge
echo "Installing dependencies..."
npm install

# Run migrations if needed
echo "Checking for migrations..."
if [ -f "migrations/pending" ]; then
  echo "Running migrations..."
  npm run migrate
fi

exit 0

```

### Using Husky

```bash
# Install Husky
npm install husky --save-dev

# Initialize Husky
npx husky install

# Add prepare script to package.json
# "prepare": "husky install"

# Create pre-commit hook
npx husky add .husky/pre-commit "npm run lint"

# Create commit-msg hook
npx husky add .husky/commit-msg "npx commitlint --edit $1"

# Create pre-push hook
npx husky add .husky/pre-push "npm test"

```

### Husky Configuration

```json
// package.json
{
  "scripts": {
    "prepare": "husky install",
    "lint": "eslint src/",
    "test": "jest",
    "format": "prettier --write ."
  },
  "devDependencies": {
    "husky": "^8.0.0",
    "lint-staged": "^13.0.0",
    "@commitlint/cli": "^17.0.0",
    "@commitlint/config-conventional": "^17.0.0"
  }
}

```

### lint-staged Configuration

```json
// .lintstagedrc.js
module.exports = {
  "*.{js,jsx,ts,tsx}": [
    "eslint --fix",
    "prettier --write",
    "jest --findRelatedTests"
  ],
  "*.{css,scss,less}": [
    "stylelint --fix",
    "prettier --write"
  ],
  "*.{json,md}": [
    "prettier --write"
  ]
};

```

### Commitlint Configuration

```javascript
// commitlint.config.js
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [
      2,
      'always',
      [
        'feat',     // New feature
        'fix',      // Bug fix
        'docs',     // Documentation
        'style',    // Formatting
        'refactor', // Code restructuring
        'test',     // Tests
        'chore',    // Maintenance
        'ci',       // CI/CD
        'build',    // Build system
        'perf'      // Performance
      ]
    ],
    'subject-max-length': [2, 'always', 72],
    'body-max-line-length': [1, 'always', 100]
  }
};

```

### Server-Side Hooks

```bash
#!/bin/sh
# hooks/pre-receive (server-side)

# Read commits from stdin
while read oldrev newrev refname; do
  # Check for large files
  git diff --name-only $oldrev $newrev | while read file; do
    size=$(git cat-file -s $newrev:$file 2>/dev/null || echo 0)
    if [ $size -gt 10485760 ]; then  # 10MB
      echo "ERROR: File $file is too large (${size} bytes)."
      exit 1
    fi
  done

  # Check for branch naming
  if [[ $refname == refs/heads/main ]] || [[ $refname == refs/heads/develop ]]; then
    # Require PR for main/develop
    echo "Direct pushes to $refname are not allowed."
    echo "Please create a Pull Request."
    exit 1
  fi
done

exit 0

```

### Custom Hook Examples

```bash
#!/bin/sh
# .git/hooks/prepare-commit-msg

# Add branch name to commit message
branch=$(git rev-parse --abbrev-ref HEAD)
if [ "$branch" != "main" ] && [ "$branch" != "develop" ]; then
  sed -i.bak -e "1s/^/[$branch] /" "$1"
fi

```

## Real-World Use Cases

1. **Code quality**: Linting, formatting, type checking before commits

2. **Testing**: Running tests before push

3. **Security**: Preventing secrets from being committed

4. **Documentation**: Auto-generating changelogs

5. **Deployment**: Triggering deployments on push

6. **Notifications**: Alerting team on important changes

## Common Mistakes

1. **Not making hooks executable**: `chmod +x .git/hooks/hook-name`

2. **Hardcoding paths**: Use relative paths or Git commands

3. **Not handling errors properly**: Exit with non-zero status on failure

4. **Ignoring performance**: Keep hooks fast

5. **Not testing hooks**: Test thoroughly before team adoption

6. **Overcomplicating**: Start simple, add complexity as needed

7. **Not documenting**: Team should know about hooks

## Best Practices

1. **Keep hooks fast**: < 5 seconds for pre-commit

2. **Fail fast**: Check critical things first

3. **Provide clear error messages**: Help developers fix issues

4. **Use Husky for management**: Easier team collaboration

5. **Version control hooks**: Store in `.husky/` directory

6. **Make hooks skippable**: `--no-verify` for emergencies

7. **Test hooks thoroughly**: Before committing to repository

8. **Document hook purpose**: Team understanding

## Performance Considerations

- **Pre-commit**: Should be fast, avoid heavy operations
- **Pre-push**: Can be slower, runs full test suite
- **Server hooks**: Can be slower, but affect all pushes
- **Async operations**: Consider background processing
- **Caching**: Cache results for repeated operations

## Summary
Git hooks are powerful for automating workflows and enforcing standards. Use Husky for easy management, lint-staged for performance, and commitlint for message validation. Keep hooks fast, provide clear feedback, and document their purpose for team adoption.

---

## Cheat Sheet
```text
GIT HOOKS CHEAT SHEET
============================================================

COMMON PATTERNS:
```
  echo "Running linter..."
  npm run lint
  if [ $? -ne 0 ]; then
    echo "Linting failed. Commit aborted."
    exit 1
  fi
```
```
  commit_msg=$(cat "$1")
  pattern="^(feat|fix|docs|style|refactor|test|chore|ci|build|perf)(\(.+\))?: .{1,72}"
  if ! echo "$commit_msg" | grep -qE "$pattern"; then
    echo "ERROR: Commit message does not follow Conventional Commits format."
    echo "Expected: type(scope): description"
    echo "Example: feat(auth): add login functionality"
```

INTERVIEW TIPS:
  - Understand the core concepts and trade-offs
  - Be ready to explain with real-world examples
  - Discuss performance implications and best practices
  - Show awareness of common pitfalls

```
---

## See Also
- [CI/CD](../15-CI-CD/)
- [Monorepo](../28-Monorepo/)

## References & Learn More

- [Git Hooks Documentation](https://git-scm.com/docs/githooks)
- [Husky Documentation](https://typicode.github.io/husky/)
- [lint-staged](https://github.com/okonet/lint-staged)
- [commitlint](https://commitlint.js.org/)
- [Git Hooks Tutorial](https://www.atlassian.com/git/tutorials/git-hooks)
