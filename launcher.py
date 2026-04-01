#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
肺癌风险预测系统启动器
直接使用Streamlit CLI启动应用
"""

import subprocess
import sys
import os

if __name__ == '__main__':
    # 获取项目根目录
    # 注：在PyInstaller打包后，__file__会指向exe所在目录
    try:
        exe_dir = os.path.dirname(sys.executable)
    except:
        exe_dir = os.getcwd()
    
    # 构建app.py的路径
    # 假设项目结构在./_internal/app目录下
    app_file = os.path.join(os.path.dirname(__file__), '..', '..', 'app', 'app.py')
    app_file = os.path.abspath(app_file)
    
    # 如果文件不存在，尝试其他路径
    if not os.path.exists(app_file):
        # 尝试相对于当前工作目录
        app_file = os.path.join(os.getcwd(), 'app', 'app.py')
    
    if not os.path.exists(app_file):
        # 尝试绝对路径
        app_file = r'c:\Users\HUAWEI\Desktop\新建文件夹\lung-cancer-prediction\app\app.py'
    
    # 检查文件是否存在
    if os.path.exists(app_file):
        print(f"[INFO] 启动应用: {app_file}")
        # 运行streamlit
        subprocess.run([sys.executable, '-m', 'streamlit', 'run', app_file])
    else:
        print(f"[ERROR] 找不到应用文件: {app_file}")
        print(f"[ERROR] 当前目录: {os.getcwd()}")
        print(f"[ERROR] sys.executable: {sys.executable}")
        input("按任意键退出...")
        sys.exit(1)
