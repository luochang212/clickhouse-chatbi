#!/bin/sh

# 启动 Next.js 初始化脚本

set -e

echo "=== Starting Next.js Service ==="

# 安装 Python 和构建工具（用于编译 bufferutil）
apk update && apk add --no-cache python3 py3-pip make g++

npm install -g pnpm
pnpm install

# 开发环境
# pnpm db:migrate
# pnpm dev

# 生产环境
pnpm build
pnpm start
