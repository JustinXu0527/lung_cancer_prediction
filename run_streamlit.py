#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
肺癌风险预测系统启动脚本
绕过streamlit版本检查的兼容性问题
"""

import sys
import os

# 禁用streamlit的版本检查
os.environ['STREAMLIT_SERVER_HEADLESS'] = 'false'

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(__file__))

# 修补streamlit的版本获取函数
import importlib.metadata as metadata
import builtins

_original_getattr = builtins.getattr

def patched_version(package_name):
    """获取包版本的修补函数"""
    try:
        return metadata.version(package_name)
    except Exception:
        # 如果无法获取版本，返回默认值
        if package_name == 'streamlit':
            return '1.28.0'
        return '1.0.0'

# 替换版本获取函数
if hasattr(metadata, 'version'):
    original_version = metadata.version
    metadata.version = patched_version

# 现在导入streamlit
import streamlit as st

# 恢复原始版本函数
if 'original_version' in locals():
    metadata.version = original_version

# 导入应用
if __name__ == '__main__':
    # 获取应用文件路径
    app_dir = os.path.dirname(__file__)
    app_file = os.path.join(app_dir, 'app', 'app.py')
    
    # 使用streamlit运行应用
    from streamlit.cli import main
    sys.argv = ["streamlit", "run", app_file]
    main()
