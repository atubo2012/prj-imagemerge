"""Tests for image utility functions."""

import pytest
from PIL import Image
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from imagemerge import image_resizing


class TestImageResizing:
    """Tests for image_resizing function."""

    def test_resizing_maintains_aspect_ratio(self):
        """Test that aspect ratio is preserved after resizing."""
        # Create a 200x100 image (2:1 ratio)
        img = Image.new("RGB", (200, 100), color="red")
        base_width = 1000
        scale = 0.1  # Should result in 100px width

        result = image_resizing(img, base_width, scale)

        # New width should be 100 (1000 * 0.1)
        assert result.width == 100
        # Height should maintain 2:1 ratio = 50
        assert result.height == 50

    def test_resizing_with_different_scales(self):
        """Test resizing with various scale factors."""
        img = Image.new("RGB", (400, 300), color="blue")
        base_width = 1000

        # Test 20% scale
        result = image_resizing(img, base_width, 0.2)
        assert result.width == 200
        assert result.height == 150

        # Test 50% scale
        result = image_resizing(img, base_width, 0.5)
        assert result.width == 500
        assert result.height == 375

    def test_resizing_square_image(self):
        """Test resizing a square image."""
        img = Image.new("RGB", (100, 100), color="green")
        base_width = 500
        scale = 0.2

        result = image_resizing(img, base_width, scale)

        assert result.width == 100
        assert result.height == 100

    def test_resizing_preserves_mode(self):
        """Test that image mode is preserved."""
        img = Image.new("RGBA", (200, 100), color="red")

        result = image_resizing(img, 1000, 0.1)

        assert result.mode == "RGBA"
