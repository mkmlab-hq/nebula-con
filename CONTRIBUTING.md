# Contributing to NebulaCon

Thank you for your interest in contributing to NebulaCon! This document provides guidelines and information for contributors.

## 🚀 Quick Start

1. **Fork** the repository
2. **Clone** your fork: `git clone https://github.com/YOUR_USERNAME/nebula-con.git`
3. **Install** in development mode: `pip install -e ".[dev]"`
4. **Create** a feature branch: `git checkout -b feat/amazing-feature`
5. **Make** your changes
6. **Test** your changes: `pytest`
7. **Commit** with proper prefix: `git commit -m "feat: add amazing feature"`
8. **Push** to your fork: `git push origin feat/amazing-feature`
9. **Create** a Pull Request

## 📋 Development Guidelines

### Branch Naming Convention

- `feat/` - New features
- `fix/` - Bug fixes
- `refactor/` - Code refactoring
- `docs/` - Documentation updates
- `test/` - Test additions/updates
- `chore/` - Maintenance tasks
- `build/` - Build system changes

**Examples:**
- `feat/add-jensen-shannon-divergence`
- `fix/dip-stat-edge-case`
- `docs/update-metrics-schema`
- `test/add-threshold-tests`

### Commit Message Format

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```bash
git commit -m "feat(metrics): add Jensen-Shannon divergence metric"
git commit -m "fix(shape): handle edge case in dip_stat calculation"
git commit -m "docs: update README with new CLI examples"
git commit -m "test(thresholds): add metric range validation tests"
```

### Code Style

- **Python**: Follow PEP 8 guidelines
- **Line length**: 88 characters (Black formatter)
- **Linting**: Use `ruff` for code quality checks
- **Type hints**: Use type hints for function parameters and return values

**Pre-commit setup:**
```bash
pip install pre-commit
pre-commit install
```

## 🧪 Testing Requirements

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/nebula_axes

# Run specific test file
pytest tests/test_metrics.py

# Run with verbose output
pytest -v
```

### Test Coverage

- **Minimum coverage**: 80%
- **Critical paths**: 90%+ (metrics calculation, CLI)
- **New features**: Must include tests

### Test Structure

```
tests/
├── test_metrics/           # Metric-specific tests
│   ├── test_temporal.py   # A-axis tests
│   ├── test_shape.py      # B-axis tests
│   ├── test_density.py    # C-axis tests
│   └── test_retention.py  # D-axis tests
├── test_cli/              # CLI tests
├── test_integration/      # Integration tests
└── conftest.py            # Test fixtures
```

## 📊 Metrics Validation

### Threshold Testing

All metrics must pass threshold validation:

```python
def test_metric_reasonable_ranges(load_sample_metrics):
    m = load_sample_metrics
    assert 0 <= m["st_var_ratio"] < 2
    assert -1 <= m["seasonal_corr"] <= 1
    assert m["psi_trigger_rate"] < 1.2
    if m["dip_stat"] is not None:
        assert 0 <= m["dip_stat"] < 0.3
```

### Performance Requirements

- **Small datasets** (< 1K samples): < 1 second
- **Medium datasets** (1K-10K samples): < 5 seconds
- **Large datasets** (10K+ samples): < 30 seconds

## 🔧 Development Environment

### Required Tools

- **Python**: 3.8+
- **Package Manager**: pip
- **Build System**: hatchling
- **Testing**: pytest
- **Linting**: ruff
- **Formatting**: Black

### Environment Setup

```bash
# Clone repository
git clone https://github.com/mkmlab-v2/nebula-con.git
cd nebula-con

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Verify installation
python -c "import nebula_axes; print(nebula_axes.__version__)"
```

### Development Workflow

1. **Update dependencies** if needed:
   ```bash
   pip install -r requirements-dev.txt
   ```

2. **Run tests** before committing:
   ```bash
   pytest
   ```

3. **Check code quality**:
   ```bash
   ruff check src/ tests/
   ```

4. **Format code**:
   ```bash
   black src/ tests/
   ```

## 📝 Pull Request Process

### PR Checklist

Before submitting a PR, ensure:

- [ ] **Tests pass**: `pytest` completes successfully
- [ ] **Code quality**: `ruff check` passes
- [ ] **Documentation**: Updated README/docs if needed
- [ ] **CHANGELOG**: Updated for user-facing changes
- [ ] **Performance**: No significant performance regression
- [ ] **Backward compatibility**: Maintained if applicable

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Performance benchmarks included

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] CHANGELOG updated

## Related Issues
Closes #(issue number)
```

## 🚨 Breaking Changes

### When to Consider Breaking Changes

- **Major version bump** (v0.x.0 → v1.0.0)
- **API incompatibility** with previous versions
- **Removal** of deprecated features
- **Significant** architectural changes

### Breaking Change Process

1. **Discuss** in GitHub Issues
2. **Create** migration guide
3. **Update** CHANGELOG with breaking changes
4. **Provide** backward compatibility layer if possible
5. **Communicate** changes clearly in PR description

## 📚 Documentation

### Required Documentation

- **README.md**: Quick start and basic usage
- **API documentation**: Function signatures and examples
- **CHANGELOG.md**: Version history and changes
- **Examples**: Working code examples
- **Migration guides**: For breaking changes

### Documentation Standards

- **Clear examples** with sample data
- **Parameter descriptions** with types and ranges
- **Edge case handling** documentation
- **Performance considerations** for large datasets

## 🐛 Bug Reports

### Bug Report Template

```markdown
## Bug Description
Clear description of the issue

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g., Windows 10, Ubuntu 20.04]
- Python: [e.g., 3.9.7]
- Package version: [e.g., 0.2.0]

## Additional Information
Any other context, logs, or screenshots
```

## 💡 Feature Requests

### Feature Request Template

```markdown
## Feature Description
Clear description of the requested feature

## Use Case
Why this feature is needed

## Proposed Implementation
How you think it should work

## Alternatives Considered
Other approaches you've considered

## Additional Context
Any other relevant information
```

## 🤝 Community Guidelines

### Code of Conduct

- **Be respectful** and inclusive
- **Welcome newcomers** and help them contribute
- **Focus on the code** and technical discussions
- **Provide constructive feedback**

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and discussions
- **Pull Requests**: Code reviews and collaboration

## 📄 License

By contributing to NebulaCon, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to NebulaCon! 🚀 