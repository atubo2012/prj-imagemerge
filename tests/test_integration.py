"""Integration tests for image merging."""

import pytest
from PIL import Image
import tempfile
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main2 import image_resizing, qrcode_generating
from qr_merge import images_merging


class TestImagesMerging:
    """Tests for images_merging function."""

    def test_qr_placed_in_bottom_right(self):
        """Test that QR code is placed in bottom-right corner."""
        main_image = Image.new("RGB", (500, 400), color="white")
        qr_image = Image.new("RGB", (50, 50), color="black")
        margin = 20

        result = images_merging(main_image, qr_image, margin)

        # Check that result has same dimensions as main image
        assert result.width == 500
        assert result.height == 400

        # Check bottom-right corner has QR code (black pixels)
        # QR should be at (500-50-20, 400-50-20) = (430, 330)
        pixel = result.getpixel((450, 350))  # Inside QR area
        assert pixel == (0, 0, 0)  # Black

    def test_converts_non_rgb_to_rgb(self):
        """Test that non-RGB images are converted."""
        main_image = Image.new("RGBA", (200, 200), color="white")
        qr_image = Image.new("RGB", (50, 50), color="black")
        margin = 10

        result = images_merging(main_image, qr_image, margin)

        assert result.mode == "RGB"

    def test_preserves_main_image_content(self):
        """Test that main image content is preserved."""
        main_image = Image.new("RGB", (200, 200), color="red")
        qr_image = Image.new("RGB", (30, 30), color="black")
        margin = 10

        result = images_merging(main_image, qr_image, margin)

        # Check top-left corner is still red
        pixel = result.getpixel((10, 10))
        assert pixel == (255, 0, 0)


class TestEndToEnd:
    """End-to-end integration tests."""

    def test_full_workflow_with_generated_qr(self):
        """Test complete workflow: create image, generate QR, merge."""
        # Create a main image
        main_image = Image.new("RGB", (800, 600), color="lightblue")

        # Generate QR code
        qr_image = qrcode_generating("https://example.com/product", 100)

        # Merge images
        result = images_merging(main_image, qr_image, margin=20)

        # Verify result
        assert result.width == 800
        assert result.height == 600

    def test_save_and_load_merged_image(self):
        """Test that merged image can be saved and loaded."""
        main_image = Image.new("RGB", (400, 300), color="green")
        qr_image = qrcode_generating("https://test.com", 80)
        result = images_merging(main_image, qr_image, margin=10)

        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
            temp_path = f.name

        try:
            result.save(temp_path, quality=95)
            loaded = Image.open(temp_path)

            assert loaded.width == 400
            assert loaded.height == 300
            loaded.close()
        finally:
            os.unlink(temp_path)

    def test_resize_then_merge(self):
        """Test resizing an image then merging with QR."""
        # Create oversized image
        large_image = Image.new("RGB", (2000, 1500), color="yellow")

        # Resize to smaller
        resized = image_resizing(large_image, 1000, 0.5)
        assert resized.width == 500

        # Generate and merge QR
        qr_image = qrcode_generating("https://example.com", 50)
        result = images_merging(resized, qr_image, margin=10)

        assert result.width == 500
        assert result.height == 375
