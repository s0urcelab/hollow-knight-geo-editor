import os
import subprocess
import sys

def check_python_version():
    version = sys.version_info
    if version.major == 3 and version.minor >= 11:
        print("Error: PyInstaller is not fully compatible with Python 3.11+")
        print("Please use Python 3.9 or 3.10 to build the executable")
        return False
    return True

def build_exe():
    # 检查 Python 版本
    if not check_python_version():
        return

    # 确保在正确的目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # 检查必要文件是否存在
    required_files = ['editor.py', 'i18n.py', 'utils.py']
    missing_files = [f for f in required_files if not os.path.exists(f)]
    if missing_files:
        print(f"Error: Missing required files: {', '.join(missing_files)}")
        return
    
    # 构建命令
    cmd = [
        'pyinstaller',
        '--noconfirm',
        'build.spec'
    ]
    
    # 执行构建
    try:
        subprocess.run(cmd, check=True)
        print("\nBuild completed! The executable can be found in the 'dist' folder.")
    except subprocess.CalledProcessError as e:
        print(f"\nBuild failed with error: {e}")
        print("\nPlease make sure all required files are present in the directory.")

if __name__ == '__main__':
    build_exe() 