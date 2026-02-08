"""Tests for generatefrontpage.py module."""

from mark2.renderer.epub.generatefrontpage import generate_frontpage, escape_html


class TestGenerateFrontpage:
    """Tests for generate_frontpage function."""

    def test_basic_frontpage_generation(self):
        """Test basic frontpage generation with simple title and author."""
        html = generate_frontpage("Test Title", "Test Author")

        assert html.startswith("<!DOCTYPE html>")
        assert html.endswith("</html>")
        assert "Test Title" in html
        assert "Test Author" in html
        assert 'xmlns="http://www.w3.org/1999/xhtml"' in html

    def test_html_structure(self):
        """Test HTML has proper structure with required elements."""
        html = generate_frontpage("Title", "Author")

        assert "<html" in html
        assert "<head>" in html
        assert "</head>" in html
        assert "<body>" in html
        assert "</body>" in html
        assert '<meta charset="utf-8"/>' in html

    def test_title_element(self):
        """Test HTML title element contains the book title."""
        html = generate_frontpage("My Book Title", "Author")

        assert "<title>My Book Title</title>" in html

    def test_multiline_title_in_head(self):
        """Test HTML title element uses only first line of multiline title."""
        html = generate_frontpage("First Line\nSecond Line", "Author")

        assert "<title>First Line</title>" in html
        assert "<title>First Line\nSecond Line</title>" not in html

    def test_multiline_title_in_body(self):
        """Test title with line breaks uses <br/> in body."""
        html = generate_frontpage("First Line\nSecond Line", "Author")

        assert "First Line<br/>Second Line" in html

    def test_multiline_author(self):
        """Test author with line breaks uses <br/>."""
        html = generate_frontpage("Title", "First Author\nSecond Author")

        assert "First Author<br/>Second Author" in html

    def test_three_line_title(self):
        """Test title with three lines."""
        html = generate_frontpage("Line 1\nLine 2\nLine 3", "Author")

        assert "Line 1<br/>Line 2<br/>Line 3" in html

    def test_title_div_class(self):
        """Test title is in div with class 'title'."""
        html = generate_frontpage("Test Title", "Author")

        assert '<div class="title">Test Title</div>' in html

    def test_author_div_class(self):
        """Test author is in div with class 'author'."""
        html = generate_frontpage("Title", "Test Author")

        assert '<div class="author">Test Author</div>' in html

    def test_frontpage_container(self):
        """Test frontpage has container div."""
        html = generate_frontpage("Title", "Author")

        assert '<div class="frontpage">' in html
        assert "</div>" in html

    def test_css_styling_present(self):
        """Test CSS style tag is present."""
        html = generate_frontpage("Title", "Author")

        assert "<style>" in html
        assert "</style>" in html

    def test_body_styling(self):
        """Test body has proper styling."""
        html = generate_frontpage("Title", "Author")

        # Check for body style properties
        assert "body {" in html or "body{" in html
        assert "text-align: center" in html
        assert "font-family: serif" in html
        assert "background-color: #f5f5f5" in html

    def test_title_styling(self):
        """Test title class has proper styling."""
        html = generate_frontpage("Title", "Author")

        assert ".title {" in html or ".title{" in html
        assert "font-weight: bold" in html
        assert "font-size: 2.5em" in html

    def test_author_styling(self):
        """Test author class has proper styling."""
        html = generate_frontpage("Title", "Author")

        assert ".author {" in html or ".author{" in html
        assert "font-size: 1.5em" in html

    def test_empty_title(self):
        """Test frontpage with empty title."""
        html = generate_frontpage("", "Author")

        assert html.startswith("<!DOCTYPE html>")
        assert "Author" in html
        assert '<div class="title"></div>' in html

    def test_empty_author(self):
        """Test frontpage with empty author."""
        html = generate_frontpage("Title", "")

        assert html.startswith("<!DOCTYPE html>")
        assert "Title" in html
        assert '<div class="author"></div>' in html

    def test_html_escaping_in_title(self):
        """Test HTML special characters are escaped in title."""
        html = generate_frontpage("Title & <Test>", "Author")

        assert "Title &amp; &lt;Test&gt;" in html
        assert "Title & <Test>" not in html

    def test_html_escaping_in_author(self):
        """Test HTML special characters are escaped in author."""
        html = generate_frontpage("Title", "Author & <Name>")

        assert "Author &amp; &lt;Name&gt;" in html
        assert "Author & <Name>" not in html

    def test_html_escaping_in_head_title(self):
        """Test HTML special characters are escaped in <title> element."""
        html = generate_frontpage("Book <Title> & More", "Author")

        assert "<title>Book &lt;Title&gt; &amp; More</title>" in html

    def test_quotes_in_title(self):
        """Test quotes are properly escaped in title."""
        html = generate_frontpage('Say "Hello"', "Author")

        assert "Say &quot;Hello&quot;" in html

    def test_apostrophe_in_author(self):
        """Test apostrophes are properly escaped in author."""
        html = generate_frontpage("Title", "O'Brien")

        assert "O&#39;Brien" in html

    def test_xmlns_namespace(self):
        """Test XHTML namespace is present."""
        html = generate_frontpage("Title", "Author")

        assert 'xmlns="http://www.w3.org/1999/xhtml"' in html

    def test_utf8_encoding(self):
        """Test UTF-8 encoding meta tag is present."""
        html = generate_frontpage("Title", "Author")

        assert 'charset="utf-8"' in html

    def test_unicode_characters(self):
        """Test unicode characters are preserved."""
        html = generate_frontpage("Café naïve", "José García")

        assert "Café naïve" in html
        assert "José García" in html

    def test_long_title(self):
        """Test very long title is properly included."""
        long_title = "A" * 100
        html = generate_frontpage(long_title, "Author")

        assert long_title in html

    def test_long_author(self):
        """Test very long author name is properly included."""
        long_author = "B" * 100
        html = generate_frontpage("Title", long_author)

        assert long_author in html

    def test_both_multiline(self):
        """Test both title and author with multiple lines."""
        html = generate_frontpage("Title 1\nTitle 2", "Author 1\nAuthor 2")

        assert "Title 1<br/>Title 2" in html
        assert "Author 1<br/>Author 2" in html

    def test_line_height_styling(self):
        """Test line-height properties are set."""
        html = generate_frontpage("Title", "Author")

        # Check for line-height in styles
        assert "line-height:" in html

    def test_margin_styling(self):
        """Test margin properties are present."""
        html = generate_frontpage("Title", "Author")

        assert "margin:" in html

    def test_special_chars_combination(self):
        """Test combination of special characters."""
        html = generate_frontpage("A&B<C>D\"E'F", "X&Y<Z>")

        assert "A&amp;B&lt;C&gt;D&quot;E&#39;F" in html
        assert "X&amp;Y&lt;Z&gt;" in html

    def test_newlines_only_in_title(self):
        """Test title with only newlines."""
        html = generate_frontpage("\n\n", "Author")

        assert html.startswith("<!DOCTYPE html>")
        assert "Author" in html

    def test_mixed_content(self):
        """Test realistic title and author combination."""
        html = generate_frontpage("The Great Gatsby\nA Novel", "F. Scott Fitzgerald")

        assert "The Great Gatsby<br/>A Novel" in html
        assert "F. Scott Fitzgerald" in html

    def test_subtitle_format(self):
        """Test common subtitle pattern."""
        html = generate_frontpage("Main Title\nSubtitle Here", "John Doe\nEditor")

        assert "Main Title<br/>Subtitle Here" in html
        assert "John Doe<br/>Editor" in html


