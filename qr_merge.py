#!/usr/bin/env python
"""Generate product image with QR code in bottom-right corner."""

import argparse
import os
import io
import urllib.request
from PIL import Image
import qrcode

from i18n import t, set_language


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Generate product image with QR code linking to product URL"
    )
    parser.add_argument("image", help="Product image (local path or URL, auto-detected)")
    parser.add_argument("url", help="Product page URL (will be encoded in QR code)")
    parser.add_argument(
        "--output", "-o",
        default="output/merged.jpg",
        help="Output file path (default: output/merged.jpg)"
    )
    parser.add_argument(
        "--qr-scale",
        type=float,
        default=0.15,
        help="QR code size as fraction of image width (default: 0.15)"
    )
    parser.add_argument(
        "--margin",
        type=int,
        default=20,
        help="Margin from edge in pixels (default: 20)"
    )
    parser.add_argument(
        "--lang",
        choices=['en', 'zh'],
        default='en',
        help="Language/语言 (default: en)"
    )

    args = parser.parse_args()
    set_language(args.lang)
    return args


def is_url(path):
    """Check if path is a URL."""
    return path.startswith('http://') or path.startswith('https://')


def image_loading_from_url(url):
    """Download image from URL and return as PIL Image."""
    headers = {"User-Agent": "Mozilla/5.0"}
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request) as response:
        image_data = response.read()
    return Image.open(io.BytesIO(image_data))


def image_loading(args):
    """Load image from URL or local path (auto-detect)."""
    if is_url(args.image):
        print(t('downloading_image', args.image))
        return image_loading_from_url(args.image)
    else:
        print(t('loading_image', args.image))
        return Image.open(args.image)


def qrcode_generating(url, size):
    """Generate QR code image for the given URL."""
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
    qr_img = qr_img.resize((size, size), Image.LANCZOS)

    return qr_img


def images_merging(main_image, qr_image, margin):
    """Place QR code in bottom-right corner of main image."""
    if main_image.mode != "RGB":
        main_image = main_image.convert("RGB")

    result = main_image.copy()

    qr_x = main_image.width - qr_image.width - margin
    qr_y = main_image.height - qr_image.height - margin

    result.paste(qr_image, (qr_x, qr_y))

    return result


def main():
    args = parse_arguments()

    try:
        main_image = image_loading(args)

        qr_size = int(main_image.width * args.qr_scale)
        print(t('generating_qr', args.url))
        qr_image = qrcode_generating(args.url, qr_size)

        result = images_merging(main_image, qr_image, args.margin)

        output_dir = os.path.dirname(args.output)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        result.save(args.output, quality=95)
        print(t('image_saved', args.output))

    except Exception as e:
        print(t('error', e))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
