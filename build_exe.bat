@echo off
REM 肺癌风险预测系统 - EXE 打包完整指南
REM 此脚本将使用 PyInstaller 打包应用成独立的exe文件

echo.
echo ================================================================
echo 肺癌风险预测系统 - PyInstaller EXE 打包指南
echo ================================================================
echo.

REM 进入项目目录
cd /d "%~dp0"

echo [说明] 本脚本将使用 PyInstaller 打包应用为 EXE 文件
echo [步骤1] 确保依赖已安装...
echo.

REM 检查必要的文件和目录
if not exist "data" (
    echo ✗ 错误: data 目录不存在
    goto error
)

if not exist "models" (
    echo ✗ 错误: models 目录不存在
    goto error
)

if not exist "app\app.py" (
    echo ✗ 错误: app\app.py 文件不存在
    goto error
)

echo ✓ 所有必要的文件和目录都存在
echo.

REM 检查Python版本
python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ 错误: 未检测到Python安装
    echo 请确保Python已安装并添加到PATH环境变量
    goto error
)

echo ✓ Python 已安装
echo.

REM 清理之前的构建
echo [步骤2] 清理之前的构建文件...
if exist "dist" (
    rmdir /s /q dist >nul 2>&1
    echo ✓ 删除了 dist 目录
)
if exist "build" (
    rmdir /s /q build >nul 2>&1
    echo ✓ 删除了 build 目录
)
if exist "*.spec" (
    del /q *.spec >nul 2>&1
    echo ✓ 删除了 spec 文件
)
echo.

REM 安装PyInstaller
echo [步骤3] 检查 PyInstaller...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo 安装 PyInstaller...
    pip install PyInstaller -q
    echo ✓ PyInstaller 已安装
) else (
    echo ✓ PyInstaller 已安装
)
echo.

REM 开始打包
echo [步骤4] 运行 PyInstaller 打包...
echo.
echo 这可能需要几分钟，请耐心等待...
echo.

REM PyInstaller 命令
python -m PyInstaller ^
    --name "肺癌预测系统" ^
    --onedir ^
    --windowed ^
    --add-data "data;data" ^
    --add-data "models;models" ^
    --hidden-import=streamlit ^
    --collect-all=streamlit ^
    --collect-all=altair ^
    app/app.py

if errorlevel 1 (
    echo.
    echo ✗ 打包失败，请检查错误信息
    goto error
)

echo.
echo ================================================================
echo ✓ 打包成功！
echo ================================================================
echo.

echo 输出文件位置：
echo   dist\肺癌预测系统\
echo.

echo 应用文件：
echo   dist\肺癌预测系统\肺癌预测系统.exe
echo.

echo 接下来，您可以：
echo.
echo 1. 进入 dist\肺癌预测系统\ 目录
echo 2. 双击 肺癌预测系统.exe 运行应用
echo.

echo ================================================================
echo 🎉 打包完成！
echo ================================================================
echo.

pause
exit /b 0

:error
echo.
echo [错误处理]...
echo.
pause
exit /b 1
