import os
import numpy as np
from PIL import Image
import torch
import folder_paths
from datetime import datetime
import json
import hashlib

class CustomImageSaver:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.compress_level = 6

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "filename": ("STRING", {
                    "default": "image",
                    "multiline": False
                }),
                "format": (["png", "jpg", "jpeg", "webp", "bmp", "tiff", "gif"], {
                    "default": "png"
                }),
                "save_path": ("STRING", {
                    "default": "",
                    "multiline": False
                }),
                "add_timestamp": ("BOOLEAN", {
                    "default": True
                }),
                "add_counter": ("BOOLEAN", {
                    "default": True
                }),
                "quality": ("INT", {
                    "default": 95,
                    "min": 1,
                    "max": 100,
                    "step": 1
                }),
                "png_compression": ("INT", {
                    "default": 6,
                    "min": 0,
                    "max": 9,
                    "step": 1
                })
            },
            "optional": {
                "metadata": ("STRING", {
                    "default": "",
                    "multiline": True
                })
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("saved_path", "filename")
    FUNCTION = "save_images"
    OUTPUT_NODE = True
    CATEGORY = "image/io"

    def save_images(self, images, filename, format, save_path, add_timestamp, 
                   add_counter, quality, png_compression, metadata=""):
        
        results = []
        saved_paths = []
        saved_filenames = []
        
        if save_path and save_path.strip():
            if os.path.isabs(save_path):
                output_dir = save_path
            else:
                output_dir = os.path.join(self.output_dir, save_path)
        else:
            output_dir = self.output_dir
            
        os.makedirs(output_dir, exist_ok=True)
        
        base_filename = filename
        if add_timestamp:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_filename = f"{base_filename}_{timestamp}"
        
        for idx, image in enumerate(images):
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8).squeeze())
            
            if add_counter and len(images) > 1:
                current_filename = f"{base_filename}_{idx:04d}"
            elif add_counter:
                counter = self._get_next_counter(output_dir, base_filename, format)
                current_filename = f"{base_filename}_{counter:04d}"
            else:
                current_filename = base_filename
            
            full_filename = f"{current_filename}.{format}"
            full_path = os.path.join(output_dir, full_filename)
            
            save_kwargs = {}
            
            if format in ['jpg', 'jpeg', 'webp']:
                save_kwargs['quality'] = quality
                if format == 'webp':
                    save_kwargs['lossless'] = False
            elif format == 'png':
                save_kwargs['compress_level'] = png_compression
                save_kwargs['optimize'] = True
            
            if metadata and format in ['png', 'webp']:
                from PIL import PngImagePlugin
                pnginfo = PngImagePlugin.PngInfo()
                pnginfo.add_text("metadata", metadata)
                save_kwargs['pnginfo'] = pnginfo
            
            img.save(full_path, **save_kwargs)
            
            saved_paths.append(full_path)
            saved_filenames.append(full_filename)
            
            results.append({
                "filename": full_filename,
                "subfolder": save_path if save_path else "",
                "type": self.type
            })
        
        return {
            "ui": {"images": results},
            "result": ("; ".join(saved_paths), "; ".join(saved_filenames))
        }
    
    def _get_next_counter(self, directory, base_filename, extension):
        pattern = f"{base_filename}_"
        existing_files = [f for f in os.listdir(directory) 
                         if f.startswith(pattern) and f.endswith(f".{extension}")]
        
        if not existing_files:
            return 0
        
        counters = []
        for f in existing_files:
            try:
                counter_str = f[len(pattern):-(len(extension)+1)]
                if counter_str.isdigit():
                    counters.append(int(counter_str))
            except:
                continue
        
        return max(counters) + 1 if counters else 0


class BatchImageSaver:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "base_filename": ("STRING", {
                    "default": "batch_image",
                    "multiline": False
                }),
                "format": (["png", "jpg", "jpeg", "webp", "bmp", "tiff"], {
                    "default": "png"
                }),
                "save_path": ("STRING", {
                    "default": "batch_output",
                    "multiline": False
                }),
                "naming_pattern": (["index", "hash", "timestamp_index", "custom"], {
                    "default": "index"
                }),
                "custom_pattern": ("STRING", {
                    "default": "{base}_{index:04d}",
                    "multiline": False
                }),
                "quality": ("INT", {
                    "default": 95,
                    "min": 1,
                    "max": 100,
                    "step": 1
                })
            }
        }

    RETURN_TYPES = ("STRING", "INT")
    RETURN_NAMES = ("saved_paths", "count")
    FUNCTION = "save_batch"
    OUTPUT_NODE = True
    CATEGORY = "image/io"

    def save_batch(self, images, base_filename, format, save_path, 
                  naming_pattern, custom_pattern, quality):
        
        output_dir = folder_paths.get_output_directory()
        if save_path:
            if os.path.isabs(save_path):
                full_output_dir = save_path
            else:
                full_output_dir = os.path.join(output_dir, save_path)
        else:
            full_output_dir = output_dir
            
        os.makedirs(full_output_dir, exist_ok=True)
        
        saved_paths = []
        results = []
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for idx, image in enumerate(images):
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8).squeeze())
            
            if naming_pattern == "index":
                filename = f"{base_filename}_{idx:04d}"
            elif naming_pattern == "hash":
                img_hash = hashlib.md5(i.tobytes()).hexdigest()[:8]
                filename = f"{base_filename}_{img_hash}"
            elif naming_pattern == "timestamp_index":
                filename = f"{base_filename}_{timestamp}_{idx:04d}"
            elif naming_pattern == "custom":
                filename = custom_pattern.format(
                    base=base_filename,
                    index=idx,
                    timestamp=timestamp,
                    hash=hashlib.md5(i.tobytes()).hexdigest()[:8]
                )
            
            full_filename = f"{filename}.{format}"
            full_path = os.path.join(full_output_dir, full_filename)
            
            save_kwargs = {}
            if format in ['jpg', 'jpeg', 'webp']:
                save_kwargs['quality'] = quality
            elif format == 'png':
                save_kwargs['compress_level'] = 6
                save_kwargs['optimize'] = True
            
            img.save(full_path, **save_kwargs)
            saved_paths.append(full_path)
            
            results.append({
                "filename": full_filename,
                "subfolder": save_path,
                "type": "output"
            })
        
        return {
            "ui": {"images": results},
            "result": ("; ".join(saved_paths), len(saved_paths))
        }


NODE_CLASS_MAPPINGS = {
    "CustomImageSaver": CustomImageSaver,
    "BatchImageSaver": BatchImageSaver
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CustomImageSaver": "Custom Image Saver",
    "BatchImageSaver": "Batch Image Saver"
}