# 大模型调用
import os
from openai import OpenAI
from dotenv import load_dotenv

from prompts import build_prompt

load_dotenv()

client = OpenAI(
    base_url=os.getenv("OPENAI_BASE_URL"),
    api_key=os.getenv("OPENAI_API_KEY")
)
MODEL = os.getenv("MODEL_NAME", "gpt-4o-mini")


def summarize_stream(text: str):
    """流式调用大模型，yield返回每个chunk，同时在终端打印"""
    system_prompt, user_prompt = build_prompt(text)

    stream = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.1,
        stream=True
    )

    full_content = ""
    print("\n" + "=" * 50)
    print("LLM输出:")
    print("=" * 50)

    for chunk in stream:
        # 安全检查：确保chunk有choices且有内容
        if chunk.choices and len(chunk.choices) > 0:
            delta = chunk.choices[0].delta
            if delta and delta.content:
                content = delta.content
                full_content += content
                # 终端实时打印
                print(content, end="", flush=True)
                yield full_content

    print("\n" + "=" * 50)

    # 最终清理（如果被代码块包裹）
    if full_content.startswith("```markdown"):
        full_content = full_content.split("```markdown")[1]
        if "```" in full_content:
            full_content = full_content.split("```")[0]
    elif full_content.startswith("```"):
        full_content = full_content.split("```")[1]
        if "```" in full_content:
            full_content = full_content.split("```")[0]

    yield full_content.strip()


def summarize(text: str) -> str:
    """非流式调用，返回完整结果"""
    system_prompt, user_prompt = build_prompt(text)

    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.1
    )

    content = resp.choices[0].message.content.strip()

    # 如果被代码块包裹，提取出来
    if content.startswith("```markdown"):
        content = content.split("```markdown")[1].split("```")[0]
    elif content.startswith("```"):
        content = content.split("```")[1].split("```")[0]

    return content.strip()