"""Tests for QR code generation functions."""

import pytest
from PIL import Image
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main2 import qrcode_generating


class TestQrcodeGenerating:
    """Tests for qrcode_generating function."""

    def test_generates_correct_size(self):
        """Test that QR code is generated with correct size."""
        url = "https://example.com"
        size = 200

        result = qrcode_generating(url, size)

        assert result.width == size
        assert result.height == size

    def test_generates_rgb_image(self):
        """Test that QR code is in RGB mode."""
        url = "https://example.com"
        size = 100

        result = qrcode_generating(url, size)

        assert result.mode == "RGB"

    def test_generates_different_qr_for_different_urls(self):
        """Test that different URLs produce different QR codes."""
        url1 = "https://example.com/page1"
        url2 = "https://example.com/page2"
        size = 100

        result1 = qrcode_generating(url1, size)
        result2 = qrcode_generating(url2, size)

        # Convert to bytes and compare
        assert result1.tobytes() != result2.tobytes()

    def test_generates_same_qr_for_same_url(self):
        """Test that same URL produces identical QR codes."""
        url = "https://example.com"
        size = 100

        result1 = qrcode_generating(url, size)
        result2 = qrcode_generating(url, size)

        assert result1.tobytes() == result2.tobytes()

    def test_handles_long_url(self):
        """Test that long URLs are handled correctly."""
        url = "https://example.com/very/long/path?" + "param=value&" * 20
        size = 300

        result = qrcode_generating(url, size)

        assert result.width == size
        assert result.height == size

    def test_handles_chinese_characters_in_url(self):
        """Test that URLs with Chinese characters work."""
        url = "https://example.com/产品/测试"
        size = 150

        result = qrcode_generating(url, size)

        assert result.width == size
        assert result.height == size
