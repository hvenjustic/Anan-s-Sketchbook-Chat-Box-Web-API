#!/bin/bash

# PM2 应用重载脚本
# 用于重新加载 anan-chatbox-api 应用

APP_NAME="anan-chatbox-api"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 切换到脚本所在目录
cd "$SCRIPT_DIR" || exit 1

# 检查应用是否存在
if ! pm2 list | grep -q "$APP_NAME"; then
    echo -e "${YELLOW}应用 $APP_NAME 未运行，尝试启动...${NC}"
    pm2 start ecosystem.config.js
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}应用已启动${NC}"
        pm2 save
        exit 0
    else
        echo -e "${RED}启动失败${NC}"
        exit 1
    fi
fi

echo -e "${YELLOW}正在重新加载应用: $APP_NAME${NC}"

# 使用 reload 进行零停机重启（推荐）
pm2 reload "$APP_NAME"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ 应用重新加载成功${NC}"
    echo ""
    echo -e "${YELLOW}应用状态:${NC}"
    pm2 status "$APP_NAME"
    echo ""
    echo -e "${YELLOW}查看日志: pm2 logs $APP_NAME${NC}"
    echo -e "${YELLOW}查看详细信息: pm2 show $APP_NAME${NC}"
else
    echo -e "${RED}✗ 重新加载失败，尝试使用 restart${NC}"
    pm2 restart "$APP_NAME"
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ 应用重启成功${NC}"
    else
        echo -e "${RED}✗ 重启失败${NC}"
        exit 1
    fi
fi

# 保存 PM2 进程列表
pm2 save

