from openai import OpenAI
from ..config import settings


def _call(prompt: str) -> str:
    if not settings.openai_api_key:
        return "[Mock Output]\n" + prompt[:400]
    client = OpenAI(api_key=settings.openai_api_key)
    res = client.responses.create(model=settings.openai_model, input=prompt)
    return res.output_text


def trend_agent(topic: str, platform: str) -> str:
    return _call(f"趋势分析: {platform} / {topic}")


def content_agent(topic: str, platform: str, trend: str, count: int) -> str:
    return _call(f"生成{count}篇 {platform} 内容，主题{topic}，参考{trend[:1000]}")


def rewrite_agent(platform: str, content: str) -> str:
    return _call(f"优化改写 {platform} 内容: {content[:2000]}")


def evaluator_agent(content: str) -> str:
    return _call(f"对内容评分并给出TOP3: {content[:2000]}")
