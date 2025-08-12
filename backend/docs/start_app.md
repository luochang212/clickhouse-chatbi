# 启动 Gradio 应用

1）一个 Chat APP，无法连接数据库

```bash
nohup python gradio_app.py > ./log/gradio_app.log 2>&1 &
```

2）一个简单的 ChatBI，可以连接 ClickHouse 数据库

```bash
nohup python gradio_ch_agent.py > ./log/gradio_ch_agent.log 2>&1 &
```