import os
from PIL import Image
from openpyxl import Workbook
from openpyxl.drawing.image import Image as OpenpyxlImage
from openpyxl.styles import Alignment
from tempfile import NamedTemporaryFile
import argparse
import re


# 解析命令行参数
parser = argparse.ArgumentParser()
parser.add_argument('--filter', type=str, help='Regex pattern to filter the description')
args = parser.parse_args()

# 编译提供的正则表达式
if args.filter:
    pattern = re.compile(args.filter)


folder_path = 'output_selected'
temp_folder = 'tmp'

target_height = 400
coloum_height = target_height * 3/4
target_width = 50

# 创建一个新的Excel工作簿
wb = Workbook()
ws = wb.active

# 设置默认格式
ws.row_dimensions[1].height = coloum_height
ws.column_dimensions['A'].width = 100
alignment = Alignment(vertical='top', wrap_text=True)

tmp_paths = []
# 遍历文件夹中的所有文件
for filename in os.listdir(folder_path):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
        # 获取图片完整路径
        image_path = os.path.join(folder_path, filename)
        
        # 打开图片并读取元信息
        with Image.open(image_path) as img:
            description = img.info.get('Description', '无描述信息')
            
            # 等比缩放图片
            aspect_ratio = img.width / img.height
            new_height = target_height
            new_width = int(aspect_ratio * new_height)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # 使用NamedTemporaryFile创建一个临时文件
            with NamedTemporaryFile(delete=False, dir=temp_folder, suffix='.png') as tmp:
                img.save(tmp.name)
                temp_image_path = tmp.name
                tmp_paths.append(temp_image_path)

            # 创建新的行，并在第一列写入'Description'元信息
            if args.filter:
                description = ','.join([d for d in description.split(',') if pattern.search(d)]).strip()
            ws.append([description])
            # 获取当前行号
            row = ws.max_row
            # 调整行高以适应图片
            ws.row_dimensions[row].height = coloum_height
            # 将Pillow图像转换为Openpyxl图像
            img_to_insert = OpenpyxlImage(temp_image_path)
            ws.add_image(img_to_insert, f'B{row}')

# 应用格式
for cell in ws['A']:
    cell.alignment = alignment

# 保存Excel文件
wb.save('images.xlsx')

# 删除临时文件
for path in tmp_paths:
    if os.path.exists(path):
        os.remove(path)
