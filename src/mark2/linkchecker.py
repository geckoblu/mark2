"""Link checker module for validating links in Markdown documents."""

import urllib.parse
import urllib.request
from collections.abc import Sequence
from typing import Any

from markdown_it.token import Token


class LinkInfo:
    """Information about a link found in the document."""

    def __init__(self, url: str, text: str, line: int):
        """Initialize link information.

        Args:
            url: The URL of the link
            text: The link text or alt text
            line: Line number where the link appears
        """
        self.url: str = url
        self.text: str = text
        self.line: int = line
        self.status: str = "unknown"
        self.error: str | None = None

    def __repr__(self) -> str:
        """String representation of link info."""
        return f"LinkInfo(url={self.url!r}, text={self.text!r}, line={self.line})"


def extract_links(tokens: Sequence[Token]) -> list[LinkInfo]:
    """Extract all links from the token stream.

    Args:
        tokens: List of markdown-it tokens

    Returns:
        List of LinkInfo objects
    """
    links: list[LinkInfo] = []

    def process_tokens(token_list: Sequence[Token], current_line: int = 0) -> None:
        """Recursively process tokens to find links.

        Args:
            token_list: List of tokens to process
            current_line: Current line number from parent token
        """
        for token in token_list:
            # Update line number if this token has map information
            if token.map is not None:
                current_line = token.map[0] + 1

            # Extract links from link_open tokens
            if token.type == "link_open":
                url = token.attrGet("href") or ""
                text = ""
                links.append(LinkInfo(url, text, current_line))

            # Extract images
            elif token.type == "image":
                url = token.attrGet("src") or ""
                text = token.content or ""
                links.append(LinkInfo(url, text, current_line))

            # Process children recursively, passing down the current line
            if token.children:
                process_tokens(token.children, current_line)

    process_tokens(tokens)

    # Post-process to add text to links
    # Flatten the token tree to find link text
    def flatten_tokens(token_list: Sequence[Token]) -> list[Token]:
        """Flatten nested tokens into a single list."""
        result: list[Token] = []
        for token in token_list:
            result.append(token)
            if token.children:
                result.extend(flatten_tokens(token.children))
        return result

    flat_tokens = flatten_tokens(tokens)
    current_link_idx = -1

    for i, token in enumerate(flat_tokens):
        if token.type == "link_open":
            current_link_idx += 1
            # Find text in next few tokens
            text_parts: list[str] = []
            for j in range(i + 1, min(i + 10, len(flat_tokens))):
                if flat_tokens[j].type == "link_close":
                    break
                if flat_tokens[j].type == "text":
                    text_parts.append(flat_tokens[j].content)
                elif flat_tokens[j].type == "code_inline":
                    text_parts.append(flat_tokens[j].content)
            if text_parts and current_link_idx < len(links):
                links[current_link_idx].text = "".join(text_parts)

    return links


def check_link(link: LinkInfo, timeout: int = 5) -> None:
    """Check if a link is valid.

    Args:
        link: LinkInfo object to check
        timeout: Timeout in seconds for HTTP requests
    """
    url = link.url

    # Skip empty links
    if not url:
        link.status = "empty"
        link.error = "Empty URL"
        return

    # Handle internal links (anchors)
    if url.startswith("#"):
        link.status = "internal"
        return

    # Handle mailto links
    if url.startswith("mailto:"):
        # Basic email validation
        email = url[7:]
        if "@" in email and "." in email.split("@")[1]:
            link.status = "valid"
        else:
            link.status = "invalid"
            link.error = "Invalid email address"
        return

    # Handle relative links
    if not url.startswith(("http://", "https://", "ftp://", "ftps://")):
        link.status = "relative"
        return

    # Check HTTP/HTTPS links
    try:
        # Create request with a user agent to avoid being blocked
        req = urllib.request.Request(
            url, headers={"User-Agent": "Mozilla/5.0 (Mark2 Link Checker)"}
        )
        with urllib.request.urlopen(req, timeout=timeout) as response:
            status_code = response.getcode()
            if status_code and 200 <= status_code < 400:
                link.status = "valid"
            else:
                link.status = "warning"
                link.error = f"HTTP {status_code}"
    except urllib.error.HTTPError as e:
        link.status = "invalid"
        link.error = f"HTTP {e.code}: {e.reason}"
    except urllib.error.URLError as e:
        link.status = "invalid"
        link.error = f"URL Error: {e.reason}"
    except Exception as e:  # pylint: disable=broad-except
        link.status = "error"
        link.error = f"Error: {str(e)}"


