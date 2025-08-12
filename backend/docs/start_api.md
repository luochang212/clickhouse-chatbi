# 启动 OpenAI API 服务

## 1. 启动 ClickHouse 容器

先按 start_docker.md 中的方法，启动 ClickHouse 容器。

## 2. 启动 ClickHouse SSE 服务

```bash
nohup bash -c "source .env && python -m mcp_clickhouse.main" > ./log/mcp_clickhouse.log 2>&1 &
```

## 3. 启动 Gradio 应用

按 start_app.md 中的方法，启动 Gradio 应用，以检查 ClickHouse SSE 是否成功启动。

```bash
python gradio_ch_agent.py
```

## 4. 启动 OpenAI API 服务

```bash
nohup python openai_api.py > ./log/openai_api.log 2>&1 &
```

## 3. 检查 OpenAI API 服务是否成功启动

```bash
ps -ef | grep -E "mcp_clickhouse|openai_api" | grep -v grep
```