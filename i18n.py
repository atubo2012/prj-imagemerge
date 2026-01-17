"""Internationalization support for multiple languages."""

MESSAGES = {
    'en': {
        # General
        'error': 'Error: {}',

        # Image operations
        'image_saved': 'Image saved to: {}',
        'loading_image': 'Loading image from: {}',
        'downloading_image': 'Downloading image from: {}',

        # QR code
        'generating_qr': 'Generating QR code for: {}',
        'qr_required': 'Must provide QR image path or use --generate-qr URL',
        'qr_library_required': 'Using --generate-qr requires qrcode library: pip install qrcode[pil]',

        # Font
        'font_load_failed': 'All fonts failed to load, using default font',

        # Processing
        'processing_error': 'Error processing image: {}',
    },
    'zh': {
        # General
        'error': '错误: {}',

        # Image operations
        'image_saved': '图片已保存到: {}',
        'loading_image': '加载图片: {}',
        'downloading_image': '从URL下载图片: {}',

        # QR code
        'generating_qr': '生成二维码: {}',
        'qr_required': '必须提供二维码图片路径或使用 --generate-qr URL 生成二维码',
        'qr_library_required': '使用 --generate-qr 需要安装 qrcode 库: pip install qrcode[pil]',

        # Font
        'font_load_failed': '所有字体加载失败，使用默认字体',

        # Processing
        'processing_error': '处理图片时出错: {}',
    }
}

# Default language
_current_lang = 'en'


def set_language(lang):
    """Set the current language."""
    global _current_lang
    if lang in MESSAGES:
        _current_lang = lang


def get_language():
    """Get the current language."""
    return _current_lang


def t(key, *args):
    """Get translated text for the given key.

    Args:
        key: Message key
        *args: Format arguments

    Returns:
        Translated and formatted string
    """
    messages = MESSAGES.get(_current_lang, MESSAGES['en'])
    text = messages.get(key, key)

    if args:
        return text.format(*args)
    return text
