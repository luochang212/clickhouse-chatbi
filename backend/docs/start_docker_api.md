# Docker 容器化部署 OpenAI API 服务

本文档介绍如何使用 Docker 容器化部署 ClickHouse ChatBI 的 OpenAI 兼容 API 服务。

## 架构说明

容器化部署包含三个主要服务：

1. **clickhouse** - ClickHouse 数据库服务
   - 端口：18123 (HTTP), 19000 (Native)
   - 容器名：clickhouse-dev

2. **mcp-clickhouse** - MCP ClickHouse 服务
   - 端口：8760
   - 容器名：mcp-clickhouse
   - 提供 ClickHouse 数据库的 MCP 协议接口

3. **openai-api** - OpenAI 兼容 API 服务
   - 端口：8001
   - 容器名：openai-api-service
   - 提供标准的 OpenAI API 接口

## 快速启动

### 1. 准备环境

确保已安装 Docker 和 Docker Compose：

```bash
docker --version
docker-compose --version
```

### 2. 配置环境变量

确保 `.env` 文件存在并包含必要的配置：

```bash
CLICKHOUSE_HOST=localhost
CLICKHOUSE_PORT=18123
CLICKHOUSE_USER=admin
CLICKHOUSE_PASSWORD=your_password
CLICKHOUSE_DATABASE=entertainment
CLICKHOUSE_MCP_SERVER_TRANSPORT=sse
CLICKHOUSE_MCP_BIND_HOST=0.0.0.0
CLICKHOUSE_MCP_BIND_PORT=8760
CLICKHOUSE_SECURE=false
CLICKHOUSE_VERIFY=false
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_API_KEY=your_deepseek_key
DASHSCOPE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
DASHSCOPE_API_KEY=your_dashscope_key
```

### 3. 一键启动所有服务

```bash
./docker-start.sh
```

或者手动启动：

```bash
# 构建并启动所有服务
docker-compose up --build -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

## 服务验证

### 1. 检查服务状态

```bash
# 检查所有容器状态
docker-compose ps

# 检查 ClickHouse
curl -u admin:your_password "http://localhost:18123/"

# 检查 MCP 服务
curl "http://localhost:8760/health"

# 检查 OpenAI API 服务
curl "http://localhost:8001/health"
```

### 2. 测试 API 功能

```bash
# 获取模型列表
curl "http://localhost:8001/v1/models"

# 测试聊天完成
curl -X POST "http://localhost:8001/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "clickhouse-agent",
    "messages": [
      {"role": "user", "content": "你好，请介绍一下你的功能"}
    ],
    "stream": false
  }'
```

## 访问地址

- **API 文档**: http://localhost:8001/docs
- **ReDoc 文档**: http://localhost:8001/redoc
- **健康检查**: http://localhost:8001/health
- **模型列表**: http://localhost:8001/v1/models
- **聊天完成**: http://localhost:8001/v1/chat/completions

## 日志查看

```bash
# 查看所有服务日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f openai-api
docker-compose logs -f mcp-clickhouse
docker-compose logs -f clickhouse

# 查看本地日志文件
tail -f log/openai_api.log
tail -f log/mcp_clickhouse.log
```

## 服务管理

```bash
# 停止所有服务
docker-compose down

# 重启特定服务
docker-compose restart openai-api

# 重新构建并启动
docker-compose up --build -d

# 查看资源使用情况
docker stats
```

## 故障排除

### 1. 容器启动失败

```bash
# 查看容器日志
docker-compose logs [service_name]

# 检查容器状态
docker-compose ps

# 重新构建镜像
docker-compose build --no-cache
```

### 2. 服务连接问题

- 确保所有服务都在同一个 Docker 网络中
- 检查环境变量配置是否正确
- 验证端口映射是否冲突

### 3. API 响应异常

- 检查 MCP 服务是否正常运行
- 验证 ClickHouse 数据库连接
- 查看 API 服务日志

## 生产环境部署建议

1. **安全配置**
   - 修改默认密码
   - 限制 CORS 允许的域名
   - 使用 HTTPS

2. **性能优化**
   - 调整容器资源限制
   - 配置日志轮转
   - 使用外部数据库

3. **监控告警**
   - 添加健康检查
   - 配置日志收集
   - 设置性能监控

## 文件说明

- `docker-compose.yml` - Docker Compose 配置文件
- `Dockerfile.api` - OpenAI API 服务的 Dockerfile
- `docker-entrypoint-api.sh` - API 服务启动脚本
- `docker-start.sh` - 一键启动脚本
- `requirements.txt` - Python 依赖列表