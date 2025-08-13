#!/bin/sh

# 启动 ClickHouse 服务并执行初始化脚本

set -e

echo "=== Starting ClickHouse Service ==="

# 启动 ClickHouse 服务器
/entrypoint.sh &
CLICKHOUSE_PID=$!

echo "Waiting for ClickHouse service to start..."
sleep 10

# 检查服务是否启动成功
retry_count=0
max_retries=30

while [ $retry_count -lt $max_retries ]; do
    if clickhouse-client --host localhost \
        --port 9000 \
        --user ${CLICKHOUSE_USER} \
        --password ${CLICKHOUSE_PASSWORD} \
        --query "SELECT 1" > /dev/null 2>&1; then
        echo "ClickHouse service started successfully"
        break
    fi
    echo "Waiting for ClickHouse service to start... ($((retry_count + 1))/$max_retries)"
    sleep 2
    retry_count=$((retry_count + 1))

    if [ $retry_count -eq $max_retries ]; then
        echo "Error: ClickHouse service startup timeout"
        exit 1
    fi
done

# 执行初始化脚本
if [ -f "/docker-entrypoint-initdb.d/init-clickhouse.sh" ]; then
    echo "Executing initialization script..."
    bash /docker-entrypoint-initdb.d/init-clickhouse.sh
else
    echo "Initialization script not found, skipping initialization"
fi

echo "Initialization completed, ClickHouse service is running..."

# 等待主进程
wait $CLICKHOUSE_PID