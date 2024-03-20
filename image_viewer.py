import argparse
import os
import shutil
from tkinter import Tk, Label, Button, Text
from PIL import Image, ImageTk

class ImageViewer:
    def __init__(self, folder_path, destination_folder):
        self.folder_path = folder_path
        self.destination_folder = destination_folder
        self.images = [file for file in os.listdir(folder_path) if file.endswith(('png', 'jpg', 'jpeg', 'gif'))]
        self.index = 0

        # 设置图形界面
        self.root = Tk()
        self.root.title('Image Viewer')
        self.image_label = Label(self.root)
        self.image_label.pack()

        # 元信息显示控件
        self.metadata_text = Text(self.root, wrap='word', height=4)
        self.metadata_text.pack(fill='x')

        # 绑定按键事件
        self.root.bind('<a>', self.prev_image)
        self.root.bind('<d>', self.next_image)
        self.root.bind('<w>', self.copy_image)

        # 显示第一张图片
        self.show_image()

    def delete_images(self):
        # 删除浏览队列中的所有图片文件
        for img in self.images:
            os.remove(os.path.join(self.folder_path, img))
        self.images.clear()  # 清空图片列表
    
    def update_image_list(self):
        # 获取当前文件夹中的所有图片文件
        current_images = [file for file in os.listdir(self.folder_path) if file.endswith(('png', 'jpg', 'jpeg', 'gif'))]
        # 添加新出现的图片到浏览队列
        new_images = [img for img in current_images if img not in self.images]
        if len(new_images) != 0:
            print(f"发现{len(new_images)}个新文件")
        self.images.extend(new_images)

    def show_image(self):
        # 刷新图片列表
        self.update_image_list()

        # 更新窗口标题
        self.root.title(f"NAI在自己画色图🥵：{self.index + 1}/{len(self.images)}")

        image_path = os.path.join(self.folder_path, self.images[self.index])
        image = Image.open(image_path)
        
        # 获取元信息
        metadata = image.info.get('Description', '未找到生成信息')
        # 显示元信息
        self.metadata_text.delete('1.0', 'end')
        self.metadata_text.insert('1.0', metadata)
        
        # 计算等比例缩放后的宽度
        aspect_ratio = image.width / image.height
        new_height = 768
        new_width = int(aspect_ratio * new_height)
        
        # 等比例缩放图像
        image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo


    def prev_image(self, event):
        self.index = self.index - 1 if self.index > 0 else 0
        self.show_image()

    def next_image(self, event):
        if self.index < len(self.images) - 1:
            self.index += 1
            self.show_image()
        else:
            # 如果已经是最后一张图片，执行删除操作
            self.delete_images()
            self.root.quit()  # 关闭窗口

    def copy_image(self, event):
        source_path = os.path.join(self.folder_path, self.images[self.index])
        shutil.copy(source_path, self.destination_folder)
        print(f'图片已复制到: {self.destination_folder}')

if __name__ == '__main__':
    # 创建解析器
    parser = argparse.ArgumentParser(description='让我康康NAI画了哪些涩图🥵')
    # 添加 --no-delete 参数
    parser.add_argument('--no-delete', action='store_true', help='不删除图片')
    # 添加 --dir 参数
    parser.add_argument('--input-dir', type=str, help='读取文件夹路径')
    parser.add_argument('--output-dir', type=str, help='输出文件夹路径')

    # 解析命令行参数
    args = parser.parse_args()

    # 根据参数设置文件夹路径
    input_path = args.input_dir if args.input_dir else 'output'
    output_path = args.output_dir if args.output_dir else 'output_selected'

    # 实例化 ImageViewer
    viewer = ImageViewer(input_path, output_path)

    # 修改 delete_images 方法，根据 --no-delete 参数决定是否删除图片
    def delete_images(self):
        if not args.no_delete:
            # 删除浏览队列中的所有图片文件
            print(f"达到队列末尾，删除文件夹中图片")
            for img in self.images:
                os.remove(os.path.join(self.folder_path, img))
            self.images.clear()  # 清空图片列表
        else:
            print("达到队列末尾，不删除图片")

    # 替换原有的 delete_images 方法
    ImageViewer.delete_images = delete_images

    viewer.root.mainloop()

