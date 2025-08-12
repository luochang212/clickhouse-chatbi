# -*- coding: utf-8 -*-

"""
带 WebUI 的 ClickHouse Agent

你可以问它：
- 所有动漫的平均评分是多少？
- ID 为 100 的动画的出品方是？
- 评分大于 9.0 的动画有多少？
- 评分人数最多的十部动漫是？
- 评分人数超过一万人的动画中，排名前 5 的是？
- 2023 年开始播出的动画有多少？
- 制作超过 15 部动漫的工作室有哪些？
"""

import os

from dotenv import load_dotenv
from gradio_ui import create_ui
from ch_agent import CHAgent


# 加载 .env 文件
load_dotenv()


# LLM 配置
# DashScope
DASHSCOPE_LLM_CFG = {
    'model': 'qwen3-coder-plus',  # qwen-plus / qwen-turbo
    'model_server': os.getenv("DASHSCOPE_BASE_URL"),
    'api_key': os.getenv("DASHSCOPE_API_KEY")
}

# DeepSeek
DEEPSEEK_LLM_CFG = {
    'model': 'deepseek-reasoner',  # deepseek-chat / deepseek-reasoner
    'model_server': os.getenv("DEEPSEEK_BASE_URL"),
    'api_key': os.getenv("DEEPSEEK_API_KEY")
}


# 数据库配置
DB_CONFIG = {
    "host": os.getenv("CLICKHOUSE_HOST"),
    "port": os.getenv("CLICKHOUSE_PORT"),
    "user": os.getenv("CLICKHOUSE_USER"),
    "password": os.getenv("CLICKHOUSE_PASSWORD"),
}


def create_react_agent(llm_cfg, db_config):
    cha = CHAgent(llm_cfg, db_config)
    react_agent = cha.create_react_agent()
    return react_agent


my_bot = create_react_agent(DASHSCOPE_LLM_CFG, DB_CONFIG)


def generate_response(message, history, max_history=6):
    if not message.strip():
        return message, history

    messages = [{
        'role': 'user',
        'content': message,
    }]

    # 保留最后 max_history 条历史记录
    messages = history[-max_history:] + messages

    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": ""})

    # 流式响应
    for chunk in my_bot.run(messages):
        content = chunk[-1].get("content", "")
        history[-1]["content"] = content
        yield "", history

    yield "", history


if __name__ == "__main__":
    model_name = DASHSCOPE_LLM_CFG['model']
    demo = create_ui(llm_func=generate_response,
                     tab_name="Gradio APP - ClickHouse Agent",
                     main_title="ClickHouse Agent Demo",
                     sub_title=f"{model_name}")
    demo.launch(
        server_name="0.0.0.0",
        server_port=7861,
        show_api=False
    )
