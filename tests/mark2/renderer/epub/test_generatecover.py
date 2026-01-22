"""Tests for generatecover.py module."""

import re
from mark2.renderer.epub.generatecover import generate_cover, escape_xml, _calculate_font_size


class TestGenerateCover:
    """Tests for generate_cover function."""

    def test_basic_cover_generation(self):
        """Test basic cover generation with simple title and author."""
        svg = generate_cover("Test Title", "Test Author")

        assert svg.startswith("<svg")
        assert svg.endswith("</svg>")
        assert "Test Title" in svg
        assert "Test Author" in svg
        assert 'xmlns="http://www.w3.org/2000/svg"' in svg

    def test_default_dimensions(self):
        """Test default dimensions are 800x1200."""
        svg = generate_cover("Title", "Author")

        assert 'viewBox="0 0 800 1200"' in svg
        assert '<rect width="800" height="1200"' in svg

    def test_custom_dimensions(self):
        """Test custom width and height."""
        svg = generate_cover("Title", "Author", width=600, height=900)

        assert 'viewBox="0 0 600 900"' in svg
        assert '<rect width="600" height="900"' in svg

    def test_multiline_title(self):
        """Test title with line breaks."""
        svg = generate_cover("First Line\nSecond Line", "Author")

        assert "First Line" in svg
        assert "Second Line" in svg
        # Should have multiple text elements for title
        title_texts = re.findall(r"<text[^>]*>First Line</text>", svg)
        assert len(title_texts) == 1
        second_line_texts = re.findall(r"<text[^>]*>Second Line</text>", svg)
        assert len(second_line_texts) == 1

    def test_multiline_author(self):
        """Test author with line breaks."""
        svg = generate_cover("Title", "First Author\nSecond Author")

        assert "First Author" in svg
        assert "Second Author" in svg

    def test_title_styling(self):
        """Test title has bold font weight."""
        svg = generate_cover("Bold Title", "Author")

        # Find title text element
        title_match = re.search(r"<text[^>]*>Bold Title</text>", svg)
        assert title_match
        title_element = title_match.group(0)
        assert 'font-weight="bold"' in title_element

    def test_author_styling(self):
        """Test author styling (no bold)."""
        svg = generate_cover("Title", "Regular Author")

        # Find author text element
        author_match = re.search(r"<text[^>]*>Regular Author</text>", svg)
        assert author_match
        author_element = author_match.group(0)
        assert 'font-weight="bold"' not in author_element

    def test_text_centered(self):
        """Test text is centered."""
        svg = generate_cover("Title", "Author", width=800)

        # All text elements should have x="400" (half of 800)
        text_elements = re.findall(r'<text x="(\d+)"', svg)
        assert all(x == "400" for x in text_elements)

    def test_background_color(self):
        """Test background rectangle has correct fill."""
        svg = generate_cover("Title", "Author")

        assert 'fill="#f5f5f5"' in svg

    def test_title_color(self):
        """Test title text color."""
        svg = generate_cover("My Title", "Author")

        title_match = re.search(r"<text[^>]*>My Title</text>", svg)
        assert title_match
        assert 'fill="#333333"' in title_match.group(0)

    def test_author_color(self):
        """Test author text color."""
        svg = generate_cover("Title", "My Author")

        author_match = re.search(r"<text[^>]*>My Author</text>", svg)
        assert author_match
        assert 'fill="#666666"' in author_match.group(0)

    def test_svg_attributes(self):
        """Test SVG has required attributes."""
        svg = generate_cover("Title", "Author")

        assert 'height="100%"' in svg
        assert 'width="100%"' in svg
        assert 'preserveAspectRatio="xMidYMid meet"' in svg
        assert 'version="1.1"' in svg

    def test_font_family_serif(self):
        """Test text uses serif font family."""
        svg = generate_cover("Title", "Author")

        text_elements = re.findall(r"<text[^>]*>", svg)
        for element in text_elements:
            assert 'font-family="serif"' in element

    def test_text_anchor_middle(self):
        """Test text has middle anchor for centering."""
        svg = generate_cover("Title", "Author")

        text_elements = re.findall(r"<text[^>]*>", svg)
        for element in text_elements:
            assert 'text-anchor="middle"' in element

    def test_empty_title(self):
        """Test cover with empty title."""
        svg = generate_cover("", "Author")

        assert svg.startswith("<svg")
        assert "Author" in svg

    def test_empty_author(self):
        """Test cover with empty author."""
        svg = generate_cover("Title", "")

        assert svg.startswith("<svg")
        assert "Title" in svg

    def test_xml_escaping_in_title(self):
        """Test XML special characters are escaped in title."""
        svg = generate_cover("Title & <Test>", "Author")

        assert "Title &amp; &lt;Test&gt;" in svg
        assert "Title & <Test>" not in svg

    def test_xml_escaping_in_author(self):
        """Test XML special characters are escaped in author."""
        svg = generate_cover("Title", "Author & <Name>")

        assert "Author &amp; &lt;Name&gt;" in svg
        assert "Author & <Name>" not in svg

    def test_very_long_title_scales_down(self):
        """Test very long title results in smaller font size."""
        svg = generate_cover("A" * 100, "Author")

        # Find the title font size
        title_match = re.search(r'<text[^>]*font-size="(\d+)"[^>]*font-weight="bold"', svg)
        assert title_match
        font_size = int(title_match.group(1))
        # Should be smaller than default 72
        assert font_size < 72

    def test_short_title_uses_larger_font(self):
        """Test short title uses default font size."""
        svg = generate_cover("Hi", "Author")

        # Find the title font size
        title_match = re.search(r'<text[^>]*font-size="(\d+)"[^>]*font-weight="bold"', svg)
        assert title_match
        font_size = int(title_match.group(1))
        # Should be at or near default 72
        assert font_size >= 60

    def test_font_sizes_relationship(self):
        """Test author font size is smaller than or equal to title font size."""
        svg = generate_cover("Test Title", "Test Author")

        # Extract font sizes using more specific patterns
        # Title has font-weight="bold"
        title_size_match = re.search(r'font-size="(\d+)"[^>]*font-weight="bold"', svg)
        # Author doesn't have font-weight="bold", find the font-size not followed by font-weight
        # Look for text elements without bold
        all_font_sizes = re.findall(r'font-size="(\d+)"', svg)
        title_size = int(title_size_match.group(1)) if title_size_match else int(all_font_sizes[0])
        author_size = int(all_font_sizes[-1])  # Last font-size is author

        assert author_size <= title_size

    def test_vertical_positioning(self):
        """Test title and author are vertically separated."""
        svg = generate_cover("Title", "Author", height=1200)

        # Extract y positions - y can be float
        title_match = re.search(r'<text x="\d+" y="([\d.]+)"[^>]*>Title</text>', svg)
        author_match = re.search(r'<text x="\d+" y="([\d.]+)"[^>]*>Author</text>', svg)

        title_y = float(title_match.group(1))
        author_y = float(author_match.group(1))

        # Author should be below title
        assert author_y > title_y
        # Should be significantly separated (at least 100 pixels)
        assert author_y - title_y > 100

    def test_multiline_vertical_spacing(self):
        """Test multiline text has proper vertical spacing."""
        svg = generate_cover("Line 1\nLine 2\nLine 3", "Author")

        # Extract all title line y positions - look for bold text elements
        # The pattern should match y attribute which may have decimal values
        line_matches = re.findall(r'y="([\d.]+)"[^>]*font-weight="bold"', svg)
        y_positions = [float(y) for y in line_matches]

        # Should have 3 lines
        assert len(y_positions) == 3
        # Each subsequent line should be below the previous
        for i in range(len(y_positions) - 1):
            assert y_positions[i + 1] > y_positions[i]


