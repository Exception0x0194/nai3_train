import gradio as gr
from PIL import Image
import os
import shutil


image_viewer_target_height = 768


class ImageSelector:
    def __init__(self, folder_path, destination_folder):
        self.folder_path = folder_path
        self.destination_folder = destination_folder
        self.images = self.get_image_list()
        self.index = 0

    def get_image_list(self):
        return [
            file
            for file in os.listdir(self.folder_path)
            if file.endswith(("png", "jpg", "jpeg", "gif"))
        ]

    def get_image(self):
        if not self.images:
            return "No images found", None
        if self.index >= len(self.images):
            self.index = 0  # Reset index if at the end
        image_path = os.path.join(self.folder_path, self.images[self.index])

        img = Image.open(image_path)
        metadata = img.info.get("Description", "None")

        # 等比例缩放图像
        # aspect_ratio = img.width / img.height
        # new_width = int(aspect_ratio * image_viewer_target_height)
        # img = img.resize(
        #     (new_width, image_viewer_target_height), Image.Resampling.LANCZOS
        # )

        return img, metadata

    def next_image(self):
        self.index += 1
        self.images = self.get_image_list()  # Update the image list
        return self.get_image()

    def prev_image(self):
        self.index -= 1
        if self.index < 0:
            self.index = len(self.images) - 1
        return self.get_image()

    def copy_image(self):
        if not self.images:
            return None
        src_path = os.path.join(self.folder_path, self.images[self.index])
        dst_path = os.path.join(self.destination_folder, self.images[self.index])
        shutil.copy2(src_path, dst_path)
        return f"{dst_path}"


# # Create the image viewer object
image_selector = ImageSelector("output", "output_selected")

with gr.Blocks() as image_viewer_demo:

    box_img = gr.Image(scale=0.5, interactive=False)
    box_metadata = gr.Textbox(label="Metadata", interactive=False)

    # Add additional buttons for navigation and actions
    with gr.Row() as btn_row:
        btn_next = gr.Button("Next Image")
        btn_next.click(image_selector.next_image, outputs=[box_img, box_metadata])

        btn_copy = gr.Button("Copy to Destination Folder")
        btn_copy.click(image_selector.copy_image)

        btn_prev = gr.Button("Prev Image")
        btn_prev.click(image_selector.prev_image, outputs=[box_img, box_metadata])

image_viewer_demo.launch()
