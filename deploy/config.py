#!/usr/bin/env python3
"""
Configuration module for cross-platform compatibility
"""

import os
import platform
import tempfile
from pathlib import Path

# Detect operating system
IS_LINUX = platform.system() == 'Linux'
IS_MACOS = platform.system() == 'Darwin'
IS_WINDOWS = platform.system() == 'Windows'

def get_data_directory():
    """Get the appropriate data directory for the current environment"""
    # Check environment variable first
    if 'DATA_DIR' in os.environ:
        return Path(os.environ['DATA_DIR'])
    
    # Check if web directory exists (Linux server environment)
    if IS_LINUX and Path('/var/www/html').exists():
        return Path('/var/www/html')
    
    # Fallback to current directory
    return Path('.')

def get_log_directory():
    """Get the appropriate log directory for the current environment"""
    # Check environment variable first
    if 'LOG_DIR' in os.environ:
        return Path(os.environ['LOG_DIR'])
    
    # Linux server environment
    if IS_LINUX and Path('/var/log').exists() and os.access('/var/log', os.W_OK):
        return Path('/var/log')
    
    # Use system temp directory
    return Path(tempfile.gettempdir())

def get_backend_path():
    """Get the backend module path"""
    # Check environment variable first
    if 'BACKEND_PATH' in os.environ:
        return os.environ['BACKEND_PATH']
    
    # Try multiple possible locations
    possible_paths = [
        Path('/home/ubuntu/news-ai-site/backend'),  # Server deployment
        Path.home() / 'news-ai-site/backend',       # User deployment
        Path(__file__).parent / 'backend',          # Relative to this file
        Path(__file__).parent                       # Current directory
    ]
    
    for path in possible_paths:
        if path.exists():
            return str(path)
    
    # Fallback to current directory
    return str(Path(__file__).parent)

def get_deploy_config():
    """Get deployment configuration"""
    return {
        'user': os.getenv('DEPLOY_USER', 'ubuntu'),
        'home': os.getenv('DEPLOY_HOME', f"/home/{os.getenv('DEPLOY_USER', 'ubuntu')}"),
        'web_dir': get_data_directory(),
        'log_dir': get_log_directory(),
        'backend_path': get_backend_path()
    }

# Global configuration
CONFIG = get_deploy_config()
DATA_DIR = get_data_directory()
LOG_DIR = get_log_directory()
BACKEND_PATH = get_backend_path()

# API Configuration
API_CONFIG = {
    'deepseek_api_key': os.getenv('DEEPSEEK_API_KEY', 'sk-9689ac1bcc6248cf842cc16816cd2829'),
    'deepseek_api_url': 'https://api.deepseek.com/chat/completions',
    'deepseek_model': 'deepseek-reasoner'
}

# Environment information
ENV_INFO = {
    'platform': platform.system(),
    'is_linux': IS_LINUX,
    'is_macos': IS_MACOS,
    'is_windows': IS_WINDOWS,
    'data_dir': str(DATA_DIR),
    'log_dir': str(LOG_DIR),
    'backend_path': BACKEND_PATH
}

if __name__ == "__main__":
    print("🔧 Environment Configuration:")
    print(f"Platform: {ENV_INFO['platform']}")
    print(f"Data Directory: {ENV_INFO['data_dir']}")
    print(f"Log Directory: {ENV_INFO['log_dir']}")
    print(f"Backend Path: {ENV_INFO['backend_path']}")
    print(f"DeepSeek API Key: {'✅ Set' if API_CONFIG['deepseek_api_key'] else '❌ Not set'}")