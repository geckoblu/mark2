"""Unit tests for the linkchecker module."""

import urllib.error
from unittest import mock

from markdown_it import MarkdownIt

from mark2 import linkchecker


class TestLinkInfo:
    """Tests for LinkInfo class."""

    def test_init(self):
        """Test LinkInfo initialization."""
        link = linkchecker.LinkInfo("https://example.com", "Example", 42)
        assert link.url == "https://example.com"
        assert link.text == "Example"
        assert link.line == 42
        assert link.status == "unknown"
        assert link.error is None

    def test_repr(self):
        """Test LinkInfo string representation."""
        link = linkchecker.LinkInfo("https://example.com", "Example", 42)
        repr_str = repr(link)
        assert "https://example.com" in repr_str
        assert "Example" in repr_str
        assert "42" in repr_str


class TestExtractLinks:
    """Tests for extract_links function."""

    def test_extract_simple_link(self):
        """Test extracting a simple link."""
        md = MarkdownIt()
        tokens = md.parse("[Example](https://example.com)")
        links = linkchecker.extract_links(tokens)

        assert len(links) == 1
        assert links[0].url == "https://example.com"
        assert links[0].text == "Example"
        assert links[0].line > 0

    def test_extract_multiple_links(self):
        """Test extracting multiple links."""
        md = MarkdownIt()
        tokens = md.parse("[Link1](https://example1.com) and [Link2](https://example2.com)")
        links = linkchecker.extract_links(tokens)

        assert len(links) == 2
        assert links[0].url == "https://example1.com"
        assert links[0].text == "Link1"
        assert links[1].url == "https://example2.com"
        assert links[1].text == "Link2"

    def test_extract_image(self):
        """Test extracting image link."""
        md = MarkdownIt()
        tokens = md.parse("![Alt text](https://example.com/image.png)")
        links = linkchecker.extract_links(tokens)

        assert len(links) == 1
        assert links[0].url == "https://example.com/image.png"
        assert links[0].text == "Alt text"

    def test_extract_internal_anchor(self):
        """Test extracting internal anchor link."""
        md = MarkdownIt()
        tokens = md.parse("[Section](#section)")
        links = linkchecker.extract_links(tokens)

        assert len(links) == 1
        assert links[0].url == "#section"
        assert links[0].text == "Section"

    def test_extract_relative_link(self):
        """Test extracting relative link."""
        md = MarkdownIt()
        tokens = md.parse("[README](README.md)")
        links = linkchecker.extract_links(tokens)

        assert len(links) == 1
        assert links[0].url == "README.md"
        assert links[0].text == "README"

    def test_extract_mailto_link(self):
        """Test extracting mailto link."""
        md = MarkdownIt()
        tokens = md.parse("[Email](mailto:test@example.com)")
        links = linkchecker.extract_links(tokens)

        assert len(links) == 1
        assert links[0].url == "mailto:test@example.com"
        assert links[0].text == "Email"

    def test_extract_empty_link(self):
        """Test extracting empty link."""
        md = MarkdownIt()
        tokens = md.parse("[Empty]()")
        links = linkchecker.extract_links(tokens)

        assert len(links) == 1
        assert links[0].url == ""
        assert links[0].text == "Empty"

    def test_no_links(self):
        """Test document with no links."""
        md = MarkdownIt()
        tokens = md.parse("This is just plain text.")
        links = linkchecker.extract_links(tokens)

        assert len(links) == 0

    def test_link_with_code_inline(self):
        """Test link containing inline code."""
        md = MarkdownIt()
        tokens = md.parse("[Link with `code`](https://example.com)")
        links = linkchecker.extract_links(tokens)

        assert len(links) == 1
        assert links[0].url == "https://example.com"
        assert "code" in links[0].text

    def test_links_on_different_lines(self):
        """Test that line numbers are correctly tracked."""
        md = MarkdownIt()
        markdown = """# Title

[Link1](https://example1.com)

More text

[Link2](https://example2.com)
"""
        tokens = md.parse(markdown)
        links = linkchecker.extract_links(tokens)

        assert len(links) == 2
        assert links[0].line < links[1].line


