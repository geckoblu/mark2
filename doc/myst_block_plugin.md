## MyST Blocks Plugin Documentation

### Overview
The `myst_block_plugin` provides support for three MyST (Markedly Structured Text) block-level features:
1. **Line Comments** - HTML comments using `%` prefix
2. **Block Breaks** - Content dividers using `+++`
3. **Targets** - Named anchors/labels using `(name)=` syntax

### 1. Line Comments (`%`)

**Syntax:**
```markdown
% This is a comment
% Multi-line comments
% can span multiple lines
```

**Features:**
- Each line must start with `%`
- Everything after `%` on the line is treated as a comment
- Multiple consecutive lines starting with `%` are combined into one comment block
- Leading whitespace is stripped from each line
- Does not work inside code blocks

**HTML Output:**
```html
<!-- This is a comment
Multi-line comments
can span multiple lines -->
```

**Examples:**
```markdown
% TODO: Add more content here
% Author: John Doe
% Date: 2024-01-01

Regular paragraph here.

% Another comment
Some content.
```

### 2. Block Breaks (`+++`)

**Syntax:**
```markdown
+++
```

**Rules:**
- Must have at least 3 plus signs (`+++`)
- Can have more than 3 (`++++`, `+++++`, etc.)
- Plus signs can be mixed with spaces/tabs
- Optional content after the markers is captured but typically ignored
- Does not work inside code blocks

**HTML Output:**
```html
<hr class="myst-block">
```

**Examples:**
```markdown
Section 1 content here.

+++

Section 2 content here.

++++++++

Section 3 content here.
```

### 3. Targets (Labels) (`(name)=`)

**Syntax:**
```markdown
(label-name)=
```

**Rules:**
- Must be on its own line
- Format: `(identifier)=` where identifier is any non-empty text
- The parentheses and equals sign are required
- Cannot be empty: `()=` is invalid
- Does not work inside code blocks

**HTML Output:**
```html
<div class="myst-target"><a href="#label-name">(label-name)=</a></div>
```

**Examples:**
```markdown
(intro)=
# Introduction

This section can be referenced elsewhere.

(fig-1)=
![My Image](image.png)

(section-results)=
## Results

Cross-reference the [intro](intro) section.
```

### Usage with markdown-it-py

**Basic Setup:**
```python
from markdown_it import MarkdownIt
from mdit_py_plugins.myst_blocks import myst_block_plugin

# Create parser and enable plugin
md = MarkdownIt()
md.use(myst_block_plugin)

# Parse markdown with MyST blocks
markdown_text = """
% This is a comment

(my-target)=
# Heading

Some content here.

+++

More content after the break.
"""

html = md.render(markdown_text)
```

**Custom Rendering:**

You can override the default renderers:

```python
from markdown_it import MarkdownIt
from mdit_py_plugins.myst_blocks import myst_block_plugin

md = MarkdownIt()
md.use(myst_block_plugin)

# Custom target renderer
def custom_target_renderer(self, tokens, idx, options, env):
    label = tokens[idx].content
    return f'<a id="{label}" class="anchor"></a>'

# Custom comment renderer (e.g., strip comments in production)
def custom_comment_renderer(self, tokens, idx, options, env):
    # Return empty string to hide comments
    return ""

md.add_render_rule("myst_target", custom_target_renderer)
md.add_render_rule("myst_line_comment", custom_comment_renderer)
```

### Important Notes

1. **Not Code Block Safe:** These features are automatically disabled inside code blocks (fenced code or indented code blocks).

2. **Parsing Priority:** These rules are inserted before certain standard markdown rules:
   - Line comments: before blockquotes
   - Block breaks: before horizontal rules
   - Targets: before horizontal rules

3. **CSS Classes:**
   - Line comments: No class (rendered as HTML comments)
   - Block breaks: `class="myst-block"`
   - Targets: `class="myst-target"`

4. **Token Names:**
   - Line comments: `myst_line_comment`
   - Block breaks: `myst_block_break`
   - Targets: `myst_target`

### Common Use Cases

**Documentation with hidden notes:**
```markdown
% FIXME: This section needs review
% See issue #123 for context
## Feature Documentation
```

**Document sections with anchors:**
```markdown
(installation)=
## Installation

(configuration)=
## Configuration

See the [installation](#installation) section.
```

**Content separation:**
```markdown
## Chapter 1
Content here.

+++

## Chapter 2
New chapter content.
```

### Limitations

- Line comments only support single-line `%` syntax (not multi-line block comments)
- Targets are simple labels without built-in cross-reference resolution
- Block breaks always render as `<hr>` elements
- No support for nested structures within these constructs

---

**Note:** This plugin is part of the `mdit-py-plugins` package and works with the MyST (Markedly Structured Text) ecosystem, commonly used in Sphinx documentation and Jupyter Book projects.

User: I don't understand what Block Breaks (+++) does, can you provide the html for your example 
Section 1 content here.

+++

Section 2 content here.

++++++++

Section 3 content here.

GitHub Copilot: Let me run a quick test to show you the exact HTML output: 

Ran terminal command: cd /home/alessio/soft/python/mark2 && python3 << 'EOF'
from markdown_it import MarkdownIt
from mdit_py_plugins.myst_blocks import myst_block_plugin

md = MarkdownIt()
md.use(myst_block_plugin)

markdown_text = """Section 1 content here.

+++

Section 2 content here.

++++++++

Section 3 content here."""

html = md.render(markdown_text)
print(html)
EOF

Here's the HTML output:

