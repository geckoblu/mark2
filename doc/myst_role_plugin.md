## MyST Role Plugin Documentation

### Overview
The `myst_role` plugin enables MyST-style roles in Markdown. Roles are inline markup elements that allow you to apply special semantics or formatting to text content.

### Syntax
```
{role-name}`content`
```

### Role Name Rules
- Must be enclosed in curly braces `{}`
- Can contain: letters (a-z, A-Z), numbers (0-9), underscores `_`, hyphens `-`, plus signs `+`, and colons `:`
- Pattern: `[a-zA-Z0-9\_\-\+\:]+`

### Backtick Rules
- You can use multiple backticks to delimit the content (like in code spans)
- The opening and closing backtick sequences must match in length
- Examples:
  - Single: `` {role}`content` ``
  - Double: ` {role}``content`` `
  - Triple: `` {role}```content``` ``

### Examples

**Valid role usage:**
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
{custom-role}`any content`
{my_role}`content`
{role-with-numbers123}`text`
{namespace:role}`content`
```

**Multiple backticks for content with backticks:**
```markdown
{code}``text with `backtick` inside``
{literal}```complex `code` with ``multiple`` backticks```
```

**Escaped roles (will NOT be parsed):**
```markdown
\{role}`this will be treated as literal text`
```

**Content with newlines:**
- Newlines in role content are automatically converted to spaces
```markdown
{role}`multi
line
content` → renders as "multi line content"
```

### HTML Output
By default, roles are rendered as:
```html
<code class="myst role">{role-name}[content]</code>
```

For example, `{emphasis}`text`` becomes:
```html
<code class="myst role">{emphasis}[text]</code>
```

### Usage in markdown-it-py

**Basic setup:**
```python
from markdown_it import MarkdownIt
from mdit_py_plugins.myst_role import myst_role_plugin

# Create parser and enable plugin
md = MarkdownIt()
md.use(myst_role_plugin)

# Parse markdown with roles
html = md.render("{emphasis}`important text`")
```

**Custom rendering:**
You can override the default renderer to handle specific roles differently:
```python
def custom_myst_role_renderer(self, tokens, idx, options, env):
    token = tokens[idx]
    name = token.meta.get("name", "unknown")
    content = token.content
    
    # Custom logic for specific roles
    if name == "emphasis":
        return f"<em>{content}</em>"
    elif name == "strong":
        return f"<strong>{content}</strong>"
    elif name == "code":
        return f"<code>{content}</code>"
    else:
        # Default rendering
        return f'<code class="myst role">{{{name}}}[{content}]</code>'

md = MarkdownIt()
md.use(myst_role_plugin)
md.add_render_rule("myst_role", custom_myst_role_renderer)
```

### Notes
- Role names are case-sensitive: `{Role}` and `{role}` are different
- No whitespace is allowed between `{role-name}` and the opening backticks
- The plugin doesn't define specific role behaviors - it only parses the syntax
- To implement specific role behaviors (like `{download}`, `{ref}`, etc.), you need to create custom renderers
- The plugin is parsed before standard backtick code spans in the inline parsing chain

### Common MyST Roles (require custom renderers)
While the plugin parses any valid role name, these are commonly used MyST roles you might want to implement custom renderers for:
- `{abbr}` - abbreviations
- `{doc}` - link to documents
- `{download}` - download links
- `{eq}` - equation references
- `{kbd}` - keyboard input
- `{math}` - inline math
- `{ref}` - cross-references
- `{sub}` - subscript
- `{sup}` - superscript

User: can I use an empty role (without content) to just place markers?
Like {line-break}

GitHub Copilot: Looking at the code, **no, you cannot use an empty role without backticks**. The plugin requires at least one backtick after the role name.

Here's the critical part:

```python
tick_length = pos - start
if not tick_length:
    return False  # Must have at least one backtick
```

However, **you CAN use a role with empty content** by using backticks with nothing between them:

```markdown
{line-break}``
```

This would parse successfully and create a token with:
- `name`: `"line-break"`
- `content`: `""` (empty string)

You could then implement a custom renderer to handle these empty-content roles as markers:

```python
def custom_myst_role_renderer(self, tokens, idx, options, env):
    token = tokens[idx]
    name = token.meta.get("name", "unknown")
    content = token.content
    
    # Handle marker-style roles with empty content
    if not content:
        if name == "line-break":
            return "<br/>"
        elif name == "page-break":
            return '<div class="page-break"></div>'
        elif name == "horizontal-rule":
            return "<hr/>"
    
    # Handle roles with content
    return f'<code class="myst role">{{{name}}}[{content}]</code>'
```

Then you could use:
- `{line-break}`` → `<br/>`
- `{page-break}`` → `<div class="page-break"></div>`
- `{horizontal-rule}`` → `<hr/>`
