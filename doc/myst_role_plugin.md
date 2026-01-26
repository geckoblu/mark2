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
<span class="role">content</span>
```

For example, `{emphasis}`text`` becomes:
```html
<span class="role">text</span>
```

### Special Empty Roles
Some roles are allowed to be used without backticks or content. These act as markers:

**Supported empty roles:**
- `{line-break}` or `{br}` - Inserts a line break

**Syntax:**
```markdown
{line-break}
{br}
```

**Rendered as:**
```html
<br/>
```

**Example:**
```markdown
First line{line-break}
Second line{br}
Third line
```

becomes:
```html
<p>First line<br/>
Second line<br/>
Third line</p>
```

**Note:** The `{br}` role is an alias for `{line-break}` and they both render identically.

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
def custom_myst_role_renderer(renderer, tokens, idx, options, env):
    token = tokens[idx]
    name = token.meta.get("name", "unknown")
    content = token.content

    # Handle special empty roles
    if name == "line-break":
        return "<br/>"

    # Custom logic for specific roles
    if name == "emphasis":
        return f"<em>{content}</em>"
    elif name == "strong":
        return f"<strong>{content}</strong>"
    elif name == "code":
        return f"<code>{content}</code>"
    else:
        # Default rendering
        return f'<span class="role">{content}</span>'

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
- Empty roles (without backticks) are only supported for roles in the `ALLOWED_EMPTY_ROLES` set
  - Currently supported: `{line-break}`, `{br}`
  - These roles act as self-closing markers

### Implementation Details

**Parser function:** `_myst_role_parser`
- Registered before "backticks" in the inline ruler
- Uses regex pattern: `^\{([a-zA-Z0-9\_\-\+\:]+)\}` to match role names
- Supports escaped roles with backslash: `\{role}` won't be parsed
- Handles multiple backticks for content containing backticks
- Special handling for empty roles in `ALLOWED_EMPTY_ROLES`

**Renderer function:** `myst_role`
- Renders `{line-break}` as `<br/>`
- Renders other roles as `<span class="role">content</span>`
- Can be overridden via `md.add_render_rule("myst_role", custom_renderer)`

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

### Extending with Custom Empty Roles

To add your own empty roles (markers), modify the `ALLOWED_EMPTY_ROLES` set in the plugin:

```python
# In myst_role_plugin.py
ALLOWED_EMPTY_ROLES = {"line-break", "br", "page-break", "clearfix"}
EMPTY_ROLES_ALIAS = {"br": "line-break"}
```

Then implement custom rendering:

```python
def custom_myst_role_renderer(renderer, tokens, idx, options, env):
    token = tokens[idx]
    name = token.meta.get("name", "unknown")

    # Handle marker-style roles with empty content
    if name == "line-break":
        return "<br/>"
    elif name == "page-break":
        return '<div class="page-break"></div>'
    elif name == "clearfix":
        return '<div class="clearfix"></div>'

    # Handle roles with content
    return f'<span class="role">{token.content}</span>'
```

Now you can use:
- `{line-break}` → `<br/>`
- `{page-break}` → `<div class="page-break"></div>`
- `{clearfix}` → `<div class="clearfix"></div>`

---

## Frequently Asked Questions

**Q: Can I use an empty role (without content) to just place markers?**

A: Yes! As of the Mark2 implementation, roles in the `ALLOWED_EMPTY_ROLES` set (`{line-break}` and `{br}`) can be used without backticks:

```markdown
First line{line-break}Second line
```

For roles not in this set, you must use backticks with empty content:

```markdown
{my-marker}``
```

**Q: Why isn't my role rendering with custom HTML?**

A: The default renderer wraps all roles in `<span class="role">`. You need to override the renderer with `md.add_render_rule("myst_role", custom_renderer)` to implement custom behavior.

**Q: Can I have nested roles?**

A: No, MyST roles are inline elements and don't support nesting. Use container blocks for nested structures.
