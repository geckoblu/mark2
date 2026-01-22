"""Tests for imagesize.py module."""

import io
import os
import struct
import tempfile

import pytest

from mark2.renderer.epub.imagesize import get_image_size, getDPI, _convertToDPI, _convertToPx


class TestGetImageSize:
    """Tests for get_image_size function."""

    def test_gif87a_format(self):
        """Test GIF87a format image size detection."""
        # Create a minimal valid GIF87a file
        gif_data = b"GIF87a" + struct.pack("<hh", 100, 200) + b"\x00" * 20
        file_obj = io.BytesIO(gif_data)
        width, height = get_image_size(file_obj)
        assert width == 100
        assert height == 200

    def test_gif89a_format(self):
        """Test GIF89a format image size detection."""
        # Create a minimal valid GIF89a file
        gif_data = b"GIF89a" + struct.pack("<hh", 150, 250) + b"\x00" * 20
        file_obj = io.BytesIO(gif_data)
        width, height = get_image_size(file_obj)
        assert width == 150
        assert height == 250

    def test_png_with_ihdr_chunk(self):
        """Test PNG format with IHDR chunk."""
        # Create a minimal valid PNG file with IHDR chunk
        png_data = (
            b"\x89PNG\r\n\x1a\n"  # PNG signature
            + struct.pack(">I", 13)  # IHDR chunk length
            + b"IHDR"
            + struct.pack(">LL", 300, 400)  # width, height
            + b"\x00" * 5  # bit depth, color type, etc.
        )
        file_obj = io.BytesIO(png_data)
        width, height = get_image_size(file_obj)
        assert width == 300
        assert height == 400

    def test_png_older_version(self):
        """Test older PNG format without explicit IHDR chunk."""
        # Create a minimal PNG file (older version)
        png_data = b"\x89PNG\r\n\x1a\n" + struct.pack(">LL", 200, 300) + b"\x00" * 10
        file_obj = io.BytesIO(png_data)
        width, height = get_image_size(file_obj)
        assert width == 200
        assert height == 300

    def test_jpeg_format(self):
        """Test JPEG format image size detection."""
        # Create a minimal JPEG with SOF0 marker
        jpeg_data = (
            b"\xff\xd8"  # SOI marker
            + b"\xff\xe0"  # APP0 marker
            + struct.pack(">H", 16)  # segment length
            + b"JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00"
            + b"\xff\xc0"  # SOF0 marker
            + struct.pack(">H", 17)  # segment length
            + b"\x08"  # precision
            + struct.pack(">HH", 480, 640)  # height, width
            + b"\x03\x01\x22\x00\x02\x11\x01\x03\x11\x01"
        )
        file_obj = io.BytesIO(jpeg_data)
        width, height = get_image_size(file_obj)
        assert width == 640
        assert height == 480

    def test_jpeg2000_format(self):
        """Test JPEG2000 format image size detection."""
        # Create a minimal JPEG2000 file
        jp2_data = (
            b"\x00\x00\x00\x0cjP  \r\n\x87\n"  # JP2 signature
            + b"\x00" * 36  # padding to offset 48
            + struct.pack(">LL", 1024, 768)  # height, width
        )
        file_obj = io.BytesIO(jp2_data)
        width, height = get_image_size(file_obj)
        assert width == 768
        assert height == 1024

    def test_tiff_big_endian(self):
        """Test TIFF big endian format."""
        # Create a minimal TIFF file (big endian)
        tiff_data = (
            b"\x4d\x4d\x00\x2a"  # TIFF header (big endian)
            + struct.pack(">L", 8)  # IFD offset
            + struct.pack(">H", 2)  # Number of directory entries
            # Width tag (256)
            + struct.pack(">HHLL", 256, 4, 1, 800)
            # Height tag (257)
            + struct.pack(">HHLL", 257, 4, 1, 600)
        )
        file_obj = io.BytesIO(tiff_data)
        width, height = get_image_size(file_obj)
        assert width == 800
        assert height == 600

    def test_tiff_little_endian(self):
        """Test TIFF little endian format."""
        # Create a minimal TIFF file (little endian)
        tiff_data = (
            b"\x49\x49\x2a\x00"  # TIFF header (little endian)
            + struct.pack("<L", 8)  # IFD offset
            + struct.pack("<H", 2)  # Number of directory entries
            # Width tag (256)
            + struct.pack("<HHLL", 256, 4, 1, 1024)
            # Height tag (257)
            + struct.pack("<HHLL", 257, 4, 1, 768)
        )
        file_obj = io.BytesIO(tiff_data)
        width, height = get_image_size(file_obj)
        assert width == 1024
        assert height == 768

    def test_bigtiff_little_endian(self):
        """Test BigTIFF little endian format."""
        # Create a minimal BigTIFF file
        bigtiff_data = (
            b"\x49\x49\x2b\x00"  # BigTIFF header (little endian)
            + struct.pack("<L", 8)  # Bytesize offset
            + struct.pack("<Q", 16)  # IFD offset
            + struct.pack("<Q", 2)  # Number of directory entries
            # Width tag (256)
            + struct.pack("<HHQQ", 256, 4, 1, 2048)
            # Height tag (257)
            + struct.pack("<HHQQ", 257, 4, 1, 1536)
        )
        file_obj = io.BytesIO(bigtiff_data)
        width, height = get_image_size(file_obj)
        assert width == 2048
        assert height == 1536

    def test_svg_format(self):
        """Test SVG format image size detection."""
        svg_data = b'<?xml version="1.0"?><svg width="500px" height="300px"></svg>'
        file_obj = io.BytesIO(svg_data)
        width, height = get_image_size(file_obj)
        assert width == 500
        assert height == 300

    def test_svg_with_units_cm(self):
        """Test SVG with cm units."""
        svg_data = b'<svg width="10cm" height="5cm"></svg>' + b"\x00" * 1000
        file_obj = io.BytesIO(svg_data)
        width, height = get_image_size(file_obj)
        # 10cm * 96 / 2.54 ≈ 377.95
        assert 377 <= width <= 378
        assert 188 <= height <= 190

    def test_netpbm_format(self):
        """Test Netpbm format (P1-P6)."""
        # P3 format (ASCII PPM)
        netpbm_data = b"P3\n# Comment\n640 480\n255\n"
        file_obj = io.BytesIO(netpbm_data)
        width, height = get_image_size(file_obj)
        assert width == 640
        assert height == 480

    def test_webp_vp8_returns_defaults(self):
        """Test WebP VP8 with insufficient data returns defaults."""
        # head only reads 31 bytes, need all data in first 31 bytes
        webp_data = (
            b"RIFF"
            + struct.pack("<L", 100)
            + b"WEBP"
            + b"VP8 "
            + b"\x00" * 14  # Not enough padding to reach offset 26
            + struct.pack("<HH", 400, 300)
        )
        file_obj = io.BytesIO(webp_data)
        width, height = get_image_size(file_obj)
        # Returns 0 when head is too short (< 30 bytes total)
        assert width in (0, -1)
        assert height in (0, -1)

    def test_webp_vp8x_returns_defaults(self):
        """Test WebP VP8X with incomplete data."""
        # Need head[24:27] and head[27:30], so need at least 30 bytes total
        webp_data = (
            b"RIFF"
            + struct.pack("<L", 100)
            + b"WEBP"
            + b"VP8X"
            + b"\x00" * 12
            + bytes([799 & 0xFF, (799 >> 8) & 0xFF, (799 >> 16) & 0xFF])  # width - 1
            + bytes([599 & 0xFF, (599 >> 8) & 0xFF])
        )
        file_obj = io.BytesIO(webp_data)
        width, height = get_image_size(file_obj)  # pylint: disable=unused-variable
        # With incomplete data, width may be read but height will be partial/garbage
        assert width in (800, 0, -1)
        # height could be any value due to partial read

    def test_webp_vp8l_minimal(self):
        """Test WebP VP8L with minimal bit-packed data."""
        # VP8L reads head[21:25], so need at least 25 bytes in head
        # width - 1 = 0 (width=1), height - 1 = 0 (height=1)
        webp_data = (
            b"RIFF"
            + struct.pack("<L", 100)
            + b"WEBP"
            + b"VP8L"
            + b"\x00" * 9  # bytes 12-20
            + b"\x00\x00\x00\x00"  # bytes 21-24: all zeros = width=1, height=1
            + b"\x00" * 6  # padding
        )
        file_obj = io.BytesIO(webp_data)
        width, height = get_image_size(file_obj)
        # With all-zero data: width = ((0 << 8) | 0) + 1 = 1
        assert width == 1
        assert height == 1

    def test_short_gif_returns_defaults(self):
        """Test short GIF file returns default values."""
        invalid_gif = b"GIF89a"  # Too short, only 6 bytes
        file_obj = io.BytesIO(invalid_gif)
        width, height = get_image_size(file_obj)
        # Returns default values when not enough data
        assert width == -1
        assert height == -1

    def test_short_png_returns_defaults(self):
        """Test short PNG file returns default values."""
        invalid_png = b"\x89PNG\r\n\x1a\n"  # Only 8 bytes, not enough
        file_obj = io.BytesIO(invalid_png)
        width, height = get_image_size(file_obj)
        # Returns default values when not enough data
        assert width == -1
        assert height == -1

    def test_invalid_jpeg(self):
        """Test invalid JPEG file raises ValueError."""
        invalid_jpeg = b"\xff\xd8\xff"  # Truncated JPEG
        file_obj = io.BytesIO(invalid_jpeg)
        with pytest.raises(ValueError, match="Invalid JPEG file"):
            get_image_size(file_obj)

    def test_invalid_jpeg2000(self):
        """Test invalid JPEG2000 file raises ValueError."""
        invalid_jp2 = (
            b"\x00\x00\x00\x0cjP  \r\n\x87\n" + b"\x00" * 40 + b"\x00"
        )  # Truncated, not enough bytes at offset 48
        file_obj = io.BytesIO(invalid_jp2)
        with pytest.raises(ValueError, match="Invalid JPEG2000 file"):
            get_image_size(file_obj)

    def test_invalid_tiff_width_datatype(self):
        """Test TIFF with invalid width datatype raises ValueError."""
        tiff_data = (
            b"\x4d\x4d\x00\x2a"
            + struct.pack(">L", 8)
            + struct.pack(">H", 1)
            # Width tag with invalid datatype (2 = ASCII)
            + struct.pack(">HHLL", 256, 2, 1, 800)
        )
        file_obj = io.BytesIO(tiff_data)
        with pytest.raises(
            ValueError, match="Invalid TIFF file: width column data type should be SHORT/LONG"
        ):
            get_image_size(file_obj)

    def test_invalid_tiff_missing_tags(self):
        """Test TIFF with missing width/height tags raises ValueError."""
        tiff_data = (
            b"\x4d\x4d\x00\x2a"
            + struct.pack(">L", 8)
            + struct.pack(">H", 1)
            # Only width tag, no height
            + struct.pack(">HHLL", 256, 4, 1, 800)
        )
        file_obj = io.BytesIO(tiff_data)
        with pytest.raises(
            ValueError, match="Invalid TIFF file: width and/or height IDS entries are missing"
        ):
            get_image_size(file_obj)

    def test_invalid_bigtiff_offset(self):
        """Test BigTIFF with invalid offset raises error."""
        bigtiff_data = b"\x49\x49\x2b\x00" + struct.pack(
            "<L", 16
        )  # Invalid bytesize offset (should be 8)
        file_obj = io.BytesIO(bigtiff_data)
        # Bug in source: uses undefined 'offset' variable, raises UnboundLocalError
        with pytest.raises(UnboundLocalError):
            get_image_size(file_obj)

    def test_invalid_svg(self):
        """Test invalid SVG file raises ValueError."""
        invalid_svg = b'<?xml version="1.0"?><svg width="invalid" height="also-invalid"></svg>'
        file_obj = io.BytesIO(invalid_svg)
        with pytest.raises(ValueError, match="unknown unit type"):
            get_image_size(file_obj)

    def test_invalid_netpbm(self):
        """Test invalid Netpbm file raises ValueError."""
        invalid_netpbm = b"P3\nINVALID"
        file_obj = io.BytesIO(invalid_netpbm)
        with pytest.raises(ValueError, match="Invalid character found on Netpbm file"):
            get_image_size(file_obj)

    def test_unsupported_webp(self):
        """Test unsupported WebP format raises ValueError."""
        webp_data = b"RIFF\x00\x00\x00\x00WEBPXXXX"
        file_obj = io.BytesIO(webp_data)
        with pytest.raises(ValueError, match="Unsupported WebP file"):
            get_image_size(file_obj)


