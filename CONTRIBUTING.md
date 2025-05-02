# Contributing to DocuDex

Thank you for your interest in contributing to **DocuDex**, a TUI for intelligent document analysis using Retrieval-Augmented Generation (RAG). We welcome contributions of all kinds — from bug reports to new features and documentation improvements.

## Getting Started

1. **Fork & Clone the Repo**

   ```bash
   git clone https://github.com/lohithsrinivasaiah/docudex.git
   cd docudex
   ```

2. **Set Up a Virtual Environment**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -e ".[dev]"
   ```

4. **Install Pre-commit Hooks**
   We use [pre-commit](https://pre-commit.com/) to maintain code quality. Run:

   ```bash
   pre-commit install
   ```

5. **Run Tests**

   ```bash
   pytest tests/
   ```

## Guidelines

* Format code with `black .`
* Lint code with `flake8`
* Use type hints and docstrings
* Write/update tests for any new functionality
* Use meaningful commit messages (`feat:`, `fix:`, `docs:`)
* Open PRs against the `main` branch

## How You Can Help

* Add new RAG strategies
* Improve the Textual-based UI
* Support more file types (Markdown, HTML, etc.)
* Enhance performance or testing
* Improve documentation

## Need Help?

* [Issue Tracker](https://github.com/lohithsrinivasaiah/docudex/issues)
* Email: [lohith.srinivasaiah@gmail.com](mailto:lohith.srinivasaiah@gmail.com)

Thanks for making DocuDex better!
