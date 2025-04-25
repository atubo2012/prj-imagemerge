from PIL import Image, ImageDraw, ImageFont
import sys
import platform

# 打开图片
img1 = Image.open(r"C:\Users\x1\Downloads\顶好葱油饼.png")  # 主图片
img2 = Image.open(r"C:\Users\x1\Downloads\一品香Logo-甄选.png")        # 二维码图片

# 设置二维码大小（可以根据需要调整）
qr_width = int(img1.width * 0.2)  # 设置二维码宽度为主图片的20%
qr_height = int(qr_width * img2.height / img2.width)  # 保持二维码的宽高比
img2_resized = img2.resize((qr_width, qr_height))

# 计算二维码放置位置（右下角，留出一定边距）
margin = 20  # 边距像素
x = img1.width - qr_width - margin
y = img1.height - qr_height - margin

# 创建新图片（使用主图片的尺寸）
new_img = Image.new("RGB", (img1.width, img1.height))
new_img.paste(img1, (0, 0))
new_img.paste(img2_resized, (x, y))

# 创建绘图对象
draw = ImageDraw.Draw(new_img)

# 设置字体和大小
font_size = 40  # 减小字体大小

# 尝试多个可能的字体路径
possible_fonts = [
    r"C:\Windows\Fonts\msyh.ttc",     # 微软雅黑
    r"C:\Windows\Fonts\simsun.ttc",    # 宋体
    r"C:\Windows\Fonts\simhei.ttf",    # 黑体
    r"C:\Windows\Fonts\simkai.ttf",    # 楷体
]

font = None
for font_path in possible_fonts:
    try:
        font = ImageFont.truetype(font_path, font_size)
        print(f"成功加载字体: {font_path}")
        break
    except Exception as e:
        print(f"尝试加载字体 {font_path} 失败")
        continue

if font is None:
    print("所有字体加载失败，使用默认字体")
    font = ImageFont.load_default()

# 添加两行文字
text_line1 = "每周五免费送货5单，18:30-20:00送达列治文指定区域（下图红框内）。"
text_line2 = "请周五12:00前完成下单。接受微信支付。先付后送。"
text_color = (0, 0, 0)  # 黑色

# 计算两行文字的大小
text_bbox1 = draw.textbbox((0, 0), text_line1, font=font)
text_bbox2 = draw.textbbox((0, 0), text_line2, font=font)
text_width1 = text_bbox1[2] - text_bbox1[0]
text_width2 = text_bbox2[2] - text_bbox2[0]
text_height = text_bbox1[3] - text_bbox1[1]

# 计算文字位置（在顶部居中）
margin_top = 20  # 顶部边距
line_spacing = 10  # 行间距

# 第一行文字位置
text_x1 = (img1.width - text_width1) // 2
text_y1 = margin_top

# 第二行文字位置
text_x2 = (img1.width - text_width2) // 2
text_y2 = text_y1 + text_height + line_spacing

# 绘制白色背景
padding = 10
background_bbox = (
    min(text_x1, text_x2) - padding,
    text_y1 - padding,
    max(text_x1 + text_width1, text_x2 + text_width2) + padding,
    text_y2 + text_height + padding
)
draw.rectangle(background_bbox, fill=(255, 255, 255))  # 白色背景

# 绘制两行文字
draw.text((text_x1, text_y1), text_line1, font=font, fill=text_color)
draw.text((text_x2, text_y2), text_line2, font=font, fill=text_color)

# 保存结果
new_img.save("merged.jpg")
print("图片已保存")