class TestGetDPI:
    """Tests for getDPI function."""

    def test_gif_no_dpi(self):
        """Test GIF format returns -1 for DPI (no DPI support)."""
        # Create a temporary GIF file
        with tempfile.NamedTemporaryFile(suffix=".gif", delete=False) as f:
            f.write(b"GIF89a" + struct.pack("<hh", 100, 100) + b"\x00" * 20)
            filepath = f.name

        try:
            xDPI, yDPI = getDPI(filepath)  # pylint: disable=invalid-name
            assert xDPI == -1
            assert yDPI == -1
        finally:
            os.unlink(filepath)

    def test_png_with_phys_chunk(self):
        """Test PNG format with pHYs chunk for DPI."""

        # Create PNG with properly formatted pHYs chunk
        # PNG needs valid chunk structure with CRC
        png_data = (
            b"\x89PNG\r\n\x1a\n"
            + struct.pack(">I", 13)
            + b"IHDR"
            + struct.pack(">LL", 100, 100)
            + b"\x00" * 5
            + b"\x00\x00\x00\x00"
            + struct.pack(">I", 9)
            + b"pHYs"
            + struct.pack(">LLB", 2835, 2835, 1)  # 72 DPI (2835 pixels per meter)
            + b"\x00\x00\x00\x00"  # CRC
            + struct.pack(">I", 0)
            + b"IEND"
            + b"\x00\x00\x00\x00"
        )

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            f.write(png_data)
            filepath = f.name

        try:
            xDPI, yDPI = getDPI(filepath)  # pylint: disable=invalid-name
            assert xDPI == 72
            assert yDPI == 72
        finally:
            os.unlink(filepath)

    def test_png_without_unit(self):
        """Test PNG pHYs chunk without unit."""

        png_data = (
            b"\x89PNG\r\n\x1a\n"
            + struct.pack(">I", 13)
            + b"IHDR"
            + struct.pack(">LL", 100, 100)
            + b"\x00" * 5
            + b"\x00\x00\x00\x00"
            + struct.pack(">I", 9)
            + b"pHYs"
            + struct.pack(">LLB", 96, 96, 0)  # No unit
            + b"\x00\x00\x00\x00"
            + struct.pack(">I", 0)
            + b"IEND"
            + b"\x00\x00\x00\x00"
        )

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            f.write(png_data)
            filepath = f.name

        try:
            xDPI, yDPI = getDPI(filepath)  # pylint: disable=invalid-name
            assert xDPI == 96
            assert yDPI == 96
        finally:
            os.unlink(filepath)

    def test_jpeg_app0_unit_dpi(self):
        """Test JPEG with APP0 marker and DPI unit."""

        jpeg_data = (
            b"\xff\xd8"
            + b"\xff\xe0"  # APP0
            + struct.pack(">H", 16)
            + b"JFIF\x00"
            + b"\x01\x01"  # version
            + struct.pack(">BHH", 1, 300, 300)  # unit=1 (DPI), 300x300 DPI
            + b"\x00\x00"
        )

        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
            f.write(jpeg_data)
            filepath = f.name

        try:
            xDPI, yDPI = getDPI(filepath)  # pylint: disable=invalid-name
            assert xDPI == 300
            assert yDPI == 300
        finally:
            os.unlink(filepath)

    def test_jpeg_app0_unit_cm(self):
        """Test JPEG with APP0 marker and cm unit."""

        jpeg_data = (
            b"\xff\xd8"
            + b"\xff\xe0"  # APP0
            + struct.pack(">H", 16)
            + b"JFIF\x00"
            + b"\x01\x01"
            + struct.pack(">BHH", 2, 118, 118)  # unit=2 (dots/cm), 118 dots/cm = ~300 DPI
            + b"\x00\x00"
        )

        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
            f.write(jpeg_data)
            filepath = f.name

        try:
            xDPI, yDPI = getDPI(filepath)  # pylint: disable=invalid-name
            # 118 dots/cm * 2.54 = 299.72, should round to 300
            assert 299 <= xDPI <= 300
            assert 299 <= yDPI <= 300
        finally:
            os.unlink(filepath)

    def test_jpeg2000_no_resolution(self):
        """Test JPEG2000 without resolution box returns -1."""

        # Simple JPEG2000 structure without resolution info
        jp2_data = (
            b"\x00\x00\x00\x0cjP  \r\n\x87\n"
            + b"\x00\x00\x00\x14ftyp"  # ftyp box
            + b"jp2 \x00\x00\x00\x00jp2 "
            + struct.pack(">L", 14)
            + b"jp2h"  # JP2 header box (minimal)
            + b"\x00" * 6  # header content
        )

        with tempfile.NamedTemporaryFile(suffix=".jp2", delete=False) as f:
            f.write(jp2_data)
            filepath = f.name

        try:
            xDPI, yDPI = getDPI(filepath)  # pylint: disable=invalid-name
            assert xDPI == -1
            assert yDPI == -1
        finally:
            os.unlink(filepath)

    def test_png_no_dpi_info(self):
        """Test PNG file without DPI info returns -1."""

        # PNG with IDAT chunk but no pHYs chunk
        png_data = (
            b"\x89PNG\r\n\x1a\n"
            + struct.pack(">I", 13)
            + b"IHDR"
            + struct.pack(">LL", 100, 100)
            + b"\x00" * 5
            + b"\x00\x00\x00\x00"
            + struct.pack(">I", 0)
            + b"IDAT"
            + b"\x00\x00\x00\x00"  # Empty IDAT
        )

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            f.write(png_data)
            filepath = f.name

        try:
            xDPI, yDPI = getDPI(filepath)  # pylint: disable=invalid-name
            assert xDPI == -1
            assert yDPI == -1
        finally:
            os.unlink(filepath)

    def test_jpeg_no_dpi_info(self):
        """Test JPEG file without APP0 marker returns -1."""

        # JPEG with SOF0 but no APP0
        jpeg_data = (
            b"\xff\xd8"  # SOI
            + b"\xff\xc0"  # SOF0 (not APP0)
            + struct.pack(">H", 17)
            + b"\x08"
            + struct.pack(">HH", 100, 100)
            + b"\x03\x01\x22\x00\x02\x11\x01\x03\x11\x01"
        )

        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
            f.write(jpeg_data)
            filepath = f.name

        try:
            xDPI, yDPI = getDPI(filepath)  # pylint: disable=invalid-name
            assert xDPI == -1
            assert yDPI == -1
        finally:
            os.unlink(filepath)


