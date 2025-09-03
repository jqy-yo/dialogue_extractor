# ComfyUI Dialogue Extractor

[中文版本](README_CN.md)

A comprehensive ComfyUI plugin for extracting dialogue text from images and managing file operations with advanced features.

## Nodes Overview

| Node | Function |
|------|----------|
| **Dialogue Extractor** | Extract dialogue/text from images using OCR, supports multiple languages |
| **Custom Image Saver** | Save images with customizable naming patterns and folder structure |
| **Text Saver** | Save extracted text to files with flexible naming options |
| **Sequential Image Loader** | Load images from folders sequentially or randomly with natural sorting |

## Features

### 🔍 Dialogue Extractor
- **Multi-language OCR Support**: Built on PaddleOCR, supports 80+ languages including English, Chinese, Japanese, Korean, etc.
- **High Accuracy**: Advanced text detection and recognition algorithms
- **Batch Processing**: Process multiple images in workflows
- **Format Preservation**: Maintains text layout and structure

**Input Parameters:**
- `image`: Input image tensor
- `language`: OCR language setting (default: ch - Chinese)
  - Options: ch (Chinese), en (English), japan (Japanese), korean (Korean), and more

**Output:**
- `text`: Extracted text content

### 💾 Custom Image Saver
- **Flexible Naming**: Support for timestamps, counters, and custom prefixes
- **Auto-increment Counter**: Automatically number saved images
- **Custom Folders**: Organize outputs in specified directories
- **Quality Control**: Adjustable compression settings

**Input Parameters:**
- `images`: Image tensor to save
- `output_folder`: Directory path for saving (default: ComfyUI/output/dialogue_extractor)
- `filename_mode`: Naming pattern
  - `timestamp`: Use current timestamp
  - `counter`: Auto-incrementing number
  - `custom`: User-defined name
- `filename_prefix`: Custom prefix for filenames
- `image_format`: Output format (png/jpg/webp)
- `quality`: Compression quality for jpg/webp (1-100)

### 📝 Text Saver
- **Multiple Formats**: Save as TXT, JSON, or Markdown
- **Encoding Options**: UTF-8, GBK, etc.
- **Append Mode**: Add to existing files or create new ones
- **Structured Output**: JSON formatting for data processing

**Input Parameters:**
- `text`: Text content to save
- `output_folder`: Save directory
- `filename_mode`: Same as Image Saver
- `filename_prefix`: Custom prefix
- `file_format`: txt/json/md
- `encoding`: File encoding (utf-8/gbk/gb2312)
- `append_mode`: Append to existing file or overwrite

### 🖼️ Sequential Image Loader
- **Natural Sorting**: Correctly sorts files with numbers (1, 2, 10, 20 instead of 1, 10, 2, 20)
- **Multiple Modes**: Fixed index, increment, decrement, or random selection
- **State Persistence**: Remembers position for sequential operations
- **Format Support**: PNG, JPG, JPEG, WebP, BMP, TIFF, GIF

**Input Parameters:**
- `folder_path`: Directory containing images
- `mode`: Loading mode
  - `fixed`: Always load the same index
  - `increment`: Auto-increment on each execution
  - `decrement`: Auto-decrement on each execution
  - `random`: Random selection
- `index`: Starting index (0-99999)
- `extensions`: Supported file types (comma-separated)
- `seed`: Random seed for random mode

**Output:**
- `image`: Loaded image tensor
- `filename`: File name without extension
- `current_index`: Current position in folder
- `total_count`: Total number of images

## Installation

### Method 1: ComfyUI Manager
1. Open ComfyUI Manager
2. Search for "Dialogue Extractor"
3. Click Install

### Method 2: Manual Installation
```bash
cd ComfyUI/custom_nodes
git clone https://github.com/jqy-yo/dialogue_extractor.git
cd dialogue_extractor
pip install -r requirements.txt
```

## Requirements
- ComfyUI
- Python 3.8+
- PaddleOCR
- PaddlePaddle
- Pillow
- NumPy

## Use Cases

### 1. Comic/Manga Translation Workflow
1. Use **Sequential Image Loader** to load comic pages
2. Apply **Dialogue Extractor** to extract text
3. Translate text (with other nodes)
4. Save results with **Text Saver**

### 2. Batch OCR Processing
1. Load images from folder with **Sequential Image Loader**
2. Extract text using **Dialogue Extractor**
3. Save both processed images and text with **Custom Image Saver** and **Text Saver**

### 3. Screenshot Text Extraction
1. Input screenshot to **Dialogue Extractor**
2. Extract text content
3. Save formatted text with **Text Saver** in JSON/MD format

## Workflow Examples

### Basic OCR Workflow
```
[Image Input] -> [Dialogue Extractor] -> [Text Saver]
                                      ├-> [Display Text]
                                      └-> [Further Processing]
```

### Batch Processing Workflow
```
[Sequential Image Loader] -> [Dialogue Extractor] -> [Text Saver]
         ├──────────────────────────────────────> [Custom Image Saver]
         └-> [Counter Display]
```

## Tips

1. **Language Selection**: Choose the correct OCR language for best results
2. **Image Quality**: Higher resolution images produce better OCR results
3. **Natural Sorting**: File naming with leading zeros (01, 02, 10) ensures consistent ordering
4. **Memory Management**: For large batches, process in smaller groups to manage memory usage

## Troubleshooting

### PaddleOCR Installation Issues
If you encounter PaddleOCR installation problems:
```bash
pip install paddlepaddle -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install paddleocr
```

### GPU Support
For GPU acceleration:
```bash
# CUDA 11.6
pip install paddlepaddle-gpu==2.5.1 -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## Contributing
Contributions are welcome! Please feel free to submit pull requests or create issues for bugs and feature requests.

## License
MIT License

## Author
[jqy-yo](https://github.com/jqy-yo)

## Acknowledgments
- ComfyUI team for the excellent framework
- PaddleOCR for powerful OCR capabilities
- Community contributors

## Links
- [GitHub Repository](https://github.com/jqy-yo/dialogue_extractor)
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI)
- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)