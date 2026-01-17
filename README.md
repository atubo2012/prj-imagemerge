# 图片合成工具

一个用于合成主图片、Logo和二维码的工具，可选择性地添加文字说明。

## 功能特点

- 将三张图片合成为一张：主图片、Logo（左下角）和二维码（右下角）
- 可选择是否添加文字说明
- 支持文字自动换行
- 可自定义图片缩放比例、边距和字体大小
- 根据URL自动生成二维码并合成到产品图片

## 使用方法

### 1. 基础用法（不添加文字）

```batch
@echo off
chcp 65001
set PYTHONIOENCODING=utf8
python "main2.py" ^
"images/顶好葱油饼.png" ^
"images/一品香二维码.png" ^
"images/一品香Logo-甄选.png" ^
--output "output/merged.jpg" ^
--qr-scale 0.2 ^
--logo-scale 0.2 ^
--margin 20
pause
```

### 2. 高级用法（添加文字说明）

```batch
@echo off
chcp 65001
set PYTHONIOENCODING=utf8
python "main2.py" ^
"images/顶好葱油饼.png" ^
"images/一品香二维码.png" ^
"images/一品香Logo-甄选.png" ^
--output "output/merged.jpg" ^
--qr-scale 0.2 ^
--logo-scale 0.2 ^
--margin 20 ^
--font-size 40 ^
--text "每周五免费送货5单，18:30-20:00送达列治文指定区域（下图红框内）。\n请周五12:00前完成下单。接受微信支付。先付后送。"
pause
```

### 3. 二维码自动生成（qr_merge.py）

根据产品URL自动生成二维码，并合成到产品图片右下角。

```bash
# 使用本地图片
python qr_merge.py <产品URL> --image-from-local <图片路径>

# 使用网络图片
python qr_merge.py <产品URL> --image-from-url <图片URL>
```

示例：
```bash
python qr_merge.py "https://example.com/product/123" --image-from-local "images/product.png" -o "output/merged.jpg"
```

参数说明：
- `url`：产品页面URL（必需，将编码为二维码）
- `--image-from-local`：本地图片路径（与--image-from-url二选一）
- `--image-from-url`：网络图片URL（与--image-from-local二选一）
- `--output`, `-o`：输出文件路径（默认：output/merged.jpg）
- `--qr-scale`：二维码尺寸比例（默认：0.15，即主图宽度的15%）
- `--margin`：边距像素（默认：20）

## 参数说明（main2.py）

必需参数：
- 第一个参数：主图片路径
- 第二个参数：二维码图片路径
- 第三个参数：Logo图片路径

可选参数：
- `--output`, `-o`：输出文件路径（默认：output/merged.jpg）
- `--qr-scale`：二维码尺寸比例（默认：0.2，即主图宽度的20%）
- `--logo-scale`：Logo尺寸比例（默认：0.2，即主图宽度的20%）
- `--margin`：边距像素（默认：20）
- `--font-size`：字体大小（默认：40）
- `--text`：文字内容，使用\n换行（可选）
- `--generate-qr`：从URL生成二维码（无需提供二维码图片）
- `--image-from-url`：从URL下载主图片

## 测试

项目包含完整的测试套件，使用 pytest 框架。

### 运行测试

```bash
# 安装依赖
pip install -r requirements.txt

# 运行所有测试
python -m pytest tests/ -v

# 运行特定测试文件
python -m pytest tests/test_qrcode.py -v
```

### 测试覆盖

| 测试文件 | 测试数量 | 测试内容 |
|---------|---------|---------|
| `test_image_utils.py` | 4 | 图片缩放、宽高比保持 |
| `test_qrcode.py` | 6 | 二维码生成、尺寸、URL编码 |
| `test_text_utils.py` | 10 | 文字换行、尺寸计算、字体加载 |
| `test_integration.py` | 6 | 图片合成、端到端工作流 |

### 测试用例说明

**图片工具测试 (test_image_utils.py)**
- `test_resizing_maintains_aspect_ratio` - 验证缩放后宽高比保持不变
- `test_resizing_with_different_scales` - 测试不同缩放比例
- `test_resizing_square_image` - 测试正方形图片缩放
- `test_resizing_preserves_mode` - 验证图片模式（RGB/RGBA）保持不变

**二维码测试 (test_qrcode.py)**
- `test_generates_correct_size` - 验证生成的二维码尺寸正确
- `test_generates_rgb_image` - 验证输出为RGB格式
- `test_generates_different_qr_for_different_urls` - 不同URL生成不同二维码
- `test_generates_same_qr_for_same_url` - 相同URL生成相同二维码
- `test_handles_long_url` - 测试长URL处理
- `test_handles_chinese_characters_in_url` - 测试中文URL处理

**文字工具测试 (test_text_utils.py)**
- `test_short_text_no_wrap` - 短文字不换行
- `test_respects_manual_line_breaks` - 手动换行符正确处理
- `test_wraps_on_chinese_punctuation` - 中文标点处换行
- `test_empty_text` - 空文字处理
- `test_preserves_empty_lines` - 保留空行
- `test_returns_tuple` - 返回正确的尺寸元组
- `test_longer_text_wider` - 长文字宽度更大
- `test_returns_font_object` - 字体加载成功
- `test_different_sizes` - 不同字体大小加载

**集成测试 (test_integration.py)**
- `test_qr_placed_in_bottom_right` - 二维码放置在右下角
- `test_converts_non_rgb_to_rgb` - 非RGB图片转换
- `test_preserves_main_image_content` - 主图内容保持不变
- `test_full_workflow_with_generated_qr` - 完整工作流测试
- `test_save_and_load_merged_image` - 保存和加载测试
- `test_resize_then_merge` - 缩放后合成测试

## 目录结构

## Done
- 对场景图的Prompt生成做了结构化。每个属性都有多种选项
- 了解到DALL模型的局限性，空间位置的精确处理欠佳，几个人都坐在了汽车的前排
- 提示词中的要素：亮度、
- 明确了图片生成的顺序：在网络上收集素材-AI对素材美化-基于单品图生成场景图-将场景图与Logo二维码拼接-上架drive

## TODO
- 为所有单品生成场景图。优化场景图的视角，增加节日。
- 例行节日和文化元素收集。形成活动话术。
- 单品
- 送货服务定时推送