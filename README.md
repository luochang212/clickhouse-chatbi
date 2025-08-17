# CKBI

基于 [ClickHouse](https://github.com/ClickHouse/ClickHouse) 数据库的 ChatBI 应用。

![frontend-image](./img/webui-img.png)

你可以导入任何感兴趣的数据，以对话的方式探索数据。应用内预置了一个动漫数据库，如果不知道问什么，可以用预设的四个 Prompt 与之交互。

## 一、技术栈

- **前端**: `Next.js`（[模版](https://vercel.com/templates/ai/nextjs-ai-chatbot)）
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
CLICKHOUSE_PORT=18123
CLICKHOUSE_USER=admin
CLICKHOUSE_PASSWORD=[YOUR_CLICKHOUSE_PASSWORD]
CLICKHOUSE_DATABASE=entertainment
CLICKHOUSE_MCP_SERVER_TRANSPORT=sse
CLICKHOUSE_MCP_BIND_HOST=0.0.0.0
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

上述配置有可能更新不及时，亦可参考 [.env.example](./.env.example) 文件中的配置。

> [!NOTE]
> 密码可以随意设置，但请注意一致性，比如 `POSTGRES_URL` 中的密码需要和 `POSTGRES_PASSWORD` 保持一致。`DEEPSEEK_API_KEY` 不是必要的，仅作为备选，如不需要可注释此配置。`DASHSCOPE_API_KEY` 是必要的，请前往 [阿里云百炼](https://www.aliyun.com/product/bailian) 平台申请。

## 四、本地运行

**1）配置 `.env` 文件**

在当前路径下，按以下方法配置 `.env`：

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
- 对于中国大陆，需要 [配置镜像源](https://luochang212.github.io/posts/chat_to_clickhouse/#1-%E9%85%8D%E7%BD%AE-docker-%E9%95%9C%E5%83%8F%E6%BA%90)

**3）启动服务**

> [!NOTE]
> 
> **Windows 用户注意事项**
> 
> Windows 用户需检查 `.sh` 文件是否是 CRLF 格式。如是，需转换为 LF 格式，否则可能导致 docker compose 启动失败，在当前目录下打开 PowerShell 执行：
> 
> ```powershell
> .\convert.ps1
> ```
> 
> 该脚本将本目录下所有 `.sh` 文件的行结束符转换为 LF 格式。

在当前路径运行：

```bash
docker compose up -d
```

上述命令将一次性拉起 ChatBI 服务所依赖的 5 个容器：

- `nextjs-dev`：前端服务
- `mcp-openai-service`：MCP SSE 与 FastAPI 后端
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

启动后，打开浏览器访问 [http://localhost:3000/](http://localhost:3000/)

由于我们使用的是 `Next.js` 的开发模式 (`pnpm dev`)，第一次启动通常需要一点时间。等待编译完成后，即可访问。如以 guest 模式多次访问遭遇对话失败，可能是 cookie 残留导致，需清除浏览器缓存后重试。

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
> 囿于 GitHub 对文件大小的限制，的动漫数据集只上传了前一千行。如果你希望探索完整数据，请下载 [top-popular-anime](https://www.kaggle.com/datasets/tanishksharma9905/top-popular-anime) 的 `popular_anime.csv` 文件，并替换 [./backend/init/data/popular_anime.csv](./backend/init/data/popular_anime.csv) 文件。

**4）关闭并删除容器**

> [!WARNING]
> 执行此步骤将删除所有相关容器和卷，包括数据库中的数据。请确保已备份重要数据。

在当前路径下执行：

```bash
# 删除所有容器
docker compose down

# 删除所有容器和卷
docker compose down -v

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
