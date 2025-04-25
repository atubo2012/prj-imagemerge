from PIL import Image, ImageDraw, ImageFont
import sys
import platform
import os

# 创建必要的目录
os.makedirs('images', exist_ok=True)
os.makedirs('output', exist_ok=True)

# 配置参数
CONFIG = {
    'main_image': r"C:\Users\x1\Downloads\顶好葱油饼.png",
    'qr_image': r"C:\Users\x1\Downloads\一品香二维码.png",
    'logo_image': r"C:\Users\x1\Downloads\一品香Logo-甄选.png",  # 新增 logo 图片路径
    'output_file': r"output\merged.jpg",
    'qr_scale': 0.2,    # 二维码占主图的比例
    'logo_scale': 0.2,  # logo 占主图的比例
    'margin': 20,       # 边距
    'font_size': 40,    # 字体大小
    'text_line1': "每周五免费送货5单，18:30-20:00送达列治文指定区域（下图红框内）。",
    'text_line2': "请周五12:00前完成下单。接受微信支付。先付后送。"
}

def resize_image(img, base_width, scale):
    """调整图片大小，保持宽高比"""
    new_width = int(base_width * scale)
    new_height = int(new_width * img.height / img.width)
    return img.resize((new_width, new_height))

def process_image():
    try:
        # 打开图片
        main_img = Image.open(CONFIG['main_image'])
        qr_img = Image.open(CONFIG['qr_image'])
        logo_img = Image.open(CONFIG['logo_image'])

        # 调整二维码和 logo 大小
        qr_resized = resize_image(qr_img, main_img.width, CONFIG['qr_scale'])
        logo_resized = resize_image(logo_img, main_img.width, CONFIG['logo_scale'])

        # 创建新图片
        new_img = Image.new("RGB", (main_img.width, main_img.height))
        new_img.paste(main_img, (0, 0))

        # 计算二维码位置（右下角）
        qr_x = main_img.width - qr_resized.width - CONFIG['margin']
        qr_y = main_img.height - qr_resized.height - CONFIG['margin']
        
        # 计算 logo 位置（左下角）
        logo_x = CONFIG['margin']
        logo_y = main_img.height - logo_resized.height - CONFIG['margin']

        # 粘贴二维码和 logo
        new_img.paste(qr_resized, (qr_x, qr_y))
        new_img.paste(logo_resized, (logo_x, logo_y))

        # 设置字体
        font = load_font(CONFIG['font_size'])
        
        # 添加文字
        add_text_with_background(new_img, font)

        # 保存结果
        new_img.save(CONFIG['output_file'])
        print(f"图片已保存到: {CONFIG['output_file']}")
        
    except Exception as e:
        print(f"处理图片时出错: {str(e)}")

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

def add_text_with_background(img, font):
    draw = ImageDraw.Draw(img)
    
    # 计算文字大小
    text_bbox1 = draw.textbbox((0, 0), CONFIG['text_line1'], font=font)
    text_bbox2 = draw.textbbox((0, 0), CONFIG['text_line2'], font=font)
    
    # 计算尺寸
    text_width1 = text_bbox1[2] - text_bbox1[0]
    text_width2 = text_bbox2[2] - text_bbox2[0]
    text_height = text_bbox1[3] - text_bbox1[1]
    
    # 计算位置
    margin_top = 20
    line_spacing = 10
    text_x1 = (img.width - text_width1) // 2
    text_y1 = margin_top
    text_x2 = (img.width - text_width2) // 2
    text_y2 = text_y1 + text_height + line_spacing

    # 绘制白色背景
    padding = 10
    background_bbox = (
        min(text_x1, text_x2) - padding,
        text_y1 - padding,
        max(text_x1 + text_width1, text_x2 + text_width2) + padding,
        text_y2 + text_height + padding
    )
    draw.rectangle(background_bbox, fill=(255, 255, 255))

    # 绘制文字
    draw.text((text_x1, text_y1), CONFIG['text_line1'], font=font, fill=(0, 0, 0))
    draw.text((text_x2, text_y2), CONFIG['text_line2'], font=font, fill=(0, 0, 0))

if __name__ == "__main__":
    process_image()