class TestEscapeHtml:
    """Tests for escape_html helper function."""

    def test_ampersand_escaping(self):
        """Test ampersand is escaped."""
        assert escape_html("Tom & Jerry") == "Tom &amp; Jerry"

    def test_less_than_escaping(self):
        """Test less than sign is escaped."""
        assert escape_html("1 < 2") == "1 &lt; 2"

    def test_greater_than_escaping(self):
        """Test greater than sign is escaped."""
        assert escape_html("2 > 1") == "2 &gt; 1"

    def test_double_quote_escaping(self):
        """Test double quotes are escaped."""
        assert escape_html('Say "Hello"') == "Say &quot;Hello&quot;"

    def test_single_quote_escaping(self):
        """Test single quotes are escaped."""
        assert escape_html("It's fine") == "It&#39;s fine"

    def test_multiple_special_chars(self):
        """Test multiple special characters at once."""
        result = escape_html('<tag attr="value"> & </tag>')
        expected = "&lt;tag attr=&quot;value&quot;&gt; &amp; &lt;/tag&gt;"
        assert result == expected

    def test_no_special_chars(self):
        """Test text without special characters remains unchanged."""
        text = "Normal text without special chars"
        assert escape_html(text) == text

    def test_empty_string(self):
        """Test empty string returns empty string."""
        assert escape_html("") == ""

    def test_only_special_chars(self):
        """Test string with only special characters."""
        assert escape_html("&<>\"'") == "&amp;&lt;&gt;&quot;&#39;"

    def test_repeated_special_chars(self):
        """Test repeated special characters."""
        assert escape_html("&&&") == "&amp;&amp;&amp;"
        assert escape_html("<<<") == "&lt;&lt;&lt;"

    def test_unicode_preserved(self):
        """Test unicode characters are preserved."""
        text = "Café naïve résumé"
        assert escape_html(text) == text

    def test_numbers_preserved(self):
        """Test numbers are preserved."""
        text = "12345 67890"
        assert escape_html(text) == text

    def test_whitespace_preserved(self):
        """Test whitespace is preserved."""
        text = "Line 1\n\tLine 2\n  Line 3"
        assert escape_html(text) == text

    def test_html_like_content(self):
        """Test HTML-like content is properly escaped."""
        html_content = '<div class="test">Content & more</div>'
        expected = "&lt;div class=&quot;test&quot;&gt;Content &amp; more&lt;/div&gt;"
        assert escape_html(html_content) == expected

    def test_order_of_escaping(self):
        """Test that ampersand is escaped first to avoid double escaping."""
        result = escape_html("&")
        assert result == "&amp;"
        # Verify no double escaping
        result2 = escape_html("&lt;")
        assert result2 == "&amp;lt;"

    def test_script_tag_escaping(self):
        """Test script tags are properly escaped."""
        script = '<script>alert("XSS")</script>'
        expected = "&lt;script&gt;alert(&quot;XSS&quot;)&lt;/script&gt;"
        assert escape_html(script) == expected

    def test_mixed_quotes(self):
        """Test mixed single and double quotes."""
        text = """It's a "test" with 'quotes'"""
        expected = """It&#39;s a &quot;test&quot; with &#39;quotes&#39;"""
        assert escape_html(text) == expected

    def test_xml_entities_not_double_escaped(self):
        """Test that already escaped entities are escaped again (as intended)."""
        # This tests the actual behavior: escaping is not idempotent
        text = "&amp;"
        result = escape_html(text)
        assert result == "&amp;amp;"

    def test_newlines_and_special_chars(self):
        """Test newlines are preserved while special chars are escaped."""
        text = "Line 1 & 2\nLine 3 < 4"
        expected = "Line 1 &amp; 2\nLine 3 &lt; 4"
        assert escape_html(text) == expected

    def test_tabs_preserved(self):
        """Test tab characters are preserved."""
        text = "Col1\tCol2\tCol3"
        assert escape_html(text) == text

    def test_carriage_return_preserved(self):
        """Test carriage return is preserved."""
        text = "Line1\r\nLine2"
        assert escape_html(text) == text

    def test_all_entities_in_order(self):
        """Test all entities are escaped in correct order."""
        # Test the order: & must be first, then <, >, ", '
        text = "&<>\"'"
        result = escape_html(text)
        # Should be: & -> &amp;, < -> &lt;, > -> &gt;, " -> &quot;, ' -> &#39;
        assert result == "&amp;&lt;&gt;&quot;&#39;"
