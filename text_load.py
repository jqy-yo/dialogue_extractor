import os
import re

class TextLoad:
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
                }),
                "load_mode": (["by_line", "by_double_newline", "by_custom_separator"], {
                    "default": "by_line"
                }),
                "custom_separator": ("STRING", {
                    "default": "---",
                    "multiline": False
                })
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("title", "content", "full_group")
    FUNCTION = "extract_dialogue"
    CATEGORY = "utils"

    def extract_dialogue(self, file_path, group_index, load_mode="by_line", custom_separator="---"):
        if not os.path.exists(file_path):
            return ("File not found", "File not found", "File not found")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split content based on load mode
            if load_mode == "by_line":
                # Each line is a separate group
                groups = [line for line in content.strip().split('\n') if line.strip()]
            elif load_mode == "by_double_newline":
                # Split by double newline (original behavior)
                groups = content.strip().split('\n\n')
            elif load_mode == "by_custom_separator":
                # Split by custom separator
                groups = content.strip().split(custom_separator)
                # Clean up groups (remove empty ones and strip whitespace)
                groups = [g.strip() for g in groups if g.strip()]
            else:
                # Default to by_line if mode is unrecognized
                groups = [line for line in content.strip().split('\n') if line.strip()]
            
            if not groups:
                return ("No groups found", "No groups found", "No groups found")
            
            if group_index >= len(groups):
                return (f"Group index {group_index} out of range (max: {len(groups)-1})", 
                       f"Group index {group_index} out of range (max: {len(groups)-1})", 
                       f"Group index {group_index} out of range (max: {len(groups)-1})")
            
            selected_group = groups[group_index]
            
            # Process selected group based on mode
            if load_mode == "by_line":
                # For single line mode, the whole line is the content
                # Check if it has a title in brackets
                title_match = re.match(r'\[([^\]]+)\]\s*(.*)', selected_group)
                if title_match:
                    title = title_match.group(1)
                    content = title_match.group(2) if title_match.group(2) else selected_group
                else:
                    # No title, use first part as title
                    parts = selected_group.split(':', 1)
                    if len(parts) > 1:
                        title = parts[0].strip()
                        content = parts[1].strip()
                    else:
                        title = f"Line {group_index}"
                        content = selected_group
                full_group = selected_group
            else:
                # For multi-line modes (double newline or custom separator)
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
                full_group = selected_group
            
            return (title, content, full_group)
        
        except Exception as e:
            error_msg = f"Error reading file: {str(e)}"
            return (error_msg, error_msg, error_msg)


class TextLoadCounter:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "file_path": ("STRING", {
                    "default": r"D:\江江\kiro\comfyui\dialogues-export-2025-08-17-with-name.txt",
                    "multiline": False
                }),
                "load_mode": (["by_line", "by_double_newline", "by_custom_separator"], {
                    "default": "by_line"
                }),
                "custom_separator": ("STRING", {
                    "default": "---",
                    "multiline": False
                })
            }
        }

    RETURN_TYPES = ("INT", "STRING")
    RETURN_NAMES = ("total_groups", "group_titles")
    FUNCTION = "count_groups"
    CATEGORY = "utils"

    def count_groups(self, file_path, load_mode="by_line", custom_separator="---"):
        if not os.path.exists(file_path):
            return (0, "File not found")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split content based on load mode
            if load_mode == "by_line":
                # Each line is a separate group
                groups = [line for line in content.strip().split('\n') if line.strip()]
            elif load_mode == "by_double_newline":
                # Split by double newline
                groups = content.strip().split('\n\n')
            elif load_mode == "by_custom_separator":
                # Split by custom separator
                groups = content.strip().split(custom_separator)
                # Clean up groups (remove empty ones and strip whitespace)
                groups = [g.strip() for g in groups if g.strip()]
            else:
                # Default to by_line if mode is unrecognized
                groups = [line for line in content.strip().split('\n') if line.strip()]
            
            titles = []
            
            for i, group in enumerate(groups):
                if load_mode == "by_line":
                    # For single line mode, extract title from the line
                    title_match = re.match(r'\[([^\]]+)\]\s*(.*)', group)
                    if title_match:
                        title = title_match.group(1)
                    else:
                        # Check for colon-separated title
                        parts = group.split(':', 1)
                        if len(parts) > 1:
                            title = parts[0].strip()
                        else:
                            title = f"Line {i}"
                else:
                    # For multi-line modes
                    lines = group.strip().split('\n')
                    if lines:
                        title_match = re.match(r'\[([^\]]+)\]', lines[0])
                        title = title_match.group(1) if title_match else f"Group {i}"
                    else:
                        title = f"Group {i}"
                
                titles.append(f"{i}: {title}")
            
            return (len(groups), '\n'.join(titles))
        
        except Exception as e:
            return (0, f"Error reading file: {str(e)}")


NODE_CLASS_MAPPINGS = {
    "TextLoad": TextLoad,
    "TextLoadCounter": TextLoadCounter
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TextLoad": "Text Load",
    "TextLoadCounter": "Text Load Counter"
}