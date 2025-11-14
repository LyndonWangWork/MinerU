# MinerU EXE 使用指南

打包完成后，你将获得一个可独立运行的MinerU可执行文件。

## 📁 文件结构

```
dist/mineru/
├── mineru.exe          # 主程序（Windows）
├── _internal/          # 依赖库和资源
│   ├── mineru/
│   ├── torch/
│   ├── transformers/
│   └── ...
└── ...
```

## 🚀 基础使用

### 1. 查看版本
```bash
mineru.exe --version
```

### 2. 解析单个PDF
```bash
mineru.exe -p document.pdf -o output_folder
```

### 3. 批量解析文件夹
```bash
mineru.exe -p pdf_folder -o output_folder
```

## 🛠️ 常用参数

### 后端选择
```bash
# 使用Pipeline后端（默认，更快）
mineru.exe -p doc.pdf -o output -b pipeline

# 使用VLM后端（更准确，需要额外安装）
mineru.exe -p doc.pdf -o output -b vlm-transformers
```

### 语言设置
```bash
# 中文文档（默认）
mineru.exe -p doc.pdf -o output -l ch

# 英文文档
mineru.exe -p doc.pdf -o output -l en

# 日语文档
mineru.exe -p doc.pdf -o output -l japan

# 韩语文档
mineru.exe -p doc.pdf -o output -l korean
```

### PDF解析方法
```bash
# 自动选择（默认）
mineru.exe -p doc.pdf -o output -m auto

# 纯文本提取（更快，适合纯文本PDF）
mineru.exe -p doc.pdf -o output -m txt

# OCR识别（适合扫描件或图片PDF）
mineru.exe -p doc.pdf -o output -m ocr
```

### 页面范围
```bash
# 只解析第1-10页（页码从0开始）
mineru.exe -p doc.pdf -o output --start 0 --end 9

# 从第5页开始解析到最后
mineru.exe -p doc.pdf -o output --start 4
```

### 功能开关
```bash
# 禁用公式识别（加快速度）
mineru.exe -p doc.pdf -o output --formula false

# 禁用表格识别
mineru.exe -p doc.pdf -o output --table false

# 同时禁用公式和表格
mineru.exe -p doc.pdf -o output --formula false --table false
```

## 📊 输出文件

解析完成后，在输出目录会生成：

```
output_folder/
└── document_name/
    └── auto/  （或txt/ocr，取决于解析方法）
        ├── document_name.md         # Markdown结果
        ├── content_list.json        # 结构化内容列表
        ├── middle.json             # 中间处理结果
        ├── model_list.txt          # 使用的模型列表
        └── images/                 # 提取的图片
            ├── image_001.png
            ├── image_002.png
            └── ...
```

## ⚙️ 首次运行

### 模型下载

首次运行时，MinerU会自动下载所需的模型文件（约1-2GB）：

```
下载位置:
Windows: C:\Users\你的用户名\.cache\mineru\models\
```

**提示**：
- 确保有稳定的网络连接
- 确保有足够的磁盘空间（至少5GB）
- 下载过程可能需要5-15分钟

### 预先下载模型

可以提前下载模型：

```bash
# 下载所有必需模型
mineru-models-download.exe

# 指定模型源（国内推荐使用modelscope）
mineru-models-download.exe --source modelscope
```

## 💡 使用技巧

### 1. 处理大型PDF

对于页数很多的PDF，建议分批处理：

```bash
# 处理前50页
mineru.exe -p large.pdf -o output --start 0 --end 49

# 处理接下来的50页
mineru.exe -p large.pdf -o output --start 50 --end 99
```

### 2. 提高速度

```bash
# 禁用不需要的功能
mineru.exe -p doc.pdf -o output --formula false --table false

# 使用txt模式（如果是纯文本PDF）
mineru.exe -p doc.pdf -o output -m txt
```

### 3. 提高准确度

```bash
# 使用OCR模式确保图片文字被识别
mineru.exe -p doc.pdf -o output -m ocr

# 指定正确的语言
mineru.exe -p doc.pdf -o output -l ch  # 中文
```

### 4. 处理特殊文档

```bash
# 扫描PDF（必须用OCR）
mineru.exe -p scanned.pdf -o output -m ocr

# 多语言混合文档
mineru.exe -p mixed.pdf -o output -l ch  # 主要语言

# 数学论文（保留公式）
mineru.exe -p math_paper.pdf -o output --formula true
```

## 🐛 常见问题

### Q: 提示"模型下载失败"

**解决方案**：
```bash
# 使用国内镜像
mineru.exe -p doc.pdf -o output --model-source modelscope

# 或设置环境变量
set MINERU_MODEL_SOURCE=modelscope
mineru.exe -p doc.pdf -o output
```

### Q: OCR识别效果不好

**解决方案**：
- 确保指定了正确的语言
- 如果PDF质量很差，可能需要预处理图片
- 尝试调整PDF的DPI

### Q: 内存不足

**解决方案**：
- 分批处理PDF页面
- 关闭其他占用内存的程序
- 使用 `--vram` 参数限制显存使用（如果有GPU）

### Q: 输出的Markdown格式不理想

**解决方案**：
- 检查 `content_list.json`，里面有结构化数据
- 可以基于 `content_list.json` 自定义格式化
- 检查 `middle.json` 了解更多中间结果

### Q: 处理速度很慢

**解决方案**：
- 禁用不需要的功能（公式/表格）
- 如果是纯文本PDF，使用 `-m txt` 模式
- 确保有足够的可用内存和磁盘空间

## 🔧 高级配置

### 环境变量

```bash
# Windows (cmd)
set MINERU_MODEL_SOURCE=modelscope
set MINERU_DEVICE_MODE=cpu
set MINERU_VIRTUAL_VRAM_SIZE=8

# Windows (PowerShell)
$env:MINERU_MODEL_SOURCE = "modelscope"
$env:MINERU_DEVICE_MODE = "cpu"
$env:MINERU_VIRTUAL_VRAM_SIZE = "8"
```

### 配置文件

在用户目录创建 `mineru.json` 配置文件（可选）：

```json
{
    "model-source": "modelscope",
    "device-mode": "cpu",
    "lang": "ch"
}
```

## 📚 完整命令参考

```bash
mineru.exe --help
```

## 🆘 获取帮助

- GitHub Issues: https://github.com/opendatalab/MinerU/issues
- 官方文档: https://opendatalab.github.io/MinerU/
- 讨论区: https://github.com/opendatalab/MinerU/discussions

---

## 示例工作流

### 1. 学术论文处理

```bash
# 完整功能，包含公式和表格
mineru.exe -p research_paper.pdf -o output -l en --formula true --table true
```

### 2. 普通文档快速处理

```bash
# 快速模式，纯文本提取
mineru.exe -p document.pdf -o output -m txt
```

### 3. 扫描文件处理

```bash
# OCR模式，中文识别
mineru.exe -p scanned_doc.pdf -o output -m ocr -l ch
```

### 4. 批量处理

```bash
# 处理整个文件夹
mineru.exe -p pdf_folder -o output_folder -m auto
```

---

**提示**: exe版本包含所有必需的依赖，无需安装Python或其他软件，可以直接在任何Windows系统上运行！
