# NAI在自己画色图🥵

NAI3，启动！

```python random_prompt.py --user-config ./json/user_config.json --prompt-config ./json/prompts.json```

## 基于JSON的prompts组织

包括的key和value的作用有：

- `selection method`：prompts的取样方法，value包括：
  - `single`：随机取一个prompt
  - `multiple`：按照指定的概率随机0个至多个prompts
  - `multiple_n`：从prompts中随机选择n个不重复的
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
- `select_n`：（`selection_method`为`multiple_n`时）随机选取的数量
- `random_brackets`：随机向`str`格式的prompts中添加0~指定数量的括号（`[]`和`{}`）

示例文件：`./json/prompts.json`和`./json/prompts.folder.json`

## 基于JSON的用户信息组织

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

`python image_viewer.py`

默认浏览`./output/`文件夹中的图片，在翻阅图片时将搜索文件夹中的新文件，并添加到浏览队列的末尾

## 键位绑定

`W`：将当前图像复制到指定文件夹中，默认输出到`./output_selected/`文件夹
`A`、`D`：前后翻阅图像