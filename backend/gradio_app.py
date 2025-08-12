# -*- coding: utf-8 -*-

"""
简单的 Agent
"""

import os

from dotenv import load_dotenv
from gradio_ui import create_ui
from qwen_agent.agents import Assistant


# 加载 .env 文件
load_dotenv()


# Qwen Agent 的 LLM 配置
LLM_CFG = {
    'model': 'deepseek-chat',  # deepseek-chat / deepseek-reasoner
    'model_server': os.getenv("DEEPSEEK_BASE_URL"),
    'api_key': os.getenv("DEEPSEEK_API_KEY")
}


def create_simple_bot(llm_cfg):
    agent = Assistant(
        llm=llm_cfg,
        name='SimpleBot',
        description='智能聊天机器人',
        system_message=""
    )

    return agent


my_bot = create_simple_bot(LLM_CFG)


def generate_response(message, history, max_history=6):
    if not message.strip():
        return message, history

    messages = [{'role': 'user', 'content': message}]

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
    model_name = LLM_CFG['model']
    demo = create_ui(llm_func=generate_response,
                     tab_name="Gradio APP - LLM",
                     main_title="Simple Agent Demo",
                     sub_title=f"{model_name}")
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        show_api=False
    )
