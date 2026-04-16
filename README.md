# PaperPulse

> 上传 PDF 文件 或输入 arXiv URL，AI 会自动帮你生成解读网页。

把枯燥的学术论文，变成一篇好读、好看、可分享的 HTML 文章。

---

## 为什么选择 PaperPulse

| | 传统阅读 | PaperPulse |
|---|---|---|
| 理解门槛 | 需要通读全文，逐段理解 | AI 帮你提炼核心，一目了然 |
| 信息提取 | 手动找链接、作者、关键词 | 自动提取，顶部卡片直接展示 |
| 阅读体验 | PDF 滚动 + 缩放，体验差 | 精心排版的网页，舒适的阅读节奏 |
| 分享协作 | 发个 PDF 文件 | 发一个链接，打开即读 |

### 核心优势

- **AI 自动解读** — 不只是提取文本，而是用大模型生成通俗易懂的结构化解读
- **精美 HTML 输出** — Tailwind CSS 定制主题，带目录、卡片、呼吸动画，直接浏览器打开
- **批量处理** — 一次上传多篇 PDF 或输入多个 URL，自动排队生成
- **零配置上手** — 填个 API Key 就能跑，支持 arXiv 链接和本地 PDF
- **信息结构化** — 自动提取论文链接、代码链接、机构、作者、关键词

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
OPENAI_API_KEY=你的密钥
OPENAI_BASE_URL=你的 API 地址
MODEL_NAME=gpt-4o-mini
```

### 3. 启动

```bash
python app_gradio.py
```

浏览器打开 **显示的网址**，上传 PDF 或粘贴 arXiv URL，点击「生成解读」即可。
---

## 输出示例

## License

MIT
