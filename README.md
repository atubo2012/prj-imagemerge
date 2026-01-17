[English](README_en.md) | 中文

# 图片合成工具

用于合成产品图片、二维码和Logo的工具，适合电商产品营销。

## 快速开始

### 安装

```bash
pip install -r requirements.txt
```

### 最简单用法

将产品图片与二维码合成：

```bash
python imagemerge.py product.png --generate-qr "https://your-shop.com/product/123"
```

这将：
- 加载产品图片
- 自动生成二维码
- 将二维码放在右下角
- 保存到 `output/merged.jpg`

### 从URL加载图片

工具自动检测输入是否为URL：

```bash
# 图片自动下载
python imagemerge.py "https://cdn.example.com/product.jpg" --generate-qr "https://shop.com/product"
```

## 使用示例

### 1. 图片 + 二维码（最简单）

```bash
python imagemerge.py product.png --generate-qr "https://example.com/product"
```

### 2. 图片 + 二维码 + Logo

```bash
python imagemerge.py product.png --generate-qr "https://example.com/product" logo.png
```

### 3. 图片 + 二维码 + Logo + 文字

```bash
python imagemerge.py product.png --generate-qr "https://example.com/product" logo.png \
  --text "免费配送！\n立即下单。"
```

### 4. 使用现有二维码图片

```bash
python imagemerge.py product.png qrcode.png logo.png
```

### 5. 完整示例（所有选项）

```bash
python imagemerge.py product.png --generate-qr "https://example.com/product" logo.png \
  --output "output/my_product.jpg" \
  --qr-scale 0.15 \
  --logo-scale 0.2 \
  --margin 30 \
  --font-size 36 \
  --text "特价优惠！\n限时抢购。" \
  --lang zh
```

## 参数说明

| 参数 | 说明 | 默认值 |
|-----|------|-------|
| `main_image` | 产品图片（本地路径或URL） | 必需 |
| `qr_image` | 二维码图片（使用--generate-qr时可省略） | - |
| `logo_image` | Logo图片（可选） | - |
| `--generate-qr` | 从URL生成二维码 | - |
| `--output`, `-o` | 输出文件路径 | output/merged.jpg |
| `--qr-scale` | 二维码尺寸比例 | 0.2 (20%) |
| `--logo-scale` | Logo尺寸比例 | 0.2 (20%) |
| `--margin` | 边距像素 | 20 |
| `--font-size` | 字体大小 | 40 |
| `--text` | 文字内容（用\n换行） | - |
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

## 许可证

MIT
