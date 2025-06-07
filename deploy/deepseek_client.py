#!/usr/bin/env python3
"""
DeepSeek API Client
Simple client for DeepSeek-R1 API integration
"""

import requests
import json
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class DeepSeekClient:
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY", "sk-9689ac1bcc6248cf842cc16816cd2829")
        self.base_url = "https://api.deepseek.com/v1"
        self.model = "deepseek-reasoner"
        
    def generate_content(self, prompt: str, temperature: float = 0.7, max_tokens: int = 3000) -> Dict:
        """
        Generate content using DeepSeek-R1 API
        """
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': self.model,
            'messages': [
                {'role': 'system', 'content': 'You are an advanced AI with deep reasoning capabilities.'},
                {'role': 'user', 'content': prompt}
            ],
            'temperature': temperature,
            'max_tokens': max_tokens,
            'stream': False
        }
        
        try:
            response = requests.post(
                f'{self.base_url}/chat/completions',
                headers=headers,
                json=data,
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"DeepSeek API error: {response.status_code} - {response.text}")
                return {"error": f"API error: {response.status_code}"}
                
        except Exception as e:
            logger.error(f"DeepSeek request failed: {str(e)}")
            return {"error": str(e)}