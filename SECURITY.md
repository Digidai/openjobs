# Security Policy

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability, please report it responsibly.

**Please do NOT open public issues for security vulnerabilities.**

### How to Report

1. **Email**: Send details to the repository maintainer
2. **GitHub Security Advisory**: Use [GitHub's private vulnerability reporting](https://github.com/Digidai/openjobs/security/advisories/new)

### What to Include

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### Response Timeline

- **Acknowledgment**: Within 48 hours
- **Initial Assessment**: Within 7 days
- **Resolution**: Depends on severity and complexity

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| main    | :white_check_mark: |
| < 1.0   | :x:                |

## Security Considerations

This project has minimal attack surface:

- **No External Dependencies**: Uses only Python standard library
- **No User Input Processing**: Read-only data aggregation
- **No Database**: Static file generation only
- **No Authentication**: Public data only
- **Minimal Permissions**: GitHub Actions uses only `contents: write`

## Best Practices

When contributing, please ensure:

1. No secrets or credentials in code
2. No hardcoded sensitive URLs
3. Validate all external data sources
4. Use HTTPS for all external requests
