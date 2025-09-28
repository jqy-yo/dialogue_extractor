import os
import torch
import numpy as np
from PIL import Image
from pathlib import Path
import random
import re

class SequentialImageLoader:
    counters = {}  # 使用类变量以保持状态

    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "folder_path": ("STRING", {"default": "", "multiline": False}),
                "mode": (["fixed", "increment", "decrement", "random"], {"default": "increment"}),
                "index": ("INT", {"default": 0, "min": 0, "max": 99999}),
                "extensions": ("STRING", {"default": "png,jpg,jpeg,webp,bmp,tiff,gif", "multiline": False}),
            }
        }
    
    RETURN_TYPES = ("IMAGE", "STRING", "INT", "INT")
    RETURN_NAMES = ("image", "filename", "current_index", "total_count")
    FUNCTION = "load_image"
    CATEGORY = "dialogue_extractor"
    
    @classmethod
    def IS_CHANGED(cls, folder_path, mode, index, extensions):
        if mode in ["increment", "decrement", "random"]:
            return float("NaN")
        return ""
    
    def natural_sort_key(self, filename):
        """
        自然排序键函数，将文件名中的数字部分按数值排序
        例如: 1.png, 2.png, 10.png, 20.png, image1.png, image2.png, image10.png
        """
        def convert(text):
            return int(text) if text.isdigit() else text.lower()
        
        return [convert(c) for c in re.split(r'(\d+)', filename)]
    
    def get_image_files(self, folder_path: str, extensions: str) -> list:
        if not os.path.exists(folder_path):
            raise ValueError(f"Folder path does not exist: {folder_path}")
        
        ext_list = [ext.strip().lower() for ext in extensions.split(',')]
        image_files = []
        
        for file in os.listdir(folder_path):
            if any(file.lower().endswith(f'.{ext}') for ext in ext_list):
                image_files.append(file)
        
        # 使用自然排序
        image_files.sort(key=self.natural_sort_key)
        
        return image_files
    
    def load_image_as_tensor(self, file_path: str) -> torch.Tensor:
        with Image.open(file_path) as img:
            # 保持原始模式，支持 RGBA
            if img.mode == 'RGBA':
                img_array = np.array(img).astype(np.float32) / 255.0
            elif img.mode != 'RGB':
                img = img.convert('RGB')
                img_array = np.array(img).astype(np.float32) / 255.0
            else:
                img_array = np.array(img).astype(np.float32) / 255.0

            # 转换为 ComfyUI 标准格式 (batch, height, width, channels)
            img_tensor = torch.from_numpy(img_array)[None,]
            return img_tensor
    
    def load_image(self, folder_path: str, mode: str, index: int, extensions: str):
        folder_path = folder_path.strip()
        if not folder_path:
            raise ValueError("Folder path cannot be empty")
        
        image_files = self.get_image_files(folder_path, extensions)
        
        if not image_files:
            raise ValueError(f"No images found in folder: {folder_path}")
        
        total_count = len(image_files)
        
        if mode == "fixed":
            current_index = index % total_count
        
        elif mode == "increment":
            # 初始化或获取计数器
            if folder_path not in SequentialImageLoader.counters:
                SequentialImageLoader.counters[folder_path] = 0
            else:
                SequentialImageLoader.counters[folder_path] = (SequentialImageLoader.counters[folder_path] + 1) % total_count

            # index 作为偏移量，始终影响结果
            current_index = (index + SequentialImageLoader.counters[folder_path]) % total_count
        
        elif mode == "decrement":
            # 初始化或获取计数器
            if folder_path not in SequentialImageLoader.counters:
                SequentialImageLoader.counters[folder_path] = 0
            else:
                SequentialImageLoader.counters[folder_path] = (SequentialImageLoader.counters[folder_path] + 1) % total_count

            # index 作为偏移量，decrement 模式下反向计数
            current_index = (index - SequentialImageLoader.counters[folder_path]) % total_count
        
        elif mode == "random":
            current_index = random.randint(0, total_count - 1)
        
        selected_file = image_files[current_index]
        file_path = os.path.join(folder_path, selected_file)
        filename = Path(selected_file).stem
        
        image_tensor = self.load_image_as_tensor(file_path)
        
        return (image_tensor, filename, current_index, total_count)

class ImagePathLoader:
    """从指定路径加载单个图片"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image_path": ("STRING", {"default": "", "multiline": False}),
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING")
    RETURN_NAMES = ("image", "filename")
    FUNCTION = "load_image"
    CATEGORY = "dialogue_extractor"

    def load_image(self, image_path: str):
        image_path = image_path.strip()
        if not image_path:
            raise ValueError("Image path cannot be empty")

        if not os.path.exists(image_path):
            raise ValueError(f"Image file does not exist: {image_path}")

        if not os.path.isfile(image_path):
            raise ValueError(f"Path is not a file: {image_path}")

        # 提取文件名（不含扩展名）
        filename = Path(image_path).stem

        try:
            with Image.open(image_path) as img:
                # 保持原始模式，支持 RGBA
                if img.mode == 'RGBA':
                    img_array = np.array(img).astype(np.float32) / 255.0
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                    img_array = np.array(img).astype(np.float32) / 255.0
                else:
                    img_array = np.array(img).astype(np.float32) / 255.0

                # 转换为 ComfyUI 标准格式 (batch, height, width, channels)
                img_tensor = torch.from_numpy(img_array)[None,]

                return (img_tensor, filename)
        except Exception as e:
            raise ValueError(f"Failed to load image from {image_path}: {str(e)}")

NODE_CLASS_MAPPINGS = {
    "SequentialImageLoader": SequentialImageLoader,
    "ImagePathLoader": ImagePathLoader,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SequentialImageLoader": "Sequential Image Loader",
    "ImagePathLoader": "Image Path Loader",
}