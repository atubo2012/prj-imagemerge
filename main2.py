from PIL import Image, ImageDraw, ImageFont
import sys
import platform
import os
import argparse
import textwrap

# 创建必要的目录
os.makedirs('images', exist_ok=True)
os.makedirs('output', exist_ok=True)

def parse_arguments():
    parser = argparse.ArgumentParser(description='图片合成工具')
    parser.add_argument('main_image', help='主图片路径')
    parser.add_argument('qr_image', help='二维码图片路径')
    parser.add_argument('logo_image', help='Logo图片路径')
    parser.add_argument('--output', '-o', default='output/merged.jpg', help='输出文件路径 (默认: output/merged.jpg)')
    parser.add_argument('--qr-scale', type=float, default=0.2, help='二维码尺寸比例 (默认: 0.2)')
    parser.add_argument('--logo-scale', type=float, default=0.2, help='Logo尺寸比例 (默认: 0.2)')
    parser.add_argument('--margin', type=int, default=20, help='边距像素 (默认: 20)')
    parser.add_argument('--font-size', type=int, default=40, help='字体大小 (默认: 40)')
    parser.add_argument('--text', help='文字内容，使用\\n换行（可选）')
    return parser.parse_args()

def resize_image(img, base_width, scale):
    """调整图片大小，保持宽高比"""
    new_width = int(base_width * scale)
    new_height = int(new_width * img.height / img.width)
    return img.resize((new_width, new_height))

def get_text_dimensions(text, font):
    """获取文本的尺寸"""
    bbox = font.getbbox(text)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]

def wrap_text(text, font, max_width):
    """将文本按最大宽度自动换行，更积极的换行策略"""
    lines = []
    for paragraph in text.split('\n'):
        if not paragraph:
            lines.append('')
            continue
            
        # 更积极的分词，包括标点符号
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

def process_image(args):
    try:
        # 打开图片
        main_img = Image.open(args.main_image)
        qr_img = Image.open(args.qr_image)
        logo_img = Image.open(args.logo_image)

        # 调整二维码和 logo 大小
        qr_resized = resize_image(qr_img, main_img.width, args.qr_scale)
        logo_resized = resize_image(logo_img, main_img.width, args.logo_scale)

        # 创建新图片
        new_img = Image.new("RGB", (main_img.width, main_img.height))
        new_img.paste(main_img, (0, 0))

        # 计算二维码位置（右下角）
        qr_x = main_img.width - qr_resized.width - args.margin
        qr_y = main_img.height - qr_resized.height - args.margin
        
        # 计算 logo 位置（左下角）
        logo_x = args.margin
        logo_y = main_img.height - logo_resized.height - args.margin

        # 粘贴二维码和 logo
        new_img.paste(qr_resized, (qr_x, qr_y))
        new_img.paste(logo_resized, (logo_x, logo_y))

        # 如果指定了文本，则添加文字
        if args.text:
            # 设置字体
            font = load_font(args.font_size)
            # 添加文字
            add_text_with_background(new_img, font, args.text)

        # 保存结果
        new_img.save(args.output)
        print(f"图片已保存到: {args.output}")
        
    except Exception as e:
        print(f"处理图片时出错: {str(e)}")
        sys.exit(1)

def load_font(font_size):
    possible_fonts = [
        r"C:\Windows\Fonts\msyh.ttc",     # 微软雅黑
        r"C:\Windows\Fonts\simsun.ttc",    # 宋体
        r"C:\Windows\Fonts\simhei.ttf",    # 黑体
        r"C:\Windows\Fonts\simkai.ttf",    # 楷体
    ]

    for font_path in possible_fonts:
        try:
            return ImageFont.truetype(font_path, font_size)
        except Exception:
            continue
    
    print("所有字体加载失败，使用默认字体")
    return ImageFont.load_default()

def add_text_with_background(img, font, text):
    draw = ImageDraw.Draw(img)
    
    # 减小最大文本宽度（改为图片宽度的60%）
    max_text_width = int(img.width * 1)
    
    # 自动换行
    lines = wrap_text(text, font, max_text_width)
    
    # 计算文本总高度
    _, line_height = get_text_dimensions('测试', font)
    line_spacing = 10  # 行间距
    total_height = len(lines) * (line_height + line_spacing)
    
    # 增加顶部边距
    margin_top = 10
    text_y = margin_top
    
    # 计算所有行的最大宽度
    max_width = max(font.getlength(line) for line in lines)
    
    # 增加背景内边距
    padding = 10
    background_bbox = (
        (img.width - max_width) // 2 - padding,
        text_y - padding,
        (img.width + max_width) // 2 + padding,
        text_y + total_height + padding
    )
    
    # 绘制白色背景，添加一点透明度
    draw.rectangle(background_bbox, fill=(255, 255, 255, 230))
    
    # 绘制每一行文字
    for line in lines:
        text_width = font.getlength(line)
        text_x = (img.width - text_width) // 2
        draw.text((text_x, text_y), line, font=font, fill=(0, 0, 0))
        text_y += line_height + line_spacing

if __name__ == "__main__":
    args = parse_arguments()
    process_image(args)