#!/bin/sh

# 启动 Next.js 初始化脚本

set -e

echo "=== Starting Next.js Service ==="

npm install -g pnpm
pnpm install

# 开发环境
# pnpm db:migrate
# pnpm dev

# 生产环境
pnpm build
pnpm start