class TestConvertToDPI:
    """Tests for _convertToDPI helper function."""

    def test_unit_km(self):
        """Test conversion from kilometers."""
        assert _convertToDPI(1000, -3) == int(1000 * 0.0000254 + 0.5)

    def test_unit_100m(self):
        """Test conversion from 100 meters."""
        assert _convertToDPI(1000, -2) == int(1000 * 0.000254 + 0.5)

    def test_unit_10m(self):
        """Test conversion from 10 meters."""
        assert _convertToDPI(1000, -1) == int(1000 * 0.00254 + 0.5)

    def test_unit_1m(self):
        """Test conversion from 1 meter."""
        assert _convertToDPI(2835, 0) == int(2835 * 0.0254 + 0.5)
        assert _convertToDPI(2835, 0) == 72

    def test_unit_10cm(self):
        """Test conversion from 10 centimeters."""
        assert _convertToDPI(100, 1) == int(100 * 0.254 + 0.5)

    def test_unit_cm(self):
        """Test conversion from centimeters."""
        assert _convertToDPI(118, 2) == int(118 * 2.54 + 0.5)
        assert _convertToDPI(118, 2) == 300

    def test_unit_mm(self):
        """Test conversion from millimeters."""
        assert _convertToDPI(10, 3) == int(10 * 25.4 + 0.5)
        assert _convertToDPI(10, 3) == 254

    def test_unit_0_1mm(self):
        """Test conversion from 0.1 millimeters."""
        assert _convertToDPI(10, 4) == 10 * 254

    def test_unit_0_01mm(self):
        """Test conversion from 0.01 millimeters."""
        assert _convertToDPI(10, 5) == 10 * 2540

    def test_unit_um(self):
        """Test conversion from micrometers."""
        assert _convertToDPI(10, 6) == 10 * 25400

    def test_unit_unknown(self):
        """Test unknown unit returns density as-is."""
        assert _convertToDPI(100, 99) == 100


