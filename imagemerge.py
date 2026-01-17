#!/usr/bin/env python
"""Image merge tool - Compose product images with QR codes and logos."""

from PIL import Image, ImageDraw, ImageFont
import sys
import platform
import os
import argparse
import textwrap
import io
import urllib.request

from i18n import t, set_language

try:
    import qrcode
    HAS_QRCODE = True
except ImportError:
    HAS_QRCODE = False

# Create necessary directories
os.makedirs('images', exist_ok=True)
os.makedirs('output', exist_ok=True)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Image merge tool / 图片合成工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s product.png --generate-qr "https://example.com"
  %(prog)s product.png --generate-qr "https://example.com" logo.png
  %(prog)s "https://cdn.com/img.jpg" --generate-qr "https://example.com"
  %(prog)s product.png qrcode.png logo.png --text "Special offer!"
'''
    )
    parser.add_argument('main_image', help='Main image (local path or URL, auto-detected)')
    parser.add_argument('qr_image', nargs='?', help='QR code image (optional if using --generate-qr)')
    parser.add_argument('logo_image', nargs='?', help='Logo image (optional)')
    parser.add_argument('--output', '-o', default='output/merged.jpg', help='Output file path (default: output/merged.jpg)')
    parser.add_argument('--qr-scale', type=float, default=0.2, help='QR code size ratio (default: 0.2)')
    parser.add_argument('--logo-scale', type=float, default=0.2, help='Logo size ratio (default: 0.2)')
    parser.add_argument('--margin', type=int, default=20, help='Margin in pixels (default: 20)')
    parser.add_argument('--font-size', type=int, default=40, help='Font size (default: 40)')
    parser.add_argument('--text', help='Text overlay, use \\n for line breaks (optional)')
    parser.add_argument('--generate-qr', metavar='URL', help='Generate QR code from URL')
    parser.add_argument('--lang', choices=['en', 'zh'], default='zh', help='Language (default: zh)')

    args = parser.parse_args()

    # Set language
    set_language(args.lang)

    # Validate arguments
    if not args.generate_qr and not args.qr_image:
        parser.error(t('qr_required'))

    if args.generate_qr and not HAS_QRCODE:
        parser.error(t('qr_library_required'))

    return args


def is_url(path):
    """Check if path is a URL."""
    return path.startswith('http://') or path.startswith('https://')


def image_resizing(img, base_width, scale):
    """Resize image while maintaining aspect ratio."""
    new_width = int(base_width * scale)
    new_height = int(new_width * img.height / img.width)
    return img.resize((new_width, new_height))


def image_loading_from_url(url):
    """Download image from URL."""
    headers = {"User-Agent": "Mozilla/5.0"}
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request) as response:
        image_data = response.read()
    return Image.open(io.BytesIO(image_data))


def qrcode_generating(url, size):
    """Generate QR code image from URL."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img = qr_img.convert("RGB")
    return qr_img.resize((size, size), Image.LANCZOS)


def images_merging(main_image, qr_image, margin):
    """Place QR code in bottom-right corner of main image."""
    if main_image.mode != "RGB":
        main_image = main_image.convert("RGB")

    result = main_image.copy()

    qr_x = main_image.width - qr_image.width - margin
    qr_y = main_image.height - qr_image.height - margin

    result.paste(qr_image, (qr_x, qr_y))

    return result


def text_dimensions_getting(text, font):
    """Get text dimensions."""
    bbox = font.getbbox(text)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def text_wrapping(text, font, max_width):
    """Wrap text to fit within max width, with smart line breaks."""
    lines = []
    for paragraph in text.split('\n'):
        if not paragraph:
            lines.append('')
            continue

        # Split on Chinese punctuation
        parts = []
        current_part = ''
        for char in paragraph:
            if char in '，。！？、；：（）':
                if current_part:
                    parts.append(current_part)
                parts.append(char)
                current_part = ''
            else:
                current_part += char
        if current_part:
            parts.append(current_part)

        current_line = ''
        for part in parts:
            test_line = current_line + part
            if font.getlength(test_line) <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = part

        if current_line:
            lines.append(current_line)

    return lines


def font_loading(font_size):
    """Load font with fallback options."""
    possible_fonts = [
        r"C:\Windows\Fonts\msyh.ttc",     # Microsoft YaHei
        r"C:\Windows\Fonts\simsun.ttc",    # SimSun
        r"C:\Windows\Fonts\simhei.ttf",    # SimHei
        r"C:\Windows\Fonts\simkai.ttf",    # SimKai
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Linux
        "/System/Library/Fonts/PingFang.ttc",  # macOS
    ]

    for font_path in possible_fonts:
        try:
            return ImageFont.truetype(font_path, font_size)
        except Exception:
            continue

    print(t('font_load_failed'))
    return ImageFont.load_default()


def text_with_background_adding(img, font, text):
    """Add text with white background to image."""
    draw = ImageDraw.Draw(img)

    max_text_width = int(img.width * 1)

    # Auto wrap text
    lines = text_wrapping(text, font, max_text_width)

    # Calculate total text height
    _, line_height = text_dimensions_getting('Test', font)
    line_spacing = 10
    total_height = len(lines) * (line_height + line_spacing)

    margin_top = 10
    text_y = margin_top

    # Calculate max width of all lines
    max_width = max(font.getlength(line) for line in lines)

    # Draw white background
    padding = 10
    background_bbox = (
        (img.width - max_width) // 2 - padding,
        text_y - padding,
        (img.width + max_width) // 2 + padding,
        text_y + total_height + padding
    )
    draw.rectangle(background_bbox, fill=(255, 255, 255, 230))

    # Draw text lines
    for line in lines:
        text_width = font.getlength(line)
        text_x = (img.width - text_width) // 2
        draw.text((text_x, text_y), line, font=font, fill=(0, 0, 0))
        text_y += line_height + line_spacing


def imagewithqrcode_generating(args):
    """Main function to generate merged image with QR code."""
    try:
        # Load main image (auto-detect URL)
        if is_url(args.main_image):
            print(t('downloading_image', args.main_image))
            main_img = image_loading_from_url(args.main_image)
        else:
            print(t('loading_image', args.main_image))
            main_img = Image.open(args.main_image)

        # Get or generate QR code
        if args.generate_qr:
            print(t('generating_qr', args.generate_qr))
            qr_size = int(main_img.width * args.qr_scale)
            qr_resized = qrcode_generating(args.generate_qr, qr_size)
        else:
            qr_img = Image.open(args.qr_image)
            qr_resized = image_resizing(qr_img, main_img.width, args.qr_scale)

        # Create new image
        new_img = Image.new("RGB", (main_img.width, main_img.height))
        new_img.paste(main_img, (0, 0))

        # Place QR code (bottom-right)
        qr_x = main_img.width - qr_resized.width - args.margin
        qr_y = main_img.height - qr_resized.height - args.margin
        new_img.paste(qr_resized, (qr_x, qr_y))

        # Add logo if provided (bottom-left)
        if args.logo_image:
            logo_img = Image.open(args.logo_image)
            logo_resized = image_resizing(logo_img, main_img.width, args.logo_scale)
            logo_x = args.margin
            logo_y = main_img.height - logo_resized.height - args.margin
            new_img.paste(logo_resized, (logo_x, logo_y))

        # Add text if provided
        if args.text:
            font = font_loading(args.font_size)
            text_with_background_adding(new_img, font, args.text)

        # Save result
        output_dir = os.path.dirname(args.output)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        new_img.save(args.output, quality=95)
        print(t('image_saved', args.output))

    except Exception as e:
        print(t('processing_error', str(e)))
        sys.exit(1)


if __name__ == "__main__":
    args = parse_arguments()
    imagewithqrcode_generating(args)
