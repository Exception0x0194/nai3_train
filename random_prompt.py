from ssl import SSLError
from requests import RequestException
import zipfile
import argparse
import time
import json
import os
import string
import random

from src.prompt_config import PromptsGenerator
from src.image_generator import NovelaiImageGenerator


def save_image_from_binary(image_data, folder_path):
    # 生成随机的文件名并保存
    file_name = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    file_path = os.path.join(folder_path, file_name + ".png")

    try:
        with open(file_path, "wb") as file:
            file.write(image_data)
        print("图像已保存到：", file_path)
    except IOError as e:
        print("保存图像时出错：", e)


if __name__ == "__main__":
    random.seed()

    parser = argparse.ArgumentParser("NAI3 Auto Generation")
    parser.add_argument("--user-config", type=str, default="./json/user.json")
    parser.add_argument("--prompt-config", type=str, default="./json/prompts.json")
    args = parser.parse_args()

    with open(args.user_config, "r", encoding="utf-8") as f:
        user_json_data = json.load(f)
    with open(args.prompt_config, "r", encoding="utf-8") as f:
        prompt_json_data = json.load(f)
    negative_prompt = "lowres, {bad}, error, fewer, extra, missing, worst quality, jpeg artifacts, bad quality, watermark, unfinished, displeasing, chromatic aberration, signature, extra digits, artistic error, username, scan, [abstract], bad anatomy, bad hands, @_@, nail polish, plump"

    # 创建 NovelaiImageGenerator 实例
    image_generator = NovelaiImageGenerator(
        user_json_data=user_json_data,
    )
    prompt_generator = PromptsGenerator(prompt_json_data)

    # 生成图像文件的保存路径
    folder_path = "./output"
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

    # 生成多张图像并保存
    batch_size = 10  # 每批次生成的图像数量
    retry_delay = 20  # 每批次生成后的休眠时间（单位：秒）
    sleep_time = 10  # 每批次生成后的休眠时间（单位：秒）
    retry_delay = 60  # 因为报错中断，脚本的重新启动时间（单位：秒）

    i = 0
    while True:
        try:
            # 生成Prompts
            prompt, comment = prompt_generator.get_prompt()
            print(comment)

            # 生成图像数据
            image_data = image_generator.generate_image(prompt, negative_prompt)

            # 保存图像文件
            save_image_from_binary(image_data, folder_path)

            if (i + 1) % batch_size == 0:
                print(f"已生成 {i + 1} 张图像，休眠 {sleep_time} 秒...")
                time.sleep(sleep_time)
        except (SSLError, RequestException) as e:
            print("发生错误:", e)
            print(f"休眠 {retry_delay} 秒后重新启动")
        except zipfile.BadZipFile as e:
            print("发生错误:", e)
            print("忽略此错误，继续脚本运行")
