import json
import random

class PromptConfig:
    def __init__(self, config, depth=-1):
        self.selection_method = config["selection method"]
        self.order = config["order"] if self.selection_method != "single" else "order"
        self.prob = config["prob"] if self.selection_method == "multiple" else 0.
        self.type = config["type"]
        self.comment = config["comment"]

        self.depth = depth + 1

        # 读取prompts
        self.prompts = []
        if self.type == "config":
            for prompt in config["prompts"]:
                self.prompts.append(PromptConfig(prompt, self.depth))
        elif self.type == "str":
            self.prompts = config["prompts"]
        elif self.type == "folder":
            # TODO: 读取文件夹中的prompts数据？
            pass

    def pick_prompts_from_config(self):
        prompt = ""
        comment = "\n"+"--"*self.depth

        # 顺序
        if self.order == "shuffled":
            random.shuffle(self.prompts)
        
        # 选取prompts
        chosenPrompts = []
        if self.selection_method == "single":
            chosenPrompts= [random.choice(self.prompts)]
        elif self.selection_method == "all":
            chosenPrompts = self.prompts
        elif self.selection_method == "multiple":
            for prompt in self.prompts:
                if random.random() < self.prob:
                    chosenPrompts.append(prompt)

        # 将选取的prompts转换成字符串
        if self.comment != None:
            comment += f"{self.comment}: "
        for chosenPrompt in chosenPrompts:
            if self.type == "str":
                prompt += f'{chosenPrompt}, '
                comment += f'{chosenPrompt}, '
            elif self.type == "config":
                prompt, comment = [i+j for i,j in zip([prompt,comment], chosenPrompt.pick_prompts_from_config())]
            elif self.type == "folder":
                pass
        return prompt, comment


class PromptsGenerator:
    def __init__(self, prompt_filename):
        self.prompt_filename = prompt_filename

    def load_list(self):
        with open(self.prompt_filename, "r", encoding='utf-8') as file:
            data = json.load(file)
            self.config = PromptConfig(data, -1)

    def get_prompt(self):
        self.load_list() # 刷新prompts数据
        return self.config.pick_prompts_from_config()
    
if __name__ == "__main__":
    # Test
    random.seed()
    generator = PromptsGenerator('./json/prompts.json')
    for _ in range(5):
        print(generator.get_prompt()[1])