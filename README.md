[English](README_en.md) | 中文

# 图片合成工具

用于合成产品图片、二维码和Logo的工具，适合电商产品营销。

## 功能特点

- 自动生成二维码 - 输入URL即可生成
- 支持URL加载图片 - 自动检测并下载网络图片
- 中英文双语支持 - 可切换输出语言
- 灵活的布局控制 - 自定义缩放比例、边距
- 支持文字叠加 - 添加营销文案

## 效果预览

原图 + 二维码 → 合成图

![效果预览](images/preview.jpg)

## 环境要求

- Python 3.8+
- 主要依赖：Pillow, qrcode

## 安装

```bash
# 克隆仓库
git clone https://github.com/atubo2012/prj-imagemerge.git
cd prj-imagemerge

# 创建虚拟环境
python -m venv ven
source ven/bin/activate  # Linux/Mac
ven\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt
```

## 快速开始

将产品图片与二维码合成：

```bash
python imagemerge.py product.png -q "https://your-shop.com/product/123"
```

这将：
- 加载产品图片
- 自动生成二维码
- 将二维码放在右下角
- 保存到 `output/merged.jpg`

从URL加载图片：

```bash
python imagemerge.py "https://cdn.example.com/product.jpg" -q "https://shop.com/product"
```

## 使用示例

### 1. 图片 + 二维码（最简单）

```bash
python imagemerge.py product.png -q "https://example.com/product"
```

### 2. 图片 + 二维码 + Logo

```bash
python imagemerge.py product.png -q "https://example.com/product" -l logo.png
```

### 3. 图片 + 二维码 + Logo + 文字

```bash
python imagemerge.py product.png -q "https://example.com/product" -l logo.png \
  -t "免费配送！\n立即下单。"
```

### 4. 使用现有二维码图片

```bash
python imagemerge.py product.png qrcode.png -l logo.png
```

### 5. 完整示例（所有选项）

```bash
python imagemerge.py product.png -q "https://example.com/product" -l logo.png \
  -o "output/my_product.jpg" \
  --qr-scale 0.15 \
  --logo-scale 0.2 \
  --qr-margin 30 \
  --logo-margin 20 \
  --text-margin 15 \
  --font-size 36 \
  -t "特价优惠！\n限时抢购。" \
  --lang zh
```

## 参数说明

| 参数 | 说明 | 默认值 |
|-----|------|-------|
| `main_image` | 产品图片（本地路径或URL） | 必需 |
| `qr_image` | 二维码图片（使用-q时可省略） | - |
| `-q`, `--generate-qr` | 从URL生成二维码 | - |
| `--qr-scale` | 二维码尺寸比例 | 0.2 (20%) |
| `--qr-margin` | 二维码边距像素 | 20 |
| `-l`, `--logo` | Logo图片文件 | - |
| `--logo-scale` | Logo尺寸比例 | 0.2 (20%) |
| `--logo-margin` | Logo边距像素 | 20 |
| `-t`, `--text` | 文字内容（用\n换行） | - |
| `--font-size` | 字体大小 | 40 |
| `--text-margin` | 文字顶部边距像素 | 10 |
| `-o`, `--output` | 输出文件路径 | output/merged.jpg |
| `--lang` | 输出语言 (en/zh) | zh |

## 测试

```bash
# 运行所有测试
python -m pytest tests/ -v

# 运行特定测试文件
python -m pytest tests/test_qrcode.py -v
```

### 测试覆盖

| 测试文件 | 测试数量 | 说明 |
|---------|---------|-----|
| `test_image_utils.py` | 4 | 图片缩放、宽高比 |
| `test_qrcode.py` | 6 | 二维码生成 |
| `test_text_utils.py` | 10 | 文字换行、字体 |
| `test_integration.py` | 6 | 端到端工作流 |

## 许可证

MIT
