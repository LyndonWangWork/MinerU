# MinerU Executable Build Guide

本指南说明如何将MinerU打包成独立的可执行文件（exe/app），适用于Windows和macOS系统。

## 📦 打包版本说明

### 包含功能
- ✅ PDF转Markdown核心功能
- ✅ 图片解析 (PNG, JPG, JPEG, WEBP, GIF, BMP, TIFF)
- ✅ OCR文本识别 (Pipeline后端)
- ✅ 多语言支持 (37种语言)
- ✅ 表格识别
- ✅ 公式识别 (LaTeX)
- ✅ 布局分析
- ✅ 命令行界面

### 不包含功能
- ❌ VLM后端 (transformers, vllm, mlx)
- ❌ API服务 (fastapi)
- ❌ Web界面 (gradio)
- ❌ GPU加速推理

### 预计大小
- **Windows x64**: ~1.5-2.5 GB
- **macOS x64 (Intel)**: ~1.5-2.5 GB
- **macOS ARM64 (Apple Silicon)**: ~1.5-2.5 GB

---

## 🚀 使用GitHub Actions自动构建

### 方法1: 推送版本标签触发（推荐）

```bash
# 创建并推送版本标签
git tag v1.0.0
git push origin v1.0.0
```

### 方法2: 手动触发

1. 访问你的GitHub仓库
2. 点击 `Actions` 选项卡
3. 选择 `Build MinerU Executable` workflow
4. 点击 `Run workflow` 按钮
5. 输入版本号（可选），点击运行

### 下载构建产物

构建完成后：
1. 进入 `Actions` 页面
2. 选择对应的workflow运行记录
3. 在 `Artifacts` 区域下载：
   - `mineru-windows-x64.zip` (Windows 64位)
   - `mineru-macos-x64.tar.gz` (macOS Intel芯片)
   - `mineru-macos-arm64.tar.gz` (macOS Apple Silicon/M1/M2/M3)

如果是标签触发，还会自动创建GitHub Release（草稿状态），可以发布正式版本。

**macOS用户注意**: 请根据你的Mac芯片类型选择对应版本：
- Intel芯片Mac (2020年及之前): 下载 `mineru-macos-x64.tar.gz`
- Apple Silicon Mac (M1/M2/M3): 下载 `mineru-macos-arm64.tar.gz`

可以通过以下命令查看芯片类型：
```bash
uname -m
# x86_64 = Intel
# arm64 = Apple Silicon
```

---

## 🛠️ 本地手动构建

### 前置要求

#### Windows
- Python 3.10-3.13
- Git
- UPX (可选，用于压缩)

#### macOS (Intel & Apple Silicon)
- Python 3.10-3.13
- Xcode Command Line Tools: `xcode-select --install`
- UPX (可选，用于压缩): `brew install upx`

**注意**:
- 在 Intel Mac 上构建会生成 x64 版本
- 在 Apple Silicon Mac (M1/M2/M3) 上构建会生成 ARM64 版本
- PyInstaller 会自动检测并使用当前架构

### 构建步骤

#### 1. 安装依赖

```bash
# 升级pip
python -m pip install --upgrade pip

# 安装构建工具
pip install pyinstaller

# 安装MinerU依赖（精简版）
pip install -r requirements-minimal.txt

# 安装MinerU本身
pip install -e .
```

#### 2. 验证安装

```bash
# 检查版本
mineru --version

# 测试基本功能
python -c "import mineru; print('MinerU installed successfully')"
```

#### 3. 运行PyInstaller

```bash
# 使用spec文件构建
pyinstaller mineru-minimal.spec --clean --noconfirm
```

构建过程可能需要10-30分钟，取决于机器性能。

#### 4. 验证构建结果

```bash
# Windows
dist\mineru-build\mineru.exe --version

# macOS/Linux
./dist/mineru-build/mineru --version
```

#### 5. 测试功能

```bash
# Windows
dist\mineru-build\mineru.exe -p test.pdf -o output

# macOS/Linux
./dist/mineru-build/mineru -p test.pdf -o output
```

---

## 📝 配置文件说明

### 1. `requirements-minimal.txt`

