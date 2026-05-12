# Contributing to MarkBlog

Thank you for considering contributing! Here's how to get started.

## Development Setup

```bash
git clone https://github.com/AndRiaBX/markblog.git
cd markblog
pip install -r requirements.txt
```

## Running Tests

```bash
python -m pytest tests/ -v
```

Tests use `pytest` with temporary content directories — no manual setup needed.

## Code Style

- Follow PEP 8
- Use meaningful variable names
- Add docstrings for public functions
- Keep functions small and focused

## Docker Development

```bash
docker compose up --build
```

This will start the blog server at `http://localhost:5000`.

## Pull Request Process

1. Fork the repo and create your feature branch (`git checkout -b feature/amazing`)
2. Add tests for any new functionality
3. Ensure all tests pass
4. Update the README if needed
5. Open a Pull Request

## Reporting Issues

Use the GitHub issue tracker. Include:
- A clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