class TestCheckLink:
    """Tests for check_link function."""

    def test_empty_link(self):
        """Test checking empty link."""
        link = linkchecker.LinkInfo("", "Empty", 1)
        linkchecker.check_link(link)

        assert link.status == "empty"
        assert link.error == "Empty URL"

    def test_internal_link(self):
        """Test checking internal anchor link."""
        link = linkchecker.LinkInfo("#section", "Section", 1)
        linkchecker.check_link(link)

        assert link.status == "internal"
        assert link.error is None

    def test_relative_link(self):
        """Test checking relative link."""
        link = linkchecker.LinkInfo("README.md", "README", 1)
        linkchecker.check_link(link)

        assert link.status == "relative"
        assert link.error is None

    def test_relative_link_with_path(self):
        """Test checking relative link with path."""
        link = linkchecker.LinkInfo("../docs/README.md", "Docs", 1)
        linkchecker.check_link(link)

        assert link.status == "relative"
        assert link.error is None

    def test_valid_mailto(self):
        """Test checking valid mailto link."""
        link = linkchecker.LinkInfo("mailto:test@example.com", "Email", 1)
        linkchecker.check_link(link)

        assert link.status == "valid"
        assert link.error is None

    def test_invalid_mailto(self):
        """Test checking invalid mailto link."""
        link = linkchecker.LinkInfo("mailto:invalid-email", "Invalid", 1)
        linkchecker.check_link(link)

        assert link.status == "invalid"
        assert link.error == "Invalid email address"

    @mock.patch("urllib.request.urlopen")
    def test_valid_http_link(self, mock_urlopen):
        """Test checking valid HTTP link."""
        mock_response = mock.MagicMock()
        mock_response.getcode.return_value = 200
        mock_urlopen.return_value.__enter__.return_value = mock_response

        link = linkchecker.LinkInfo("https://example.com", "Example", 1)
        linkchecker.check_link(link)

        assert link.status == "valid"
        assert link.error is None

    @mock.patch("urllib.request.urlopen")
    def test_redirect_http_link(self, mock_urlopen):
        """Test checking HTTP link with redirect."""
        mock_response = mock.MagicMock()
        mock_response.getcode.return_value = 301
        mock_urlopen.return_value.__enter__.return_value = mock_response

        link = linkchecker.LinkInfo("https://example.com", "Example", 1)
        linkchecker.check_link(link)

        assert link.status == "valid"
        assert link.error is None

    @mock.patch("urllib.request.urlopen")
    def test_http_error_404(self, mock_urlopen):
        """Test checking HTTP link with 404 error."""
        mock_urlopen.side_effect = urllib.error.HTTPError(
            "https://example.com", 404, "Not Found", {}, None
        )

        link = linkchecker.LinkInfo("https://example.com/notfound", "NotFound", 1)
        linkchecker.check_link(link)

        assert link.status == "invalid"
        assert "404" in link.error  # pylint: disable=unsupported-membership-test

    @mock.patch("urllib.request.urlopen")
    def test_http_error_500(self, mock_urlopen):
        """Test checking HTTP link with 500 error."""
        mock_urlopen.side_effect = urllib.error.HTTPError(
            "https://example.com", 500, "Internal Server Error", {}, None
        )

        link = linkchecker.LinkInfo("https://example.com/error", "Error", 1)
        linkchecker.check_link(link)

        assert link.status == "invalid"
        assert "500" in link.error  # pylint: disable=unsupported-membership-test

    @mock.patch("urllib.request.urlopen")
    def test_url_error(self, mock_urlopen):
        """Test checking link with URL error."""
        mock_urlopen.side_effect = urllib.error.URLError("Connection refused")

        link = linkchecker.LinkInfo("https://nonexistent.invalid", "Invalid", 1)
        linkchecker.check_link(link)

        assert link.status == "invalid"
        assert "URL Error" in link.error  # pylint: disable=unsupported-membership-test

    @mock.patch("urllib.request.urlopen")
    def test_timeout_error(self, mock_urlopen):
        """Test checking link with timeout."""
        mock_urlopen.side_effect = TimeoutError("Connection timed out")

        link = linkchecker.LinkInfo("https://slow.example.com", "Slow", 1)
        linkchecker.check_link(link)

        assert link.status == "error"
        assert "Error" in link.error  # pylint: disable=unsupported-membership-test

    @mock.patch("urllib.request.urlopen")
    def test_custom_timeout(self, mock_urlopen):
        """Test checking link with custom timeout."""
        mock_response = mock.MagicMock()
        mock_response.getcode.return_value = 200
        mock_urlopen.return_value.__enter__.return_value = mock_response

        link = linkchecker.LinkInfo("https://example.com", "Example", 1)
        linkchecker.check_link(link, timeout=10)

        assert link.status == "valid"
        # Verify timeout was passed to urlopen
        call_args = mock_urlopen.call_args
        assert call_args[1]["timeout"] == 10

    @mock.patch("urllib.request.urlopen")
    def test_user_agent_header(self, mock_urlopen):
        """Test that user agent header is set."""
        mock_response = mock.MagicMock()
        mock_response.getcode.return_value = 200
        mock_urlopen.return_value.__enter__.return_value = mock_response

        link = linkchecker.LinkInfo("https://example.com", "Example", 1)
        linkchecker.check_link(link)

        # Verify user agent was set
        call_args = mock_urlopen.call_args
        request = call_args[0][0]
        # HTTP headers are case-insensitive, urllib stores as 'User-agent'
        assert "User-agent" in request.headers
        assert "Mark2 Link Checker" in request.headers["User-agent"]