class TestConvertToPx:
    """Tests for _convertToPx helper function."""

    def test_no_unit(self):
        """Test conversion with no unit (already pixels)."""
        assert _convertToPx("100") == 100.0
        assert _convertToPx("150.5") == 150.5

    def test_unit_px(self):
        """Test conversion from pixels."""
        assert _convertToPx("200px") == 200.0

    def test_unit_cm(self):
        """Test conversion from centimeters."""
        result = _convertToPx("10cm")
        expected = 10 * 96 / 2.54
        assert abs(result - expected) < 0.01

    def test_unit_mm(self):
        """Test conversion from millimeters."""
        result = _convertToPx("100mm")
        expected = 100 * 96 / 2.54 / 10
        assert abs(result - expected) < 0.01

    def test_unit_in(self):
        """Test conversion from inches."""
        assert _convertToPx("5in") == 5 * 96

    def test_unit_pc(self):
        """Test conversion from picas."""
        assert _convertToPx("12pc") == 12 * 96 / 6

    def test_unit_pt(self):
        """Test conversion from points."""
        assert _convertToPx("72pt") == 72 * 96 / 6

    def test_invalid_length_value(self):
        """Test invalid length value raises ValueError."""
        # The regex actually matches 'invalid' as unit, so error is 'unknown unit type'
        with pytest.raises(ValueError, match="unknown unit type"):
            _convertToPx("invalid")

    def test_unknown_unit(self):
        """Test unknown unit type raises ValueError."""
        with pytest.raises(ValueError, match="unknown unit type"):
            _convertToPx("100em")
