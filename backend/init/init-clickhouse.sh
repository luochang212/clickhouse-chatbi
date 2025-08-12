#!/bin/bash

# ClickHouse 初始化脚本

set -e

echo "=== ClickHouse initialization started ==="

# 将文件复制到指定目录下
cp /docker-entrypoint-initdb.d/data/popular_anime.csv /var/lib/clickhouse/user_files/

# 检查是否存在数据文件
if [ -f "/var/lib/clickhouse/user_files/popular_anime.csv" ]; then
    echo "Data file found, starting data import..."
    clickhouse-client --host localhost \
        --port 9000 \
        --user ${CLICKHOUSE_USER:-admin} \
        --password ${CLICKHOUSE_PASSWORD} \
        --multiquery < /docker-entrypoint-initdb.d/init-database.sql
    echo "Data import completed"
else
    echo "Warning: popular_anime.csv file not found"
fi

echo "=== ClickHouse initialization completed ==="