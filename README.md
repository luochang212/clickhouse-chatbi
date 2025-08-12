# clickhouse-chatbi

一个可以访问 [ClickHouse](https://github.com/ClickHouse/ClickHouse) 的、带 WebUI 的 ChatBI。

## 一、技术栈

- **前端**: `Next.js`
- **后端**: `Qwen Agent`
- **数据库**: `ClickHouse`
- **MCP**: `mcp-clickhouse`
- **部署**: `docker compose`

## 二、配置文件

docker compose 的环境变量在 `.env` 文件，按律不上传。 

具体配置参考 [.env.example](./.env.example) 文件。

> [!NOTE]
> 密码可以随意配置，但请注意一致性，比如 `POSTGRES_URL` 中的密码 需要和 `POSTGRES_PASSWORD` 保持一致。`DEEPSEEK_API_KEY` 不是必要的，仅作为备选，如不需要可注释掉此配置。`DASHSCOPE_API_KEY` 是必要的，请前往 [阿里云百炼](https://www.aliyun.com/product/bailian) 平台申请。

## 三、本地运行

**1）配置 `.env` 文件**

在当前路径下

```bash
# 1. 复制配置格式
cp .env.example .env

# 2. 参考上一节，编辑 .env 文件中的环境变量
# vim .env
# ...
```

**2）启动 Docker**

这包括：

- 启动 Docker Desktop
- 中国大陆需配置 Docker 镜像 `registry-mirrors`

**3）启动服务**

> **⚠️ Windows 用户注意事项**
> 
> 请检查 `.sh` 文件是否是 CRLF 格式。如是，需转换为 LF 格式，否则可能导致 docker compose 启动失败，打开 PowerShell 执行：
> 
> ```powershell
> .\convert.ps1
> ```
> 
> 该脚本将本目录下所有 `.sh` 文件的行结束符转换为 LF 格式。

然后在当前路径运行：

```bash
docker compose up -d
```

上述命令将拉起 ChatBI 服务依赖的 5 个容器：

- `nextjs-dev`
- `mcp-openai-service`
- `clickhouse-dev`
- `postgres-db`
- `redis-cache`

检查容器是否正常运行：

```bash
# 查看运行中的容器
docker ps

# 查看 nextjs-dev 容器日志
docker logs nextjs-dev -f
```

启动后，打开浏览器访问 [http://localhost:3000/](http://localhost:3000/)

由于我们使用的是 `Next.js` 的开发模式 (`pnpm dev`)，第一次启动通常需要一点时间。等待编译完成后，即可访问。

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
> 囿于 GitHub 仓库上传文件的限制，我并未上传完整的动漫数据集，而是用 [sample.sh](./backend/init/data/sample.sh) 脚本取前一千行作为样例数据，随代码上传。如果你希望访问完整的动漫数据集，需要下载 [top-popular-anime](https://www.kaggle.com/datasets/tanishksharma9905/top-popular-anime) 的 `popular_anime.csv` 文件，替代当前一千行版本的 [./backend/init/data/popular_anime.csv](./backend/init/data/popular_anime.csv) 文件。

**4）关闭并删除容器**

> [!WARNING]
> 执行此步骤将删除所有相关容器和卷，包括数据库中的数据。请确保已备份重要数据。

在当前路径下执行：

```bash
# 删除所有容器
docker compose down

# 删除所有容器和卷
docker compose down -v
```
