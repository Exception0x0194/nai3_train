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

img_px_height = 400
img_cell_height = img_px_height * 3/4
img_cell_width = 0
ratio = 0.125
text_cell_width = 30

# 创建一个新的Excel工作簿
wb = Workbook()
ws = wb.active

# 设置默认格式
ws.row_dimensions[1].height = img_cell_height
ws.column_dimensions['A'].width = text_cell_width
ws.column_dimensions['C'].width = text_cell_width
ws.column_dimensions['E'].width = text_cell_width
alignment = Alignment(vertical='top', wrap_text=True)

col, row = 'A', 1

tmp_paths = []
# 遍历文件夹中的所有文件
for index, filename in enumerate(os.listdir(folder_path), start=1):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
        # 获取图片完整路径
        image_path = os.path.join(folder_path, filename)
        
        # 打开图片并读取元信息
        with Image.open(image_path) as img:
            description = img.info.get('Description', '无描述信息')
            
            # 等比缩放图片
            aspect_ratio = img.width / img.height
            new_height = img_px_height
            new_width = int(aspect_ratio * new_height)
            if img_cell_width < int(new_width * ratio):
                img_cell_width = int(new_width * ratio)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # 使用NamedTemporaryFile创建一个临时文件
            with NamedTemporaryFile(delete=False, dir=temp_folder, suffix='.png') as tmp:
                img.save(tmp.name)
                temp_image_path = tmp.name
                tmp_paths.append(temp_image_path)

            # 创建新的行，并在第一列写入'Description'元信息
            if args.filter:
                description = ','.join([d for d in description.split(',') if pattern.search(d)]).strip()

            # ws.append([description])
            # # 获取当前行号
            # row = ws.max_row
            # # 调整行高以适应图片
            # ws.row_dimensions[row].height = coloum_height
            # # 将Pillow图像转换为Openpyxl图像
            # img_to_insert = OpenpyxlImage(temp_image_path)
            # ws.add_image(img_to_insert, f'B{row}')

            # 创建新的行，并在当前列写入'Description'元信息
            cell = f'{col}{row}'
            ws[cell] = description
            ws[cell].alignment = alignment
            
            # 调整行高以适应图片
            ws.row_dimensions[row].height = img_cell_height
            
            # 将Pillow图像转换为Openpyxl图像并插入到下一列
            img_col = chr(ord(col) + 1)  # 下一列
            img_to_insert = OpenpyxlImage(temp_image_path)
            ws.add_image(img_to_insert, f'{img_col}{row}')

        # 更新列计数器，每三个图片换行
        if index % 3 == 0:
            row += 1
            col = 'A'
        else:
            col = chr(ord(col) + 2)  # 移动到下一个metadata列

# 应用格式
for cell in ws['A']:
    cell.alignment = alignment

ws.column_dimensions['B'].width = img_cell_width
ws.column_dimensions['D'].width = img_cell_width
ws.column_dimensions['F'].width = img_cell_width

# 保存Excel文件
wb.save('images.xlsx')

# 删除临时文件
for path in tmp_paths:
    if os.path.exists(path):
        os.remove(path)
