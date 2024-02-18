<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-bf1marneserverlist

_✨ 查询BF1-MarneServer服务器信息 ✨_


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/safeluren/nonebot-plugin-bf1marneserverlist.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-bf1marneserverlist">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-bf1marneserverlist.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">

</div>

## 📖 介绍

查询BF1的MarneServer服务器信息

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-bf1marneserverlist

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-bf1marneserverlist
</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-bf1marneserverlist
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-bf1marneserverlist
</details>
<details>
<summary>conda</summary>

    conda install nonebot-plugin-bf1marneserverlist
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_bf1marneserverlist"]

</details>

## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的必填配置

| 配置项 | 必填 | 默认值 | 说明 |
|:-----:|:----:|:----:|:----:|
| marne_url | 是 | 无 | 自行寻找相关URL，需要以/结尾 |
| marne_plugin_enabled | 是 | True | 是否启用插件 |
| marne_data_dir | 是 | './marne_data/' | 存储绑定数据的目录，目前是以群号为命名的.json文件，里面保存的是通过API返回到数据 |

## 🎉 使用
### 指令表
| 指令 | 权限 | 需要@ | 范围 | 说明 |
|:-----:|:----:|:----:|:----:|:----:|
| marne bind {服务器ID} | 主人、群主、管理员 | 否 | 群聊 | 服务器ID需要你自己寻找~ |
| marne | 群员 | 否 | 群聊 | 无 |