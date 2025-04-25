# 图片合成工具

一个用于合成主图片、Logo和二维码的工具，可选择性地添加文字说明。

## 功能特点

- 将三张图片合成为一张：主图片、Logo（左下角）和二维码（右下角）
- 可选择是否添加文字说明
- 支持文字自动换行
- 可自定义图片缩放比例、边距和字体大小

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

## 参数说明

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