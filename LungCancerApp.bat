@echo off
REM ================================================================
REM 肺癌风险预测系统 v1.0
REM Lung Cancer Risk Prediction System
REM ================================================================
REM 这是应用的主启动脚本
REM 使用虚拟环境中的Python运行Streamlit应用
REM ================================================================

setlocal enabledelayedexpansion

REM 获取脚本所在目录
set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%

echo.
echo ================================================================
echo 肺癌风险预测系统启动中...
echo Initializing Lung Cancer Prediction System...
echo ================================================================
echo.

REM 检查虚拟环境是否存在
if not exist "!PROJECT_ROOT!venv\" (
    echo [ERROR] 虚拟环境不存在！
    echo 请运行 setup_env.bat 来创建虚拟环境。
    echo.
    pause
    exit /b 1
)

REM 检查app.py是否存在
if not exist "!PROJECT_ROOT!app\app.py" (
    echo [ERROR] 应用文件不存在！
    echo 预期位置: !PROJECT_ROOT!app\app.py
    echo.
    pause
    exit /b 1
)

REM 检查数据文件
if not exist "!PROJECT_ROOT!data" (
    echo [WARNING] 数据目录不存在！
    mkdir "!PROJECT_ROOT!data"
)

REM 检查模型文件
if not exist "!PROJECT_ROOT!models" (
    echo [WARNING] 模型目录不存在！
    mkdir "!PROJECT_ROOT!models"
)

REM 改变到项目目录
cd /d "!PROJECT_ROOT!"

REM 激活虚拟环境
echo [INFO] 激活Python虚拟环境...
call venv\Scripts\activate.bat

if errorlevel 1 (
    echo [ERROR] 无法激活虚拟环境！
    pause
    exit /b 1
)

echo [INFO] 虚拟环境已激活
echo [INFO] 启动Streamlit应用...
echo [INFO] 应用地址: http://localhost:8501
echo.
echo ================================================================
echo 按 Ctrl+C 停止应用
echo ================================================================
echo.

REM 启动Streamlit应用
python -m streamlit run app\app.py --logger.level=error

echo.
echo.
echo 应用已关闭。
pause
