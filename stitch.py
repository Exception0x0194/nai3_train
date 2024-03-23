import os
from PIL import Image, PngImagePlugin, ImageFont, ImageDraw
import math


def find_optimal_grid(num_images):
    # 寻找最接近平方根的因数
    root = math.sqrt(num_images)
    rows = math.floor(root)
    cols = math.ceil(root)

    # 如果行数和列数的乘积小于图像总数，则增加行数
    while rows * cols < num_images:
        rows += 1

    return cols, rows


def create_image_matrix(folder_path):
    images = [
        Image.open(os.path.join(folder_path, f))
        for f in os.listdir(folder_path)
        if f.endswith(("jpeg", "png", "jpg"))
    ]
    if not images:
        return None

    # 加载字体
    try:
        font = ImageFont.truetype("arial.ttf", 100)
    except IOError:
        font = ImageFont.load_default()

    image_width, image_height = images[0].size
    num_images = len(images)
    num_columns, num_rows = find_optimal_grid(num_images)

    new_im = Image.new("RGB", (image_width * num_columns, image_height * num_rows))
    draw = ImageDraw.Draw(new_im)

    descriptions = []

    for i, im in enumerate(images):
        x_offset = (i % num_columns) * image_width
        y_offset = (i // num_columns) * image_height

        new_im.paste(im, (x_offset, y_offset))
        draw.text(
            (x_offset + 10, y_offset + 10), str(i + 1), font=font, fill=(255, 0, 0)
        )

        description = im.info.get("Description", "None")
        descriptions.append(f"{i+1}: {description}")

    # 将描述添加到新图片的元信息中
    meta = PngImagePlugin.PngInfo()
    meta.add_text("Description", "\n".join(descriptions))
    new_im.save("stitched.png", pnginfo=meta)


folder_path = "output_selected"  # 替换为你的图片文件夹路径
final_image = create_image_matrix(folder_path)
