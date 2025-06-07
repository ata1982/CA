#!/usr/bin/env python3
"""
News Update System with Real News Fetching and DeepSeek-R1 Integration
Fetches real news from RSS feeds and generates detailed articles
"""

import os
import sys
import json
import logging
import tempfile
from datetime import datetime, timezone
from pathlib import Path
import time

# Add backend directory to path - check for multiple possible locations
possible_paths = [
    '/home/ubuntu/news-ai-site/backend',
    Path.home() / 'news-ai-site/backend',
    Path(__file__).parent / 'backend',
    Path(__file__).parent
]

for path in possible_paths:
    if Path(path).exists():
        sys.path.insert(0, str(path))
        break

from deepseek_processor import DeepSeekProcessor
from news_fetcher import NewsFetcher

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Path(tempfile.gettempdir()) / 'news_update_real.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class RealNewsUpdater:
    def __init__(self, public_dir=None):
        if public_dir:
            self.public_dir = Path(public_dir)
        else:
            try:
                from config import DATA_DIR
                self.public_dir = DATA_DIR
            except ImportError:
                self.public_dir = Path('/var/www/html') if Path('/var/www/html').exists() else Path('.')
        self.public_dir.mkdir(exist_ok=True)
        
        self.processor = DeepSeekProcessor()
        self.fetcher = NewsFetcher()
        
    def process_news(self):
        """Main process: fetch, analyze, and generate articles"""
        try:
            logger.info("Starting real news update process...")
            
            # 1. Fetch real news from RSS feeds
            logger.info("Fetching news from RSS feeds...")
            raw_articles = self.fetcher.fetch_all_feeds(max_per_feed=3)
            
            # 2. Filter recent articles (last 24 hours)
            recent_articles = self.fetcher.filter_recent(raw_articles, hours=24)
            logger.info(f"Found {len(recent_articles)} recent articles")
            
            if not recent_articles:
                logger.warning("No recent articles found, using all fetched articles")
                recent_articles = raw_articles[:10]  # Use top 10 articles
            
            # 3. Analyze articles with DeepSeek
            logger.info("Analyzing articles with DeepSeek...")
            analyzed_articles = []
            
            for i, article in enumerate(recent_articles[:6]):  # Process max 6 articles
                try:
                    logger.info(f"Analyzing article {i+1}/{min(6, len(recent_articles))}: {article['title'][:50]}...")
                    
                    # First analyze the article
                    analyzed = self.processor.analyze_article(article)
                    
                    # Then generate detailed content
                    if analyzed.get('ai_analysis'):
                        detailed = self.processor.generate_detailed_article(analyzed)
                        analyzed_articles.append(detailed)
                        logger.info(f"Successfully processed: {article['source']} - {article['title'][:30]}...")
                    
                    # Rate limiting
                    time.sleep(2)
                    
                except Exception as e:
                    logger.error(f"Error processing article: {str(e)}")
                    continue
            
            # 4. Save processed articles
            self._save_articles(analyzed_articles)
            
            # 5. Generate HTML
            html_content = self._generate_html(analyzed_articles)
            self._save_html(html_content)
            
            logger.info(f"Update completed. Processed {len(analyzed_articles)} articles.")
            
        except Exception as e:
            logger.error(f"Fatal error in news update: {str(e)}")
            raise
        
        finally:
            self.processor.close()
            self.fetcher.close()
    
    def _save_articles(self, articles):
        """Save articles as JSON"""
        # Add metadata
        data = {
            "last_updated": datetime.utcnow().isoformat(),
            "article_count": len(articles),
            "articles": articles
        }
        
        json_path = self.public_dir / 'data.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Saved {len(articles)} articles to {json_path}")
    
    def _generate_html(self, articles):
        """Generate HTML page with real news articles"""
        html_content = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI News Portal - Real Global News with DeepSeek-R1</title>
    <meta http-equiv="refresh" content="900">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
            color: #333;
            min-height: 100vh;
        }
        
        .header {
            background: rgba(255, 255, 255, 0.98);
            box-shadow: 0 2px 15px rgba(0,0,0,0.1);
            padding: 25px 0;
            position: sticky;
            top: 0;
            z-index: 100;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }
        
        h1 {
            font-size: 2.8em;
            color: #0f2027;
            text-align: center;
            margin-bottom: 10px;
        }
        
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 10px;
            font-size: 1.2em;
        }
        
        .powered-by {
            text-align: center;
            color: #2c5364;
            font-weight: bold;
            margin-bottom: 20px;
            font-size: 1.1em;
        }
        
        .real-news-badge {
            display: inline-block;
            background: #4CAF50;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            margin-left: 10px;
        }
        
        .stats {
            display: flex;
            justify-content: center;
            gap: 40px;
            margin-bottom: 25px;
            flex-wrap: wrap;
        }
        
        .stat {
            text-align: center;
        }
        
        .stat-value {
            font-size: 2.2em;
            font-weight: bold;
            color: #2c5364;
        }
        
        .stat-label {
            color: #666;
            font-size: 0.9em;
        }
        
        .articles {
            display: grid;
            gap: 30px;
            margin-top: 30px;
            padding-bottom: 50px;
        }
        
        .article {
            background: white;
            border-radius: 20px;
            padding: 35px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .article::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 5px;
            background: linear-gradient(90deg, #4CAF50, #2196F3, #FF9800);
        }
        
        .article:hover {
            transform: translateY(-8px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.15);
        }
        
        .article-source {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            font-size: 0.9em;
            color: #666;
        }
        
        .source-info {
            display: flex;
            gap: 15px;
            align-items: center;
        }
        
        .source-name {
            font-weight: bold;
            color: #2c5364;
        }
        
        .original-link {
            color: #2196F3;
            text-decoration: none;
            font-size: 0.85em;
        }
        
        .original-link:hover {
            text-decoration: underline;
        }
        
        .article-title {
            font-size: 2em;
            color: #0f2027;
            margin-bottom: 15px;
            line-height: 1.3;
        }
        
        .article-meta {
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            margin-bottom: 25px;
        }
        
        .category {
            background: #2c5364;
            color: white;
            padding: 6px 18px;
            border-radius: 20px;
            font-size: 0.9em;
        }
        
        .language-badge {
            background: #f0f0f0;
            color: #666;
            padding: 6px 18px;
            border-radius: 20px;
            font-size: 0.9em;
        }
        
        .importance {
            background: #ff6b6b;
            color: white;
            padding: 6px 18px;
            border-radius: 20px;
            font-size: 0.9em;
        }
        
        .importance.high {
            background: #ff4757;
        }
        
        .importance.medium {
            background: #ff6348;
        }
        
        .importance.low {
            background: #ff9ff3;
        }
        
        .article-content {
            line-height: 1.8;
            color: #444;
        }
        
        .original-summary {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            border-left: 4px solid #2196F3;
            font-style: italic;
        }
        
        .ai-summary {
            background: #e8f5e9;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            border-left: 4px solid #4CAF50;
        }
        
        .analysis-section {
            margin-top: 25px;
            padding-top: 25px;
            border-top: 2px solid #f0f0f0;
        }
        
        .section-title {
            font-size: 1.1em;
            color: #2c5364;
            margin-bottom: 10px;
            font-weight: bold;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .keywords {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-top: 15px;
        }
        
        .keyword {
            background: #e3f2fd;
            color: #1976d2;
            padding: 5px 12px;
            border-radius: 15px;
            font-size: 0.85em;
        }
        
        .timestamp {
            text-align: center;
            color: #999;
            margin-top: 40px;
            font-size: 0.9em;
        }
        
        @media (max-width: 768px) {
            h1 {
                font-size: 2em;
            }
            
            .stats {
                gap: 20px;
            }
            
            .article {
                padding: 25px;
            }
            
            .article-title {
                font-size: 1.6em;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="container">
            <h1>🌐 AI News Portal <span class="real-news-badge">REAL NEWS</span></h1>
            <div class="subtitle">世界中の実際のニュースをDeepSeek-R1が深層分析</div>
            <div class="powered-by">Powered by DeepSeek-R1 Advanced Reasoning + Real RSS Feeds</div>
            <div class="stats">
                <div class="stat">
                    <div class="stat-value">""" + str(len(articles)) + """</div>
                    <div class="stat-label">記事数</div>
                </div>
                <div class="stat">
                    <div class="stat-value">""" + str(len(set(a.get('source', '') for a in articles))) + """</div>
                    <div class="stat-label">ニュースソース</div>
                </div>
                <div class="stat">
                    <div class="stat-value">""" + str(len(set(a.get('language', '') for a in articles))) + """</div>
                    <div class="stat-label">言語</div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="container">
        <div class="articles">
"""
        
        for article in articles:
            ai_analysis = article.get('ai_analysis', {})
            importance = ai_analysis.get('importance', 5)
            
            # Determine importance class
            importance_class = 'high' if importance >= 8 else 'medium' if importance >= 5 else 'low'
            
            # Get detailed article if available
            detailed = article.get('detailed_article', {})
            
            html_content += f"""
            <div class="article">
                <div class="article-source">
                    <div class="source-info">
                        <span class="source-name">📰 {article.get('source', 'Unknown')}</span>
                        <span class="language-badge">🌍 {article.get('language', '').upper()}</span>
                        <span>{article.get('published', '')[:10]}</span>
                    </div>
                    <a href="{article.get('url', '#')}" target="_blank" class="original-link">元記事を読む →</a>
                </div>
                
                <h2 class="article-title">{ai_analysis.get('title_ja', article.get('title', 'タイトルなし'))}</h2>
                
                <div class="article-meta">
                    <span class="category">{ai_analysis.get('category', 'その他')}</span>
                    <span class="importance {importance_class}">重要度: {importance}/10</span>
                    <span class="sentiment-{ai_analysis.get('sentiment', 'neutral')}">{ai_analysis.get('sentiment', 'neutral').upper()}</span>
                </div>
                
                <div class="article-content">
                    <div class="original-summary">
                        <strong>元記事概要:</strong> {article.get('content', '')[:200]}...
                    </div>
                    
                    <div class="ai-summary">
                        <strong>AI要約:</strong> {ai_analysis.get('summary', '')}
                    </div>
                    
                    <div class="analysis-section">
                        <div class="section-title">🌏 グローバルな影響</div>
                        <p>{ai_analysis.get('global_impact', '分析中...')}</p>
                    </div>
                    
                    <div class="analysis-section">
                        <div class="section-title">🇯🇵 日本への関連性</div>
                        <p>{ai_analysis.get('japan_relevance', '分析中...')}</p>
                    </div>
                    
                    {f'''<div class="analysis-section">
                        <div class="section-title">📊 AI推論プロセス</div>
                        <p>{ai_analysis.get('reasoning', '')}</p>
                    </div>''' if ai_analysis.get('reasoning') else ''}
                    
                    <div class="keywords">
                        {''.join([f'<span class="keyword">{kw}</span>' for kw in ai_analysis.get('keywords', [])])}
                    </div>
                </div>
            </div>
"""
        
        html_content += f"""
        </div>
        <div class="timestamp">
            最終更新: {datetime.now(timezone.utc).strftime('%Y年%m月%d日 %H:%M:%S UTC')}<br>
            次回更新: 15分後
        </div>
    </div>
</body>
</html>
"""
        
        return html_content
    
    def _save_html(self, html_content):
        """Save HTML to file"""
        html_path = self.public_dir / 'index.html'
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        logger.info(f"Saved HTML to {html_path}")

if __name__ == "__main__":
    try:
        updater = RealNewsUpdater()
        updater.process_news()
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        sys.exit(1)