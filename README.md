# Mark2

A powerful and flexible Markdown converter that transforms Markdown files into multiple output formats including HTML, EPUB, PDF, and ConTeXt (TeX).

## Features

- **Multiple Output Formats**: Convert Markdown to HTML, EPUB, PDF, ConTeXt (TeX), or Markdown
- **MyST Markdown Support**: Extended Markdown syntax with MyST (Markedly Structured Text) features
- **Front Matter**: Support for YAML front matter metadata
- **Footnotes**: Automatic footnote handling and rendering
- **Custom Heading IDs**: Automatic generation of heading identifiers for cross-referencing
- **EPUB Customization**: Add custom covers and stylesheets to EPUB output
- **Flexible I/O**: Read from files or stdin, write to files or stdout

## Installation

```bash
# Clone the repository
git clone https://github.com/geckoblu/mark2.git
cd mark2

# Install dependencies (requires Python 3.x)
pip3 install markdown-it-py mdit-py-plugins
```

## Usage

### Basic Usage

```bash
# Convert Markdown to HTML (default)
./mark2.sh input.md

# Specify output format
./mark2.sh input.md -f epub
./mark2.sh input.md -f pdf
./mark2.sh input.md -f tex

# Specify output file
./mark2.sh input.md -o output.html

# Read from stdin
cat input.md | ./mark2.sh - -f html
```

### Command-Line Options

```
positional arguments:
  INPUT_FILENAME        Input Markdown (.md) file to convert (use '-' for stdin)

optional arguments:
  -h, --help            Show help message and exit
  -f, --format {html,epub,pdf,tex,md}
                        Output format (default: html)
  -o, --output-filename OUTPUT_FILENAME
                        Output file name (use '-' for stdout)
                        Default: input name with format extension
  -q, --quiet           Suppress non-error messages

EPUB options:
  --epub-cover COVER    Cover image for EPUB (jpg, jpeg, png)
  --epub-stylesheet CSS Stylesheet for EPUB
```

### Examples

```bash
# Generate HTML with automatic output filename
./mark2.sh document.md

# Create an EPUB with custom cover and stylesheet
./mark2.sh book.md -f epub --epub-cover cover.jpg --epub-stylesheet style.css

# Convert to PDF
./mark2.sh report.md -f pdf

# Generate ConTeXt source
./mark2.sh article.md -f tex -o article.tex

# Process stdin to stdout
cat notes.md | ./mark2.sh - -f html > notes.html
```

## Supported Markdown Features

Mark2 uses the `markdown-it-py` parser with support for:

- **Standard Markdown**: Headers, emphasis, lists, links, images, code blocks
- **Tables**: GFM-style tables
- **Footnotes**: Reference-style footnotes
- **Front Matter**: YAML metadata blocks
- **Heading IDs**: Automatic or custom heading identifiers
- **MyST Extensions**: Extended syntax for scientific and technical writing

## Architecture

The project is structured as follows:

- `src/mark2/`: Main package
  - `main.py`: Entry point and conversion orchestration
  - `args.py`: Command-line argument parsing
  - `plugins/`: Custom markdown-it plugins
    - `footnote_plugin.py`: Enhanced footnote handling
    - `headingsid_plugin.py`: Heading ID generation
    - `yaml_parser.py`: YAML front matter parsing
  - `renderer/`: Output format renderers
    - `html.py`: HTML renderer
    - `md.py`: Markdown renderer
    - `pdf.py`: PDF renderer
    - `context.py`: ConTeXt renderer
    - `epub/`: EPUB-specific rendering

## Development

### Running Tests

```bash
# Run tests
python3 -m pytest tests/
```

### Direct Python Usage

```bash
# Set PYTHONPATH and run directly
export PYTHONPATH=./src
python3 src/mark2/main.py input.md
```

## References

- [markdown-it-py](https://github.com/executablebooks/markdown-it-py) - Python port of markdown-it
- [markdown-it](https://github.com/markdown-it/markdown-it) - Original JavaScript implementation
- [MyST Markdown](https://mystmd.org/guide/quickstart-myst-markdown) - MyST quickstart guide (JavaScript)
- [MyST Specification (myst-parser)](https://myst-parser.readthedocs.io/en/latest/syntax/typography.html) - Typography and syntax
- [MyST Specification (mystmd)](https://mystmd.org/guide/typography) - MyST typography guide (JavaScript)
- [ConTeXt Garden](https://wiki.contextgarden.net) - ConTeXt documentation

## License

This project is released under the MIT License, see [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

