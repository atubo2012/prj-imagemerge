from PIL import Image

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

# 保存结果
new_img.save("merged.jpg")

