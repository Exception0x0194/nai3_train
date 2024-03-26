import json
import random
import os
import re
import itertools


class PromptConfig:
    def __init__(self, config: dict, depth=-1):
        self.selection_method = config.get(
            "selection_method", config.get("selection method", None)
        )
        self.shuffled = config.get("shuffled", False)
        self.prob = config.get("prob", 0.0)
        self.num = config.get("num", config.get("select_n", 0))
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

        # 初始化遍历
        self.seq_idx = 0
        self.seq_list = list(
            itertools.permutations(list(range(len(self.prompts))), max(1, self.num))
        )

    def add_brackets(self, s):
        brackets = ["[", "]"] if random.random() > 0.5 else ["{", "}"]
        n = random.randint(0, self.random_brackets)
        brackets = [b * n for b in brackets]
        return brackets[0] + s + brackets[1]

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
                chosenPrompts = [p for p in self.prompts if random.random() < self.prob]
            elif self.selection_method == "multiple_num":
                chosenPrompts = random.sample(self.prompts, self.num)
            elif self.selection_method == "sequential":
                chosenPrompts = [
                    self.prompts[idx] for idx in self.seq_list[self.seq_idx]
                ]
                self.seq_idx = (self.seq_idx + 1) % len(self.seq_list)

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

    def get_config(self):
        return self.config

    def get_prompt(self):
        return self.config.pick_prompts_from_config()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser("Prompt conifg debug program")
    parser.add_argument("--prompt-config", type=str, default="./json/prompts.json")
    args = parser.parse_args()

    random.seed()
    with open(args.prompt_config, "r", encoding="utf-8") as file:
        data = json.load(file)
    generator = PromptsGenerator(data)
    for _ in range(10):
        prompt, comment = generator.get_prompt()
        print(comment)
