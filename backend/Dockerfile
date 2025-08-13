# https://hub.docker.com/r/clickhouse/clickhouse-server/

FROM clickhouse/clickhouse-server:25.7

# 复制初始化脚本
COPY init/ /docker-entrypoint-initdb.d/

# 创建自定义入口点脚本
COPY docker-entrypoint.sh /custom-entrypoint.sh
RUN apt-get update && apt-get install -y dos2unix && dos2unix /custom-entrypoint.sh
RUN chmod +x /custom-entrypoint.sh

# 设置入口点
ENTRYPOINT ["/custom-entrypoint.sh"]