class TestCheckAllLinks:
    """Tests for check_all_links function."""

    @mock.patch("urllib.request.urlopen")
    def test_check_all_links_empty(self, mock_urlopen):
        """Test checking document with no links."""
        md = MarkdownIt()
        tokens = md.parse("No links here.")
        results = linkchecker.check_all_links(tokens, quiet=True)

        assert results["total"] == 0
        assert results["links"] == []  # pylint: disable=use-implicit-booleaness-not-comparison

    @mock.patch("urllib.request.urlopen")
    def test_check_all_links_mixed(self, mock_urlopen):
        """Test checking document with mixed link types."""
        mock_response = mock.MagicMock()
        mock_response.getcode.return_value = 200
        mock_urlopen.return_value.__enter__.return_value = mock_response

        md = MarkdownIt()
        markdown = """
[Valid](https://example.com)
[Internal](#section)
[Relative](README.md)
[Empty]()
"""
        tokens = md.parse(markdown)
        results = linkchecker.check_all_links(tokens, quiet=True)

        assert results["total"] == 4
        assert len(results["links"]) == 4
        assert "status_counts" in results

        status_counts = results["status_counts"]
        assert status_counts.get("valid", 0) == 1
        assert status_counts.get("internal", 0) == 1
        assert status_counts.get("relative", 0) == 1
        assert status_counts.get("empty", 0) == 1

    @mock.patch("urllib.request.urlopen")
    def test_check_all_links_http_errors(self, mock_urlopen):
        """Test checking document with HTTP errors."""
        # First call succeeds, second fails with 404
        mock_response = mock.MagicMock()
        mock_response.getcode.return_value = 200

        mock_urlopen.side_effect = [
            mock.MagicMock(__enter__=lambda s: mock_response, __exit__=mock.Mock()),
            urllib.error.HTTPError("url", 404, "Not Found", {}, None),
        ]

        md = MarkdownIt()
        markdown = """
[Valid](https://example.com)
[Invalid](https://example.com/notfound)
"""
        tokens = md.parse(markdown)
        results = linkchecker.check_all_links(tokens, quiet=True)

        assert results["total"] == 2
        status_counts = results["status_counts"]
        assert status_counts.get("valid", 0) == 1
        assert status_counts.get("invalid", 0) == 1


class TestPrintLinkReport:
    """Tests for print_link_report function."""

    def test_print_empty_report(self, capsys):
        """Test printing report with no links."""
        results = {"total": 0, "links": [], "status_counts": {}}
        success = linkchecker.print_link_report(results)

        assert success is True

    @mock.patch("urllib.request.urlopen")
    def test_print_valid_links_report(self, mock_urlopen, capsys):
        """Test printing report with valid links."""
        mock_response = mock.MagicMock()
        mock_response.getcode.return_value = 200
        mock_urlopen.return_value.__enter__.return_value = mock_response

        md = MarkdownIt()
        tokens = md.parse("[Example](https://example.com)")
        results = linkchecker.check_all_links(tokens, quiet=True)
        success = linkchecker.print_link_report(results)

        captured = capsys.readouterr()
        assert "LINK CHECK REPORT" in captured.out
        assert "VALID LINKS" in captured.out
        assert "https://example.com" in captured.out
        assert success is True

    @mock.patch("urllib.request.urlopen")
    def test_print_invalid_links_report(self, mock_urlopen, capsys):
        """Test printing report with invalid links."""
        mock_urlopen.side_effect = urllib.error.HTTPError("url", 404, "Not Found", {}, None)

        md = MarkdownIt()
        tokens = md.parse("[Broken](https://example.com/notfound)")
        results = linkchecker.check_all_links(tokens, quiet=True)
        success = linkchecker.print_link_report(results)

        captured = capsys.readouterr()
        assert "INVALID/ERROR LINKS" in captured.out
        assert "404" in captured.out
        assert success is False

    def test_print_internal_links_report(self, capsys):
        """Test printing report with internal links."""
        md = MarkdownIt()
        tokens = md.parse("[Section](#section)")
        results = linkchecker.check_all_links(tokens, quiet=True)
        success = linkchecker.print_link_report(results)

        captured = capsys.readouterr()
        assert "INTERNAL ANCHORS" in captured.out
        assert "#section" in captured.out
        assert success is True

    def test_print_relative_links_report(self, capsys):
        """Test printing report with relative links."""
        md = MarkdownIt()
        tokens = md.parse("[README](README.md)")
        results = linkchecker.check_all_links(tokens, quiet=True)
        success = linkchecker.print_link_report(results)

        captured = capsys.readouterr()
        assert "RELATIVE LINKS" in captured.out
        assert "README.md" in captured.out
        assert success is True

    def test_print_empty_links_report(self, capsys):
        """Test printing report with empty links."""
        md = MarkdownIt()
        tokens = md.parse("[Empty]()")
        results = linkchecker.check_all_links(tokens, quiet=True)
        success = linkchecker.print_link_report(results)

        captured = capsys.readouterr()
        assert "EMPTY LINKS" in captured.out
        assert success is True

    def test_print_summary(self, capsys):
        """Test that summary is printed."""
        md = MarkdownIt()
        tokens = md.parse("[Link](#section)")
        results = linkchecker.check_all_links(tokens, quiet=True)
        linkchecker.print_link_report(results)

        captured = capsys.readouterr()
        assert "SUMMARY" in captured.out
        assert "Total links:" in captured.out
