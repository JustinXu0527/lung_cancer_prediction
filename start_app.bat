@echo off
REM 肺癌风险预测系统 - 一键启动脚本
REM 此脚本会自动设置环境并启动应用

echo.
echo ========================================
echo 肺癌风险预测系统 v1.0
echo ========================================
echo.

REM 获取当前目录
set CURRENT_DIR=%~dp0

REM 检查虚拟环境
if not exist "%CURRENT_DIR%venv" (
    echo [1/3] 创建虚拟环境...
    call D:\Anaconda3\python.exe -m venv venv
    echo ✓ 虚拟环境已创建
    echo.
)

REM 激活虚拟环境
echo [2/3] 激活虚拟环境...
call venv\Scripts\activate.bat
echo ✓ 虚拟环境已激活
echo.

REM 安装依赖（如果需要）
echo [3/3] 检查依赖...
pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo 首次运行，正在安装依赖包...
    pip install streamlit pandas numpy scikit-learn xgboost matplotlib seaborn -q
    echo ✓ 依赖包已安装
)
echo ✓ 依赖检查完毕
echo.

REM 启动应用
echo ========================================
echo 启动Streamlit应用...
echo ========================================
echo.
echo 应用地址: http://localhost:8501
echo.
echo 按 Ctrl+C 停止运行
echo.

cd app
streamlit run app.py --logger.level=error

pause
