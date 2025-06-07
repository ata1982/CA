#!/usr/bin/env python3
"""
News Update System with DeepSeek-R1 Integration
Generates global news articles using advanced AI reasoning
"""

import os
import sys
import json
import logging
import tempfile
from datetime import datetime, timezone
from pathlib import Path

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
from news_collector import NewsCollector

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Path(tempfile.gettempdir()) / 'news_update_deepseek.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class NewsUpdater:
    def __init__(self, public_dir='/var/www/html'):
        self.public_dir = Path(public_dir)
        self.public_dir.mkdir(exist_ok=True)
        
        self.processor = DeepSeekProcessor()
        self.collector = NewsCollector()
        
    def generate_html(self, articles):
        """Generate HTML page with news articles"""
        html_content = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI News Portal - DeepSeek-R1 Powered</title>
    <meta http-equiv="refresh" content="300">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: #333;
            min-height: 100vh;
        }
        
        .header {
            background: rgba(255, 255, 255, 0.95);
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 20px 0;
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
            font-size: 2.5em;
            color: #1e3c72;
            text-align: center;
            margin-bottom: 10px;
        }
        
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 10px;
            font-size: 1.1em;
        }
        
        .powered-by {
            text-align: center;
            color: #2a5298;
            font-weight: bold;
            margin-bottom: 20px;
        }
        
        .stats {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-bottom: 20px;
        }
        
        .stat {
            text-align: center;
        }
        
        .stat-value {
            font-size: 2em;
            font-weight: bold;
            color: #2a5298;
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
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .article:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        }
        
        .article-header {
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 20px;
        }
        
        .article-title {
            font-size: 1.8em;
            color: #1e3c72;
            margin-bottom: 10px;
            flex: 1;
        }
        
        .article-meta {
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            margin-bottom: 20px;
        }
        
        .category {
            background: #2a5298;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
        }
        
        .region {
            background: #f0f0f0;
            color: #666;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
        }
        
        .importance {
            background: #ff6b6b;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
        }
        
        .article-section {
            margin-bottom: 25px;
        }
        
        .section-title {
            font-size: 1.2em;
            color: #2a5298;
            margin-bottom: 10px;
            font-weight: bold;
        }
        
        .section-content {
            line-height: 1.8;
            color: #444;
        }
        
        .lead {
            font-size: 1.1em;
            font-weight: 500;
            color: #333;
            margin-bottom: 20px;
            padding: 15px;
            background: #f8f9fa;
            border-left: 4px solid #2a5298;
        }
        
        .reasoning {
            background: #e8f4f8;
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
            font-style: italic;
            color: #666;
        }
        
        .timestamp {
            text-align: center;
            color: #999;
            margin-top: 30px;
            font-size: 0.9em;
        }
        
        @media (max-width: 768px) {
            h1 {
                font-size: 2em;
            }
            
            .stats {
                flex-wrap: wrap;
                gap: 15px;
            }
            
            .article {
                padding: 20px;
            }
            
            .article-title {
                font-size: 1.5em;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="container">
            <h1>🌍 AI News Portal</h1>
            <div class="subtitle">グローバルニュースを深層分析</div>
            <div class="powered-by">Powered by DeepSeek-R1 Advanced Reasoning</div>
            <div class="stats">
                <div class="stat">
                    <div class="stat-value">""" + str(len(articles)) + """</div>
                    <div class="stat-label">記事数</div>
                </div>
                <div class="stat">
                    <div class="stat-value">""" + str(len(set(a.get('category', '') for a in articles))) + """</div>
                    <div class="stat-label">カテゴリ</div>
                </div>
                <div class="stat">
                    <div class="stat-value">""" + str(len(set(a.get('source_region', '') for a in articles))) + """</div>
                    <div class="stat-label">地域</div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="container">
        <div class="articles">
"""
        
        for article in articles:
            html_content += f"""
            <div class="article">
                <div class="article-header">
                    <h2 class="article-title">{article.get('title_ja', 'タイトルなし')}</h2>
                </div>
                
                <div class="article-meta">
                    <span class="category">{article.get('category', 'その他')}</span>
                    <span class="region">📍 {article.get('source_region', 'グローバル')}</span>
                    <span class="importance">重要度: {article.get('importance_score', 5)}/10</span>
                </div>
                
                <div class="lead">{article.get('lead_ja', '')}</div>
                
                <div class="article-section">
                    <div class="section-title">📖 背景</div>
                    <div class="section-content">{article.get('background_ja', '')}</div>
                </div>
                
                <div class="article-section">
                    <div class="section-title">🔍 詳細分析</div>
                    <div class="section-content">{article.get('analysis_ja', '')}</div>
                </div>
                
                <div class="article-section">
                    <div class="section-title">🔮 今後の展望</div>
                    <div class="section-content">{article.get('outlook_ja', '')}</div>
                </div>
                
                <div class="article-section">
                    <div class="section-title">🔗 関連情報</div>
                    <div class="section-content">{article.get('related_info_ja', '')}</div>
                </div>
                
                {f'<div class="reasoning">💭 {article.get("reasoning_process", "")}</div>' if article.get('reasoning_process') else ''}
            </div>
"""
        
        html_content += f"""
        </div>
        <div class="timestamp">最終更新: {datetime.now(timezone.utc).strftime('%Y年%m月%d日 %H:%M:%S UTC')}</div>
    </div>
</body>
</html>
"""
        
        return html_content
    
    def update_news(self):
        """Main update function"""
        try:
            logger.info("Starting news update with DeepSeek-R1...")
            
            # Generate global news
            articles = self.collector.generate_global_news()
            
            if not articles:
                logger.warning("No articles generated, using fallback")
                articles = self._generate_fallback_articles()
            
            # Save as JSON
            json_path = self.public_dir / 'data.json'
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(articles, f, ensure_ascii=False, indent=2)
            
            # Generate and save HTML
            html_content = self.generate_html(articles)
            html_path = self.public_dir / 'index.html'
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"Updated {len(articles)} articles successfully")
            
        except Exception as e:
            logger.error(f"Update failed: {str(e)}")
            raise
        
        finally:
            self.processor.close()
    
    def _generate_fallback_articles(self):
        """Generate fallback articles if API fails"""
        return [
            {
                "id": "fallback1",
                "title_ja": "DeepSeek-R1 AI News Portal 稼働開始",
                "lead_ja": "最新のAI技術DeepSeek-R1を活用したグローバルニュース配信システムが稼働を開始しました。",
                "background_ja": "このシステムは世界各地のニュースを収集・分析し、日本語で詳細な記事を生成します。",
                "analysis_ja": "DeepSeek-R1の高度な推論能力により、単なる翻訳を超えた深い分析が可能になりました。",
                "outlook_ja": "今後は更に多くの言語とニュースソースに対応予定です。",
                "related_info_ja": "AI技術の進化により、言語の壁を越えた情報共有が実現します。",
                "category": "テクノロジー",
                "source_region": "日本",
                "importance_score": 8,
                "published_date": datetime.utcnow().isoformat()
            }
        ]

if __name__ == "__main__":
    try:
        updater = NewsUpdater()
        updater.update_news()
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        sys.exit(1)