class TestCalculateFontSize:
    """Tests for _calculate_font_size helper function."""

    def test_single_short_line(self):
        """Test font size for single short line."""
        font_size = _calculate_font_size(["Hi"], 72, 760, bold=False)

        # Short text should use initial size
        assert font_size == 72

    def test_single_long_line(self):
        """Test font size reduces for long line."""
        long_line = "A" * 100
        font_size = _calculate_font_size([long_line], 72, 760, bold=False)

        # Long text should reduce font size
        assert font_size < 72

    def test_multiple_lines_uses_longest(self):
        """Test font size calculation uses longest line."""
        lines = ["Short", "A" * 50, "Med"]
        font_size = _calculate_font_size(lines, 72, 760, bold=False)

        # Should be reduced due to longest line
        assert font_size < 72

    def test_bold_text_wider(self):
        """Test bold text results in smaller font size."""
        text = ["A" * 30]
        normal_size = _calculate_font_size(text, 72, 760, bold=False)
        bold_size = _calculate_font_size(text, 72, 760, bold=True)

        # Bold should be same or smaller (wider characters)
        assert bold_size <= normal_size

    def test_minimum_font_size(self):
        """Test font size doesn't go below minimum (20)."""
        very_long_line = "X" * 1000
        font_size = _calculate_font_size([very_long_line], 72, 100, bold=False)

        # Should not go below 20
        assert font_size >= 20

    def test_empty_lines_list(self):
        """Test with empty lines list returns initial size."""
        font_size = _calculate_font_size([], 50, 500, bold=False)

        assert font_size == 50

    def test_exact_fit(self):
        """Test text that fits exactly at initial size."""
        # Calculate a line that fits at initial size
        initial_size = 50
        max_width = 500
        char_width = 0.5
        # Line length that should fit: max_width / (initial_size * char_width)
        line_length = int(max_width / (initial_size * char_width))
        line = "A" * line_length

        font_size = _calculate_font_size([line], initial_size, max_width, bold=False)

        # Should be at or near initial size
        assert font_size >= initial_size - 2

    def test_iterative_reduction(self):
        """Test font size reduces by 2 per iteration."""
        # Create text that needs reduction
        text = ["A" * 50]
        font_size = _calculate_font_size(text, 72, 300, bold=False)

        # Should be an even reduction from 72
        assert (72 - font_size) % 2 == 0

    def test_different_initial_sizes(self):
        """Test function works with different initial sizes."""
        text = ["Test"]

        size_30 = _calculate_font_size(text, 30, 760, bold=False)
        size_50 = _calculate_font_size(text, 50, 760, bold=False)
        size_100 = _calculate_font_size(text, 100, 760, bold=False)

        # Short text should keep initial sizes
        assert size_30 == 30
        assert size_50 == 50
        assert size_100 == 100

    def test_narrow_width_constraint(self):
        """Test with very narrow max width."""
        text = ["Medium text"]
        font_size = _calculate_font_size(text, 72, 50, bold=False)

        # Should reduce significantly or reach minimum
        assert font_size <= 30


