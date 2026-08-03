"""
Blockline EXE Builder Script
Build Blockline into a standalone executable with PyInstaller

Usage:
    1. Install PyInstaller: pip install pyinstaller
    2. Run this script: python build_exe.py
    3. Find the EXE in the 'dist' folder
"""

import os
import shutil
import subprocess
import sys

def build_exe():
    print("=" * 60)
    print("Building Blockline EXE - by domore100")
    print("=" * 60)
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print("✓ PyInstaller found")
    except ImportError:
        print("✗ PyInstaller not found!")
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller installed")
    
    # Check if logo exists
    logo_path = "logo.png"
    icon_path = "logo.ico"
    
    if not os.path.exists(logo_path):
        print(f"⚠ Warning: {logo_path} not found - building without logo")
        logo_path = None
    else:
        print(f"✓ Logo found: {logo_path}")
    
    # Create icon if needed (Windows)
    if logo_path and not os.path.exists(icon_path):
        try:
            from PIL import Image
            img = Image.open(logo_path)
            img.save(icon_path, format='ICO', sizes=[(256, 256)])
            print(f"✓ Created icon: {icon_path}")
        except Exception as e:
            print(f"⚠ Could not create icon: {e}")
            icon_path = None
    
    # Build PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",  # Single executable file
        "--windowed",  # No console window (for GUI apps)
        "--name=Blockline",
        "--clean",  # Clean build
    ]
    
    # Add icon if available
    if icon_path and os.path.exists(icon_path):
        cmd.append(f"--icon={icon_path}")
    
    # Add data files
    cmd.extend([
        "--add-data=languages;languages",  # Include all language blocks
        "--add-data=ui.py;.",
    ])
    
    # Add logo if exists
    if logo_path and os.path.exists(logo_path):
        cmd.append(f"--add-data={logo_path};.")
    
    # Add hidden imports
    cmd.extend([
        "--hidden-import=tkinter",
        "--hidden-import=tkinter.ttk",
        "--hidden-import=PIL",
        "--hidden-import=PIL.Image",
        "--hidden-import=PIL.ImageTk",
    ])
    
    # Main script
    cmd.append("main.py")
    
    print("\n" + "=" * 60)
    print("Running PyInstaller...")
    print("=" * 60)
    print("Command:", " ".join(cmd))
    print()
    
    try:
        subprocess.check_call(cmd)
        
        print("\n" + "=" * 60)
        print("✓ Build Complete!")
        print("=" * 60)
        print(f"Executable location: dist/Blockline.exe")
        print(f"Size: {os.path.getsize('dist/Blockline.exe') / (1024*1024):.1f} MB")
        print("\nYou can now distribute dist/Blockline.exe")
        print("Users don't need Python installed!")
        
    except subprocess.CalledProcessError as e:
        print("\n" + "=" * 60)
        print("✗ Build Failed!")
        print("=" * 60)
        print(f"Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    build_exe()