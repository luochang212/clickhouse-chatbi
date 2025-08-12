# chat-to-clickhouse

一个可以访问 [ClickHouse](https://github.com/ClickHouse/ClickHouse) 的、带 WebUI 的 Agent。

## 一、技术栈

- **前端**: `Gradio`
- **后端**: `Qwen Agent`
- **数据库**: `ClickHouse`
- **MCP**: `mcp-clickhouse`

## 二、配置文件

LLM 和 数据库 的配置在 `.env` 文件中，按律不上传。

它的格式如下：

```
CLICKHOUSE_HOST=localhost
CLICKHOUSE_PORT=18123
CLICKHOUSE_USER=admin
CLICKHOUSE_PASSWORD=[YOUR_CLICKHOUSE_PASSWORD]
CLICKHOUSE_DATABASE=entertainment
CLICKHOUSE_MCP_SERVER_TRANSPORT=sse
CLICKHOUSE_MCP_BIND_HOST=0.0.0.0
CLICKHOUSE_MCP_BIND_PORT=8760
CLICKHOUSE_SECURE=false
CLICKHOUSE_VERIFY=false
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_API_KEY=[YOUR_DEEPSEEK_API_KEY]
DASHSCOPE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
DASHSCOPE_API_KEY=[YOUR_DASHSCOPE_API_KEY]
```

> **Note:** 请在项目根目录下创建 `.env` 文件

## 三、本地运行

> [!NOTE]
> 运行前，需要先安装 ClickHouse 数据库，然后导入可供查询的数据。这些步骤可以参考[《耶是 ClickHouse！我们有救了！！》](https://mp.weixin.qq.com/s/MO0l_bQ2ET_FnerLrFtUEA)，里面有详细记录。完成这些步骤之后，记得把配置信息写入 `.env`，以便 Agent 访问这些信息。

启动 Gradio：

```bash
python gradio_ch_agent.py
```

启动后，打开浏览器访问 [http://localhost:7860/](http://localhost:7860/)

如果你像我一样，导入了动漫数据集 [top-popular-anime](https://www.kaggle.com/datasets/tanishksharma9905/top-popular-anime)，可以这么提问：

- 所有动漫的平均评分是多少？
- ID 为 100 的动画的出品方是？
- 评分大于 9.0 的动画有多少？
- 评分人数最多的十部动漫是？
- 评分人数超过一万人的动画中，排名前 5 的是？
- 2023 年开始播出的动画有多少？
- 制作超过 15 部动漫的工作室有哪些？

## 四、MCP 启动方式

本仓库默认通过 `stdio` 的方式启动。如您想通过 `sse` 的方式启动 MCP Server：

**1）启动 SSE 服务**

安装 `mcp-clickhouse` 包：

```bash
pip install mcp-clickhouse
```

启动 MCP Server：

```bash
source .env && python -m mcp_clickhouse.main
```

验证服务是否正常启动：

```bash
curl http://localhost:8760/health
```

**2）修改 Agent 代码**

请将 [ch_agent.py](./ch_agent.py) 中的 `create_tools` 函数，用以下代码替换：

```python
    def create_tools(self):
        """获取工具列表"""

        tools = [
            {
                "mcpServers": {
                    "mcp-clickhouse": {
                        "url": "http://localhost:8760/sse"
                    }
                }
            },
        ]

        return tools
```
