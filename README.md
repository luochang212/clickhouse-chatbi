<div style="text-align: center;">
    <img src="https://pityboy.oss-cn-beijing.aliyuncs.com/ckbi.png" alt="LOGO" />
    <!-- <img src="./img/ckbi.png" alt="LOGO" /> -->
</div>

# CKBI

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Next.js](https://img.shields.io/badge/frontend-Next.js-black.svg)](https://nextjs.org/)
[![AI Agent](https://img.shields.io/badge/AI-Qwen%20Agent-purple.svg)](https://github.com/QwenLM/Qwen-Agent)
[![MCP](https://img.shields.io/badge/protocol-MCP-red.svg)](https://modelcontextprotocol.io/)
[![ClickHouse](https://img.shields.io/badge/database-ClickHouse-orange.svg)](https://clickhouse.com/)
[![Docker Compose](https://img.shields.io/badge/deployment-Docker%20Compose-2496ED.svg?logo=docker)](docker-compose.yml)

基于 [ClickHouse](https://github.com/ClickHouse/ClickHouse) 数据库的 ChatBI 应用。

![frontend-image](./img/webui-img.png)

你可以导入任何感兴趣的数据，以对话的方式探索数据。应用内预置了一个动漫数据库，如果不知道问什么，可以用预设的四个 Prompt 与之交互。

## 一、技术栈

- **前端**: `Next.js`（[模板](https://vercel.com/templates/ai/nextjs-ai-chatbot)）
- **后端**: `Qwen Agent`
- **数据库**: `ClickHouse`
- **MCP**: `mcp-clickhouse`
- **部署**: `docker compose`

## 二、特性

- **容器化部署**：docker compose 一键启停
- **OLAP 引擎**：内置 ClickHouse，支持千万级数据的高速查询
- **推理 Agent**：开启 ReAct 模式，Agent 具备更强的规划与工具调用能力
- **现代化前端**：基于深受 startup 们喜爱的 Next.js 框架开发

## 三、配置文件

docker compose 的环境变量在 `.env` 文件，按律不上传，其格式如下：

```env
# backend
CLICKHOUSE_HOST=clickhouse
CLICKHOUSE_PORT=8123
CLICKHOUSE_USER=admin
CLICKHOUSE_PASSWORD=[YOUR_CLICKHOUSE_PASSWORD]
CLICKHOUSE_DATABASE=entertainment
CLICKHOUSE_MCP_SERVER_TRANSPORT=sse
CLICKHOUSE_MCP_BIND_HOST=localhost
CLICKHOUSE_MCP_BIND_PORT=8760
CLICKHOUSE_SECURE=false
CLICKHOUSE_VERIFY=false
DASHSCOPE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
DASHSCOPE_API_KEY=[YOUR_DASHSCOPE_API_KEY]

# frontend
POSTGRES_USER=postgres
POSTGRES_PASSWORD=[YOUR_POSTGRES_PASSWORD]
POSTGRES_DB=nextjsdev
REDIS_PASSWORD=[YOUR_REDIS_PASSWORD]
AUTH_SECRET=[YOUR_AUTH_SECRET]
AUTH_URL=http://localhost:3000
POSTGRES_URL=postgres://postgres:[YOUR_POSTGRES_PASSWORD]@postgres:5432/nextjsdev
REDIS_URL=redis://:[YOUR_REDIS_PASSWORD]@redis:6379
DISABLE_SECURE_COOKIE=true
```

上述配置可能更新不及时，亦可参考 [.env.example](./.env.example) 中的配置。

> [!NOTE]
> 请前往 [阿里云百炼](https://www.aliyun.com/product/bailian) 申请 `DASHSCOPE_API_KEY`。

## 四、本地运行

**1）配置 `.env` 文件**

在当前路径下，创建并配置 `.env`：

```bash
# 1. 复制配置文件的格式
cp .env.example .env

# 2. 参考上一节，将你的环境变量填入 .env 文件
# vim .env
# ......
```

**2）启动 Docker**

这包括：

- 下载并启动 Docker Desktop
- 对于中国大陆用户，需要 [配置镜像源](https://luochang212.github.io/posts/chat_to_clickhouse/#1-%E9%85%8D%E7%BD%AE-docker-%E9%95%9C%E5%83%8F%E6%BA%90)

在 terminal 运行以下命令，确认 docker 的客户端和服务端均成功启动：

```bash
docker info
```

**3）启动服务**

> [!WARNING]
> 
> 对于 Windows 用户，若 `.sh` 文件为 CRLF 格式，需转换成 LF 格式，否则 docker compose 将无法正常启动。为处理这种情况，请在当前目录打开 PowerShell，执行转换程序：
> 
> ```powershell
> .\convert.ps1
> ```

在当前路径下运行以下命令，启动 docker compose：

```bash
docker compose up -d
```

上述命令将一次性拉起 ChatBI 服务依赖的 5 个容器：

- `nextjs-dev`：前端服务
- `mcp-openai-service`：MCP SSE 和 FastAPI 后端服务
- `clickhouse-dev`：ClickHouse 数据库
- `postgres-db`：Postgres 数据库（前端依赖）
- `redis-cache`：Redis 服务（前端依赖）

检查容器是否正常运行：

```bash
# 查看运行中的容器
docker ps

# 查看 nextjs-dev 容器日志
docker logs nextjs-dev -f
```

待前端初始化完成后，打开浏览器访问应用 [http://localhost:3000/](http://localhost:3000/)

> [!NOTE]
>
> 如以 guest 身份提问，应用无回复，请尝试清除浏览器 cookie 后重试。

如果你像我一样，导入了动漫数据集 [top-popular-anime](https://www.kaggle.com/datasets/tanishksharma9905/top-popular-anime)，可以这样提问：

- 所有动漫的平均评分是多少？
- ID 为 100 的动画的出品方是？
- 评分大于 9.0 的动画有多少？
- 评分人数最多的十部动漫是？
- 评分人数超过一万人的动画中，排名前 5 的是？
- 2023 年开始播出的动画有多少？
- 制作超过 15 部动漫的工作室有哪些？
- 2024 年开始播出的动画中，评分最高的是？

> [!NOTE]
> 囿于 GitHub 对文件大小的限制，本仓库只上传了动漫数据库的前一千行，作为样例。如果希望探索完整的动漫数据，从 [top-popular-anime](https://www.kaggle.com/datasets/tanishksharma9905/top-popular-anime) 下载 `popular_anime.csv` 文件，然后替换掉本仓库的 [./backend/init/data/popular_anime.csv](./backend/init/data/popular_anime.csv) 文件即可。

**4）关闭并删除容器**

在当前路径下执行：

```bash
# 删除所有容器
docker compose down

# 删除所有容器和卷
docker compose down -v

# 删除所有容器、卷和本地构建的镜像
docker compose down -v --rmi local

# 重新构建容器
docker compose build --no-cache
```

## 五、changelog

- [x] 开发 Qwen Agent 后端
- [x] 开发 MCP SSE
- [x] 开发 FastAPI
- [x] 开发 Next.js 前端
- [x] 开发 entrypoint 脚本
- [x] 开发 docker compose 启动脚本
