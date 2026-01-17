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
python imagemerge.py product.png --generate-qr "https://your-shop.com/product/123"
```

This will:
- Load your product image
- Auto-generate a QR code from the URL
- Place QR code in bottom-right corner
- Save to `output/merged.jpg`

Load image from URL:

```bash
python imagemerge.py "https://cdn.example.com/product.jpg" --generate-qr "https://shop.com/product"
```

## Usage Examples

### 1. Image + QR Code (Simplest)

```bash
python imagemerge.py product.png --generate-qr "https://example.com/product"
```

### 2. Image + QR Code + Logo

```bash
python imagemerge.py product.png --generate-qr "https://example.com/product" logo.png
```

### 3. Image + QR Code + Logo + Text

```bash
python imagemerge.py product.png --generate-qr "https://example.com/product" logo.png \
  --text "Free shipping!\nOrder now."
```

### 4. Using Existing QR Image

```bash
python imagemerge.py product.png qrcode.png logo.png
```

### 5. Full Example with All Options

```bash
python imagemerge.py product.png --generate-qr "https://example.com/product" logo.png \
  --output "output/my_product.jpg" \
  --qr-scale 0.15 \
  --logo-scale 0.2 \
  --margin 30 \
  --font-size 36 \
  --text "Special Offer!\nLimited time only." \
  --lang en
```

## Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `main_image` | Product image (local path or URL) | Required |
| `qr_image` | QR code image (optional if using --generate-qr) | - |
| `logo_image` | Logo image (optional) | - |
| `--generate-qr` | Generate QR code from URL | - |
| `--output`, `-o` | Output file path | output/merged.jpg |
| `--qr-scale` | QR code size ratio | 0.2 (20%) |
| `--logo-scale` | Logo size ratio | 0.2 (20%) |
| `--margin` | Edge margin in pixels | 20 |
| `--font-size` | Font size for text | 40 |
| `--text` | Text overlay (use \n for line breaks) | - |
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
