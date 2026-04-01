#!/bin/bash

# 肺癌风险预测系统 - 一键启动脚本（Mac/Linux）

echo ""
echo "========================================"
echo "肺癌风险预测系统 v1.0"
echo "========================================"
echo ""

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 检查虚拟环境
if [ ! -d "$SCRIPT_DIR/venv" ]; then
    echo "[1/3] 创建虚拟环境..."
    python3 -m venv venv
    echo "✓ 虚拟环境已创建"
    echo ""
fi

# 激活虚拟环境
echo "[2/3] 激活虚拟环境..."
source venv/bin/activate
echo "✓ 虚拟环境已激活"
echo ""

# 安装依赖（如果需要）
echo "[3/3] 检查依赖..."
pip show streamlit > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "首次运行，正在安装依赖包..."
    pip install -r requirements.txt -q
    echo "✓ 依赖包已安装"
else
    echo "✓ 依赖检查完毕"
fi
echo ""

# 启动应用
echo "========================================"
echo "启动Streamlit应用..."
echo "========================================"
echo ""
echo "应用地址: http://localhost:8501"
echo ""
echo "按 Ctrl+C 停止运行"
echo ""

cd app
streamlit run app.py --logger.level=error

read -p "按 Enter 键关闭..."
