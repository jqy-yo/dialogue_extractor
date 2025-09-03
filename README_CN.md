# ComfyUI 对话提取器

[English Version](README.md)

一个功能全面的 ComfyUI 插件，用于从图像中提取对话文本并提供高级文件管理功能。

## 节点概览

| 节点名称 | 功能简介 |
|---------|---------|
| **Dialogue Extractor（对话提取器）** | 使用 OCR 从图像中提取对话/文本，支持多语言 |
| **Custom Image Saver（自定义图像保存器）** | 使用可自定义的命名模式和文件夹结构保存图像 |
| **Text Saver（文本保存器）** | 将提取的文本保存到文件，支持灵活的命名选项 |
| **Sequential Image Loader（顺序图像加载器）** | 从文件夹中顺序或随机加载图像，支持自然排序 |

## 功能特性

### 🔍 对话提取器（Dialogue Extractor）
- **多语言 OCR 支持**：基于 PaddleOCR，支持 80+ 种语言，包括中文、英文、日文、韩文等
- **高精度识别**：采用先进的文本检测和识别算法
- **批量处理**：支持在工作流中处理多张图像
- **格式保持**：保留文本布局和结构

**输入参数：**
- `image`：输入图像张量
- `language`：OCR 语言设置（默认：ch - 中文）
  - 选项：ch（中文）、en（英文）、japan（日文）、korean（韩文）等

**输出：**
- `text`：提取的文本内容

### 💾 自定义图像保存器（Custom Image Saver）
- **灵活命名**：支持时间戳、计数器和自定义前缀
- **自动递增计数器**：自动为保存的图像编号
- **自定义文件夹**：在指定目录中组织输出
- **质量控制**：可调节的压缩设置

**输入参数：**
- `images`：要保存的图像张量
- `output_folder`：保存目录路径（默认：ComfyUI/output/dialogue_extractor）
- `filename_mode`：命名模式
  - `timestamp`：使用当前时间戳
  - `counter`：自动递增数字
  - `custom`：用户自定义名称
- `filename_prefix`：文件名前缀
- `image_format`：输出格式（png/jpg/webp）
- `quality`：jpg/webp 的压缩质量（1-100）

### 📝 文本保存器（Text Saver）
- **多种格式**：保存为 TXT、JSON 或 Markdown
- **编码选项**：UTF-8、GBK 等
- **追加模式**：追加到现有文件或创建新文件
- **结构化输出**：JSON 格式化便于数据处理

**输入参数：**
- `text`：要保存的文本内容
- `output_folder`：保存目录
- `filename_mode`：同图像保存器
- `filename_prefix`：自定义前缀
- `file_format`：txt/json/md
- `encoding`：文件编码（utf-8/gbk/gb2312）
- `append_mode`：追加到现有文件或覆盖

### 🖼️ 顺序图像加载器（Sequential Image Loader）
- **自然排序**：正确排序包含数字的文件（1、2、10、20 而非 1、10、2、20）
- **多种模式**：固定索引、递增、递减或随机选择
- **状态保持**：记住顺序操作的位置
- **格式支持**：PNG、JPG、JPEG、WebP、BMP、TIFF、GIF

**输入参数：**
- `folder_path`：包含图像的目录
- `mode`：加载模式
  - `fixed`：始终加载相同索引
  - `increment`：每次执行自动递增
  - `decrement`：每次执行自动递减
  - `random`：随机选择
- `index`：起始索引（0-99999）
- `extensions`：支持的文件类型（逗号分隔）
- `seed`：随机模式的随机种子

**输出：**
- `image`：加载的图像张量
- `filename`：不含扩展名的文件名
- `current_index`：文件夹中的当前位置
- `total_count`：图像总数

## 安装方法

### 方法 1：ComfyUI Manager
1. 打开 ComfyUI Manager
2. 搜索 "Dialogue Extractor"
3. 点击安装

### 方法 2：手动安装
```bash
cd ComfyUI/custom_nodes
git clone https://github.com/jqy-yo/dialogue_extractor.git
cd dialogue_extractor
pip install -r requirements.txt
```

## 系统要求
- ComfyUI
- Python 3.8+
- PaddleOCR
- PaddlePaddle
- Pillow
- NumPy

## 使用场景

### 1. 漫画翻译工作流
1. 使用**顺序图像加载器**加载漫画页面
2. 应用**对话提取器**提取文本
3. 翻译文本（配合其他节点）
4. 使用**文本保存器**保存结果

### 2. 批量 OCR 处理
1. 使用**顺序图像加载器**从文件夹加载图像
2. 使用**对话提取器**提取文本
3. 使用**自定义图像保存器**和**文本保存器**保存处理后的图像和文本

### 3. 截图文本提取
1. 将截图输入到**对话提取器**
2. 提取文本内容
3. 使用**文本保存器**以 JSON/MD 格式保存格式化文本

## 工作流示例

### 基础 OCR 工作流
```
[图像输入] -> [对话提取器] -> [文本保存器]
                        ├-> [显示文本]
                        └-> [进一步处理]
```

### 批量处理工作流
```
[顺序图像加载器] -> [对话提取器] -> [文本保存器]
        ├──────────────────────> [自定义图像保存器]
        └-> [计数器显示]
```

## 使用技巧

1. **语言选择**：选择正确的 OCR 语言以获得最佳效果
2. **图像质量**：高分辨率图像能产生更好的 OCR 结果
3. **自然排序**：使用前导零命名文件（01、02、10）确保一致的排序
4. **内存管理**：对于大批量处理，分组处理以管理内存使用

## 故障排除

### PaddleOCR 安装问题
如果遇到 PaddleOCR 安装问题：
```bash
pip install paddlepaddle -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install paddleocr
```

### GPU 支持
为了 GPU 加速：
```bash
# CUDA 11.6
pip install paddlepaddle-gpu==2.5.1 -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 贡献

欢迎贡献代码！请随时提交拉取请求或为错误和功能请求创建问题。

## 许可证
MIT 许可证

## 作者
[jqy-yo](https://github.com/jqy-yo)

## 致谢
- ComfyUI 团队提供的优秀框架
- PaddleOCR 提供的强大 OCR 功能
- 社区贡献者

## 相关链接
- [GitHub 仓库](https://github.com/jqy-yo/dialogue_extractor)
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI)
- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)