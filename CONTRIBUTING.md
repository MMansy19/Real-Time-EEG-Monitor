# Contributing to NeuroViz Pro

First off, thank you for considering contributing to NeuroViz Pro! 🎉

This document provides guidelines for contributing to the project. Following these guidelines helps maintain code quality and makes the contribution process smooth for everyone.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Style Guidelines](#style-guidelines)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)
- [Testing](#testing)
- [Documentation](#documentation)
- [Community](#community)

---

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for everyone. Please be respectful and constructive in all interactions.

### Our Standards

**Positive behaviors:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards others

**Unacceptable behaviors:**
- Harassment, trolling, or insulting comments
- Publishing others' private information
- Other conduct inappropriate for a professional setting

---

## How Can I Contribute?

### 🐛 Reporting Bugs

**Before submitting a bug report:**
1. Check the [Issues](https://github.com/MMansy19/NeuroViz-Pro-EEG-Monitor/issues) page
2. Verify you're using the latest version
3. Check if it's already documented in troubleshooting

**Good bug reports include:**
- Clear, descriptive title
- Steps to reproduce the issue
- Expected vs. actual behavior
- Screenshots (if applicable)
- System information (OS, Python version)
- Error messages or logs

**Example:**
```markdown
**Bug:** Application crashes when saving data

**Steps to reproduce:**
1. Launch application (codeV1.py)
2. Click "START RECORDING"
3. Wait 10 seconds
4. Click "STOP RECORDING"
5. Click "SAVE DATA"
6. Application crashes

**Expected:** File dialog opens
**Actual:** Application closes with error

**Environment:**
- OS: Windows 10
- Python: 3.9.7
- Error: KeyError: 'recorded_data'
```

---

### ✨ Suggesting Enhancements

**Enhancement suggestions include:**
- New features
- UI improvements
- Performance optimizations
- Documentation improvements

**Good enhancement requests include:**
- Clear description of the feature
- Use case / motivation
- Potential implementation approach
- Examples from similar projects

---

### 💻 Code Contributions

Areas where we need help:
- Multi-channel EEG support
- Additional filter types
- Export to more formats (HDF5, EDF)
- Real-time feedback features
- Machine learning integration
- Mobile/tablet support
- Cloud data storage
- Performance optimizations

---

## Getting Started

### 1. Fork the Repository

```bash
# Click "Fork" button on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/NeuroViz-Pro-EEG-Monitor.git
cd NeuroViz-Pro-EEG-Monitor
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest black flake8 mypy
```

### 3. Create a Branch

```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Or a bugfix branch
git checkout -b bugfix/issue-number-description
```

---

## Development Workflow

### 1. Make Your Changes

```bash
# Edit files
# Test thoroughly
# Document changes
```

### 2. Format Code

```bash
# Format with Black
black codeV1.py codeV2.py

# Check with flake8
flake8 codeV1.py codeV2.py

# Type check with mypy (optional)
mypy codeV1.py
```

### 3. Test

```bash
# Run tests
pytest tests/

# Test both modes
python codeV1.py  # Simulation mode
python codeV2.py  # Arduino mode (if available)
```

### 4. Commit

```bash
git add .
git commit -m "feat: add new feature description"
```

### 5. Push

```bash
git push origin feature/your-feature-name
```

### 6. Create Pull Request

Go to GitHub and click "New Pull Request"

---

## Style Guidelines

### Python Code Style

We follow **PEP 8** with some modifications:

**General:**
- Line length: 88 characters (Black default)
- Indentation: 4 spaces
- Encoding: UTF-8

**Naming Conventions:**
```python
# Classes: PascalCase
class EEG_GUI:
    pass

# Functions: snake_case
def butter_bandpass():
    pass

# Constants: UPPER_CASE
SAMPLE_RATE = 1000
USE_ARDUINO = False

# Variables: snake_case
data_buffer = []
is_recording = False
```

**Imports:**
```python
# Standard library first
import sys
import os

# Third-party libraries
import numpy as np
from PyQt5 import QtWidgets

# Local imports
from utils import helper_function
```

**Docstrings:**
```python
def function_name(param1, param2):
    """
    Brief description of function.
    
    Parameters:
    -----------
    param1 : type
        Description of param1
    param2 : type
        Description of param2
    
    Returns:
    --------
    return_type
        Description of return value
    """
    pass
```

---

### Documentation Style

**Markdown files:**
- Clear headings (H1, H2, H3)
- Code blocks with language specification
- Tables for comparisons
- Examples for clarity

**Comments in code:**
```python
# Good: Explain WHY, not WHAT
# Apply bandpass filter to remove DC drift and high-freq noise
filtered = bandpass_filter(data)

# Bad: States the obvious
# Filter the data
filtered = bandpass_filter(data)
```

---

## Commit Messages

Follow **Conventional Commits** specification:

### Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding tests
- `chore`: Maintenance tasks

### Examples

**Good:**
```
feat(ui): add dark mode toggle

Added toggle button in control panel to switch between light and dark themes.
Saves preference to config file for persistence across sessions.

Closes #42
```

```
fix(serial): handle Arduino disconnect gracefully

Previously crashed when Arduino disconnected during acquisition.
Now catches exception and falls back to simulation mode.

Fixes #38
```

```
docs(readme): add installation steps for macOS

Added detailed installation instructions for macOS including
Homebrew setup and Python installation.
```

**Bad:**
```
updated stuff
```

```
fix bug
```

```
changes
```

---

## Pull Request Process

### Before Submitting

**Checklist:**
- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] Documentation updated
- [ ] Commit messages follow convention
- [ ] Branch is up to date with main
- [ ] No merge conflicts

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
- [ ] Tested in simulation mode
- [ ] Tested with Arduino (if applicable)
- [ ] Added unit tests

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No breaking changes
- [ ] Commit messages follow convention

## Screenshots (if applicable)
Add screenshots here

## Related Issues
Closes #issue_number
```

### Review Process

1. **Automated checks** run (if configured)
2. **Maintainer review** (may request changes)
3. **Discussion and iteration**
4. **Approval and merge**

**Expected timeline:** 2-7 days

---

## Testing

### Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_filtering.py

# Run with coverage
pytest --cov=. tests/
```

### Writing Tests

**Example test:**
```python
import pytest
import numpy as np
from scipy.signal import butter, lfilter

def test_bandpass_filter():
    """Test bandpass filter removes DC and high frequencies."""
    # Generate test signal
    fs = 1000
    t = np.linspace(0, 1, fs)
    signal = np.sin(2*np.pi*10*t) + 5  # 10 Hz + DC offset
    
    # Apply filter
    b, a = butter(4, [1/500, 50/500], btype='band')
    filtered = lfilter(b, a, signal)
    
    # Check DC removed
    assert abs(np.mean(filtered)) < 0.1
    
    # Check 10 Hz preserved
    fft = np.abs(np.fft.rfft(filtered))
    freqs = np.fft.rfftfreq(len(filtered), 1/fs)
    peak_freq = freqs[np.argmax(fft)]
    assert 9 < peak_freq < 11
```

---

## Documentation

### Types of Documentation

1. **Code comments**: Explain complex logic
2. **Docstrings**: API documentation
3. **README.md**: Project overview
4. **Guides**: QUICKSTART.md, INSTALLATION.md, etc.
5. **Technical docs**: DOCUMENTATION.md

### Documentation Standards

**When to document:**
- All public functions and classes
- Complex algorithms
- Configuration options
- Non-obvious behavior
- Workarounds for known issues

**Example:**
```python
class EEG_GUI(QtWidgets.QMainWindow):
    """
    Main application window for EEG monitoring.
    
    This class handles the GUI, data acquisition, signal processing,
    and visualization for real-time EEG monitoring.
    
    Attributes:
        use_simulation (bool): True if using synthetic data
        ser (serial.Serial): Serial port object for Arduino
        data_buffer (np.ndarray): Rolling buffer of samples
        
    Example:
        >>> app = QtWidgets.QApplication(sys.argv)
        >>> window = EEG_GUI()
        >>> window.show()
        >>> sys.exit(app.exec_())
    """
    pass
```

---

## Community

### Communication Channels

- **GitHub Issues**: Bug reports, feature requests
- **GitHub Discussions**: Questions, ideas, show & tell
- **Pull Requests**: Code contributions

### Getting Help

**If you're stuck:**
1. Check documentation (README, QUICKSTART, etc.)
2. Search existing issues
3. Ask in GitHub Discussions
4. Create a new issue with details

### Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in documentation

---

## Development Tips

### Debugging

```python
# Enable debug mode
import logging
logging.basicConfig(level=logging.DEBUG)

# Add debug prints
print(f"DEBUG: value={value}, filtered={filtered[-1]}")

# Profile performance
import time
start = time.time()
# ... code ...
print(f"Elapsed: {time.time() - start:.3f}s")
```

### Common Pitfalls

**Issue:** Serial port permission denied  
**Solution:** Add user to dialout group (Linux)

**Issue:** ImportError for PyQt5  
**Solution:** Install system Qt5 libraries

**Issue:** Slow performance  
**Solution:** Increase UPDATE_INTERVAL, reduce BUFFER_SIZE

---

## Release Process

### Version Numbering

We use **Semantic Versioning** (MAJOR.MINOR.PATCH):

- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes

**Examples:**
- 1.0.0 → Initial release
- 1.1.0 → Add multi-channel support
- 1.1.1 → Fix serial bug

### Creating a Release

1. Update version number
2. Update CHANGELOG.md
3. Create git tag
4. Push to GitHub
5. Create GitHub release

---

## Questions?

**Not sure where to start?**
- Check [Issues](https://github.com/MMansy19/NeuroViz-Pro-EEG-Monitor/issues) labeled "good first issue"
- Read the documentation thoroughly
- Ask in GitHub Discussions

**Want to propose a major change?**
- Open an issue first to discuss
- Get feedback before coding
- Break into smaller PRs if possible

---

## Thank You! 🙏

Every contribution, no matter how small, is valuable and appreciated!

**Ways to contribute beyond code:**
- Report bugs
- Suggest features
- Improve documentation
- Help others in discussions
- Share the project
- Star the repository ⭐

---

<div align="center">

**Happy Contributing!** 🚀

*Together we make NeuroViz Pro better for everyone*

</div>

---

*Last updated: December 5, 2025*
