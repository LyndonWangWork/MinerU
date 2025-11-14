"""
PyInstaller hook for PyTorch
Ensures all DLLs and dependencies are properly collected on Windows
"""

from PyInstaller.utils.hooks import collect_dynamic_libs, collect_data_files, get_package_paths
import os

# Get torch package path
_, torch_path = get_package_paths('torch')

# Collect all torch binaries
binaries = collect_dynamic_libs('torch')

# On Windows, explicitly add torch/lib directory which contains c10.dll and other DLLs
if os.name == 'nt':  # Windows
    torch_lib_path = os.path.join(torch_path, 'lib')
    if os.path.exists(torch_lib_path):
        for file in os.listdir(torch_lib_path):
            if file.endswith(('.dll', '.pyd')):
                src = os.path.join(torch_lib_path, file)
                # Place in torch/lib to match original structure
                binaries.append((src, 'torch/lib'))

# Collect torch data files (might be needed)
datas = collect_data_files('torch', include_py_files=False)

# Hidden imports
hiddenimports = [
    'torch',
    'torch.jit',
    'torch.nn',
    'torch.optim',
    'torch._C',
    'torch._VF',
]
