# MinerU EXE 打包 - 快速开始

这是一个快速指南，帮助你在5分钟内开始打包MinerU可执行文件。

## 🚀 三种打包方式

### 方式1: 使用GitHub Actions (推荐)

**优点**: 无需本地配置，云端自动构建，支持多平台
**适合**: 想要发布正式版本的场景

```bash
# 1. 创建版本标签
git tag v1.0.0

# 2. 推送到GitHub
git push origin v1.0.0

# 3. 等待5-15分钟，在Actions页面查看进度

# 4. 下载构建好的exe
#    访问: https://github.com/你的用户名/MinerU/actions
#    下载: mineru-windows-x64.zip 或 mineru-macos-x64.tar.gz
```

### 方式2: 使用自动化脚本 (最简单)

**优点**: 一键构建，自动检查依赖
**适合**: 本地快速测试

```bash
# 运行构建脚本
python build_local.py

# 或包含测试
python build_local.py --test

# 完成后在 dist/mineru/ 找到可执行文件
```

### 方式3: 手动构建 (完全控制)

**优点**: 完全控制构建过程
**适合**: 需要自定义配置的场景

```bash
# 1. 安装构建工具
pip install pyinstaller

# 2. 安装依赖
pip install -r requirements-minimal.txt
pip install -e .

# 3. 构建
pyinstaller mineru-minimal.spec --clean

# 4. 测试
./dist/mineru/mineru --version
```

---

## 📁 项目文件说明

```
MinerU/
├── requirements-minimal.txt      # 精简版依赖（基础+OCR）
├── mineru-minimal.spec           # PyInstaller配置文件
├── build_local.py                # 自动化构建脚本
├── BUILD_EXE.md                  # 详细构建文档
├── QUICK_START_BUILD.md          # 本文件
└── .github/workflows/
    └── build-exe.yml             # GitHub Actions配置
```

---

## 🎯 快速对比

| 特性 | GitHub Actions | 自动化脚本 | 手动构建 |
|------|---------------|-----------|---------|
| 难度 | ⭐ 简单 | ⭐⭐ 较简单 | ⭐⭐⭐ 中等 |
| 时间 | 10-15分钟 | 10-20分钟 | 15-30分钟 |
| 本地配置 | 不需要 | 最小化 | 需要 |
| 多平台 | ✅ 自动 | ❌ 手动切换 | ❌ 手动切换 |
| 自定义 | ⚠️ 修改workflow | ✅ 修改spec | ✅ 完全控制 |
| 适用场景 | 发布版本 | 本地测试 | 调试/定制 |

---

## ⚡ 最快路径

### 只想试试看 → 方式2 (自动化脚本)
```bash
git clone https://github.com/opendatalab/MinerU.git
cd MinerU
python build_local.py
```

### 要发布正式版 → 方式1 (GitHub Actions)
```bash
git tag v1.0.0
git push origin v1.0.0
# 访问 GitHub Actions 下载
```

### 需要自定义 → 方式3 (手动构建)
```bash
# 编辑 mineru-minimal.spec
# 然后运行
pyinstaller mineru-minimal.spec
```

---

## 📊 构建产物

成功后你会得到：

```
dist/mineru/               # 可执行文件目录
├── mineru.exe            # Windows可执行文件
│   或 mineru             # macOS/Linux可执行文件
├── _internal/            # 依赖库和资源
└── ...

mineru-windows-x64.zip    # 分发包 (如果使用脚本)
mineru-windows-x64.zip.sha256  # 校验和
```

**大小预期**: 1.5-2.5 GB（包含OCR模型）

---

## 🔥 常见问题速查

### Q: 构建失败，提示"Module not found"
```bash
# 检查是否安装了所有依赖
pip install -r requirements-minimal.txt
pip install -e .
```

### Q: exe太大，如何减小？
编辑 `mineru-minimal.spec`，排除不需要的模块：
```python
excludes += ['scipy', 'pandas', 'IPython']
```

### Q: macOS提示无法验证开发者
```bash
xattr -cr dist/mineru
```

### Q: Windows Defender误报
添加例外：设置 → 病毒和威胁防护 → 排除项

### Q: 想包含VLM后端？
使用完整依赖：
```bash
pip install -e ".[all]"
# 然后修改 spec 文件移除 VLM excludes
```

---

## 📖 详细文档

- **完整构建指南**: [BUILD_EXE.md](BUILD_EXE.md)
- **MinerU文档**: https://opendatalab.github.io/MinerU/
- **问题反馈**: https://github.com/opendatalab/MinerU/issues

---

## 🎯 下一步

1. ✅ **选择构建方式** (推荐: 自动化脚本)
2. ✅ **运行构建**
3. ✅ **测试可执行文件**
   ```bash
   # 测试版本
   ./dist/mineru/mineru --version

   # 测试功能
   ./dist/mineru/mineru -p test.pdf -o output
   ```
4. ✅ **分发给用户**

---

## 💡 提示

- 首次构建会下载大量依赖，需要较长时间
- 确保有至少 **10GB** 可用磁盘空间
- 网络不稳定时，使用国内镜像：
  ```bash
  pip install -r requirements-minimal.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
  ```
- 构建完成后，记得测试所有核心功能

---

**开始构建**:
```bash
python build_local.py
```

祝你构建顺利！ 🚀
