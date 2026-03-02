# main.spec

block_cipher = None

a = Analysis(
    ['src/main.py'],          # entry point
    pathex=['src'],           # include entire src/ directory
    binaries=[],
    datas=[],
    hiddenimports=[],
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
