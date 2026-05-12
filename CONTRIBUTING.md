# Contributing to MarkBlog

Thank you for considering contributing to MarkBlog! Here's everything you need to know.

## Table of Contents

- [Development Setup](#development-setup)
- [Running Tests](#running-tests)
- [Code Style Guidelines](#code-style-guidelines)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)
- [Reporting Issues](#reporting-issues)
- [Feature Requests](#feature-requests)

---

## Development Setup

### Prerequisites

- **Python** 3.9+ (3.12 recommended)
- **pip**

### Steps

```bash
# Fork the repository (click Fork button on GitHub)

# Clone your fork
git clone https://github.com/YOUR_USERNAME/markblog.git
cd markblog

# Add upstream remote
git remote add upstream https://github.com/AndRiaBX/markblog.git

# (Recommended) Create and activate a virtual environment
python -m venv venv
source venv/bin/activate         # Linux/macOS
# venv\Scripts\activate          # Windows

# Install dependencies
pip install -r requirements.txt

# Verify setup by running tests
python -m pytest tests/ -v
```

---

## Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=. -v
```

Tests use `pytest` with temporary content directories — no manual setup needed. Each test gets an isolated content directory via `tmp_path` fixtures.

---

## Code Style Guidelines

### General (PEP 8)

- **Indentation:** 4 spaces (no tabs)
- **Line length:** 100 characters max
- **Quotes:** Double quotes for docstrings, single quotes for short strings
- **Naming:** `snake_case` for functions/variables, `CamelCase` for classes

### Example

```python
# Good
def load_posts(force=False, content_dir=None):
    """Load all markdown posts from content directory. Caches via JSON."""
    if content_dir is None:
        content_dir = CONTENT_DIR
    ...

# Avoid
def LoadPosts(force = False, contentDir = None):
    """load all posts"""
    if contentDir is None:
        contentDir = CONTENT_DIR
    ...
```

### Docstrings

- **Public functions** get a docstring explaining what they do
- **Internal helpers** get comments for *why*, not *what*
- Use triple double-quotes `"""..."""`

### Imports

Order imports in groups separated by a blank line:
1. Standard library (`os`, `sys`, `json`, etc.)
2. Third-party (`flask`, `markdown`, etc.)
3. Local application (`from blog import ...`)

### Error handling

- Handle file I/O errors with try/except
- Log failures but don't crash on cache or non-critical operations
- Validate inputs at API/route boundaries

---

## Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
type(scope): brief description

Optional body explaining the motivation.
```

**Types:** `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

**Examples:**
```
feat(content): add support for draft posts via status flag
fix(cache): handle corrupted cache file gracefully
docs(readme): add deployment guide and API reference
test: add edge case tests for frontmatter parsing
```

---

## Pull Request Process

1. **Create a feature branch** from `master`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the code style guidelines

3. **Add tests** for any new functionality

4. **Run the test suite** and ensure all tests pass:
   ```bash
   python -m pytest tests/ -v
   ```

5. **Keep your branch up to date**:
   ```bash
   git fetch upstream
   git rebase upstream/master
   ```

6. **Commit your changes** with a clear commit message:
   ```bash
   git commit -m "feat: add descriptive message"
   ```

7. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

8. **Open a Pull Request** on GitHub with:
   - A clear title describing the change
   - A description of what and why
   - Reference to any related issues (e.g., "Closes #42")

### PR Review Checklist

- [ ] Tests pass (`python -m pytest tests/ -v`)
- [ ] New code has tests
- [ ] Code follows PEP 8 and project style
- [ ] Documentation updated if needed
- [ ] No unnecessary files committed
- [ ] Commit messages follow conventions

---

## Reporting Issues

Use the [GitHub issue tracker](https://github.com/AndRiaBX/markblog/issues).

### Bug Reports

Include:
- A clear, descriptive title
- Steps to reproduce the problem
- Expected vs actual behavior
- Environment details (OS, Python version, browser)
- Example markdown file that triggers the issue
- Screenshots or logs if applicable

### Feature Requests

Include:
- A clear description of the feature
- The problem it solves
- How the feature should work
- Alternative approaches you've considered

---

## Code of Conduct

Be respectful and constructive. We're all here to build something useful.

---

## Getting Help

- Open an issue for questions
- PR comments for discussion on specific changes
- Check existing issues before asking

---

*Thank you for helping make MarkBlog better!*
