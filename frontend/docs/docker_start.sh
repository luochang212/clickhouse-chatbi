# 启动集群
docker compose up -d

# 删除集群
# docker compose down --volumes
docker compose down -v

# 显示当前活跃的容器
docker ps

# 进入 nextjs-dev 容器
docker exec -it nextjs-dev sh

# 测试 redis 是否运行
docker exec -it redis-cache redis-cli -a [REDIS_PASSWORD] ping

# 测试 postgres 是否运行
docker exec -it postgres-db psql -U postgres -d nextjsdev