def check_all_links(tokens: Sequence[Token], quiet: bool = False) -> dict[str, Any]:
    """Extract and check all links in the document.

    Args:
        tokens: List of markdown-it tokens
        quiet: If True, suppress progress messages

    Returns:
        Dictionary with link check results
    """
    links = extract_links(tokens)

    if not links:
        if not quiet:
            print("No links found in the document.")
        return {"total": 0, "links": []}

    # if not quiet:
    #     print(f"\nFound {len(links)} link(s) in the document.\n")
    #     print("Checking links...\n")

    for _i, link in enumerate(links, 1):
        # if not quiet:
        #     print(f"[{i}/{len(links)}] Checking: {link.url}")
        check_link(link)

    # Summarize results
    status_counts: dict[str, int] = {}
    for link in links:
        status_counts[link.status] = status_counts.get(link.status, 0) + 1

    return {"total": len(links), "links": links, "status_counts": status_counts}


def print_link_report(results: dict[str, Any]) -> bool:
    """Print a formatted report of link check results.

    Args:
        results: Results dictionary from check_all_links

    Returns:
        True if all links are valid, False if any are invalid/error
    """
    links = results["links"]
    status_counts = results["status_counts"]

    if not links:
        return True

    print("\n" + "=" * 80)
    print("LINK CHECK REPORT")
    print("=" * 80)

    # Group links by status
    groups: dict[str, list[LinkInfo]] = {
        "invalid": [],
        "error": [],
        "warning": [],
        "valid": [],
        "internal": [],
        "relative": [],
        "empty": [],
    }

    for link in links:
        groups[link.status].append(link)

    # Print invalid/error links first
    if groups["invalid"] or groups["error"]:
        print("\n❌ INVALID/ERROR LINKS:")
        print("-" * 80)
        for link in groups["invalid"] + groups["error"]:
            print(f"  Line {link.line}: {link.url}")
            if link.text:
                print(f"    Text: {link.text}")
            if link.error:
                print(f"    Error: {link.error}")
            print()

    # Print warnings
    if groups["warning"]:
        print("\n⚠️  WARNING LINKS:")
        print("-" * 80)
        for link in groups["warning"]:
            print(f"  Line {link.line}: {link.url}")
            if link.text:
                print(f"    Text: {link.text}")
            if link.error:
                print(f"    Warning: {link.error}")
            print()

    # Print valid links
    if groups["valid"]:
        print(f"\n✅ VALID LINKS ({len(groups['valid'])}):")
        print("-" * 80)
        for link in groups["valid"]:
            print(f"  Line {link.line}: {link.url}")

    # Print internal/relative links
    if groups["internal"]:
        print(f"\n🔗 INTERNAL ANCHORS ({len(groups['internal'])}):")
        print("-" * 80)
        for link in groups["internal"]:
            print(f"  Line {link.line}: {link.url}")

    if groups["relative"]:
        print(f"\n📁 RELATIVE LINKS ({len(groups['relative'])}):")
        print("-" * 80)
        for link in groups["relative"]:
            print(f"  Line {link.line}: {link.url}")

    if groups["empty"]:
        print(f"\n⚠️  EMPTY LINKS ({len(groups['empty'])}):")
        print("-" * 80)
        for link in groups["empty"]:
            print(f"  Line {link.line}: (empty URL)")

    # Print summary
    print("\n" + "=" * 80)
    print("SUMMARY:")
    print("-" * 80)
    print(f"Total links: {results['total']}")
    for status, count in sorted(status_counts.items()):
        print(f"  {status}: {count}")
    print("=" * 80)

    # Return exit code
    invalid_count = status_counts.get("invalid", 0) + status_counts.get("error", 0)
    if invalid_count > 0:
        print(f"\n❌ Found {invalid_count} invalid/error link(s)")
        return False
    else:
        print("\n✅ All external links are valid!")
        return True
