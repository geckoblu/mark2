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

## Extensions Over CommonMark

Mark2 extends the [CommonMark specification](https://spec.commonmark.org/) with several powerful features for scientific, technical, and professional documentation. Below is a comprehensive guide to these extensions.

### 1. YAML Front Matter

Add metadata to your documents using YAML front matter at the beginning of your file.

**Syntax:**
```markdown
---
title: Document Title
author: John Doe
date: 2024-01-22
description: A comprehensive guide
---

# Content starts here
```

**Features:**
- Must be the first thing in the file
- Enclosed by `---` markers
- Supports standard YAML syntax including multi-line values
- Metadata can be used by renderers (especially EPUB and PDF)

**Example:**
```markdown
---
title: The Great Gatsby
author: F. Scott Fitzgerald
publisher: Charles Scribner's Sons
date: 1925-04-10
subject: Fiction, Classic Literature
description: |
  A story of decadence and excess,
  and the American dream in the 1920s.
---

# Chapter 1

In my younger and more vulnerable years...
```

### 2. Footnotes

Create reference-style footnotes with automatic numbering and positioning.

**Syntax:**
```markdown
Text with a footnote[^1] and another[^note].

[^1]: This is the first footnote.
[^note]: This is a named footnote.
```

**Inline Footnotes:**
```markdown
Text with an inline footnote^[This note appears inline].
```

**Features:**
- Automatic numbering
- Support for both numeric and named references
- Footnote definitions can appear anywhere in the document
- Inline footnotes using `^[...]` syntax
- Footnotes are collected and rendered at the end of the document

**Example:**
```markdown
The theory of relativity[^einstein] revolutionized physics.

According to recent studies^[Smith et al., 2024], this approach
shows promising results.

[^einstein]: Proposed by Albert Einstein in 1905.
```

### 3. MyST Roles (Inline Extensions)

Apply semantic meaning or special formatting to inline text using MyST roles.

**Syntax:**
```markdown
{role-name}`content`
```

**Features:**
- Role names can contain letters, numbers, underscores, hyphens, plus signs, and colons
- Support for multiple backticks: `` {role}``content with `backtick` `` ``
- Newlines in content are converted to spaces
- Can be escaped with backslash: `\{role}`content``

**Examples:**
```markdown
{emphasis}`important text`
{download}`filename.pdf`
{ref}`section-label`
{doc}`../other-file`
{math}`x^2 + y^2 = z^2`
{kbd}`Ctrl+C`
{abbr}`HTML (HyperText Markup Language)`
{sub}`subscript text`
{sup}`superscript text`
```

**Rendered as:**
```html
<code class="myst role">{role-name}[content]</code>
```

### 4. MyST Directives (Block Extensions)

#### 4.1 Line Comments

Add comments to your Markdown that won't appear in the output.

**Syntax:**
```markdown
% This is a comment
% Comments can span multiple lines
% when each line starts with %

Regular content here.
```

**Features:**
- Lines starting with `%` are treated as comments
- Multiple consecutive comment lines are combined into one HTML comment block
- Leading whitespace is stripped
- Does not work inside code blocks

#### 4.2 Block Breaks

Create visual separators or section breaks.

**Syntax:**
```markdown
Content above

+++

Content below
```

**Features:**
- Minimum 3 plus signs: `+++`
- Can use more plus signs: `++++++++`
- Rendered as `<hr class="myst-block">`
- Useful for section breaks in longer documents

#### 4.3 Targets (Labels)

Create named anchors for cross-referencing.

**Syntax:**
```markdown
(my-label)=
# Section Title

Reference the label elsewhere: {ref}`my-label`
```

**Features:**
- Labels must be on their own line
- Typically placed before headings
- Can be referenced using role syntax
- Useful for internal document linking

### 5. Container Blocks

Create custom block-level containers with semantic meaning.

**Syntax:**
```markdown
::: container-name
Content with **markdown** support.
:::
```

**Features:**
- Minimum 3 colons: `:::`
- Content inside supports full Markdown syntax
- Containers can be nested with more colons: `::::`, `:::::`, etc.
- Useful for admonitions, warnings, notes, etc.

**Examples:**
```markdown
::: warning
This is a warning message with *emphasis*.
:::

::: note
Important information goes here.
:::

:::: outer-container
::: inner-container
Nested content
:::
::::
```

**Rendered as:**
```html
<div class="warning">
<p>This is a warning message with <em>emphasis</em>.</p>
</div>
```

### 6. Superscript and Subscript

**Superscript Syntax:**
```markdown
E = mc^2^
This is a footnote reference^1^
```

**Subscript Syntax:**
```markdown
H~2~O
Temperature at T~0~
```

**Examples:**
```markdown
Water molecule: H~2~O
Einstein's equation: E = mc^2^
Chemical formula: CO~2~ concentration
Mathematical expression: x^n^ + y^n^ = z^n^
```

**Rendered as:**
```html
H<sub>2</sub>O
E = mc<sup>2</sup>
```

### 7. Page Breaks

Insert page breaks for PDF and print output.

**Syntax:**
```markdown
Content on first page

---

Content on second page
```

**Features:**
- Three consecutive dashes: `---`
- Only horizontal rules with dashes become page breaks
- Thematic breaks with asterisks (`***`) remain unchanged
- Rendered differently depending on output format (special handling for PDF/EPUB)

**Example:**
```markdown
# Chapter 1

This is the content of chapter 1.

---

# Chapter 2

This starts on a new page in PDF output.
```

### 8. Custom Heading IDs

Automatically generates or allows custom IDs for headings.

**Automatic IDs:**
```markdown
# My Section Title
```
Generates: `<h1 id="my-section-title">My Section Title</h1>`

**Custom IDs (using targets):**
```markdown
(custom-id)=
# My Section Title
```
Generates: `<h1 id="custom-id">My Section Title</h1>`

**Features:**
- Automatic slug generation from heading text
- Support for custom IDs via target syntax
- Enables internal linking and table of contents generation

### 9. Tables (GFM Style)

Standard GitHub-Flavored Markdown tables.

**Syntax:**
```markdown
| Header 1 | Header 2 | Header 3 |
| -------- | -------- | -------- |
| Cell 1   | Cell 2   | Cell 3   |
| Cell 4   | Cell 5   | Cell 6   |
```

**Alignment:**
```markdown
| Left | Center | Right |
| :--- | :----: | ----: |
| L1   |   C1   |    R1 |
| L2   |   C2   |    R2 |
```

## Complete Example

Here's a comprehensive example using multiple extensions:

```markdown
---
title: Research Paper
author: Dr. Jane Smith
date: 2024-01-22
---

% This is a comment explaining the document structure
% It won't appear in the output

(introduction)=
# Introduction

This paper discusses the formula E = mc^2^ and the importance
of H~2~O in biological systems[^1].

{emphasis}`Note:` This is a MyST role for emphasis.

::: warning
Please read this section carefully.
:::

## Methods

The experimental setup is described below.

+++

[^1]: Water is essential for all known forms of life.

---

# Conclusion

See the {ref}`introduction` for background information.
```

This example demonstrates:
- YAML front matter
- Comments
- Custom heading targets
- Superscript and subscript
- Footnotes
- MyST roles
- Container blocks
- Block breaks
- Page breaks
- Internal references

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

- [CommonMark](https://commonmark.org/)
- [CommonMark Spec](https://spec.commonmark.org/)
- [Markdown-It-Py](https://markdown-it-py.readthedocs.io/en/latest/)
- [Markdown-It-Py Plugin Extensions](https://mdit-py-plugins.readthedocs.io/en/latest/)
- [markdown-it-py (source)](https://github.com/executablebooks/markdown-it-py) - Python port of markdown-it
- [markdown-it](https://github.com/markdown-it/markdown-it) - Original JavaScript implementation
- [MyST Markdown](https://mystmd.org/guide/quickstart-myst-markdown) - MyST quickstart guide (JavaScript)
- [MyST Specification (myst-parser)](https://myst-parser.readthedocs.io/en/latest/syntax/typography.html) - Typography and syntax
- [MyST Specification (mystmd)](https://mystmd.org/guide/typography) - MyST typography guide (JavaScript)
- [ConTeXt Garden](https://wiki.contextgarden.net) - ConTeXt documentation

## License

This project is released under the MIT License, see [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

