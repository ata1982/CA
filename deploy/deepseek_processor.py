#!/usr/bin/env python3
"""
DeepSeek-R1 API Processor for News Articles
Replaces Claude API with DeepSeek API for article analysis and generation
"""

import os
import json
import httpx
import logging
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class DeepSeekProcessor:
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY", "sk-9689ac1bcc6248cf842cc16816cd2829")
        self.api_url = "https://api.deepseek.com/chat/completions"
        self.model = "deepseek-reasoner"
        
        self.client = httpx.Client(
            timeout=60.0,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
        )
    
    def analyze_article(self, article: Dict) -> Dict:
        """
        Analyze a news article using DeepSeek-R1 API
        """
        try:
            # Check if translation is needed
            is_japanese = article.get('language', '') == 'ja' or not article.get('needs_translation', True)
            
            prompt = f"""
            以下の実際のニュース記事を分析して、JSON形式で結果を返してください。

            元記事情報:
            - タイトル: {article.get('title', '')}
            - 言語: {article.get('language', 'unknown')}
            - ソース: {article.get('source', 'unknown')}
            - 公開日: {article.get('published', '')}
            - 内容: {article.get('content', '')}
            - URL: {article.get('url', '')}
            
            {"この記事は日本語以外で書かれています。翻訳が必要です。" if not is_japanese else ""}
            
            以下の項目を含むJSONを返してください：
            1. title_ja: 日本語タイトル（30文字以内）
            2. summary: 80-100文字の日本語要約
            3. category: 技術/経済/健康/科学/スポーツ/政治/環境/文化/その他 から1つ選択
            4. importance: 1-10の重要度スコア（グローバルな影響を考慮）
            5. sentiment: positive/neutral/negative
            6. keywords: 主要キーワード3-5個のリスト（日本語）
            7. reasoning: なぜこの分類・スコアにしたのかの簡潔な説明
            8. global_impact: このニュースのグローバルな影響の簡潔な説明
            9. japan_relevance: 日本への影響や関連性
            
            必ずJSON形式のみで返答してください。
            """
            
            response = self.client.post(
                self.api_url,
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": "あなたは高度なニュース分析AIです。正確でバランスの取れた分析を提供します。"},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.3,
                    "max_tokens": 500
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                # JSON部分を抽出してパース
                try:
                    # より強固なJSON抽出
                    cleaned_content = self._extract_json_from_response(content)
                    analysis = json.loads(cleaned_content)
                    
                    # 記事データと分析結果を統合
                    return {
                        **article,
                        "ai_analysis": {
                            "summary": analysis.get("summary", article.get("content", "")[:100]),
                            "category": analysis.get("category", "その他"),
                            "importance": analysis.get("importance", 5),
                            "sentiment": analysis.get("sentiment", "neutral"),
                            "keywords": analysis.get("keywords", []),
                            "reasoning": analysis.get("reasoning", ""),
                            "analyzed_at": datetime.utcnow().isoformat()
                        }
                    }
                except json.JSONDecodeError:
                    logger.error(f"Failed to parse JSON from DeepSeek response: {content}")
                    return self._get_fallback_analysis(article)
            else:
                logger.error(f"DeepSeek API error: {response.status_code}")
                return self._get_fallback_analysis(article)
                
        except Exception as e:
            logger.error(f"DeepSeek processing error: {str(e)}")
            return self._get_fallback_analysis(article)
    
    def generate_detailed_article(self, article: Dict, target_length: int = 2000) -> Dict:
        """
        Generate a detailed article using DeepSeek-R1's advanced reasoning
        """
        try:
            # Use original article data for better context
            original_title = article.get('title', '')
            original_lang = article.get('language', 'unknown')
            source = article.get('source', 'unknown')
            url = article.get('url', '')
            
            # Get analyzed data if available
            ai_analysis = article.get('ai_analysis', {})
            title_ja = ai_analysis.get('title_ja', article.get('title', ''))
            
            prompt = f"""
            以下の実際のニュース記事を基に、{target_length}文字程度の詳細な日本語記事を作成してください。

            元記事情報：
            - タイトル: {original_title}
            - 言語: {original_lang}
            - ソース: {source}
            - URL: {url}
            - 公開日: {article.get('published', '')}
            - 内容: {article.get('content', '')}
            
            分析結果：
            - 日本語タイトル: {title_ja}
            - カテゴリ: {ai_analysis.get('category', '')}
            - 重要度: {ai_analysis.get('importance', '')}/10
            - キーワード: {', '.join(ai_analysis.get('keywords', []))}
            - グローバル影響: {ai_analysis.get('global_impact', '')}
            - 日本への関連性: {ai_analysis.get('japan_relevance', '')}
            
            作成する記事の構成：
            1. 日本語タイトル（30文字以内）
            2. リード文（200文字）- ニュースの核心を簡潔に
            3. 背景説明（500文字）- なぜこのニュースが重要か、歴史的文脈
            4. 詳細分析（800文字）- DeepSeek-R1の推論能力を活用した深い分析
               - 技術的・経済的な詳細
               - グローバルな影響の具体的分析
               - 日本への具体的な影響
            5. 今後の展望（400文字）- 将来への影響と予測
            6. 関連情報（100文字）- 読者が更に知るべき情報
            
            特に以下の点を分析してください：
            - このニュースの真の意味と重要性
            - 各国・地域への具体的影響
            - 日本の産業・社会への影響
            - 将来のシナリオと対応策
            
            深い推論と分析を含む、洞察に富んだ記事を作成してください。
            """
            
            response = self.client.post(
                self.api_url,
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": "あなたは経験豊富なジャーナリストであり、深い分析力を持つAIです。"},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 3000
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                detailed_content = result['choices'][0]['message']['content']
                
                return {
                    **article,
                    "detailed_article": {
                        "content": detailed_content,
                        "word_count": len(detailed_content),
                        "generated_at": datetime.utcnow().isoformat(),
                        "model": self.model
                    }
                }
            else:
                logger.error(f"DeepSeek API error for detailed generation: {response.status_code}")
                return article
                
        except Exception as e:
            logger.error(f"DeepSeek detailed generation error: {str(e)}")
            return article
    
    def _extract_json_from_response(self, content: str) -> str:
        """
        Extract JSON from DeepSeek response with multiple strategies
        """
        import re
        
        # Strategy 1: Look for code blocks
        if "```json" in content:
            try:
                json_part = content.split("```json")[1].split("```")[0].strip()
                if json_part and (json_part.startswith('{') or json_part.startswith('[')):
                    return json_part
            except:
                pass
        
        if "```" in content:
            try:
                json_part = content.split("```")[1].split("```")[0].strip()
                if json_part and (json_part.startswith('{') or json_part.startswith('[')):
                    return json_part
            except:
                pass
        
        # Strategy 2: Find JSON objects using regex
        json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
        matches = re.findall(json_pattern, content, re.DOTALL)
        for match in matches:
            try:
                # Test if it's valid JSON
                json.loads(match.strip())
                return match.strip()
            except:
                continue
        
        # Strategy 3: Look for JSON-like structure manually
        start_idx = content.find('{')
        if start_idx != -1:
            brace_count = 0
            for i, char in enumerate(content[start_idx:], start_idx):
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        potential_json = content[start_idx:i+1]
                        try:
                            json.loads(potential_json)
                            return potential_json
                        except:
                            break
        
        # Strategy 4: Clean common issues and return as-is
        cleaned = content.strip()
        cleaned = re.sub(r'^[^{]*({.*})[^}]*$', r'\1', cleaned, flags=re.DOTALL)
        cleaned = re.sub(r'\n\s*', '', cleaned)  # Remove newlines and indentation
        cleaned = re.sub(r',\s*}', '}', cleaned)  # Remove trailing commas
        cleaned = re.sub(r',\s*]', ']', cleaned)  # Remove trailing commas in arrays
        
        return cleaned

    def _get_fallback_analysis(self, article: Dict) -> Dict:
        """
        Fallback analysis when API fails
        """
        return {
            **article,
            "ai_analysis": {
                "summary": article.get("content", "")[:100] + "...",
                "category": "その他",
                "importance": 5,
                "sentiment": "neutral",
                "keywords": [],
                "reasoning": "API接続エラーのため、基本的な分析のみ",
                "analyzed_at": datetime.utcnow().isoformat()
            }
        }
    
    def batch_analyze(self, articles: List[Dict]) -> List[Dict]:
        """
        Analyze multiple articles
        """
        analyzed_articles = []
        for article in articles:
            analyzed = self.analyze_article(article)
            analyzed_articles.append(analyzed)
            logger.info(f"Analyzed: {article.get('title', 'Unknown')}")
        
        return analyzed_articles
    
    def close(self):
        """
        Close the HTTP client
        """
        self.client.close()