精简版依赖列表，包含：
- 基础依赖 (click, loguru, numpy, pillow等)
- PDF处理 (pdfminer, pypdfium2, pypdf)
- Pipeline OCR (torch, transformers, onnxruntime, ultralytics)

**不包含**:
- VLM后端 (sglang, vllm, mlx-vlm)
- API/Web (fastapi, gradio)
- 云服务 (boto3)

### 2. `mineru-minimal.spec`

PyInstaller配置文件，定义：
- **入口点**: `mineru/cli/client.py`
- **数据文件**: `mineru/resources/*`
- **隐藏导入**: torch, transformers等动态导入的模块
- **排除模块**: tkinter, tests, VLM后端等
- **压缩**: 启用UPX压缩

### 3. `.github/workflows/build-exe.yml`

GitHub Actions工作流，包含：
- **触发条件**: 版本标签推送或手动触发
- **构建矩阵**: Windows x64 + macOS Intel (x64) + macOS Apple Silicon (ARM64)
- **Runner配置**:
  - `macos-13`: Intel x64 架构
  - `macos-14`: Apple Silicon ARM64 架构 (M1/M2/M3)
- **构建步骤**:
  1. 设置Python环境
  2. 安装系统依赖 (UPX)
  3. 安装Python依赖
  4. 运行PyInstaller（自动检测架构）
  5. 创建压缩包
  6. 计算SHA256校验和
  7. 上传artifacts
  8. 创建Release (标签触发时)

---

## 🎯 使用打包后的可执行文件

### 解压

```bash
# Windows
Expand-Archive -Path mineru-windows-x64.zip -DestinationPath ./mineru

# macOS Intel (x64)
tar -xzf mineru-macos-x64.tar.gz

# macOS Apple Silicon (ARM64)
tar -xzf mineru-macos-arm64.tar.gz
```

### 运行

```bash
# Windows
cd mineru-build
mineru.exe --help
mineru.exe -p document.pdf -o output

# macOS
cd mineru-build
./mineru --help
./mineru -p document.pdf -o output
```

### 首次运行

首次运行时，MinerU会自动下载所需的模型文件（约1-2GB），请确保：
- 有稳定的网络连接
- 有足够的磁盘空间（至少5GB可用）

可以提前下载模型：

```bash
# Windows
mineru.exe models-download

# macOS
./mineru models-download
```

---

## 🔧 自定义构建

### 调整打包内容

编辑 `mineru-minimal.spec`:

```python
# 添加更多隐藏导入
hiddenimports += [
    'your_module_here',
]

# 排除额外模块
excludes += [
    'module_to_exclude',
]

# 添加数据文件
datas += [
    ('path/to/data', 'destination/path'),
]
```

### 减小exe体积

1. **禁用UPX** (如果压缩导致问题):
   ```python
   upx=False
   ```

2. **排除更多模块**:
   ```python
   excludes += ['scipy', 'pandas', 'IPython']
   ```

3. **使用单文件模式** (启动慢但方便分发):
   ```python
   exe = EXE(
       pyz,
       a.scripts,
       a.binaries,  # 包含二进制文件
       a.zipfiles,
       a.datas,
       [],
       name='mineru',
       debug=False,
       bootloader_ignore_signals=False,
       strip=False,
       upx=True,
       upx_exclude=[],
       runtime_tmpdir=None,
       console=True,
   )
   # 删除COLLECT部分
   ```

### 添加图标

```python
exe = EXE(
    # ...
    icon='path/to/icon.ico',  # Windows: .ico, macOS: .icns
)
```

---

## 🐛 常见问题

### 1. 构建失败: "Module not found"

**原因**: 缺少隐藏导入

**解决**: 在 `mineru-minimal.spec` 的 `hiddenimports` 列表中添加缺失的模块

```python
hiddenimports += ['missing_module']
```

### 2. 运行时错误: "No module named 'xxx'"

**原因**: PyInstaller未检测到动态导入

**解决**: 使用 `--hidden-import` 参数或在spec文件中添加

```bash
pyinstaller mineru-minimal.spec --hidden-import=module_name
```

### 3. exe体积过大

