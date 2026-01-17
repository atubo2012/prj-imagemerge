English | [中文](README.md)

# Image Merge Tool

A tool for composing product images with QR codes and logos. Perfect for e-commerce product marketing.

## Features

- Auto QR Code Generation - Just input a URL
- URL Image Loading - Auto-detect and download images from URLs
- Bilingual Support - Switch between English and Chinese output
- Flexible Layout Control - Customize scale ratios and margins
- Text Overlay Support - Add marketing copy

## Preview

Original + QR Code → Merged Image

![Preview](images/preview.jpg)

## Requirements

- Python 3.8+
- Main dependencies: Pillow, qrcode

## Installation

```bash
# Clone repository
git clone https://github.com/atubo2012/prj-imagemerge.git
cd prj-imagemerge

# Create virtual environment
python -m venv ven
source ven/bin/activate  # Linux/Mac
ven\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

Merge your product image with a QR code:

```bash
python imagemerge.py product.png -q "https://your-shop.com/product/123"
```

This will:
- Load your product image
- Auto-generate a QR code from the URL
- Place QR code in bottom-right corner
- Save to `output/merged.jpg`

Load image from URL:

```bash
python imagemerge.py "https://cdn.example.com/product.jpg" -q "https://shop.com/product"
```

## Usage Examples

### 1. Image + QR Code (Simplest)

```bash
python imagemerge.py product.png -q "https://example.com/product"
```

### 2. Image + QR Code + Logo

```bash
python imagemerge.py product.png -q "https://example.com/product" -l logo.png
```

### 3. Image + QR Code + Logo + Text

```bash
python imagemerge.py product.png -q "https://example.com/product" -l logo.png \
  -t "Free shipping!\nOrder now."
```

### 4. Using Existing QR Image

```bash
python imagemerge.py product.png qrcode.png -l logo.png
```

### 5. Full Example with All Options

```bash
python imagemerge.py product.png -q "https://example.com/product" -l logo.png \
  -o "output/my_product.jpg" \
  --qr-scale 0.15 \
  --logo-scale 0.2 \
  --qr-margin 30 \
  --logo-margin 20 \
  --text-margin 15 \
  --font-size 36 \
  -t "Special Offer!\nLimited time only." \
  --lang en
```

## Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `main_image` | Product image (local path or URL) | Required |
| `qr_image` | QR code image (optional if using -q) | - |
| `-q`, `--generate-qr` | Generate QR code from URL | - |
| `--qr-scale` | QR code size ratio | 0.2 (20%) |
| `--qr-margin` | QR code margin in pixels | 20 |
| `-l`, `--logo` | Logo image file | - |
| `--logo-scale` | Logo size ratio | 0.2 (20%) |
| `--logo-margin` | Logo margin in pixels | 20 |
| `-t`, `--text` | Text overlay (use \n for line breaks) | - |
| `--font-size` | Font size for text | 40 |
| `--text-margin` | Text top margin in pixels | 10 |
| `-o`, `--output` | Output file path | output/merged.jpg |
| `--lang` | Output language (en/zh) | zh |

## Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_qrcode.py -v
```

### Test Coverage

| Test File | Tests | Description |
|-----------|-------|-------------|
| `test_image_utils.py` | 4 | Image resizing, aspect ratio |
| `test_qrcode.py` | 6 | QR code generation |
| `test_text_utils.py` | 10 | Text wrapping, fonts |
| `test_integration.py` | 6 | End-to-end workflows |

## License

MIT
