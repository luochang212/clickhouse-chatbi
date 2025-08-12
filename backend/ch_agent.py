# -*- coding: utf-8 -*-

"""
ClickHouse Agent
"""

from qwen_agent.agents import Assistant, ReActChat


SYSTEM_PROMPT = """
你是一个数据库查询助手，专门帮助用户查询和分析 ClickHouse 数据库中的数据。

规则：
1. 始终确保 SQL 查询的安全性，避免修改数据
2. 以清晰易懂的方式呈现查询结果
"""


class CHAgent:
    """ClickHouse Agent"""

    def __init__(self, llm_cfg, db_config=None):
        self.llm_cfg = llm_cfg

        # ClickHouse 数据库配置
        self.db_config = db_config

    def create_tools(self):
        """获取工具列表"""
        import os

        # 根据环境变量动态配置MCP服务地址
        mcp_host = os.getenv("CLICKHOUSE_MCP_BIND_HOST", "localhost")
        mcp_port = os.getenv("CLICKHOUSE_MCP_BIND_PORT", "8760")
        mcp_url = f"http://{mcp_host}:{mcp_port}/sse"

        tools = [
            {
                "mcpServers": {
                    "mcp-clickhouse": {
                        "url": mcp_url
                    }
                }
            },
        ]

        return tools

    def create_react_agent(self):
        """创建 ReActChat 模式的 Agent"""
        tools = self.create_tools()
        return ReActChat(
            llm=self.llm_cfg,
            name='ClickHouse 数据库助手',
            description='ReActChat 模式',
            system_message=SYSTEM_PROMPT,
            function_list=tools,
        )

    def create_assistant_agent(self):
        """创建 Assistant 模式的 Agent"""
        tools = self.create_tools()
        return Assistant(
            llm=self.llm_cfg,
            name='ClickHouse 数据库助手',
            description='Assistant 模式',
            system_message=SYSTEM_PROMPT,
            function_list=tools,
        )

    def ask(self, bot, messages: list) -> str:
        """使用指定的 bot 进行查询"""
        response = bot.run_nonstream(messages)
        message = response[-1].get('content').strip()
        return message


if __name__ == '__main__':
    import os
    from dotenv import load_dotenv

    # 加载 .env 文件
    load_dotenv()

    # llm 配置
    llm_cfg = {
        'model': 'deepseek-chat',
        'model_server': os.getenv("DEEPSEEK_BASE_URL"),
        'api_key': os.getenv("DEEPSEEK_API_KEY")
    }

    # 数据库配置
    db_config = {
        "host": os.getenv("CLICKHOUSE_HOST"),
        "port": os.getenv("CLICKHOUSE_PORT"),
        "user": os.getenv("CLICKHOUSE_USER"),
        "password": os.getenv("CLICKHOUSE_PASSWORD"),
    }

    # 实例化 CHAgent
    cha = CHAgent(llm_cfg, db_config)

    # 创建一个 Agent
    react_agent = cha.create_react_agent()
    # assistant_agent = cha.create_assistant_agent()

    # 使用 Agent 查询数据库
    query = "咱们都有哪些表，表里都有啥字段"
    messages = [
        {
            'role': 'user',
            'content': query
        }
    ]
    answer = cha.ask(react_agent, messages)
    print(answer)
