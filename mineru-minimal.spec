# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for MinerU Minimal (Basic + OCR Pipeline)
Supports: Windows and macOS
"""

import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules
import os

block_cipher = None

# Collect data files
datas = []

# Add mineru resources
datas += collect_data_files('mineru', include_py_files=False)
datas += [('mineru/resources', 'mineru/resources')]

# Add pytorchocr resources (REQUIRED for OCR)
datas += [('mineru/model/utils/pytorchocr/utils/resources', 'mineru/model/utils/pytorchocr/utils/resources')]

# Add magika data files (REQUIRED - models and config)
try:
    datas += collect_data_files('magika', include_py_files=False)
except:
    pass

# Add doclayout_yolo config files (REQUIRED for OCR)
try:
    datas += collect_data_files('doclayout_yolo', include_py_files=False)
except:
    pass

# Add ultralytics config files (REQUIRED for YOLO)
try:
    datas += collect_data_files('ultralytics', include_py_files=False)
except:
    pass

# Add fast_langdetect model files (REQUIRED for language detection)
try:
    datas += collect_data_files('fast_langdetect', include_py_files=False)
except:
    pass

# Add transformers/torch resources if they exist
try:
    datas += collect_data_files('transformers', include_py_files=False)
except:
    pass

try:
    datas += collect_data_files('torch', include_py_files=False)
except:
    pass

# Collect hidden imports
hiddenimports = [
    'mineru',
    'mineru.cli',
    'mineru.cli.client',
    'mineru.cli.common',
    'mineru.backend',
    'mineru.backend.pipeline',
    'mineru.backend.vlm',
    'mineru.utils',
    'mineru.data',
    'mineru.model',

    # Core dependencies
    'click',
    'loguru',
    'tqdm',
    'numpy',
    'PIL',
    'cv2',

    # PDF processing
    'pdfminer',
    'pypdfium2',
    'pypdf',
    'pdftext',

    # ML/OCR dependencies
    'torch',
    'torchvision',
    'transformers',
    'onnxruntime',
    'ultralytics',
    'doclayout_yolo',

    # Utilities
    'requests',
    'httpx',
    'bs4',
    'json_repair',
    'langdetect',
    'magika',
    'yaml',
    'omegaconf',
    'shapely',
    'pyclipper',
    'matplotlib',
    'skimage',

    # Model downloads
    'modelscope',
    'huggingface_hub',
]

# Collect all submodules for critical packages
hiddenimports += collect_submodules('mineru')
hiddenimports += collect_submodules('transformers')
hiddenimports += collect_submodules('torch')
hiddenimports += collect_submodules('onnxruntime')

# Exclude unnecessary modules to reduce size
excludes = [
    'tkinter',
    'matplotlib.tests',
    'numpy.tests',
    'pytest',
    'test',
    '_pytest',

    # Exclude VLM backends we don't need
    'sglang',
    'vllm',
    'mlx',
    'mlx_vlm',

    # Exclude API/Web UI
    'fastapi',
    'uvicorn',
    'gradio',
    'gradio_pdf',
]

a = Analysis(
    ['mineru_entry.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=['hook-transformers-doc.py'],
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
    name='mineru',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Enable UPX compression
    console=True,  # Keep console for CLI tool
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon path if you have one
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='mineru-build',
)
