# NAI在自己画色图🥵

NAI3，启动！

```python random_prompts.py [--user-config PATH/TO/USER.JSON] [--prompt-config PATH/TO/PROMPT.JSON]```

## Prompt设置（随机正向提示词）

默认读取`json/prompts.json`中的设置，包括的key和value的作用有：

- `selection_method`：prompts的取样方法，value包括：
  - `single`：随机取一个prompt
  - `multiple_prob`：按照指定的概率随机0个至多个prompts
  - `multiple_num`：从prompts中随机选择n个不重复的
  - `sequential`：顺序遍历所有prompts
  - `all`：使用所有的prompts
- `prob`：（`selection_method`为`multiple_prob`时）随机选取的概率
- `num`：选取的数量
  - `selection_method`为`multiple_num`时，为随机选取的数量
  - `selection_method`为`sequential`时,时顺序选取的数量，大于1时将顺序遍历所有组合
- `random_brackets`：随机向`str`格式的prompts中添加0~指定数量的括号（`[]`和`{}`）
- `filter`：包含正则表达式的字符串，只有取样的prompts符合正则表达式才会被输出
- `shuffled`：取样prompts前是否打乱顺序，缺省为`false`
- `comment`：prompts的注释，在取样prompts时便于阅读
- `type`：指示接下来prompts的类型，value包括：
  - `config`：prompts包含嵌套的prompts设置，将迭代地进行解析和输出
  - `str`：字符串格式的prompts
  - `folder`：包含prompts文件的文件夹，将读取文件夹中文件保存的prompts作为输出
- `prompts`：包含prompts数据的数组

### 一些示例Prompts文件

一些特定场景下的配置文件示例：

- `./json/prompts.json`：随机选取角色、风格、服装、风格等，组合prompts并生成图片

- `./json/prompts.folder.json`：从自动打标图片的文件夹中，利用正则表达式选取符合xp的prompts并生成图片
  - 其中的自动打标文件来自[prompt_4k](https://huggingface.co/datasets/windsingai/random_prompt/resolve/main/prompt_4k.zip)，其它类似格式的prompt文件均可

## 用户设置（API Key、代理）

默认读取`./json/user.json`中的用户设置，包括的key和value的作用有：

- `token`：NAI的API token
- `proxy`：http和https代理设置

一个user.json的示例：

```
{
    "token": "NAI_TOKEN_HERE",
    "proxies": {
        "http": "http://localhost:12345",
        "https": "http://localhost:12345"
    }
}
```
# 简单的图像浏览和筛选GUI

让我康康你生成的正不正常啊

`python image_viewer.py [--no-delete] [--input-dir INPUT_DIR] [--output-dir OUTPUT_DIR]`

- 功能说明
  - 浏览指定文件夹中的图片，将使用快捷键将所需图片筛选到输出文件夹中
  - 在翻阅图片时将搜索文件夹中的新文件，并添加到浏览队列的末尾
  - **默认情况下，达到浏览队列末尾时删除浏览队列中的所有文件**

- 参数说明
  - `--input-dir INPUT_DIR`：浏览的文件夹（默认`./output/`）
  - `--output-dir OUTPUT_DIR`：筛选图片的输出文件夹（默认`./output_selected/`）
  - `--no-delete`：在浏览达到队列末尾时不删除队列中的所有图片

- 键位绑定
  - `W`：将当前图像复制到指定文件夹中
  - `A`、`D`：前后翻阅图像

# 简单的XLSX图鉴生成器

用筛选出的图片全自动生成法典

`python export_xlsx.py [--input-dir INPUT_DIR] [--output OUTPUT] [--filter REGEX] [--per-row IMAGES_PER_ROW] [--img-height IMG_HEIGHT_PX]`

- 功能说明
  - 默认读取指定文件夹中的图片信息，读取图片元信息并缩放图片，输出到指定表格文件

- 参数说明
  - `--input-dir INPUT_DIR`：输入图片所在的文件夹（默认`./output_selected/`）
  - `--output OUTPUT`：输出文件名（默认`./spellbook.xlsx`）
  - `--filter REGEX`：按正则筛选符合条件的prompts
    - 如`--filter '.*character:.*'`将选出所有含有"character:"的prompts记录在法典中
    - Prompts不符合要求（过滤后字符串为空）的图片将不被插入到表格文件中
  - `--per-row IMAGES_PER_ROW`：更改每行的图片数量（默认3个）
    - 当每行图片数量为`1`时，将把筛选后prompts相同的图片置于同一行
  - `--img-height IMG_HEIGHT_PX`：更改图片的高度（以像素计，默认512px）