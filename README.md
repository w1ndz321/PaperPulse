# PaperPulse

> 上传 PDF 文件 或输入 arXiv URL，AI 会自动帮你生成解读网页。

把学术论文变成一篇易读，可分享的 HTML 文章。
---

## 在线预览效果

- [A-MEM：给 LLM Agent 装上“会自己整理笔记”的长期记忆，复杂推理最高接近翻倍](https://w1ndz321.github.io/PaperPulse/A-MEM.html)
- [ACE：别再把提示词越改越短了，这篇论文让上下文像“作战手册”一样越用越强](https://w1ndz321.github.io/PaperPulse/ACE.html)
- [GEPA：不用几万次RL采样，靠“反思改提示词”也能赢，最高少用35倍rollouts](https://w1ndz321.github.io/PaperPulse/GEPA.html)
- [MemAgent：只用8K窗口，竟把大模型长文本问答拉到350万token还几乎不掉点](https://w1ndz321.github.io/PaperPulse/MemAgent.html)
- [Meta-Harness：让AI自己改“外挂代码”，把手写LLM系统优化成榜单第一](https://w1ndz321.github.io/PaperPulse/Meta-Harness.html)
- [花了147万美元，造出4.5万个可执行SWE环境：OpenSWE把“训练修Bug智能体”这件事彻底开源了](https://w1ndz321.github.io/PaperPulse/OPENSWE.html)
---

## Why PaperPulse

| | 传统阅读 | PaperPulse |
|---|---|---|
| 阅读门槛 | 需要专业知识和英语能力 | AI 提炼成通俗易懂的中文概述，同时紧贴原文知识 |
| 资源发现 | 手动搜索论文和代码链接 | 自动提取并展示关联的论文链接和开源代码 |
| 阅读节奏 | 翻译、理解需要专门规划时间 | 几分钟即可快速判断文章是否值得读，想深入了解也有完整解读 |
| 分享效率 | 发一个 PDF 文件，对方要自己啃 | 发一个链接，同样时间内获取的信息量远超原文 |

### 核心优势

- **零配置上手** — 填个 API Key 就能跑，支持 arXiv 链接和本地 PDF
- **面向读者的内容编排** — 不是机器翻译或摘要，而是面向普通读者的内容重写，让非专业读者也能快速抓住论文核心
- **HTML 格式输出** — 支持目录跳转，可直接分享链接浏览器打开
- **批量处理** — 一次上传多篇 PDF 或输入多个 URL，自动排队生成
---

## Quick Start

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 API

复制 `.env.example` 为 `.env`，填入你的 API 信息：

```bash
cp .env.example .env
```

编辑 `.env`：

```
OPENAI_API_KEY= "密钥"
OPENAI_BASE_URL= "API 地址"
MODEL_NAME= "模型名称"
```

### 3. 启动

```bash
python app_gradio.py
```
浏览器打开显示的网址，上传 PDF 或粘贴 arXiv URL，点击「生成解读」即可。

## License
MIT
-