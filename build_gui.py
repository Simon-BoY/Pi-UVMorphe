#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Build Pi-Morphe GUI executable (Optimized for size)
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path


def clean_build():
    """Clean build directories"""
    print("Cleaning old build files...")
    for dir_name in ['dist', 'build']:
        dir_path = Path(dir_name)
        if dir_path.exists():
            shutil.rmtree(dir_path)
            print(f"  ✓ Deleted {dir_path}")

    for file in Path('.').glob('*.spec'):
        file.unlink()
        print(f"  ✓ Deleted {file}")


def build_gui():
    """Build GUI executable"""
    print("=" * 60)
    print("Pi-Morphe GUI Builder (Size Optimized)")
    print("=" * 60)

    # Clean previous builds
    clean_build()

    # Check dependencies
    try:
        import PyInstaller
        print("✓ PyInstaller installed")
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'], check=True)

    # Base build command
    # Base build command
    cmd = [
        'pyinstaller',
        '--name', 'PiMorphe',
        '--onedir',
        '--windowed',
        '--clean',
        '--noconfirm',

        # 1. 排除真正无关且不被依赖的大型第三方库
        '--exclude-module', 'PyQt6',
        '--exclude-module', 'PyQt6.sip',
        '--exclude-module', 'PyQt6.QtCore',
        '--exclude-module', 'PyQt6.QtGui',
        '--exclude-module', 'PyQt6.QtWidgets',
        # '--exclude-module', 'matplotlib',
        # '--exclude-module', 'tkinter',
        '--exclude-module', 'notebook',
        # '--exclude-module', 'nbconvert',
        # '--exclude-module', 'nbformat',
        # '--exclude-module', 'triton',
        # ⚠️ 【重要修改】：删除了 '--exclude-module', 'scipy'

        # Data files
        '--add-data', f'best_model.pth{os.pathsep}.',
        '--add-data', f'scaler0424.pkl{os.pathsep}.',
        '--add-data', f'gui{os.pathsep}gui',

        # 2. 显式告知 PyInstaller 包含的核心库
        '--hidden-import', 'PyQt5',
        '--hidden-import', 'torch',
        '--hidden-import', 'torch._C',
        '--hidden-import', 'torchvision',
        '--hidden-import', 'numpy',
        '--hidden-import', 'pandas',
        '--hidden-import', 'matplotlib',
        '--hidden-import', 'tkinter',
        '--hidden-import', 'nbconvert',
        '--hidden-import', 'nbformat',
        '--hidden-import', 'triton',
        '--hidden-import', 'scipy',  # 👈 确保隐式导入 scipy
        '--hidden-import', 'plotly',
        '--hidden-import', 'sklearn',
        '--hidden-import', 'pyteomics',
        '--hidden-import', 'tqdm',

        # 3. 自动收集运行时需要的二进制动态链接库
        '--collect-binaries', 'torch',
        '--collect-binaries', 'scipy',  # 👈 确保抓取 scipy 的二进制底层 dll

        'run_gui.py'
    ]

    # Add icon if it exists
    icon_path = Path('resources/icon.ico')
    if icon_path.exists():
        cmd.extend(['--icon', str(icon_path)])

    print("\nRunning build command...")
    print(" ".join(cmd))
    print()

    try:
        subprocess.run(cmd, check=True)
        print("\n" + "=" * 60)
        print("✅ Build completed successfully!")
        print(f"   Output Directory: {Path('dist') / 'PiMorphe'}")
        print(f"   Executable: {Path('dist') / 'PiMorphe' / 'PiMorphe.exe'}")
        print("=" * 60)


    except subprocess.CalledProcessError as e:
        print(f"\n❌ Build failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    build_gui()