@echo off
chcp 65001
set PYTHONIOENCODING=utf8
python "main2.py" "images/顶好葱油饼.png" "images/一品香二维码.png" "images/一品香Logo-甄选.png" --output "output/merged.jpg" --qr-scale 0.2 --logo-scale 0.2 --margin 5 --font-size 25 
pause