"""
PyInstaller 打包脚本
将Streamlit应用打包成可执行exe文件
"""

import subprocess
import os
import shutil
import sys

def build_exe():
    """
    使用PyInstaller打包应用
    """
    print("="*70)
    print(" 🫁 肺癌风险预测系统 - PyInstaller打包")
    print("="*70)
    print()
    
    # 检查必要的目录和文件
    if not os.path.exists('data'):
        print("❌ 'data' 目录不存在")
        return False
    
    if not os.path.exists('models'):
        print("❌ 'models' 目录不存在")
        return False
    
    if not os.path.exists('app/app.py'):
        print("❌ 'app/app.py' 文件不存在")
        return False
    
    print("✓ 所有必要文件和目录检查完毕\n")
    
    # 清理之前的构建
    print("清理之前的构建文件...")
    for dir_name in ['dist', 'build']:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"  ✓ 删除 {dir_name} 目录")
    
    # 删除旧的spec文件
    if os.path.exists('LungCancerApp.spec'):
        os.remove('LungCancerApp.spec')
    
    print()
    print("使用PyInstaller打包应用...")
    print()
    
    # PyInstaller命令
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--name', '肺癌预测系统',
        '--onefile',
        '--windowed',
        '--add-data', 'data;data',
        '--add-data', 'models;models',
        '--hidden-import=streamlit',
        '--hidden-import=sklearn',
        '--hidden-import=xgboost',
        '--hidden-import=pandas',
        '--hidden-import=matplotlib',
        '--hidden-import=seaborn',
        '--collect-all=streamlit',
        '--icon=INFOICON',  # 使用默认icon
        'app/app.py'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ 打包成功!")
            print()
            print("="*70)
            print("🎉 打包完成！")
            print("="*70)
            print()
            print("输出文件位置：")
            print("  dist/肺癌预测系统.exe")
            print()
            print("接下来，您可以：")
            print("1. 双击运行 dist/肺癌预测系统.exe")
            print("2. 将exe文件分享给他人（需要附加data和models文件夹）")
            print()
            print("="*70)
            return True
        else:
            print("❌ 打包失败!")
            print("\n错误信息:")
            print(result.stderr)
            return False
    
    except Exception as e:
        print(f"❌ 打包过程出错: {e}")
        return False


if __name__ == '__main__':
    success = build_exe()
    sys.exit(0 if success else 1)
