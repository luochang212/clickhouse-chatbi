#!/bin/sh

# 合并服务启动脚本 - MCP ClickHouse + OpenAI API

set -e

echo "=== Starting Combined Services (MCP ClickHouse + OpenAI API) ==="

# 环境变量已通过docker-compose传递，无需手动加载
# source .env

# 等待ClickHouse服务启动
echo "Waiting for ClickHouse service..."
retry_count=0
max_retries=30

while [ $retry_count -lt $max_retries ]; do
    if curl -s -u "${CLICKHOUSE_USER}:${CLICKHOUSE_PASSWORD}" "http://${CLICKHOUSE_HOST}:${CLICKHOUSE_PORT}/" > /dev/null 2>&1; then
        echo "ClickHouse service is ready"
        break
    fi
    echo "Waiting for ClickHouse service... ($((retry_count + 1))/$max_retries)"
    sleep 2
    retry_count=$((retry_count + 1))
    
    if [ $retry_count -eq $max_retries ]; then
        echo "Error: ClickHouse service startup timeout"
        exit 1
    fi
done

echo "🚀 Starting Combined Services:"
echo "📊 MCP ClickHouse Service on port 8760"
echo "🤖 OpenAI Compatible API Service on port 8001"
echo "📖 API Documentation: http://localhost:8001/docs"
echo "🔍 ReDoc Documentation: http://localhost:8001/redoc"
echo "💚 Health Check: http://localhost:8001/health"
echo "🤖 Model List: http://localhost:8001/v1/models"

# 启动supervisor来管理两个服务
exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf