# NAI在自己画色图🥵

NAI3，启动！

```python random_prompts.py [--user-config PATH/TO/USER.JSON] [--prompt-config PATH/TO/PROMPT.JSON]```

## Prompt设置（随机正向提示词）

默认读取`json/prompts.json`中的设置，包括的key和value的作用有：

- `selection_method`：prompts的取样方法，value包括：
  - `single`：随机取一个prompt
  - `multiple_prob`：按照指定的概率随机0个至多个prompts
  - `multiple_num`：从prompts中随机选择n个不重复的
  - `all`：使用所有的prompts
- `shuffled`：取样prompts前是否打乱顺序，缺省为`false`
- `comment`：prompts的注释，在取样prompts时便于阅读
- `type`：指示接下来prompts的类型，value包括：
  - `config`：prompts包含嵌套的prompts设置，将迭代地进行解析和输出
  - `str`：字符串格式的prompts
  - `folder`：包含prompts文件的文件夹，将读取文件夹中文件保存的prompts作为输出
- `prompts`：包含prompts数据的数组
- `filter`：包含正则表达式的字符串，只有取样的prompts符合正则表达式才会被输出
- `prob`：（`selection_method`为`multiple`时）随机选取的概率
- `num`：（`selection_method`为`multiple_n`时）随机选取的数量
- `random_brackets`：随机向`str`格式的prompts中添加0~指定数量的括号（`[]`和`{}`）

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

浏览指定文件夹（默认`./output/`）中的图片，在翻阅图片时将搜索文件夹中的新文件，并添加到浏览队列的末尾

**默认情况下，达到浏览队列末尾时删除浏览队列中的所有文件**；可以使用`--no-delete`启动参数避免删除

浏览过程中可以按键将图像复制到指定文件夹中（默认`./output_select/`）

图片的正面提示词将被显示在图片下方的文本框中

### 键位绑定

`W`：将当前图像复制到指定文件夹中

`A`、`D`：前后翻阅图像

# 简单的XLSX图鉴生成器

用筛选出的图片全自动生成法典

`python export_xlsx.py [--filter REGEX] [--per-row IMAGES_PER_ROW]`

默认读取`./output_selected/`中的图片信息，将元信息中的`Description`字段输入第一列，将图片缩放到高度400px并插入到第二列，输出到`images.xlsx`

可以使用`--filter`参数，使用英文逗号`,`分隔后，按正则筛选符合条件的prompts，如`--filter '.*character:.*'`将选出所有含有"character:"的prompts记录在法典中

可以使用`--per-row`参数，更改每行的图片数量（默认3个）