# Requirements and Dependencies

## Runtime Requirements

**Zero external dependencies!** This tool uses only Python's standard library.

### Python Version
- **Minimum**: Python 3.6
- **Recommended**: Python 3.7+

### System Requirements
- **Operating System**: macOS, Linux, or Windows (with WSL)
- **Git**: Optional (for branch detection)

### Python Standard Library Modules Used
- `sys` - Command-line argument handling, stdin/stdout
- `json` - Configuration and data parsing
- `os` - Environment variables, path operations
- `pathlib` - Cross-platform path handling
- `subprocess` - Git command execution
- `typing` - Type hints (Python 3.6+)

## Development/Testing Requirements

If you want to run the test suite or contribute to development:

```bash
pip install -r requirements-test.txt
```

### Test Dependencies
- **pytest** >= 7.4.0 - Test framework
- **pytest-cov** >= 4.1.0 - Coverage reporting

## Why Separate requirements-test.txt?

We follow the best practice of separating test dependencies from runtime requirements:

1. **Lightweight deployment** - Users don't need to install pytest to use the tool
2. **Clear separation** - Development tools are clearly distinguished from runtime needs
3. **Faster installs** - Production installs are instant (no dependencies to download)
4. **Standard practice** - Follows Python packaging conventions

## Why No requirements.txt?

This project intentionally has **no runtime dependencies** because:

1. **Simplicity** - Easier to install and maintain
2. **Reliability** - No dependency version conflicts or breakage
3. **Performance** - No dependency resolution overhead
4. **Portability** - Works anywhere Python 3.6+ is installed
5. **Security** - Smaller attack surface (no third-party code)

## Installation for Users

No pip install needed! Just run:

```bash
./install.sh
```

The installer only requires Python 3.6+ (which includes all necessary modules).

## Installation for Developers

If you want to contribute or run tests:

```bash
# Clone the repository
git clone <repository-url>
cd claude-code-status-line

# Install test dependencies
pip install -r requirements-test.txt

# Run tests
python3 -m pytest tests/
```

## Version History

- **v1.0.0**: Initial release - zero dependencies
- **v1.0.1**: Still zero dependencies
- **v1.0.2**: Added test dependencies in requirements-test.txt, runtime still zero dependencies

## Future Considerations

We are committed to keeping **zero runtime dependencies**. Any future enhancements will continue to use only the Python standard library to maintain simplicity and reliability.
