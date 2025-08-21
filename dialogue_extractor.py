import os
import re

class DialogueExtractor:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "file_path": ("STRING", {
                    "default": r"D:\江江\kiro\comfyui\dialogues-export-2025-08-17-with-name.txt",
                    "multiline": False
                }),
                "group_index": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 9999,
                    "step": 1
                })
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("title", "content", "full_group")
    FUNCTION = "extract_dialogue"
    CATEGORY = "utils"

    def extract_dialogue(self, file_path, group_index):
        if not os.path.exists(file_path):
            return ("File not found", "File not found", "File not found")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            groups = content.strip().split('\n\n')
            
            if not groups:
                return ("No groups found", "No groups found", "No groups found")
            
            if group_index >= len(groups):
                return (f"Group index {group_index} out of range (max: {len(groups)-1})", 
                       f"Group index {group_index} out of range (max: {len(groups)-1})", 
                       f"Group index {group_index} out of range (max: {len(groups)-1})")
            
            selected_group = groups[group_index]
            lines = selected_group.strip().split('\n')
            
            if not lines:
                return ("Empty group", "Empty group", "Empty group")
            
            title_match = re.match(r'\[([^\]]+)\]', lines[0])
            title = title_match.group(1) if title_match else lines[0]
            
            content_lines = []
            for line in lines:
                if not re.match(r'^\[.*\]$', line):
                    content_lines.append(line)
            
            content = '\n'.join(content_lines)
            
            return (title, content, selected_group)
        
        except Exception as e:
            error_msg = f"Error reading file: {str(e)}"
            return (error_msg, error_msg, error_msg)


class DialogueGroupCounter:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "file_path": ("STRING", {
                    "default": r"D:\江江\kiro\comfyui\dialogues-export-2025-08-17-with-name.txt",
                    "multiline": False
                })
            }
        }

    RETURN_TYPES = ("INT", "STRING")
    RETURN_NAMES = ("total_groups", "group_titles")
    FUNCTION = "count_groups"
    CATEGORY = "utils"

    def count_groups(self, file_path):
        if not os.path.exists(file_path):
            return (0, "File not found")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            groups = content.strip().split('\n\n')
            titles = []
            
            for i, group in enumerate(groups):
                lines = group.strip().split('\n')
                if lines:
                    title_match = re.match(r'\[([^\]]+)\]', lines[0])
                    title = title_match.group(1) if title_match else f"Group {i}"
                    titles.append(f"{i}: {title}")
            
            return (len(groups), '\n'.join(titles))
        
        except Exception as e:
            return (0, f"Error reading file: {str(e)}")


NODE_CLASS_MAPPINGS = {
    "DialogueExtractor": DialogueExtractor,
    "DialogueGroupCounter": DialogueGroupCounter
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DialogueExtractor": "Dialogue Extractor",
    "DialogueGroupCounter": "Dialogue Group Counter"
}