# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec文件 - 肺癌预测应用
避免matplotlib ctypes问题
"""

block_cipher = None

a = Analysis(
    ['run_streamlit.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('data', 'data'),
        ('models', 'models'),
    ],
    hiddenimports=[
        'sklearn',
        'xgboost',
        'streamlit',
        'streamlit.cli',
        'pandas',
        'numpy',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],  # 禁用所有runtime hooks来避免matplotlib ctypes问题
    excludedimports=[
        'matplotlib',  # 排除matplotlib
        'tkinter',     # 排除tkinter
    ],
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
    name='LungCancerApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='LungCancerApp',
)
