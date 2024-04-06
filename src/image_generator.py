import random
import requests
import zipfile
import io


class NovelaiImageGenerator:
    def __init__(self, user_json_data):

        self.proxies = user_json_data.get("proxies", "None")
        self.token = user_json_data.get("token")  # 设置 API 的访问令牌

        # 初始化函数，接受两个参数：prompt_folder 和 negative_prompt
        self.api = "https://image.novelai.net/ai/generate-image"  # API 的地址
        self.headers = {
            "authorization": f"Bearer {self.token}",  # 设置请求头中的授权信息
            "referer": "https://novelai.net",  # 设置请求头中的 referer
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",  # 设置请求头中的 user-agent
        }
        self.json = {
            "input": "",  # 设置请求的输入文本
            "model": "nai-diffusion-3",  # 设置模型名称
            "action": "generate",  # 设置动作为生成图像
            "parameters": {
                "width": 832,  # 设置生成图像的宽度
                "height": 1216,  # 设置生成图像的高度
                "scale": 6.5,  # 设置图像的缩放比例
                "sampler": "k_euler_ancestral",  # 设置采样器类型
                "steps": 28,  # 设置生成图像的步数
                "seed": 0,  # 设置生成图像的随机种子
                "n_samples": 1,  # 设置生成图像的样本数
                "ucPreset": 0,  # 设置 ucPreset 参数
                "qualityToggle": True,  # 设置 qualityToggle 参数
                "sm": True,  # 设置 sm 参数
                "sm_dyn": True,  # 设置 sm_dyn 参数
                "dynamic_thresholding": False,  # 设置 dynamic_thresholding 参数
                "controlnet_strength": 1,  # 设置 controlnet_strength 参数
                "legacy": False,  # 设置 legacy 参数
                "add_original_image": False,  # 设置 add_original_image 参数
                "uncond_scale": 1,  # 设置 uncond_scale 参数
                "cfg_rescale": 0.1,  # 设置 cfg_rescale 参数
                "noise_schedule": "native",  # 设置 noise_schedule 参数
            },
        }

    def generate_image(self, pos_prompt, neg_prompt):
        # 生成图像的方法
        seed = random.randint(0, 9999999999)  # 生成一个随机种子
        self.json["parameters"]["seed"] = seed  # 将随机种子设置到请求参数中

        self.json["input"] = pos_prompt  # 添加自定义前缀
        self.json["parameters"]["negative_prompt"] = neg_prompt
        r = requests.post(
            self.api,
            json=self.json,
            headers=self.headers,
            proxies=self.proxies if self.proxies != "None" else None,
        )  # 发送 POST 请求
        # print(f"Response: {r}")
        # if len(r.content) < 1000:
        #     print(f"Response content: {r.content}")
        with zipfile.ZipFile(
            io.BytesIO(r.content), mode="r"
        ) as zip:  # 将响应内容解压缩为 Zip 文件
            with zip.open("image_0.png") as image:  # 打开解压后的 Zip 文件中的图像文件
                return image.read()  # 返回图像的二进制数据


if __name__ == "__main__":
    import json

    with open("./json/user.json") as f:
        user_json_data = json.load(f)
    # 创建 NovelaiImageGenerator 实例
    image_generator = NovelaiImageGenerator(
        user_json_data=user_json_data,
    )

    for i in range(5):
        imgBytes = image_generator.generate_image(
            "solo, loli, best quality, amazing quality, very aesthetic, absurdres",
            "lowres, {bad}, error, fewer, extra, missing, worst quality, jpeg artifacts, bad quality, watermark, unfinished, \
        displeasing, chromatic aberration, signature, extra digits, artistic error, username, scan, [abstract], \
        bad anatomy, bad hands, @_@, nail polish, plump",
        )
