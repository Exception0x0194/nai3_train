import json
import random
import os
import re


class PromptConfig:
    def __init__(self, config, depth=-1):
        self.selection_method = config.get("selection method")
        self.shuffled = config.get("shuffled", False)
        self.prob = config.get("prob", 0.0)
        self.random_brackets = config.get("random_brackets", 0)
        self.select_n = config.get("select_n")
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

    def pick_prompts_from_config(self):
        while True:

            prompt = ""
            comment = "\n" + "--" * self.depth

            # 顺序
            if self.shuffled:
                random.shuffle(self.prompts)

            # 选取prompts
            chosenPrompts = []
            if self.selection_method == "single":
                chosenPrompts = [random.choice(self.prompts)]
            elif self.selection_method == "all":
                chosenPrompts = self.prompts
            elif self.selection_method == "multiple":
                for prompt in self.prompts:
                    if random.random() < self.prob:
                        chosenPrompts.append(prompt)
            elif self.selection_method == "multiple_n":
                chosenPrompts = random.sample(self.prompts, self.select_n)

            # 随机添加括号
            if self.random_brackets != 0:
                print("adding brackets")
                for i, prompt in enumerate(chosenPrompts):
                    brackets = ("[", "]") if random.random() > 0.5 else ("{", "}")
                    n = random.randint(0, self.random_brackets)
                    for b in brackets:
                        b = b * n
                    chosenPrompts[i] = brackets[0] + prompt + brackets[1]

            # 将选取的prompts转换成字符串
            if self.comment != None:
                comment += f"{self.comment}: "
            for chosenPrompt in chosenPrompts:
                if self.type == "str":
                    prompt += f"{chosenPrompt}, "
                    comment += f"{chosenPrompt}, "
                elif self.type == "config":
                    prompt, comment = [
                        i + j
                        for i, j in zip(
                            [prompt, comment], chosenPrompt.pick_prompts_from_config()
                        )
                    ]
                elif self.type == "folder":
                    with open(chosenPrompt, "r") as f:
                        line = f.readline() + ", "
                        prompt += line
                        comment += line
                        f.close()

            # 检查是否符合过滤器要求
            if self.filter is None or re.search(self.filter, prompt):
                break

        return prompt, comment


class PromptsGenerator:
    def __init__(self, prompt_filename):
        self.prompt_filename = prompt_filename

    def load_list(self):
        with open(self.prompt_filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            self.config = PromptConfig(data, -1)

    def get_prompt(self):
        self.load_list()  # 刷新prompts数据
        return self.config.pick_prompts_from_config()


if __name__ == "__main__":
    # Test
    random.seed()
    generator = PromptsGenerator("./json/prompts.json")
    for _ in range(5):
        print(generator.get_prompt()[1])
