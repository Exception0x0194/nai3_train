import json
import random
import os
import re


class PromptConfig:
    def __init__(self, config, depth=-1):
        self.selection_method = config.get("selection_method")
        self.shuffled = config.get("shuffled", False)
        self.prob = config.get("prob", 0.0)
        self.num = config.get("num", 0)
        self.random_brackets = config.get("random_brackets", 0)
        self.type = config.get("type")
        self.comment = config.get("comment", "")
        self.filter = config.get("filter")
        self.depth = depth + 1

        # 读取prompts
        self.prompts = []
        if self.type == "config":
            for prompt in config["prompts"]:
                self.prompts.append(PromptConfig(prompt, self.depth))
        elif self.type == "str":
            self.prompts = config["prompts"]
        elif self.type == "folder":
            # 读取文件夹中的tag文件名
            for pathPrefix in config["prompts"]:
                fileNameList = os.listdir(pathPrefix)
                for fileName in fileNameList:
                    self.prompts.append(os.path.join(pathPrefix, fileName))

    def add_brackets(self, s):
        brackets = ["[", "]"] if random.random() > 0.5 else ["{", "}"]
        n = random.randint(0, self.random_brackets)
        brackets = [b * n for b in brackets]
        s = brackets[0] + s + brackets[1]

    def pick_prompts_from_config(self):
        while True:

            prompt = ""
            comment = "\n" + "--" * self.depth

            # 打乱顺序
            if self.shuffled:
                random.shuffle(self.prompts)

            # 选取prompts
            chosenPrompts = []
            if self.selection_method == "single":
                chosenPrompts = [random.choice(self.prompts)]
            elif self.selection_method == "all":
                chosenPrompts = self.prompts
            elif self.selection_method == "multiple_prob":
                chosenPrompts = random.choices(
                    self.prompts, [self.prob] * len(self.prompts)
                )
            elif self.selection_method == "multiple_num":
                chosenPrompts = random.sample(self.prompts, self.num)

            # 将选取的prompts转换成字符串
            if self.comment != None:
                comment += f"{self.comment}: "

            for p in chosenPrompts:
                if self.type == "str":
                    # 随机添加括号
                    if self.random_brackets != 0:
                        p = self.add_brackets(p)
                    prompt += f"{p}, "
                    comment += f"{p}, "
                elif self.type == "config":
                    prompt, comment = [
                        i + j
                        for i, j in zip([prompt, comment], p.pick_prompts_from_config())
                    ]
                elif self.type == "folder":
                    with open(p, "r") as f:
                        line = f.readline() + ", "
                        prompt += line
                        comment += line
                        f.close()

            # 检查是否符合过滤器要求
            if self.filter is None or re.search(self.filter, prompt):
                break

        return prompt, comment


class PromptsGenerator:
    def __init__(self, jsonData):
        self.config = PromptConfig(jsonData, -1)

    def get_prompt(self):
        return self.config.pick_prompts_from_config()


if __name__ == "__main__":
    random.seed()
    with open("./json/prompts.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    generator = PromptsGenerator(data)
    for _ in range(5):
        prompt, comment = generator.get_prompt()
        print(comment)
