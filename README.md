# DocuDex

![Development](https://img.shields.io/badge/status-in%20development-orange)
![GitHub](https://img.shields.io/github/license/lohithsrinivasaiah/docudex)
![GitHub last commit](https://img.shields.io/github/last-commit/lohithsrinivasaiah/docudex)
![GitHub top language](https://img.shields.io/github/languages/top/lohithsrinivasaiah/docudex)


DocuDex is a Python CLI tool that allows you to interact with documents using large language models (LLMs) directly from your terminal. It supports various document formats like PDF and DOCX, enabling seamless document processing and information retrieval.

## Features
- **Seamless Document Interaction**: Load and interact with documents using LLMs.
- **Multi-format Support**: Compatible with PDF and DOCX files.
- **Flexible Configuration**: Customize document processing and retrieval settings.
- **Extensible and Customizable**: Easily extendable to fit different use cases.

## Installation

### Steps
1. **Clone the repository**
   ```bash
   git clone https://github.com/lohithsrinivasaiah/docudex.git
   cd docudex
   ```

2. **Create and activate a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```

3. **Install Poetry**
   ```bash
   pip install poetry
   ```

4. **Install dependencies and DocuDex using Poetry**
   ```bash
   poetry install
   ```

5. **Run DocuDex**
   ```bash
   docudex -h
   ```

6. **Version Check**

   To check the installed version of DocuDex, use:
   ```bash
   docudex -v
   ```

## Usage

To use DocuDex, simply pass a file as an argument to the CLI:

```bash
docudex -f path/to/your/document.pdf
```

To use with an entire directory, pass the directory as an argument to the CLI:

```bash
docudex -d path/to/your/directory
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
