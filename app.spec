# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Lung Cancer Prediction App
用于将Streamlit应用打包成exe可执行文件
"""

import sys
import os
from PyInstaller.utils.hooks import collect_all

block_cipher = None

# 收集动态导入的模块
hiddenimports = [
    'streamlit',
    'sklearn',
    'xgboost',
    'pandas',
    'numpy',
    'matplotlib',
    'seaborn'
]

# 为hiddenimports添加更多依赖
datas = [
    ('data', 'data'),           # 复制data目录
    ('models', 'models'),       # 复制models目录
    ('app', 'app'),             # 复制app目录
]

a = Analysis(
    ['app/app.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='肺癌预测系统',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 不显示命令行窗口
    disable_windowed_traceback=False,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='LungCancerPredictionApp',
)
