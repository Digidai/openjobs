# Contributing to OpenJobs

Thank you for your interest in contributing to OpenJobs! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/digidai/openjobs/issues)
2. If not, create a new issue with:
   - A clear, descriptive title
   - Steps to reproduce the bug
   - Expected vs actual behavior
   - Your environment (OS, Python version, etc.)

### Suggesting Features

1. Check existing issues and discussions for similar suggestions
2. Create a new issue with the `enhancement` label
3. Describe the feature and its use case

### Submitting Changes

1. **Fork the repository**

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow existing code style
   - Add comments for complex logic
   - Update documentation if needed

4. **Test your changes**
   ```bash
   python scripts/update_readme.py
   ```

5. **Commit with a clear message**
   ```bash
   git commit -m "feat: add job category filtering"
   ```

6. **Push and create a Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

## Commit Message Format

We follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding tests
- `chore:` - Maintenance tasks

## Development Setup

### Prerequisites

- Python 3.11+
- Git

### Local Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/openjobs.git
cd openjobs

# Run the update script
python scripts/update_readme.py

# View generated files
open README.md
open public/index.html
```

## Project Structure

```
openjobs/
├── .github/
│   ├── workflows/          # GitHub Actions
│   └── ISSUE_TEMPLATE/     # Issue templates
├── scripts/
│   └── update_readme.py    # Main script
├── public/
│   ├── index.html          # Cloudflare site
│   └── sitemap.xml         # Cloudflare sitemap
├── README.md               # GitHub Pages + docs
├── sitemap.xml             # GitHub sitemap
└── _config.yml             # Jekyll config
```

## Areas for Contribution

### High Priority

- [ ] Add job search/filter functionality
- [ ] Implement job category tags
- [ ] Add RSS feed support
- [ ] Create job statistics dashboard

### Good First Issues

- Improve documentation
- Add more error handling
- Optimize XML parsing
- Add unit tests

## Questions?

Feel free to open an issue or start a discussion if you have questions!

---

Thank you for contributing!
