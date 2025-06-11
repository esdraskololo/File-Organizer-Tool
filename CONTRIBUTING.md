# Contributing to File Organizer Tool

Thank you for considering contributing to the File Organizer Tool! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and considerate of others when contributing to this project. We aim to foster an inclusive and welcoming community.

## How Can I Contribute?

### Reporting Bugs

If you find a bug, please create an issue with the following information:
- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior and what actually happened
- Any additional context (screenshots, error messages, etc.)

### Suggesting Features

Have an idea for a new feature? Create an issue with:
- A clear, descriptive title
- A detailed description of the proposed feature
- Why this feature would be useful to most users

### Pull Requests

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Development Setup

1. Clone the repository
   ```bash
   git clone https://github.com/MC-Oruc/file-organizer-tool.git
   cd file-organizer-tool
   ```

2. No external Python packages are required if using a standard Python installation that includes Tkinter.

3. Run the application
   ```bash
   python main.py
   ```

## Styleguides

### Git Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests after the first line

### Python Styleguide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use descriptive variable names
- Include docstrings for all classes and functions
- Keep functions focused on a single responsibility

### Localization

When adding new UI strings:
1. Add them to all language files in the `locales/` directory
2. Use meaningful keys that describe the content
3. Use placeholders like `{variable_name}` for dynamic content

## Adding New Languages

1. Copy an existing locale file (e.g., `en.json`) to a new file with the appropriate language code (`xx.json`)
2. Translate all string values (not the keys)
3. Make sure the `_lang_name_` key contains the native name of the language

## License

By contributing, you agree that your contributions will be licensed under the project's MIT License.
