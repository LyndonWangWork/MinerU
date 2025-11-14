# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for MinerU Basic (No OCR - Testing Only)
For quick build testing without heavy dependencies
"""

block_cipher = None

# Minimal data files
datas = [
    ('mineru/resources', 'mineru/resources'),
]

# Minimal hidden imports
hiddenimports = [
    'mineru',
    'mineru.cli',
    'mineru.cli.client',
    'mineru.cli.common',
    'mineru.utils',
    'mineru.data',
    'click',
    'loguru',
    'tqdm',
    'numpy',
    'PIL',
    'pdfminer',
    'pypdfium2',
    'pypdf',
]

# Exclude heavy dependencies for testing
excludes = [
    'torch',
    'transformers',
    'ultralytics',
    'tkinter',
    'matplotlib',
    'scipy',
    'pandas',
    'test',
    'unittest',
]

a = Analysis(
    ['mineru/cli/client.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='mineru-basic',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # Disable UPX for faster test build
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
    name='mineru-basic',
)
