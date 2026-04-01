# 禁用matplotlib的mplconfig runtime hook以避免ctypes问题
from PyInstaller.utils.hooks import collect_submodules

hiddenimports = []
