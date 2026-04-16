# PDF下载与文本提取
import os
import re
from pathlib import Path
import fitz
import requests

# papers目录
PAPERS_DIR = Path(__file__).parent / "papers"
PAPERS_DIR.mkdir(exist_ok=True)


def download_pdf(url: str) -> str:
    """从URL下载PDF，返回本地路径"""
    # 处理arXiv链接
    if "arxiv.org" in url:
        match = re.search(r"(\d{4}\.\d{4,5})", url)
        if match:
            paper_id = match.group(1)
            url = f"https://arxiv.org/pdf/{paper_id}.pdf"
            filepath = PAPERS_DIR / f"{paper_id}.pdf"
        else:
            filepath = PAPERS_DIR / f"paper_{os.getpid()}.pdf"
    else:
        filepath = PAPERS_DIR / f"paper_{os.getpid()}.pdf"

    resp = requests.get(url, timeout=30)
    resp.raise_for_status()

    with open(filepath, "wb") as f:
        f.write(resp.content)

    print(f"[INFO] PDF下载到: {filepath}")
    return str(filepath)


def parse_pdf(filepath: str, save_text: bool = True) -> str:
    """提取PDF文本，清洗格式，删除References之后内容"""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"PDF不存在: {filepath}")

    doc = fitz.open(filepath)
    text = "".join(page.get_text() for page in doc)
    doc.close()

    if not text.strip():
        raise ValueError("PDF文本为空")

    # 删除References之后内容
    for pattern in ["\nReferences\n", "\nREFERENCES\n", "\nBibliography\n"]:
        if pattern in text:
            text = text.split(pattern)[0]
            break

    # 文本清洗
    text = clean_text(text)

    # 保存文本到papers目录
    if save_text:
        pdf_name = Path(filepath).stem
        text_file = PAPERS_DIR / f"{pdf_name}.txt"
        text_file.write_text(text, encoding="utf-8")
        print(f"[INFO] 文本已保存: {text_file}")

    return text.strip()


def clean_text(text: str) -> str:
    """清洗PDF提取的文本格式"""
    # 1. 合并单行断句（句末没有标点但下一行开头是小写字母）
    lines = text.split('\n')
    merged = []
    for i, line in enumerate(lines):
        if i == 0:
            merged.append(line)
        else:
            prev = merged[-1]
            # 如果前一行末尾不是句末标点，且当前行开头是小写字母或数字，合并
            if prev and not prev.endswith(('.', '!', '?', '。', '！', '？', ':', '：', ',', ',')):
                if line and (line[0].islower() or line[0].isdigit()):
                    merged[-1] = prev + ' ' + line
                else:
                    merged.append(line)
            else:
                merged.append(line)

    text = '\n'.join(merged)

    # 2. 清理多余空行
    text = re.sub(r'\n{3,}', '\n\n', text)

    # 3. 清理行内多余空格
    text = re.sub(r' {2,}', ' ', text)

    return text