```html
<p>Section 1 content here.</p>
<hr class="myst-block" />
<p>Section 2 content here.</p>
<hr class="myst-block" />
<p>Section 3 content here.</p>
```

**What Block Breaks (`+++`) do:**
- They create **horizontal rule elements** (`<hr>`) with the class `myst-block`
- They visually separate content sections (like thematic breaks)
- They're similar to standard Markdown horizontal rules (`---` or `***`), but use MyST syntax (`+++`)
- You can style them with CSS using the `.myst-block` class

**Visual rendering:** In a browser, each `<hr>` would typically appear as a horizontal line separating the three sections of content. The `myst-block` class allows you to style these breaks differently from regular `<hr>` elements if needed.

User: why use it against --- or ***

GitHub Copilot: Ran terminal command: cd /home/alessio/soft/python/mark2 && python3 << 'EOF'
from markdown_it import MarkdownIt
from mdit_py_plugins.myst_blocks import myst_block_plugin

md = MarkdownIt()
md.use(myst_block_plugin)

markdown_text = """Section 1

---

Section 2

***

Section 3

+++

Section 4"""

html = md.render(markdown_text)
print(html)
EOF

The key difference is the **CSS class**:

```html
<!-- Standard Markdown (--- or ***) -->
<hr />

<!-- MyST Block Breaks (+++) -->
<hr class="myst-block" />
```

**Why use `+++` instead of `---` or `***`:**

1. **Distinguishable styling** - The `myst-block` class lets you style MyST breaks differently via CSS:
   ```css
   hr { /* standard breaks */ }
   hr.myst-block { /* MyST breaks only */ }
   ```

2. **Semantic differentiation** - In MyST documents, `+++` has a specific meaning as a "thematic break" vs generic horizontal rules, useful for document processing/transformation

3. **MyST compatibility** - If you're using MyST in Jupyter Book or Sphinx, `+++` is the standard syntax for consistency across the ecosystem

4. **Future extensibility** - The class name allows MyST parsers to potentially handle these differently (e.g., page breaks in PDF, slide breaks in presentations)

**Practical answer:** If you don't need the distinction, `---` works fine. Use `+++` when you want MyST-specific styling or are working within the MyST/Jupyter Book ecosystem where it's the convention.

User: what do you mean with "Future extensibility - The class name allows MyST parsers to potentially handle these differently (e.g., page breaks in PDF, slide breaks in presentations)", explain better

GitHub Copilot: Searched for text `myst-block`, 3 results

Read [](file:///home/alessio/soft/python/mark2/src/mark2/renderer/pdf.py)

Let me check how the renderers handle hr tokens: 

Searched for text `def hr(`, 4 results

Searched for text `myst_block_break`, 3 results

Read [](file:///home/alessio/soft/python/mark2/src/mark2/renderer/context.py#230-230), lines 230 to 250

Perfect! Now let me create a demonstration to explain this concept: 

Ran terminal command: cd /home/alessio/soft/python/mark2 && python3 << 'EOF'
from markdown_it import MarkdownIt
from mdit_py_plugins.myst_blocks import myst_block_plugin

# Let's show how the token looks internally
md = MarkdownIt()
md.use(myst_block_plugin)

markdown_text = """Content before

---

Content middle

+++

Content after"""

tokens = md.parse(markdown_text)

# Show the difference in tokens
for token in tokens:
    if token.type in ['hr', 'myst_block_break']:
        print(f"Token type: {token.type}")
        print(f"  Tag: {token.tag}")
        print(f"  Attributes: {token.attrs}")
        print()

EOF

Now let me explain with a concrete example:

**The key is that MyST creates a *different token type* (`myst_block_break`) with a *class attribute*, while standard Markdown creates a plain `hr` token.**

Here's what "future extensibility" means in practice:

### Example 1: Custom PDF Rendering

A renderer could detect `myst_block_break` tokens and convert them to page breaks in PDF instead of just horizontal lines:

```python
# In a PDF renderer
def myst_block_break(self, tokens, idx, options, env):
    """Render MyST block break as a page break in PDF."""
    return "\\page\n"  # LaTeX/ConTeXt page break

def hr(self, tokens, idx, options, env):
    """Render normal hr as a thin rule."""
    return "\\thinrule\n"  # Just a line
```

**Result:**
- `---` → thin horizontal line in PDF
- `+++` → new page in PDF

### Example 2: Presentation/Slides

In slide generation, you could use `+++` to separate slides:

```python
# In a reveal.js/slides renderer
def myst_block_break(self, tokens, idx, options, env):
    """Start a new slide."""
    return '</section>\n<section>\n'

def hr(self, tokens, idx, options, env):
    """Just a decorative line within a slide."""
    return '<hr />'
```

**Result in your markdown:**
```markdown
## Slide 1 Title
Content for slide 1

+++

## Slide 2 Title
Content for slide 2
```

### Example 3: EPUB Chapter Breaks

```python
def myst_block_break(self, tokens, idx, options, env):
    """Start a new EPUB chapter."""
    return self.create_new_chapter()

def hr(self, tokens, idx, options, env):
    """Just a decorative element."""
    return '<hr />'
```

### Why This Matters

**Standard `---`:**
- Always means "horizontal line"
- Same output in HTML, PDF, EPUB

**MyST `+++`:**
- Means "thematic/major break"
- Can be interpreted differently per output format: 
  - HTML → `<hr class="myst-block">`
  - PDF → page break
  - Slides → new slide
  - EPUB → new chapter

The class name `myst-block` and separate token type `myst_block_break` give tools the *information* to make these decisions. Currently in your mark2 project, it just renders as `<hr>`, but a custom renderer could handle it specially.
