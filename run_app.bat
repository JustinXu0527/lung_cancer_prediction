@echo off
REM 肺癌风险预测应用启动脚本

echo ========================================
echo 肺癌风险预测系统 v1.0
echo ========================================
echo.

REM 检查虚拟环境
if exist venv (
    echo ✓ 虚拟环境已存在
    call venv\Scripts\activate.bat
) else (
    echo ✗ 虚拟环境不存在，请先运行 setup_env.bat
    pause
    exit /b 1
)

echo.
echo 启动Streamlit应用...
echo.

cd app
streamlit run app.py

pause
