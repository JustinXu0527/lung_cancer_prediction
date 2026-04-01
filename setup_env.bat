@echo off
REM 环境设置脚本

echo ========================================
echo 肺癌风险预测系统 - 环境设置
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ 未检测到Python安装
    echo 请确保Python已安装并添加到PATH
    pause
    exit /b 1
)

echo ✓ 检测到Python

REM 创建虚拟环境
echo.
echo 创建虚拟环境...
python -m venv venv

REM 激活虚拟环境
echo.
echo 激活虚拟环境...
call venv\Scripts\activate.bat

REM 升级pip
echo.
echo 升级pip...
python -m pip install --upgrade pip

REM 安装依赖
echo.
echo 安装项目依赖...
pip install -r requirements.txt

REM 训练模型
echo.
echo 训练模型...
python train_main.py

echo.
echo ========================================
echo ✓ 环境设置完成！
echo ========================================
echo.
echo 接下来，运行以下命令启动应用：
echo   run_app.bat
echo.
pause
