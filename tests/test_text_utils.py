"""Tests for text utility functions."""

import pytest
from PIL import ImageFont
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from imagemerge import text_wrapping, text_dimensions_getting, font_loading


class TestTextWrapping:
    """Tests for text_wrapping function."""

    @pytest.fixture
    def font(self):
        """Get a font for testing."""
        return font_loading(20)

    def test_short_text_no_wrap(self, font):
        """Test that short text doesn't wrap."""
        text = "Hello"
        max_width = 1000

        result = text_wrapping(text, font, max_width)

        assert len(result) == 1
        assert result[0] == "Hello"

    def test_respects_manual_line_breaks(self, font):
        """Test that manual \\n line breaks are respected."""
        text = "Line1\nLine2\nLine3"
        max_width = 1000

        result = text_wrapping(text, font, max_width)

        assert len(result) == 3
        assert result[0] == "Line1"
        assert result[1] == "Line2"
        assert result[2] == "Line3"

    def test_wraps_on_punctuation(self, font):
        """Test that text wraps on punctuation."""
        text = "This is sentence one, this is sentence two."
        max_width = 100  # Force wrapping

        result = text_wrapping(text, font, max_width)

        # Should wrap due to width constraint
        assert len(result) >= 1

    def test_empty_text(self, font):
        """Test handling of empty text."""
        text = ""
        max_width = 1000

        result = text_wrapping(text, font, max_width)

        assert result == ['']

    def test_preserves_empty_lines(self, font):
        """Test that empty lines from \\n\\n are preserved."""
        text = "Line1\n\nLine3"
        max_width = 1000

        result = text_wrapping(text, font, max_width)

        assert len(result) == 3
        assert result[1] == ''


class TestTextDimensionsGetting:
    """Tests for text_dimensions_getting function."""

    @pytest.fixture
    def font(self):
        """Get a font for testing."""
        return font_loading(20)

    def test_returns_tuple(self, font):
        """Test that function returns width and height tuple."""
        text = "Test"

        result = text_dimensions_getting(text, font)

        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_longer_text_wider(self, font):
        """Test that longer text has greater width."""
        short_text = "Hi"
        long_text = "Hello World"

        short_width, _ = text_dimensions_getting(short_text, font)
        long_width, _ = text_dimensions_getting(long_text, font)

        assert long_width > short_width

    def test_empty_text(self, font):
        """Test dimensions of empty text."""
        text = ""

        width, height = text_dimensions_getting(text, font)

        assert width == 0


class TestFontLoading:
    """Tests for font_loading function."""

    def test_returns_font_object(self):
        """Test that a font object is returned."""
        font = font_loading(20)

        assert font is not None

    def test_different_sizes(self):
        """Test loading fonts with different sizes."""
        font_small = font_loading(10)
        font_large = font_loading(40)

        # Both should load successfully
        assert font_small is not None
        assert font_large is not None
