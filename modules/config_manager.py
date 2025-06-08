import json
import os
import random
from typing import Dict, List, Optional

class ConfigManager:
    def __init__(self, default_style: str = "casual_ru"):
        self.default_style = default_style
        self.current_style = default_style
        self.config_dir = "config"
        self.styles_dir = os.path.join(self.config_dir, "styles")
        
        # Load configuration
        self.reload_config()
    
    def reload_config(self):
        """Reload all configuration files"""
        try:
            # Load main config
            main_config_path = os.path.join(self.config_dir, "config.json")
            with open(main_config_path, 'r', encoding='utf-8') as f:
                self.main_config = json.load(f)
            
            self.current_style = self.main_config.get("current_style", self.default_style)
            
            # Load style config
            style_config_path = os.path.join(self.styles_dir, f"{self.current_style}.json")
            with open(style_config_path, 'r', encoding='utf-8') as f:
                self.style_config = json.load(f)
                
            print(f"✅ Configuration loaded for style: {self.current_style}")
            
        except FileNotFoundError as e:
            print(f"❌ Configuration file not found: {e}")
            print("Please ensure all config files are present in the config directory")
            raise
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in configuration file: {e}")
            raise
    
    def get_available_styles(self) -> List[str]:
        """Get list of available communication styles"""
        if not os.path.exists(self.styles_dir):
            return []
        
        styles = []
        for file in os.listdir(self.styles_dir):
            if file.endswith('.json'):
                styles.append(file[:-5])  # Remove .json extension
        return styles
    
    def get_style_info(self, style_name: str) -> Dict:
        """Get information about a specific style"""
        try:
            style_path = os.path.join(self.styles_dir, f"{style_name}.json")
            with open(style_path, 'r', encoding='utf-8') as f:
                style_data = json.load(f)
                return {
                    "name": style_data.get("style_info", {}).get("name", style_name),
                    "description": style_data.get("style_info", {}).get("description", "No description"),
                    "language": style_data.get("style_info", {}).get("language", "Unknown"),
                    "tone": style_data.get("style_info", {}).get("tone", "Unknown")
                }
        except:
            return {"name": style_name, "description": "Unknown style", "language": "Unknown", "tone": "Unknown"}
    
    def set_style(self, style: str) -> bool:
        """Set current communication style"""
        if style not in self.get_available_styles():
            return False
        
        self.current_style = style
        
        # Update main config file
        self.main_config["current_style"] = style
        main_config_path = os.path.join(self.config_dir, "config.json")
        
        try:
            with open(main_config_path, 'w', encoding='utf-8') as f:
                json.dump(self.main_config, f, ensure_ascii=False, indent=4)
            
            # Reload style config
            self.reload_config()
            return True
        except Exception as e:
            print(f"❌ Error saving style setting: {e}")
            return False
    
    def get_random_greeting(self) -> str:
        """Get random greeting message"""
        greetings = self.style_config.get("greetings", [])
        return random.choice(greetings) if greetings else self.style_config.get("default_greeting", "Welcome {user}!")
    
    def get_random_leave_message(self) -> str:
        """Get random leave message"""
        leave_messages = self.style_config.get("leave_messages", [])
        return random.choice(leave_messages) if leave_messages else "Goodbye {user}!"
    
    def get_embed_title(self, key: str) -> str:
        """Get embed title by key"""
        return self.style_config.get("embeds", {}).get(key, key)
    
    def get_message(self, key: str) -> str:
        """Get message by key"""
        return self.style_config.get("messages", {}).get(key, key)
    
    def get_feature_enabled(self, feature: str) -> bool:
        """Check if feature is enabled"""
        return self.main_config.get("features", {}).get(feature, True)
    
    def get_current_style_info(self) -> Dict:
        """Get current style information"""
        return self.get_style_info(self.current_style)
