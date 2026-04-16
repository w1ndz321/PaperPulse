# HTML生成器 - Markdown转HTML（Jinja2 + Tailwind）
import markdown
from pathlib import Path
from datetime import datetime
import uuid
from jinja2 import Environment, FileSystemLoader

TEMPLATES_DIR = Path(__file__).parent / "templates"
OUTPUTS_DIR = Path(__file__).parent / "outputs"

OUTPUTS_DIR.mkdir(exist_ok=True)

env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))


def extract_title(md_text: str) -> str:
    """从Markdown中提取标题"""
    lines = md_text.strip().split('\n')
    for line in lines:
        if line.startswith('# '):
            return line[2:].strip()
    return "论文解读"


def generate_html(md_text: str) -> str:
    """将Markdown转为HTML，生成网页文件"""
    # Markdown转HTML
    html_content = markdown.markdown(
        md_text,
        extensions=['tables', 'fenced_code']
    )

    # 提取标题
    title = extract_title(md_text)

    # 渲染模板
    template = env.get_template("summary.html")
    html = template.render(
        title=title,
        content=html_content,
        date=datetime.now().strftime("%Y-%m-%d")
    )

    # 保存文件
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"summary_{timestamp}_{uuid.uuid4().hex[:6]}.html"
    filepath = OUTPUTS_DIR / filename
    filepath.write_text(html, encoding="utf-8")

    print(f"[INFO] HTML已保存: {filepath}")
    return str(filepath), filename