# Contributing to Task Timer CLI

First off, thank you for considering contributing to Task Timer CLI! 🎉

It's people like you that make Task Timer CLI such a great tool. We welcome contributions from everyone, whether you're a seasoned developer or just starting out.

## 🎃 Hacktoberfest

This project participates in Hacktoberfest! We're excited to help you make your open-source contributions. Please make sure your PRs are meaningful and follow our guidelines.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Getting Started](#getting-started)
- [Development Process](#development-process)
- [Style Guidelines](#style-guidelines)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)

## 📜 Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please be respectful, inclusive, and considerate of others.

## 🤝 How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list to avoid duplicates. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples** to demonstrate the steps
- **Describe the behavior you observed** and what you expected to see
- **Include screenshots** if relevant
- **Include your environment details** (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide a detailed description** of the suggested enhancement
- **Explain why this enhancement would be useful**
- **List some examples** of how it would be used

### Your First Code Contribution

Unsure where to begin? You can start by looking through `good-first-issue` and `help-wanted` issues:

- **Good First Issues** - issues that should only require a few lines of code
- **Help Wanted Issues** - issues that are a bit more involved

## 🚀 Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/task-timer-cli.git
   cd task-timer-cli
   ```

3. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Set up your development environment**:
   ```bash
   python --version  # Ensure you're using Python 3.6+
   ```

5. **Make your changes** and test them thoroughly

6. **Test the script**:
   ```bash
   python task_timer.py list
   python task_timer.py add "Test task" 25
   python task_timer.py start 1
   ```

## 💻 Development Process

1. **Always create a new branch** for your work
2. **Write clear, commented code** that follows our style guidelines
3. **Test your changes** thoroughly before submitting
4. **Update documentation** if you're changing functionality
5. **Keep your PR focused** - one feature/fix per PR

## 🎨 Style Guidelines

### Python Style Guide

We follow PEP 8 style guidelines with some flexibility:

- **Indentation**: 4 spaces (no tabs)
- **Line length**: Aim for 79 characters, but 100 is acceptable
- **Naming conventions**:
  - Functions and variables: `snake_case`
  - Classes: `PascalCase`
  - Constants: `UPPER_CASE`

- **Docstrings**: Use triple quotes for all functions
  ```python
  def add_task(name, duration=25):
      """Add a new task to the task list"""
      pass
  ```

- **Comments**: Use them to explain "why", not "what"
  ```python
  # Good
  # Convert to seconds for the timer loop
  duration = task["duration"] * 60
  
  # Bad
  # Multiply duration by 60
  duration = task["duration"] * 60
  ```

### Code Quality

- Write clean, readable code
- Avoid unnecessary complexity
- Remove debugging code and print statements
- Handle errors gracefully
- Don't repeat yourself (DRY principle)

## 📝 Commit Messages

Write clear and meaningful commit messages:

### Format:
```
<type>: <subject>

<body (optional)>
```

### Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples:
```
feat: add CSV export functionality

Added export command that allows users to export their tasks to a CSV file.
Includes headers and all task details.
```

```
fix: handle invalid task IDs gracefully

Previously the app would crash with invalid IDs. Now it shows a friendly
error message and continues running.
```

```
docs: update README with new export command
```

## 🔄 Pull Request Process

1. **Update the README.md** if you're adding new features or changing usage
2. **Ensure your code follows** the style guidelines
3. **Test your changes** thoroughly
4. **Write a clear PR description**:
   - What does this PR do?
   - What issue does it close? (use "Closes #123")
   - How has it been tested?
   - Screenshots (if applicable)

5. **PR Title Format**:
   ```
   [Type] Brief description of changes
   ```
   Examples:
   - `[Feature] Add CSV export functionality`
   - `[Fix] Handle invalid task IDs`
   - `[Docs] Update installation instructions`

6. **Wait for review** - maintainers will review your PR and may request changes
7. **Be responsive** to feedback and make requested changes promptly

## ✅ Checklist Before Submitting PR

- [ ] My code follows the style guidelines of this project
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings or errors
- [ ] I have tested my changes thoroughly
- [ ] My commit messages follow the commit message guidelines

## 🎯 Good Practices

### DO:
- ✅ Keep PRs small and focused
- ✅ Write descriptive commit messages
- ✅ Comment your code when necessary
- ✅ Test your changes
- ✅ Be respectful and patient
- ✅ Ask questions if you're unsure

### DON'T:
- ❌ Submit PRs with unrelated changes
- ❌ Copy code without attribution
- ❌ Make formatting-only changes to large portions of code
- ❌ Submit untested code
- ❌ Be rude or dismissive of feedback

## 🆘 Need Help?

- Check out existing issues and PRs
- Read the README.md thoroughly
- Comment on the issue you're working on
- Ask questions - we're here to help!

## 🙏 Recognition

Contributors will be recognized in our README.md file. Thank you for making Task Timer CLI better!

---

Happy Contributing! 🚀

Remember: The best PR is the one that's submitted. Don't be afraid to contribute, even if you're not sure if your code is perfect. We're all learning together!
