#!/usr/bin/env python3
"""
Viral News Update System
100+ categories, SNS trends, gossip, YouTube integration, real-time viral detection
"""

import os
import sys
import json
import logging
import asyncio
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

# Add backend directory to path
sys.path.insert(0, '/home/ubuntu/news-ai-site/backend')

from deepseek_processor import DeepSeekProcessor
from extended_news_fetcher import ExtendedNewsFetcher
from viral_frontend import generate_viral_frontend

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Path(tempfile.gettempdir()) / 'news_update_viral.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ViralNewsUpdater:
    def __init__(self, public_dir='/var/www/html'):
        self.public_dir = Path(public_dir)
        self.public_dir.mkdir(exist_ok=True)
        
        self.processor = DeepSeekProcessor()
        self.fetcher = ExtendedNewsFetcher()
        
        # 更新間隔設定
        self.update_interval = 180  # 3分間隔
        self.max_articles = 50      # 最大記事数
        
    async def process_viral_news(self):
        """
        バイラルニュースの処理メイン関数
        """
        try:
            logger.info("🔥 Starting viral news update process...")
            
            # 1. 拡張ニュースソースから収集
            logger.info("📡 Fetching from 100+ sources...")
            raw_articles = await self.fetcher.fetch_all_extended_feeds(max_per_category=2)
            
            if not raw_articles:
                logger.warning("No articles fetched, using fallback")
                raw_articles = self._generate_fallback_articles()
            
            # 2. バイラルスコア順でソート
            sorted_articles = sorted(raw_articles, key=lambda x: x.get('viral_score', 0), reverse=True)
            top_articles = sorted_articles[:self.max_articles]
            
            logger.info(f"📊 Processing top {len(top_articles)} viral articles...")
            
            # 3. DeepSeekで分析（高スコア記事優先）
            analyzed_articles = []
            
            for i, article in enumerate(top_articles[:20]):  # 上位20記事のみ分析
                try:
                    logger.info(f"🤖 Analyzing article {i+1}/20: {article['title'][:50]}...")
                    
                    # トレンド・炎上系は特別プロンプト使用
                    if self._is_trend_article(article):
                        analyzed = await self._analyze_trend_article(article)
                    else:
                        analyzed = self.processor.analyze_article(article)
                    
                    analyzed_articles.append(analyzed)
                    
                    # レート制限対策
                    await asyncio.sleep(1)
                    
                except Exception as e:
                    logger.error(f"Error analyzing article: {str(e)}")
                    analyzed_articles.append(article)  # 分析失敗時は元記事をそのまま
                    continue
            
            # 未分析記事も追加（分析なし）
            analyzed_articles.extend(top_articles[20:])
            
            # 4. データ保存
            await self._save_viral_data(analyzed_articles)
            
            # 5. バイラルフロントエンド生成
            html_content = self._generate_viral_html(analyzed_articles)
            await self._save_html(html_content)
            
            # 6. 統計情報出力
            self._log_viral_stats(analyzed_articles)
            
            logger.info(f"✅ Viral news update completed. Processed {len(analyzed_articles)} articles.")
            
        except Exception as e:
            logger.error(f"💥 Fatal error in viral news update: {str(e)}")
            raise
        
        finally:
            await self.fetcher.close()
            self.processor.close()
    
    def _is_trend_article(self, article: Dict) -> bool:
        """
        トレンド・炎上系記事の判定
        """
        category = article.get('category', '').lower()
        platform = article.get('platform', '').lower()
        viral_score = article.get('viral_score', 0)
        
        trend_categories = ['sns_trend', 'gossip', 'youtube_trend']
        trend_platforms = ['twitter', 'youtube', 'tiktok']
        
        return (category in trend_categories or 
                platform in trend_platforms or 
                viral_score >= 600)
    
    async def _analyze_trend_article(self, article: Dict) -> Dict:
        """
        トレンド記事の特別分析
        """
        try:
            # トレンド分析用プロンプト
            prompt = f"""
            以下のトレンド・バイラル記事を分析して、JSON形式で結果を返してください。
            
            記事情報:
            - タイトル: {article.get('title', '')}
            - プラットフォーム: {article.get('platform', 'unknown')}
            - ソース: {article.get('source', 'unknown')}
            - バイラルスコア: {article.get('viral_score', 0)}
            - 内容: {article.get('content', '')}
            - トレンドキーワード: {article.get('trend_keyword', '')}
            
            以下の項目を含むJSONを返してください：
            1. title_ja: 日本語タイトル（キャッチーだが誇張しない、30文字以内）
            2. summary: 80-100文字の日本語要約
            3. trend_analysis: なぜトレンドになっているかの分析
            4. viral_potential: バイラル性の評価（1-10）
            5. controversy_level: 論争度（1-10）
            6. social_impact: 社会的影響度の説明
            7. keywords: 関連キーワード3-5個
            8. fact_check: 事実確認済みの部分
            9. speculation: 推測・噂の部分
            10. target_audience: メインターゲット層
            
            必ずJSON形式のみで返答してください。
            """
            
            response = self.processor.client.post(
                self.processor.api_url,
                json={
                    "model": self.processor.model,
                    "messages": [
                        {"role": "system", "content": "あなたはSNSトレンド分析の専門家です。"},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.5,
                    "max_tokens": 1000
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                try:
                    # より強固なJSON抽出
                    from deepseek_processor import DeepSeekProcessor
                    processor_instance = DeepSeekProcessor()
                    cleaned_content = processor_instance._extract_json_from_response(content)
                    analysis = json.loads(cleaned_content)
                    
                    # 元記事データと分析結果を統合
                    return {
                        **article,
                        "trend_analysis": {
                            "title_ja": analysis.get("title_ja", article.get("title", "")),
                            "summary": analysis.get("summary", ""),
                            "trend_reason": analysis.get("trend_analysis", ""),
                            "viral_potential": analysis.get("viral_potential", 5),
                            "controversy_level": analysis.get("controversy_level", 1),
                            "social_impact": analysis.get("social_impact", ""),
                            "keywords": analysis.get("keywords", []),
                            "fact_check": analysis.get("fact_check", ""),
                            "speculation": analysis.get("speculation", ""),
                            "target_audience": analysis.get("target_audience", ""),
                            "analyzed_at": datetime.utcnow().isoformat()
                        }
                    }
                    
                except json.JSONDecodeError:
                    logger.error(f"Failed to parse trend analysis JSON: {content}")
                    return self._get_fallback_trend_analysis(article)
            else:
                logger.error(f"Trend analysis API error: {response.status_code}")
                return self._get_fallback_trend_analysis(article)
                
        except Exception as e:
            logger.error(f"Trend analysis error: {str(e)}")
            return self._get_fallback_trend_analysis(article)
    
    def _get_fallback_trend_analysis(self, article: Dict) -> Dict:
        """
        トレンド分析のフォールバック
        """
        return {
            **article,
            "trend_analysis": {
                "title_ja": article.get("title", "")[:30],
                "summary": article.get("content", "")[:100],
                "trend_reason": "API接続エラーのため詳細分析不可",
                "viral_potential": 5,
                "controversy_level": 1,
                "social_impact": "分析中",
                "keywords": [],
                "fact_check": "未確認",
                "speculation": "情報収集中",
                "target_audience": "一般",
                "analyzed_at": datetime.utcnow().isoformat()
            }
        }
    
    async def _save_viral_data(self, articles: List[Dict]):
        """
        バイラルデータの保存
        """
        # メタデータ付きで保存
        data = {
            "last_updated": datetime.utcnow().isoformat(),
            "update_interval": self.update_interval,
            "article_count": len(articles),
            "viral_articles": len([a for a in articles if a.get('viral_score', 0) >= 800]),
            "trend_articles": len([a for a in articles if a.get('viral_score', 0) >= 400]),
            "sources_count": len(set(a.get('source', '') for a in articles)),
            "platforms": list(set(a.get('platform', '') for a in articles if a.get('platform'))),
            "categories": list(set(a.get('category', '') for a in articles)),
            "articles": articles
        }
        
        json_path = self.public_dir / 'viral_data.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"💾 Saved viral data to {json_path}")
    
    def _generate_viral_html(self, articles: List[Dict]) -> str:
        """
        バイラルHTML生成
        """
        # トレンドキーワード抽出
        trending_keywords = self._extract_trending_keywords(articles)
        
        # バイラルフロントエンド生成
        return generate_viral_frontend(articles, trending_keywords)
    
    def _extract_trending_keywords(self, articles: List[Dict]) -> List[str]:
        """
        トレンドキーワード抽出
        """
        keywords = {}
        
        for article in articles:
            # バイラルスコアに応じて重み付け
            weight = max(1, article.get('viral_score', 0) // 100)
            
            # タイトルからキーワード抽出
            title = article.get('title', '')
            
            # 日本語キーワード
            import re
            jp_words = re.findall(r'[ァ-ヶー]{2,}|[一-龯]{2,}', title)
            for word in jp_words:
                keywords[word] = keywords.get(word, 0) + weight
            
            # 英語キーワード
            en_words = re.findall(r'[A-Za-z]{3,}', title)
            for word in en_words:
                keywords[word.lower()] = keywords.get(word.lower(), 0) + weight
            
            # 既存のトレンドキーワード
            if article.get('trend_keyword'):
                keywords[article['trend_keyword']] = keywords.get(article['trend_keyword'], 0) + weight * 3
        
        # 上位キーワードを返す
        sorted_keywords = sorted(keywords.items(), key=lambda x: x[1], reverse=True)
        return [kw[0] for kw in sorted_keywords[:15]]
    
    async def _save_html(self, html_content: str):
        """
        HTMLファイル保存
        """
        html_path = self.public_dir / 'index.html'
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        logger.info(f"💾 Saved HTML to {html_path}")
    
    def _log_viral_stats(self, articles: List[Dict]):
        """
        バイラル統計のログ出力
        """
        stats = {
            'total': len(articles),
            'viral': len([a for a in articles if a.get('viral_score', 0) >= 800]),
            'trending': len([a for a in articles if a.get('viral_score', 0) >= 400]),
            'youtube': len([a for a in articles if a.get('platform') == 'youtube']),
            'gossip': len([a for a in articles if 'gossip' in a.get('category', '')]),
            'sources': len(set(a.get('source', '') for a in articles)),
            'avg_viral_score': sum(a.get('viral_score', 0) for a in articles) / len(articles) if articles else 0
        }
        
        logger.info("📊 Viral News Statistics:")
        logger.info(f"   Total articles: {stats['total']}")
        logger.info(f"   🔥 Viral (800+): {stats['viral']}")
        logger.info(f"   📈 Trending (400+): {stats['trending']}")
        logger.info(f"   📺 YouTube: {stats['youtube']}")
        logger.info(f"   💬 Gossip: {stats['gossip']}")
        logger.info(f"   📡 Sources: {stats['sources']}")
        logger.info(f"   📊 Avg Viral Score: {stats['avg_viral_score']:.1f}")
    
    def _generate_fallback_articles(self) -> List[Dict]:
        """
        フォールバック記事生成
        """
        return [
            {
                "id": "fallback_viral",
                "title": "🔥 バイラルニュースシステム稼働開始",
                "content": "100カテゴリ以上のニュースソースからリアルタイムでバイラル・トレンド記事を収集・分析するシステムが稼働しました。",
                "source": "Viral News System",
                "language": "ja",
                "category": "system",
                "viral_score": 500,
                "reliability_score": 0.9,
                "sensitive_level": 1,
                "published": datetime.utcnow().isoformat(),
                "platform": "system"
            }
        ]

# メイン実行部分
async def main():
    """
    非同期メイン関数
    """
    try:
        updater = ViralNewsUpdater()
        await updater.process_viral_news()
    except Exception as e:
        logger.error(f"💥 Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    # 非同期実行
    asyncio.run(main())