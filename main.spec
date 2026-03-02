# main.spec

from PyInstaller.utils.hooks import collect_submodules, collect_dynamic_libs

block_cipher = None

# Add all dependencies your project actually uses.
DEPENDENCIES = [
    "psutil",
    "pygame",
    "numpy",
]

hiddenimports = []
binaries = []

# Collect submodules + dynamic libraries for each dependency.
for dep in DEPENDENCIES:
    hiddenimports += collect_submodules(dep)
    binaries += collect_dynamic_libs(dep)

# Exclude Python's internal test modules (these contain invalid encodings).
EXCLUDED_MODULES = [
    "test",
    "tkinter.test",
    "distutils.tests",
    "lib2to3.tests",
    "unittest.test",
]

hiddenimports = [
    m for m in hiddenimports
    if not any(m.startswith(ex) for ex in EXCLUDED_MODULES)
]

a = Analysis(
    ['src/main.py'],          # Entry point
    pathex=['src'],           # Include your entire src/ directory
    binaries=binaries,
    datas=[],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=EXCLUDED_MODULES,
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
