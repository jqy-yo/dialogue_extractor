import os
import folder_paths
from datetime import datetime

class TextSaver:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {
                    "multiline": True,
                    "default": ""
                }),
                "filename": ("STRING", {
                    "default": "output",
                    "multiline": False
                }),
                "save_path": ("STRING", {
                    "default": "",
                    "multiline": False
                }),
                "add_timestamp": ("BOOLEAN", {
                    "default": False
                }),
                "write_mode": (["overwrite", "append"], {
                    "default": "overwrite"
                }),
                "add_spacing": ("BOOLEAN", {
                    "default": True
                }),
                "spacing_type": (["empty_line", "double_line", "custom"], {
                    "default": "empty_line"
                }),
                "custom_separator": ("STRING", {
                    "default": "\n\n",
                    "multiline": False
                })
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("saved_path", "content")
    FUNCTION = "save_text"
    OUTPUT_NODE = True
    CATEGORY = "text/io"

    def save_text(self, text, filename, save_path, add_timestamp, write_mode, 
                 add_spacing, spacing_type, custom_separator):
        
        output_dir = folder_paths.get_output_directory()
        
        if save_path and save_path.strip():
            if os.path.isabs(save_path):
                full_output_dir = save_path
            else:
                full_output_dir = os.path.join(output_dir, save_path)
        else:
            full_output_dir = output_dir
            
        os.makedirs(full_output_dir, exist_ok=True)
        
        base_filename = filename
        if add_timestamp:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_filename = f"{base_filename}_{timestamp}"
        
        full_filename = f"{base_filename}.txt"
        full_path = os.path.join(full_output_dir, full_filename)
        
        content_to_write = text
        
        if add_spacing and content_to_write.strip():
            if spacing_type == "empty_line":
                content_to_write = content_to_write + "\n\n"
            elif spacing_type == "double_line":
                content_to_write = content_to_write + "\n\n\n"
            elif spacing_type == "custom":
                content_to_write = content_to_write + custom_separator
        
        mode = 'a' if write_mode == "append" else 'w'
        
        try:
            with open(full_path, mode, encoding='utf-8') as f:
                f.write(content_to_write)
            
            return (full_path, content_to_write)
        
        except Exception as e:
            error_msg = f"Error saving file: {str(e)}"
            return (error_msg, error_msg)


class MultiTextSaver:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "texts": ("STRING", {
                    "multiline": True,
                    "default": ""
                }),
                "filename": ("STRING", {
                    "default": "multi_output",
                    "multiline": False
                }),
                "save_path": ("STRING", {
                    "default": "",
                    "multiline": False
                }),
                "separator": ("STRING", {
                    "default": "\n\n",
                    "multiline": False
                }),
                "add_index": ("BOOLEAN", {
                    "default": False
                }),
                "index_format": ("STRING", {
                    "default": "[{index}] ",
                    "multiline": False
                }),
                "add_timestamp": ("BOOLEAN", {
                    "default": False
                }),
                "write_mode": (["overwrite", "append"], {
                    "default": "overwrite"
                })
            },
            "optional": {
                "text1": ("STRING", {"multiline": True, "default": ""}),
                "text2": ("STRING", {"multiline": True, "default": ""}),
                "text3": ("STRING", {"multiline": True, "default": ""}),
                "text4": ("STRING", {"multiline": True, "default": ""}),
                "text5": ("STRING", {"multiline": True, "default": ""})
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "INT")
    RETURN_NAMES = ("saved_path", "combined_content", "text_count")
    FUNCTION = "save_multiple_texts"
    OUTPUT_NODE = True
    CATEGORY = "text/io"

    def save_multiple_texts(self, texts, filename, save_path, separator, 
                           add_index, index_format, add_timestamp, write_mode,
                           text1="", text2="", text3="", text4="", text5=""):
        
        output_dir = folder_paths.get_output_directory()
        
        if save_path and save_path.strip():
            if os.path.isabs(save_path):
                full_output_dir = save_path
            else:
                full_output_dir = os.path.join(output_dir, save_path)
        else:
            full_output_dir = output_dir
            
        os.makedirs(full_output_dir, exist_ok=True)
        
        all_texts = []
        if texts and texts.strip():
            all_texts.append(texts)
        for text in [text1, text2, text3, text4, text5]:
            if text and text.strip():
                all_texts.append(text)
        
        if add_index:
            formatted_texts = []
            for i, text in enumerate(all_texts):
                formatted_text = index_format.format(index=i+1) + text
                formatted_texts.append(formatted_text)
            all_texts = formatted_texts
        
        combined_content = separator.join(all_texts)
        
        base_filename = filename
        if add_timestamp:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_filename = f"{base_filename}_{timestamp}"
        
        full_filename = f"{base_filename}.txt"
        full_path = os.path.join(full_output_dir, full_filename)
        
        mode = 'a' if write_mode == "append" else 'w'
        
        content_to_write = combined_content
        if write_mode == "append" and os.path.exists(full_path) and os.path.getsize(full_path) > 0:
            content_to_write = separator + combined_content
        
        try:
            with open(full_path, mode, encoding='utf-8') as f:
                f.write(content_to_write)
            
            return (full_path, combined_content, len(all_texts))
        
        except Exception as e:
            error_msg = f"Error saving file: {str(e)}"
            return (error_msg, error_msg, 0)


class TextAppender:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "file_path": ("STRING", {
                    "default": "",
                    "multiline": False
                }),
                "text_to_append": ("STRING", {
                    "multiline": True,
                    "default": ""
                }),
                "add_timestamp": ("BOOLEAN", {
                    "default": True
                }),
                "timestamp_format": ("STRING", {
                    "default": "[{timestamp}] ",
                    "multiline": False
                }),
                "separator_before": ("STRING", {
                    "default": "\n\n",
                    "multiline": False
                }),
                "separator_after": ("STRING", {
                    "default": "\n",
                    "multiline": False
                })
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("file_path", "appended_content")
    FUNCTION = "append_text"
    OUTPUT_NODE = True
    CATEGORY = "text/io"

    def append_text(self, file_path, text_to_append, add_timestamp, 
                   timestamp_format, separator_before, separator_after):
        
        if not file_path or not file_path.strip():
            return ("Error: No file path specified", "")
        
        if not os.path.isabs(file_path):
            output_dir = folder_paths.get_output_directory()
            file_path = os.path.join(output_dir, file_path)
        
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        content_to_append = text_to_append
        
        if add_timestamp:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            timestamp_prefix = timestamp_format.format(timestamp=timestamp)
            content_to_append = timestamp_prefix + content_to_append
        
        final_content = separator_before + content_to_append + separator_after
        
        try:
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(final_content)
            
            return (file_path, final_content)
        
        except Exception as e:
            error_msg = f"Error appending to file: {str(e)}"
            return (error_msg, "")


NODE_CLASS_MAPPINGS = {
    "TextSaver": TextSaver,
    "MultiTextSaver": MultiTextSaver,
    "TextAppender": TextAppender
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TextSaver": "Text Saver",
    "MultiTextSaver": "Multi Text Saver", 
    "TextAppender": "Text Appender"
}