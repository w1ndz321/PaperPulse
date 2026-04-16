# Gradio界面 - 公众号风格论文解读工具
import os
import shutil
import gradio as gr
import time
from pathlib import Path

from pdf_parser import download_pdf, parse_pdf, PAPERS_DIR
from summarizer import summarize_stream
from html_generator import generate_html, OUTPUTS_DIR

OUTPUTS_DIR.mkdir(exist_ok=True)


def log(msg: str):
    """终端日志"""
    print(f"[{time.strftime('%H:%M:%S')}] {msg}")


def process_single_paper(pdf_path=None, url=None):
    """处理单篇论文，返回 (pdf_path, html_path, html_filename)"""
    # Step 1: 获取PDF
    if url:
        filepath = download_pdf(url)
    else:
        src_path = pdf_path.name if hasattr(pdf_path, 'name') else pdf_path
        filename = Path(src_path).stem + ".pdf"
        filepath = str(PAPERS_DIR / filename)
        shutil.copy(src_path, filepath)
        log(f"PDF已保存: {filepath}")

    # Step 2: 解析PDF
    text = parse_pdf(filepath)
    log(f"文本长度: {len(text)} 字符")

    # Step 3: 流式生成解读
    full_text = ""
    for partial_text in summarize_stream(text):
        full_text = partial_text

    log("解读完成")

    # Step 4: 生成HTML
    html_path, html_filename = generate_html(full_text)
    log(f"HTML路径: {html_path}")

    return filepath, html_path, html_filename


def process_batch(pdf_files, urls_text: str):
    """批量处理多篇论文"""
    # 解析输入
    files = pdf_files if isinstance(pdf_files, list) else ([pdf_files] if pdf_files else [])
    urls = [u.strip() for u in urls_text.split('\n') if u.strip()] if urls_text else []

    if not files and not urls:
        yield "请上传PDF或输入URL", ""
        return

    total = len(files) + len(urls)
    results = []

    # 处理上传的PDF
    for i, f in enumerate(files):
        name = f.name if hasattr(f, 'name') else str(f)
        log(f"[{i+1}/{total}] 处理: {Path(name).stem}")
        yield f"📥 正在处理 {i+1}/{total}: {Path(name).stem}...", ""

        try:
            pdf_path, html_path, html_filename = process_single_paper(pdf_path=f)
            results.append((Path(name).stem, pdf_path, html_path, html_filename))
        except Exception as e:
            log(f"[{i+1}/{total}] 失败: {e}")
            results.append((Path(name).stem, None, None, f"❌ {e}"))

    # 处理URL
    for i, url in enumerate(urls):
        log(f"[{len(files)+i+1}/{total}] 处理: {url}")
        yield f"📥 正在处理 {len(files)+i+1}/{total}: {url.split('/')[-1]}...", ""

        try:
            pdf_path, html_path, html_filename = process_single_paper(url=url)
            results.append((url.split('/')[-1], pdf_path, html_path, html_filename))
        except Exception as e:
            log(f"[{len(files)+i+1}/{total}] 失败: {e}")
            results.append((url, None, None, f"❌ {e}"))

    # 汇总结果
    success = [r for r in results if r[2] is not None]
    fail = [r for r in results if r[2] is None]

    status = f"✅ 全部完成! 成功 {len(success)}/{total}"
    if fail:
        status += f"，失败 {len(fail)}"

    html_lines = ""
    for name, _, html_path, filename in success:
        html_lines += f"- **{name}**: [打开 {filename}](/file={html_path})\n"
    for name, _, _, error in fail:
        html_lines += f"- **{name}**: {error}\n"

    yield status, html_lines


# Gradio界面
with gr.Blocks(title="PaperPulse", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""<div style="display:flex;align-items:center;gap:12px;margin-bottom:8px">
<span style="font-size:2.5rem">🐻‍❄️</span>
<span style="font-family:Outfit,sans-serif;font-size:2rem;font-weight:700;color:#5a7a9a">PaperPulse</span>
<span style="font-family:'JetBrains Mono',monospace;font-size:0.75rem;color:#5a7a9a;margin-left:8px">A TOOL for PDF→HTML</span>
</div>
<span style="font-family:Outfit,sans-serif;font-size:1.25rem;color:#5a7a9a">把你的论文转换成HTML来阅读</span>""")

    with gr.Row(equal_height=True):
        with gr.Column(scale=1, min_width=320):
            pdf_input = gr.File(label="上传PDF（支持多选）", file_types=[".pdf"], file_count="multiple")
            url_input = gr.Textbox(label="论文URL（每行一个）", placeholder="https://arxiv.org/abs/xxx\nhttps://arxiv.org/abs/yyy", lines=3)
            submit_btn = gr.Button("生成解读", variant="primary", size="lg")

        with gr.Column(scale=1, min_width=320):
            status_output = gr.Textbox(label="处理状态", lines=8)
            html_link_output = gr.Markdown(label="结果")

    submit_btn.click(
        process_batch,
        [pdf_input, url_input],
        [status_output, html_link_output]
    )

    gr.Markdown("**示例URL**: `https://arxiv.org/abs/1706.03762` (Attention is All You Need)")


if __name__ == "__main__":
    print("=" * 50)
    print("PaperPulse Lite")
    print("=" * 50)
    print(f"HTML保存目录: {OUTPUTS_DIR}")
    print("=" * 50)
    demo.launch(server_port=7780, allowed_paths=[str(OUTPUTS_DIR)])
