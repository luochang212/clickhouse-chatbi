# 启动 clickhouse sse 服务

使用以下命令启动 ClickHouse SSE 服务：

```bash
#!/bin/bash

# USAGE: pip install mcp-clickhouse
# TEST: curl http://localhost:8760/health

source .env
python -m mcp_clickhouse.main
```
