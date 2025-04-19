from PIL import Image, ImageDraw, ImageFont
import sys
import platform

# 打开图片
img1 = Image.open("/Users/seanhuang/Downloads/deliverroute.png")  # 主图片
img2 = Image.open("/Users/seanhuang/Downloads/qrcode.jpg")        # 二维码图片

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
font_size = 80  # 增大字体大小

# 尝试多个可能的字体路径
possible_fonts = [
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/STHeiti Light.ttc",
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/Library/Fonts/Arial Unicode.ttf",
    "/System/Library/Fonts/AppleGothic.ttf",
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

# 添加文字
text = "每周五下午免费送货5单，18:30-20:00送达列治文指定区域，请周五12:00前完成下单。"
text_color = (0, 0, 0)  # 黑色

# 计算文字大小
text_bbox = draw.textbbox((0, 0), text, font=font)
text_width = text_bbox[2] - text_bbox[0]
text_height = text_bbox[3] - text_bbox[1]

# 在图片顶部居中显示文字
text_position = ((img1.width - text_width) // 2, 50)

# 先绘制白色背景（可选）
padding = 10
background_bbox = (
    text_position[0] - padding,
    text_position[1] - padding,
    text_position[0] + text_width + padding,
    text_position[1] + text_height + padding
)
draw.rectangle(background_bbox, fill=(255, 255, 255))  # 白色背景

# 绘制文字
draw.text(text_position, text, font=font, fill=text_color)

# 打印调试信息
print(f"图片尺寸: {img1.width} x {img1.height}")
print(f"文字位置: {text_position}")
print(f"文字大小: {text_width} x {text_height}")

# 保存结果
new_img.save("merged.jpg")
print("图片已保存")

