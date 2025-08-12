FROM clickhouse/clickhouse-server:latest

# 复制初始化脚本
COPY init/ /docker-entrypoint-initdb.d/

# 创建自定义入口点脚本
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# 设置入口点
ENTRYPOINT ["/docker-entrypoint.sh"]