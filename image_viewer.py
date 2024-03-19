import os
import shutil
from tkinter import Tk, Label, Button
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

        # 绑定按键事件
        self.root.bind('<a>', self.prev_image)
        self.root.bind('<d>', self.next_image)
        self.root.bind('<w>', self.copy_image)

        # 显示第一张图片
        self.show_image()

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

        image_path = os.path.join(self.folder_path, self.images[self.index])
        image = Image.open(image_path)
        
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
        self.index = (self.index - 1) % len(self.images)
        self.show_image()

    def next_image(self, event):
        self.index = (self.index + 1) % len(self.images)
        self.show_image()

    def copy_image(self, event):
        source_path = os.path.join(self.folder_path, self.images[self.index])
        shutil.copy(source_path, self.destination_folder)
        print(f'图片已复制到: {self.destination_folder}')

if __name__ == '__main__':
    folder_path = 'output'
    destination_folder = 'output_selected'
    viewer = ImageViewer(folder_path, destination_folder)
    viewer.root.mainloop()