class TestEscapeXml:
    """Tests for escape_xml helper function."""

    def test_ampersand_escaping(self):
        """Test ampersand is escaped."""
        assert escape_xml("Tom & Jerry") == "Tom &amp; Jerry"

    def test_less_than_escaping(self):
        """Test less than sign is escaped."""
        assert escape_xml("1 < 2") == "1 &lt; 2"

    def test_greater_than_escaping(self):
        """Test greater than sign is escaped."""
        assert escape_xml("2 > 1") == "2 &gt; 1"

    def test_double_quote_escaping(self):
        """Test double quotes are escaped."""
        assert escape_xml('Say "Hello"') == "Say &quot;Hello&quot;"

    def test_single_quote_escaping(self):
        """Test single quotes are escaped."""
        assert escape_xml("It's fine") == "It&apos;s fine"

    def test_multiple_special_chars(self):
        """Test multiple special characters at once."""
        result = escape_xml('<tag attr="value"> & </tag>')
        expected = "&lt;tag attr=&quot;value&quot;&gt; &amp; &lt;/tag&gt;"
        assert result == expected

    def test_no_special_chars(self):
        """Test text without special characters remains unchanged."""
        text = "Normal text without special chars"
        assert escape_xml(text) == text

    def test_empty_string(self):
        """Test empty string returns empty string."""
        assert escape_xml("") == ""

    def test_only_special_chars(self):
        """Test string with only special characters."""
        assert escape_xml("&<>\"'") == "&amp;&lt;&gt;&quot;&apos;"

    def test_repeated_special_chars(self):
        """Test repeated special characters."""
        assert escape_xml("&&&") == "&amp;&amp;&amp;"
        assert escape_xml("<<<") == "&lt;&lt;&lt;"

    def test_unicode_preserved(self):
        """Test unicode characters are preserved."""
        text = "Café naïve résumé"
        assert escape_xml(text) == text

    def test_numbers_preserved(self):
        """Test numbers are preserved."""
        text = "12345 67890"
        assert escape_xml(text) == text

    def test_whitespace_preserved(self):
        """Test whitespace is preserved."""
        text = "Line 1\n\tLine 2\n  Line 3"
        assert escape_xml(text) == text

    def test_html_like_content(self):
        """Test HTML-like content is properly escaped."""
        html = '<div class="test">Content & more</div>'
        expected = "&lt;div class=&quot;test&quot;&gt;Content &amp; more&lt;/div&gt;"
        assert escape_xml(html) == expected

    def test_order_of_escaping(self):
        """Test that ampersand is escaped first to avoid double escaping."""
        # "&lt;" should become "&amp;lt;" not "&amp;amp;lt;"
        result = escape_xml("&")
        assert result == "&amp;"
        # Verify no double escaping
        result2 = escape_xml("&lt;")
        assert result2 == "&amp;lt;"
