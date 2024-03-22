from cli import *
import gradio as gr

if __name__ == "__main__":

    prompt_config = "./json/prompts.json"
    with open(prompt_config, "r", encoding="utf-8") as f:
        prompt_json_data = json.load(f)
    prompt_generator = PromptsGenerator(prompt_json_data)

    config = prompt_generator.get_config()

    print(config)
