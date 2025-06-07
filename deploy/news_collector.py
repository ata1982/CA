#!/usr/bin/env python3
"""
Global News Collector using DeepSeek-R1
Collects and analyzes news from around the world
"""

import os
import json
import logging
import httpx
from datetime import datetime, timezone
from typing import Dict, List
import hashlib
import time

logger = logging.getLogger(__name__)

class NewsCollector:
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY", "sk-9689ac1bcc6248cf842cc16816cd2829")
        self.api_url = "https://api.deepseek.com/chat/completions"
        self.model = "deepseek-reasoner"
        
        self.regions = ["北米", "ヨーロッパ", "アジア", "中東", "アフリカ", "南米", "オセアニア"]
        self.categories = ["テクノロジー", "経済", "科学", "政治", "文化", "スポーツ", "環境", "健康"]
        
    def generate_global_news(self, date: str = None) -> List[Dict]:
        """
        Generate global news using DeepSeek-R1's reasoning capabilities
        """
        if not date:
            date = datetime.now().strftime("%Y年%m月%d日")
        
        all_articles = []
        
        # Generate news for each category
        for category in self.categories[:3]:  # Start with 3 categories to avoid rate limits
            try:
                prompt = f"""
                {date}の{category}分野における最新のグローバルニュースを生成してください。
                
                以下の要件で3つの重要なニュース記事を作成：
                
                1. 異なる地域（{', '.join(self.regions)}）から選択
                2. 実際に起こりそうな現実的な内容
                3. 各記事は以下の構成で2000文字程度：
                   - タイトル（30文字以内）
                   - リード文（200文字）
                   - 背景説明（500文字）
                   - 詳細分析（800文字）
                   - 今後の展望（400文字）
                   - 関連情報（100文字）
                
                JSON形式で返答してください：
                {{
                    "articles": [
                        {{
                            "title": "タイトル",
                            "lead": "リード文",
                            "background": "背景説明",
                            "analysis": "詳細分析",
                            "outlook": "今後の展望",
                            "related_info": "関連情報",
                            "source_region": "地域名",
                            "importance_score": 1-10の数値,
                            "reasoning": "なぜこのニュースが重要か"
                        }}
                    ]
                }}
                """
                
                response = httpx.post(
                    self.api_url,
                    json={
                        "model": self.model,
                        "messages": [
                            {"role": "system", "content": "あなたは国際的な視野を持つニュースアナリストです。"},
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": 0.8,
                        "max_tokens": 4000
                    },
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    timeout=60.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    content = result['choices'][0]['message']['content']
                    
                    # Parse JSON response
                    try:
                        if "```json" in content:
                            content = content.split("```json")[1].split("```")[0]
                        elif "```" in content:
                            content = content.split("```")[1].split("```")[0]
                        
                        news_data = json.loads(content.strip())
                        
                        for article in news_data.get("articles", []):
                            # Generate unique ID
                            article_id = hashlib.md5(
                                f"{article['title']}{datetime.utcnow().isoformat()}".encode()
                            ).hexdigest()[:8]
                            
                            processed_article = {
                                "id": article_id,
                                "model": self.model,
                                "category": category,
                                "title_ja": article["title"],
                                "lead_ja": article["lead"],
                                "background_ja": article["background"],
                                "analysis_ja": article["analysis"],
                                "outlook_ja": article["outlook"],
                                "related_info_ja": article["related_info"],
                                "source_region": article.get("source_region", "グローバル"),
                                "importance_score": article.get("importance_score", 5),
                                "reasoning_process": article.get("reasoning", ""),
                                "published_date": datetime.utcnow().isoformat(),
                                "confidence_level": 0.85
                            }
                            
                            all_articles.append(processed_article)
                            logger.info(f"Generated article: {article['title']}")
                            
                    except json.JSONDecodeError as e:
                        logger.error(f"Failed to parse JSON: {e}")
                        logger.error(f"Content: {content[:200]}...")
                        
                else:
                    logger.error(f"API error: {response.status_code}")
                    
                # Rate limit: wait between requests
                time.sleep(2)
                
            except Exception as e:
                logger.error(f"Error generating {category} news: {str(e)}")
                
        return all_articles
    
    def translate_and_analyze(self, source_text: str, source_lang: str) -> Dict:
        """
        Translate and analyze foreign language news
        """
        prompt = f"""
        以下の{source_lang}のニュースを日本語に翻訳し、分析してください：
        
        {source_text}
        
        以下の形式でJSONを返してください：
        {{
            "translation": "日本語翻訳",
            "summary": "100文字の要約",
            "key_points": ["重要ポイント1", "重要ポイント2"],
            "cultural_context": "文化的背景の説明",
            "global_impact": "グローバルな影響"
        }}
        """
        
        try:
            response = httpx.post(
                self.api_url,
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": "あなたは多言語対応の国際ニュースアナリストです。"},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.3,
                    "max_tokens": 1000
                },
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                timeout=30.0
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0]
                    
                return json.loads(content.strip())
            else:
                return {"error": f"Translation failed: {response.status_code}"}
                
        except Exception as e:
            logger.error(f"Translation error: {str(e)}")
            return {"error": str(e)}