**方案**:
- 检查是否包含了不必要的依赖（查看build日志）
- 使用 `excludes` 排除大型但非必需的库
- 确保UPX已正确安装并启用

### 4. macOS运行时提示"无法验证开发者"

**解决**:
```bash
# 移除quarantine属性
xattr -cr mineru-build

# 或允许来自任何来源（不推荐）
sudo spctl --master-disable

# 推荐方式：给执行权限并允许运行
chmod +x mineru-build/mineru
# 首次运行时在"系统偏好设置 → 安全性与隐私"中点击"仍要打开"
```

### 5. Windows Defender误报

**原因**: PyInstaller打包的exe可能被误判为可疑文件

**解决**:
- 添加例外: Windows Security → Virus & threat protection → Exclusions
- 签名exe (需要代码签名证书)

### 6. 模型下载失败

**原因**: 网络问题或镜像源不可用

**解决**:
```bash
# 使用ModelScope镜像（国内更快）
mineru --model-source modelscope -p test.pdf -o output

# 或手动下载模型后指定本地路径
export MINERU_MODEL_SOURCE=local
```

### 7. macOS ARM64 架构不匹配错误

**症状**: 在 Apple Silicon Mac 上运行 x64 版本时出现 "Bad CPU type in executable" 错误

**原因**: 下载了错误的架构版本

**解决**:
```bash
# 检查当前系统架构
uname -m
# arm64 = Apple Silicon，需要下载 mineru-macos-arm64.tar.gz
# x86_64 = Intel，需要下载 mineru-macos-x64.tar.gz

# 或使用 Rosetta 2 运行 x64 版本（不推荐，性能较差）
arch -x86_64 ./mineru --version
```

### 8. PyTorch/ONNX Runtime ARM64 兼容性问题

**症状**: 在 ARM64 Mac 上构建时提示某些库不支持 ARM64

**解决**:
```bash
# 确保使用最新版本的依赖（requirements-minimal.txt 已包含兼容版本）
# PyTorch 2.0+ 和 ONNX Runtime 1.17+ 都已支持 ARM64

# 如果遇到问题，可以强制安装 ARM64 版本
pip install --force-reinstall torch torchvision onnxruntime
```

---

## 📊 性能优化建议

### 1. 使用本地模型缓存

模型默认下载到：
- **Windows**: `%USERPROFILE%\.cache\mineru`
- **macOS**: `~/.cache/mineru`

可以预先下载并打包到exe目录：

```bash
mineru-models-download --output ./models
# 然后在spec文件中添加:
datas += [('models', 'models')]
```

### 2. 多核并行处理

```bash
# 使用多个进程处理多个PDF
mineru -p folder_with_pdfs -o output
```

### 3. 内存优化

对于大型PDF，可以分页处理：

```bash
# 只处理前10页
mineru -p large.pdf -o output --start 0 --end 9

# 处理第11-20页
mineru -p large.pdf -o output --start 10 --end 19
```

---

## 📦 分发建议

### 1. 包含README

在分发包中添加简单的README：
- 系统要求
- 使用说明
- 模型下载说明
- 问题反馈渠道

### 2. 校验和验证

提供SHA256校验和文件，用户可验证完整性：

```bash
# Windows
certutil -hashfile mineru-windows-x64.zip SHA256

# macOS
shasum -a 256 mineru-macos-x64.tar.gz
```

### 3. 版本管理

在文件名中包含版本号和架构：
```
mineru-v1.0.0-windows-x64.zip
mineru-v1.0.0-macos-x64.tar.gz
mineru-v1.0.0-macos-arm64.tar.gz
```

---

## 🔗 相关链接

- [MinerU GitHub](https://github.com/opendatalab/MinerU)
- [MinerU 文档](https://opendatalab.github.io/MinerU/)
- [PyInstaller 文档](https://pyinstaller.org/)
- [问题反馈](https://github.com/opendatalab/MinerU/issues)

---

## 📄 许可证

MinerU使用AGPL-3.0许可证，打包的可执行文件也应遵守相同许可证条款。

---

**注意**: 此打包方案为社区贡献，非官方支持。如遇问题，请先在Issues中搜索或提问。
