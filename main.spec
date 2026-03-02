# main.spec

from PyInstaller.utils.hooks import collect_submodules, collect_dynamic_libs
import pkgutil
import sys

block_cipher = None

# Collect ALL installed modules
all_hiddenimports = []
all_binaries = []

for module in pkgutil.iter_modules():
    name = module.name
    try:
        all_hiddenimports += collect_submodules(name)
        all_binaries += collect_dynamic_libs(name)
    except Exception:
        pass  # Some modules may not have dynamic libs or submodules

a = Analysis(
    ['src/main.py'],          # entry point
    pathex=['src'],           # include entire src/ directory
    binaries=all_binaries,
    datas=[],
    hiddenimports=all_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='tower-defense',
    console=True,
)
