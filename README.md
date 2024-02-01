<!-- markdownlint-disable MD031 MD033 MD036 MD041 -->

<div align="center">

<a href="https://v2.nonebot.dev/store">
  <img src="https://raw.githubusercontent.com/A-kirami/nonebot-plugin-template/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo">
</a>

<p>
  <img src="https://raw.githubusercontent.com/lgc-NB2Dev/readme/main/template/plugin.svg" alt="NoneBotPluginText">
</p>

# NoneBot-Plugin-Riffusion

_✨ 你给歌词，AI 作曲 ✨_

<img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">
<a href="https://pdm.fming.dev">
  <img src="https://img.shields.io/badge/pdm-managed-blueviolet" alt="pdm-managed">
</a>
<a href="https://wakatime.com/badge/user/b61b0f9a-f40b-4c82-bc51-0a75c67bfccf/project/018c6a44-7df9-4dca-822c-6c16c4743537">
  <img src="https://wakatime.com/badge/user/b61b0f9a-f40b-4c82-bc51-0a75c67bfccf/project/018c6a44-7df9-4dca-822c-6c16c4743537.svg" alt="wakatime">
</a>

<br />

<a href="./LICENSE">
  <img src="https://img.shields.io/github/license/lgc-NB2Dev/nonebot-plugin-riffusion.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-riffusion">
  <img src="https://img.shields.io/pypi/v/nonebot-plugin-riffusion.svg" alt="pypi">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-riffusion">
  <img src="https://img.shields.io/pypi/dm/nonebot-plugin-riffusion" alt="pypi download">
</a>

</div>

## 💿 安装

以下提到的方法 任选**其一** 即可

<details open>
<summary>[推荐] 使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

```bash
nb plugin install nonebot-plugin-riffusion
```

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

```bash
pip install nonebot-plugin-riffusion
```

</details>
<details>
<summary>pdm</summary>

```bash
pdm add nonebot-plugin-riffusion
```

</details>
<details>
<summary>poetry</summary>

```bash
poetry add nonebot-plugin-riffusion
```

</details>
<details>
<summary>conda</summary>

```bash
conda install nonebot-plugin-riffusion
```

</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分的 `plugins` 项里追加写入

```toml
[tool.nonebot]
plugins = [
    # ...
    "nonebot_plugin_riffusion"
]
```

</details>

## ⚙️ 配置

在 NoneBot2 项目的 `.env` 文件中添加下表中的必填配置

|        配置项         | 必填 | 默认值  |                  说明                   |
| :-------------------: | :--: | :-----: | :-------------------------------------: |
|        `PROXY`        |  否  | `None`  |       插件请求 API 使用的代理地址       |
|  `RIFFUSION_TIMEOUT`  |  否  |  `30`   |        插件请求接口超时，单位秒         |
| `RIFFUSION_BREAK_URL` |  否  | `False` | 是否破坏插件消息中的 URL 以降低风控概率 |

## 🎉 使用

使用指令 `riffusion -h` 查看帮助

## 📞 联系

QQ：3076823485  
Telegram：[@lgc2333](https://t.me/lgc2333)  
吹水群：[1105946125](https://jq.qq.com/?_wv=1027&k=Z3n1MpEp)  
邮箱：<lgc2333@126.com>

## 💡 鸣谢

### [Riffusion](https://www.riffusion.com/)

- 服务提供

### [nonebot/plugin-alconna](https://github.com/nonebot/plugin-alconna)

- 强大的命令解析库，和多平台适配方案

## 💰 赞助

感谢大家的赞助！你们的赞助将是我继续创作的动力！

- [爱发电](https://afdian.net/@lgc2333)
- <details>
    <summary>赞助二维码（点击展开）</summary>

  ![讨饭](https://raw.githubusercontent.com/lgc2333/ShigureBotMenu/master/src/imgs/sponsor.png)

  </details>

## 📝 更新日志

### 0.1.2

- 添加 `PROXY` 配置项

### 0.1.1

- 修复 `-h` 参数无效的问题
