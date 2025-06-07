#!/usr/bin/env python3
"""
Real News System with Source Links
Fetches actual news from RSS feeds and maintains source attribution
"""

import os
import sys
import json
import logging
import random
import hashlib
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List, Optional

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import feedparser
    import httpx
except ImportError:
    feedparser = None
    httpx = None

from comment_system import AnonymousCommentSystem, RankingSystem
from comment_generator import CommentGenerator

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class RealNewsFetcher:
    def __init__(self):
        # Comprehensive Japanese news sources by major categories
        self.news_sources = [
            # === 政治・総合 ===
            {
                'name': 'NHK ニュース',
                'url': 'https://www3.nhk.or.jp/rss/news/cat0.xml',
                'category': '政治',
                'language': 'ja',
                'reliability': 0.95
            },
            {
                'name': 'Yahoo!ニュース - 主要',
                'url': 'https://news.yahoo.co.jp/rss/topics/top-picks.xml',
                'category': '政治',
                'language': 'ja', 
                'reliability': 0.85
            },
            {
                'name': '朝日新聞デジタル',
                'url': 'https://www.asahi.com/rss/asahi/newsheadlines.rdf',
                'category': '政治',
                'language': 'ja',
                'reliability': 0.90
            },
            {
                'name': '毎日新聞',
                'url': 'https://mainichi.jp/rss/etc/mainichi-flash.rss',
                'category': '政治',
                'language': 'ja',
                'reliability': 0.92
            },
            
            # === 経済・ビジネス ===
            {
                'name': '日経新聞',
                'url': 'https://www.nikkei.com/news/feed/',
                'category': '経済',
                'language': 'ja',
                'reliability': 0.95
            },
            {
                'name': 'ロイター（経済）',
                'url': 'https://feeds.reuters.com/reuters/JPBusinessNews',
                'category': '経済',
                'language': 'ja',
                'reliability': 0.90
            },
            {
                'name': '東洋経済オンライン',
                'url': 'https://toyokeizai.net/list/feed/rss',
                'category': '経済',
                'language': 'ja',
                'reliability': 0.85
            },
            
            # === 芸能・エンタメ ===
            {
                'name': 'オリコンニュース',
                'url': 'https://www.oricon.co.jp/rss/news/',
                'category': '芸能',
                'language': 'ja',
                'reliability': 0.75
            },
            {
                'name': 'モデルプレス',
                'url': 'https://mdpr.jp/rss',
                'category': '芸能',
                'language': 'ja',
                'reliability': 0.70
            },
            {
                'name': 'シネマトゥデイ',
                'url': 'https://www.cinematoday.jp/rss/news.rss',
                'category': '芸能',
                'language': 'ja',
                'reliability': 0.75
            },
            {
                'name': 'マイナビニュース（芸能）',
                'url': 'https://news.mynavi.jp/rss/entertainment',
                'category': '芸能',
                'language': 'ja',
                'reliability': 0.80
            },
            
            # === スポーツ ===
            {
                'name': 'スポーツ報知',
                'url': 'https://hochi.news/rss',
                'category': 'スポーツ',
                'language': 'ja',
                'reliability': 0.85
            },
            {
                'name': 'スポーツニッポン',
                'url': 'https://www.sponichi.co.jp/rss/',
                'category': 'スポーツ',
                'language': 'ja',
                'reliability': 0.85
            },
            {
                'name': 'Number Web',
                'url': 'https://number.bunshun.jp/rss',
                'category': 'スポーツ',
                'language': 'ja',
                'reliability': 0.80
            },
            {
                'name': 'Goal.com（サッカー）',
                'url': 'https://www.goal.com/jp/feeds/news',
                'category': 'スポーツ',
                'language': 'ja',
                'reliability': 0.75
            },
            
            # === テクノロジー・IT ===
            {
                'name': 'GIGAZINE',
                'url': 'https://gigazine.net/news/rss_2.0/',
                'category': 'テクノロジー',
                'language': 'ja',
                'reliability': 0.80
            },
            {
                'name': 'ITmedia',
                'url': 'https://rss.itmedia.co.jp/rss/2.0/topstory.xml',
                'category': 'テクノロジー',
                'language': 'ja',
                'reliability': 0.85
            },
            {
                'name': 'CNET Japan',
                'url': 'https://feeds.japan.cnet.com/rss/cnet/all.rdf',
                'category': 'テクノロジー',
                'language': 'ja',
                'reliability': 0.85
            },
            {
                'name': 'Engadget日本版',
                'url': 'https://japanese.engadget.com/rss.xml',
                'category': 'テクノロジー',
                'language': 'ja',
                'reliability': 0.80
            },
            {
                'name': 'TechCrunch Japan',
                'url': 'https://jp.techcrunch.com/feed/',
                'category': 'テクノロジー',
                'language': 'ja',
                'reliability': 0.85
            },
            
            # === グルメ・ライフスタイル ===
            {
                'name': 'ぐるなび みんなのごはん',
                'url': 'https://r.gnavi.co.jp/g-interview/rss/',
                'category': 'グルメ',
                'language': 'ja',
                'reliability': 0.70
            },
            {
                'name': 'クックパッドニュース',
                'url': 'https://news.cookpad.com/rss',
                'category': 'グルメ',
                'language': 'ja',
                'reliability': 0.75
            },
            {
                'name': 'dancyu（ダンチュウ）',
                'url': 'https://dancyu.jp/rss',
                'category': 'グルメ',
                'language': 'ja',
                'reliability': 0.80
            },
            
            # === YouTuber・配信 ===
            {
                'name': 'YouTube Creator Blog',
                'url': 'https://blog.youtube/rss/',
                'category': 'ユーチューバー',
                'language': 'en',
                'reliability': 0.85
            },
            {
                'name': 'TubeFilter',
                'url': 'https://www.tubefilter.com/feed/',
                'category': 'ユーチューバー',
                'language': 'en',
                'reliability': 0.80
            },
            
            # === 炎上・ネット・SNS ===
            {
                'name': 'ねとらぼ',
                'url': 'https://nlab.itmedia.co.jp/rss/2.0/',
                'category': '炎上',
                'language': 'ja',
                'reliability': 0.75
            },
            {
                'name': 'J-CASTニュース',
                'url': 'https://www.j-cast.com/feed/',
                'category': '炎上',
                'language': 'ja',
                'reliability': 0.70
            },
            {
                'name': 'BuzzFeed Japan',
                'url': 'https://www.buzzfeed.com/jp.xml',
                'category': '炎上',
                'language': 'ja',
                'reliability': 0.65
            },
            
            # === 国際ニュース ===
            {
                'name': 'BBC News',
                'url': 'http://feeds.bbci.co.uk/news/rss.xml',
                'category': '国際',
                'language': 'en',
                'reliability': 0.95
            },
            {
                'name': 'Reuters',
                'url': 'https://feeds.reuters.com/reuters/topNews',
                'category': '国際',
                'language': 'en',
                'reliability': 0.95
            },
            {
                'name': 'CNN',
                'url': 'http://rss.cnn.com/rss/edition.rss',
                'category': '国際',
                'language': 'en',
                'reliability': 0.88
            }
        ]
        
        if httpx:
            self.client = httpx.Client(
                timeout=30.0,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )
        else:
            self.client = None
    
    def fetch_all_feeds(self, max_per_feed: int = 3) -> List[Dict]:
        """Fetch news from all RSS feeds"""
        all_articles = []
        
        for source in self.news_sources:
            try:
                logger.info(f"Fetching from {source['name']}")
                articles = self._fetch_single_feed(source, max_per_feed)
                all_articles.extend(articles)
                logger.info(f"Fetched {len(articles)} articles from {source['name']}")
                
            except Exception as e:
                logger.error(f"Error fetching from {source['name']}: {str(e)}")
                continue
        
        # Remove duplicates
        unique_articles = self._remove_duplicates(all_articles)
        logger.info(f"Total unique articles: {len(unique_articles)}")
        
        return unique_articles
    
    def _fetch_single_feed(self, source: Dict, max_items: int) -> List[Dict]:
        """Fetch from a single RSS feed"""
        articles = []
        
        try:
            if self.client is None:
                logger.error("httpx client not available")
                return articles
            
            response = self.client.get(source['url'])
            response.raise_for_status()
            
            if feedparser:
                # Use feedparser if available
                feed = feedparser.parse(response.text)
                entries = feed.entries[:max_items]
                
                for entry in entries:
                    article = self._parse_feedparser_entry(entry, source)
                    if article:
                        articles.append(article)
            else:
                # Basic XML parsing fallback
                articles = self._parse_xml_basic(response.text, source, max_items)
                
        except Exception as e:
            logger.error(f"Error fetching RSS feed {source['url']}: {str(e)}")
        
        return articles
    
    def _parse_feedparser_entry(self, entry, source: Dict) -> Optional[Dict]:
        """Parse entry using feedparser"""
        try:
            # Clean HTML tags from summary
            summary = getattr(entry, 'summary', '')
            if summary:
                import re
                summary = re.sub(r'<[^>]+>', '', summary)
                summary = summary.strip()[:500]
            
            article = {
                'id': hashlib.md5(f"{entry.get('link', '')}{entry.get('title', '')}".encode()).hexdigest()[:12],
                'title': entry.get('title', '').strip(),
                'content': summary or entry.get('description', '').strip()[:500],
                'url': entry.get('link', ''),
                'source': source['name'],
                'source_url': source['url'],
                'category': source['category'],
                'language': source['language'],
                'reliability_score': source['reliability'],
                'published': self._parse_date(entry.get('published', '')),
                'fetch_timestamp': datetime.utcnow().isoformat(),
                'is_real_news': True
            }
            
            # Only include articles with essential data
            if article['title'] and article['url']:
                return article
                
        except Exception as e:
            logger.error(f"Error parsing entry: {str(e)}")
        
        return None
    
    def _parse_xml_basic(self, xml_content: str, source: Dict, max_items: int) -> List[Dict]:
        """Basic XML parsing fallback"""
        articles = []
        
        try:
            import xml.etree.ElementTree as ET
            root = ET.fromstring(xml_content)
            
            # Find items (RSS format)
            items = root.findall('.//item')[:max_items]
            
            for item in items:
                title_elem = item.find('title')
                link_elem = item.find('link')
                desc_elem = item.find('description')
                pub_elem = item.find('pubDate')
                
                if title_elem is not None and link_elem is not None:
                    title = title_elem.text or ''
                    link = link_elem.text or ''
                    description = desc_elem.text or '' if desc_elem is not None else ''
                    pub_date = pub_elem.text or '' if pub_elem is not None else ''
                    
                    article = {
                        'id': hashlib.md5(f"{link}{title}".encode()).hexdigest()[:12],
                        'title': title.strip(),
                        'content': description.strip()[:500],
                        'url': link,
                        'source': source['name'],
                        'source_url': source['url'],
                        'category': source['category'],
                        'language': source['language'],
                        'reliability_score': source['reliability'],
                        'published': self._parse_date(pub_date),
                        'fetch_timestamp': datetime.utcnow().isoformat(),
                        'is_real_news': True
                    }
                    
                    if article['title'] and article['url']:
                        articles.append(article)
                        
        except Exception as e:
            logger.error(f"Error parsing XML: {str(e)}")
        
        return articles
    
    def _parse_date(self, date_str: str) -> str:
        """Parse and normalize date string"""
        if not date_str:
            return datetime.utcnow().isoformat()
        
        try:
            # Try multiple date formats
            formats = [
                '%a, %d %b %Y %H:%M:%S %z',
                '%a, %d %b %Y %H:%M:%S %Z',
                '%Y-%m-%d %H:%M:%S',
                '%Y-%m-%dT%H:%M:%S%z',
                '%Y-%m-%dT%H:%M:%SZ'
            ]
            
            for fmt in formats:
                try:
                    dt = datetime.strptime(date_str, fmt)
                    return dt.isoformat()
                except ValueError:
                    continue
            
            # If all formats fail, use current time
            return datetime.utcnow().isoformat()
            
        except Exception as e:
            logger.error(f"Date parsing error: {str(e)}")
            return datetime.utcnow().isoformat()
    
    def _remove_duplicates(self, articles: List[Dict]) -> List[Dict]:
        """Remove duplicate articles"""
        seen_urls = set()
        seen_titles = set()
        unique_articles = []
        
        for article in articles:
            url = article.get('url', '')
            title = article.get('title', '').lower()
            
            # Check URL duplicates
            if url and url in seen_urls:
                continue
            
            # Check title similarity (basic)
            is_duplicate = False
            for seen_title in seen_titles:
                if self._calculate_similarity(title, seen_title) > 0.8:
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                unique_articles.append(article)
                if url:
                    seen_urls.add(url)
                seen_titles.add(title)
        
        return unique_articles
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate text similarity"""
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def close(self):
        """Close HTTP client"""
        if self.client:
            self.client.close()


class RealNewsSystem:
    def __init__(self, data_dir='/var/www/html'):
        self.data_dir = Path(data_dir)
        self.comment_system = AnonymousCommentSystem(data_dir)
        self.ranking_system = RankingSystem(self.comment_system)
        self.comment_generator = CommentGenerator()
        self.news_fetcher = RealNewsFetcher()
    
    def generate_real_news_website(self):
        """Generate website with real news"""
        try:
            logger.info("🔄 Starting real news system...")
            
            # Fetch real news
            logger.info("📡 Fetching real news from RSS feeds...")
            real_articles = self.news_fetcher.fetch_all_feeds(max_per_feed=3)
            
            if not real_articles:
                logger.warning("No real articles fetched, using fallback")
                real_articles = self._get_fallback_articles()
            
            # Initialize comments for new articles
            self._initialize_comments_for_articles(real_articles)
            
            # Track views
            for article in real_articles:
                for _ in range(random.randint(10, 50)):
                    self.comment_system.track_view(article['id'])
            
            # Generate HTML
            html_content = self._generate_real_news_html(real_articles)
            
            # Save to website
            html_path = self.data_dir / 'index.html'
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"✅ Real news website saved to {html_path}")
            
            # Save articles data
            articles_path = self.data_dir / 'articles.json'
            with open(articles_path, 'w', encoding='utf-8') as f:
                json.dump(real_articles, f, ensure_ascii=False, indent=2)
            
            logger.info("🎉 Real news system update completed!")
            
        except Exception as e:
            logger.error(f"💥 Error in real news system: {str(e)}")
            raise
        finally:
            self.news_fetcher.close()
    
    def _initialize_comments_for_articles(self, articles: List[Dict]):
        """Initialize comments for articles that don't have them"""
        existing_comments = self.comment_system._load_comments()
        
        for article in articles:
            article_id = article['id']
            
            # Skip if comments already exist
            if article_id in existing_comments and len(existing_comments[article_id]) > 5:
                continue
            
            logger.info(f"Generating comments for real article: {article['title'][:50]}...")
            
            # Generate comments based on article content
            num_comments = random.randint(8, 20)
            initial_comments = self.comment_generator.generate_initial_comments(
                article['content'], num_comments
            )
            
            # Post comments to system
            for comment_data in initial_comments:
                minutes_ago = random.randint(5, 180)
                timestamp = datetime.now(timezone.utc) - timedelta(minutes=minutes_ago)
                
                comment = {
                    'id': self.comment_system.generate_comment_id(),
                    'name': comment_data['name'],
                    'text': comment_data['text'],
                    'timestamp': {
                        'iso': timestamp.isoformat(),
                        'display': timestamp.strftime('%Y/%m/%d %H:%M:%S'),
                        'jst_display': (timestamp + timedelta(hours=9)).strftime('%Y/%m/%d %H:%M:%S')
                    },
                    'number': len(existing_comments.get(article_id, [])) + 1,
                    'reply_to': None,
                    'likes': comment_data['likes'],
                    'dislikes': comment_data['dislikes']
                }
                
                if article_id not in existing_comments:
                    existing_comments[article_id] = []
                
                existing_comments[article_id].append(comment)
            
            self.comment_system._save_comments(existing_comments)
    
    def _generate_real_news_html(self, articles: List[Dict]) -> str:
        """Generate HTML for real news"""
        current_time = datetime.now(timezone.utc)
        jst_time = current_time + timedelta(hours=9)
        
        # Get ranking data
        hourly_ranking = self.ranking_system.get_hourly_ranking(10)
        
        html_content = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔥 【速報】ニュースまとめ速 - 最新ニュース・コメント</title>
    <meta name="description" content="最新の実際のニュースを最速でお届け！政治・芸能・経済・社会のニュースとリアルタイムコメント">
    <meta name="keywords" content="ニュース,速報,政治,芸能,経済,コメント,まとめ,RSS">
    <meta http-equiv="refresh" content="900">
    
    <!-- OGP Tags -->
    <meta property="og:title" content="【速報】ニュースまとめ速">
    <meta property="og:description" content="最新の実際のニュースを最速でお届け！">
    <meta property="og:type" content="website">
    <meta property="og:url" content="http://18.179.38.25">
    
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            line-height: 1.6;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }}
        
        .header {{
            background: rgba(30, 30, 46, 0.95);
            color: white;
            padding: 20px 0;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
        }}
        
        .header h1 {{
            font-size: 2.5em;
            text-align: center;
            margin-bottom: 5px;
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1);
            background-clip: text;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: glow 2s ease-in-out infinite alternate;
        }}
        
        @keyframes glow {{
            from {{ filter: drop-shadow(0 0 5px rgba(255, 107, 107, 0.5)); }}
            to {{ filter: drop-shadow(0 0 20px rgba(78, 205, 196, 0.8)); }}
        }}
        
        .subtitle {{
            text-align: center;
            font-size: 1.2em;
            margin-bottom: 10px;
            color: #ccc;
        }}
        
        .live-indicator {{
            text-align: center;
            margin-top: 10px;
        }}
        
        .live-dot {{
            display: inline-block;
            width: 12px;
            height: 12px;
            background: #ff4757;
            border-radius: 50%;
            margin-right: 8px;
            animation: pulse 1.5s infinite;
        }}
        
        @keyframes pulse {{
            0% {{ transform: scale(1); opacity: 1; }}
            50% {{ transform: scale(1.2); opacity: 0.7; }}
            100% {{ transform: scale(1); opacity: 1; }}
        }}
        
        .main-content {{
            display: grid;
            grid-template-columns: 1fr 300px;
            gap: 30px;
            margin: 30px 0;
        }}
        
        .articles-section {{
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }}
        
        .sidebar {{
            display: flex;
            flex-direction: column;
            gap: 20px;
        }}
        
        .ranking-box {{
            background: white;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }}
        
        .ranking-title {{
            font-size: 1.3em;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 15px;
            border-bottom: 2px solid #3498db;
            padding-bottom: 5px;
        }}
        
        .ranking-item {{
            display: flex;
            align-items: center;
            padding: 8px 0;
            border-bottom: 1px solid #eee;
        }}
        
        .rank-number {{
            background: #3498db;
            color: white;
            width: 25px;
            height: 25px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.9em;
            font-weight: bold;
            margin-right: 10px;
        }}
        
        .article {{
            background: white;
            border-radius: 12px;
            padding: 25px;
            margin-bottom: 25px;
            box-shadow: 0 3px 15px rgba(0,0,0,0.08);
            border-left: 4px solid #27ae60;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
        
        .article:hover {{
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }}
        
        .article-title {{
            font-size: 1.4em;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 10px;
            line-height: 1.3;
        }}
        
        .article-meta {{
            display: flex;
            gap: 15px;
            margin-bottom: 15px;
            font-size: 0.9em;
            color: #666;
            flex-wrap: wrap;
        }}
        
        .meta-tag {{
            background: #ecf0f1;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 0.8em;
        }}
        
        .meta-tag.reliable {{
            background: #d5f4e6;
            color: #27ae60;
            font-weight: bold;
        }}
        
        .article-content {{
            color: #555;
            margin-bottom: 20px;
            line-height: 1.7;
        }}
        
        .source-link {{
            background: #e8f6f3;
            border: 1px solid #27ae60;
            border-radius: 8px;
            padding: 12px;
            margin-bottom: 15px;
        }}
        
        .source-link a {{
            color: #27ae60;
            text-decoration: none;
            font-weight: bold;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .source-link a:hover {{
            text-decoration: underline;
        }}
        
        .article-stats {{
            display: flex;
            gap: 20px;
            margin-bottom: 20px;
            font-size: 0.9em;
            color: #666;
        }}
        
        .stat-item {{
            display: flex;
            align-items: center;
            gap: 5px;
        }}
        
        .comments-section {{
            border-top: 2px solid #ecf0f1;
            padding-top: 20px;
        }}
        
        .comments-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}
        
        .comments-title {{
            font-size: 1.1em;
            font-weight: bold;
            color: #2c3e50;
        }}
        
        .comment {{
            background: #f8f9fa;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 12px;
            position: relative;
        }}
        
        .comment-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }}
        
        .comment-author {{
            font-weight: bold;
            color: #34495e;
            font-size: 0.9em;
        }}
        
        .comment-time {{
            font-size: 0.8em;
            color: #7f8c8d;
        }}
        
        .comment-text {{
            color: #2c3e50;
            white-space: pre-wrap;
            line-height: 1.5;
        }}
        
        .comment-actions {{
            display: flex;
            gap: 15px;
            margin-top: 10px;
            font-size: 0.9em;
        }}
        
        .comment-action {{
            background: none;
            border: none;
            color: #7f8c8d;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 5px;
            padding: 5px;
            border-radius: 4px;
            transition: all 0.2s;
        }}
        
        .comment-action:hover {{
            background: #ecf0f1;
            color: #2c3e50;
        }}
        
        .comment-form {{
            background: #ecf0f1;
            border-radius: 8px;
            padding: 20px;
            margin-top: 20px;
        }}
        
        .comment-form h4 {{
            margin-bottom: 15px;
            color: #2c3e50;
        }}
        
        .form-group {{
            margin-bottom: 15px;
        }}
        
        .form-group input,
        .form-group textarea {{
            width: 100%;
            padding: 12px;
            border: 1px solid #bdc3c7;
            border-radius: 6px;
            font-size: 0.9em;
            background: white;
        }}
        
        .form-group textarea {{
            resize: vertical;
            min-height: 80px;
        }}
        
        .submit-btn {{
            background: #3498db;
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.9em;
            transition: background 0.2s;
        }}
        
        .submit-btn:hover {{
            background: #2980b9;
        }}
        
        .ad-space {{
            background: #f0f0f0;
            border: 2px dashed #ccc;
            height: 250px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #666;
            font-size: 1.1em;
            margin: 20px 0;
            border-radius: 8px;
        }}
        
        .footer {{
            background: rgba(30, 30, 46, 0.95);
            color: white;
            text-align: center;
            padding: 30px 0;
            margin-top: 50px;
        }}
        
        .update-info {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 20px;
            text-align: center;
        }}
        
        .real-news-badge {{
            background: #27ae60;
            color: white;
            padding: 5px 10px;
            border-radius: 12px;
            font-size: 0.8em;
            font-weight: bold;
            display: inline-block;
            margin-bottom: 10px;
        }}
        
        @media (max-width: 768px) {{
            .main-content {{
                grid-template-columns: 1fr;
                gap: 20px;
            }}
            
            .article {{
                padding: 20px;
            }}
            
            .header h1 {{
                font-size: 2em;
            }}
            
            .comment {{
                padding: 12px;
            }}
            
            .article-meta {{
                flex-direction: column;
                gap: 8px;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="container">
            <h1>🔥 【速報】ニュースまとめ速</h1>
            <div class="subtitle">最新の実際のニュースを最速でお届け！</div>
            <div class="live-indicator">
                <span class="live-dot"></span>
                <span>リアルタイム更新中</span>
            </div>
        </div>
    </div>
    
    <div class="container">
        <div class="real-news-badge">✅ 実際のニュースソースから配信</div>
        
        <div class="update-info">
            <strong>📅 最終更新:</strong> {jst_time.strftime('%Y年%m月%d日 %H:%M:%S')} (JST)<br>
            <strong>🔄 次回更新:</strong> 約15分後 | <strong>📊 記事数:</strong> {len(articles)}件 | <strong>📡 ソース数:</strong> {len(set(a.get('source', '') for a in articles))}個
        </div>
        
        <div class="main-content">
            <div class="articles-section">
                <h2 style="margin-bottom: 25px; color: #2c3e50;">📰 最新の実際のニュース</h2>
                {self._generate_real_articles_html(articles)}
            </div>
            
            <div class="sidebar">
                <div class="ranking-box">
                    <div class="ranking-title">🔥 アクセスランキング</div>
                    {self._generate_ranking_html(hourly_ranking, articles)}
                </div>
                
                <div class="ad-space">
                    💰 広告スペース<br>
                    <small>収益化準備中</small>
                </div>
                
                <div class="ranking-box">
                    <div class="ranking-title">📊 信頼性情報</div>
                    <div style="font-size: 0.9em; line-height: 1.8;">
                        • 実際のニュースソース: ✅<br>
                        • RSS フィード収集: ✅<br>
                        • ソース元リンク: ✅<br>
                        • 信頼性スコア表示: ✅<br>
                        • 自動更新: 15分間隔
                    </div>
                </div>
                
                <div class="ranking-box">
                    <div class="ranking-title">📈 サイト統計</div>
                    <div style="font-size: 0.9em; line-height: 1.8;">
                        • 総記事数: {len(articles)}件<br>
                        • 総コメント数: {self._get_total_comments()}件<br>
                        • 信頼できるソース: {len(set(a.get('source', '') for a in articles))}個<br>
                        • 平均信頼性: {self._get_average_reliability(articles):.1%}
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="footer">
        <div class="container">
            <p>© 2025 【速報】ニュースまとめ速 - 実際のニュースをお届け</p>
            <p style="font-size: 0.9em; margin-top: 10px; color: #bbb;">
                当サイトは信頼できるニュースソースのRSSフィードから情報を収集し、元記事へのリンクを必ず提供しています
            </p>
        </div>
    </div>
    
    <script>
        // Auto-refresh page every 15 minutes
        setTimeout(() => {{
            location.reload();
        }}, 900000);
        
        // Comment functionality
        function likeComment(articleId, commentId) {{
            const likeBtn = event.target;
            const currentLikes = parseInt(likeBtn.textContent.split(' ')[1]);
            likeBtn.innerHTML = `👍 ${{currentLikes + 1}}`;
        }}
        
        function dislikeComment(articleId, commentId) {{
            const dislikeBtn = event.target;
            const currentDislikes = parseInt(dislikeBtn.textContent.split(' ')[1]);
            dislikeBtn.innerHTML = `👎 ${{currentDislikes + 1}}`;
        }}
        
        function submitComment(articleId) {{
            const form = event.target.closest('.comment-form');
            const nameInput = form.querySelector('input[placeholder*="名前"]');
            const textArea = form.querySelector('textarea');
            
            const name = nameInput.value.trim() || '匿名さん';
            const text = textArea.value.trim();
            
            if (!text) {{
                alert('コメントを入力してください');
                return;
            }}
            
            // Create new comment element
            const commentsContainer = form.previousElementSibling;
            const newComment = document.createElement('div');
            newComment.className = 'comment';
            newComment.innerHTML = `
                <div class="comment-header">
                    <span class="comment-author">${{name}}</span>
                    <span class="comment-time">${{new Date().toLocaleString('ja-JP')}}</span>
                </div>
                <div class="comment-text">${{text}}</div>
                <div class="comment-actions">
                    <button class="comment-action" onclick="likeComment('${{articleId}}', 'new')">👍 0</button>
                    <button class="comment-action" onclick="dislikeComment('${{articleId}}', 'new')">👎 0</button>
                </div>
            `;
            
            commentsContainer.appendChild(newComment);
            
            // Clear form
            nameInput.value = '';
            textArea.value = '';
            
            // Update comment count
            const commentTitle = form.parentElement.querySelector('.comments-title');
            const currentCount = parseInt(commentTitle.textContent.match(/\\d+/)[0]);
            commentTitle.textContent = `💬 コメント (${{currentCount + 1}}件)`;
            
            alert('コメントを投稿しました！');
        }}
        
        // External link tracking
        document.addEventListener('click', function(e) {{
            if (e.target.tagName === 'A' && e.target.getAttribute('href').startsWith('http')) {{
                // Track external link clicks
                console.log('External link clicked:', e.target.href);
            }}
        }});
    </script>
</body>
</html>"""
        
        return html_content
    
    def _generate_real_articles_html(self, articles: List[Dict]) -> str:
        """Generate HTML for real articles"""
        html = ""
        
        for i, article in enumerate(articles):
            article_id = article['id']
            comments = self.comment_system.get_comments(article_id)
            stats = self.comment_system.get_article_stats(article_id)
            
            # Generate recent comments for display
            recent_comments = comments[-5:] if len(comments) > 5 else comments
            
            comments_html = ""
            for comment in recent_comments:
                comments_html += f"""
                <div class="comment">
                    <div class="comment-header">
                        <span class="comment-author">{comment['name']}</span>
                        <span class="comment-time">{comment['timestamp']['jst_display']}</span>
                    </div>
                    <div class="comment-text">{comment['text']}</div>
                    <div class="comment-actions">
                        <button class="comment-action" onclick="likeComment('{article_id}', '{comment['id']}')">👍 {comment['likes']}</button>
                        <button class="comment-action" onclick="dislikeComment('{article_id}', '{comment['id']}')">👎 {comment['dislikes']}</button>
                    </div>
                </div>
                """
            
            # Parse published time
            try:
                published_time = datetime.fromisoformat(article['published'].replace('Z', '+00:00'))
                jst_published = published_time + timedelta(hours=9)
                time_display = jst_published.strftime('%m/%d %H:%M')
            except:
                time_display = "不明"
            
            # Reliability indicator
            reliability = article.get('reliability_score', 0.5)
            reliability_text = f"{int(reliability * 100)}%"
            reliability_class = "reliable" if reliability >= 0.8 else ""
            
            html += f"""
            <div class="article" id="{article_id}">
                <div class="article-title">{article['title']}</div>
                <div class="article-meta">
                    <span class="meta-tag">📂 {article['category']}</span>
                    <span class="meta-tag">📰 {article['source']}</span>
                    <span class="meta-tag">🕐 {time_display}</span>
                    <span class="meta-tag {reliability_class}">🛡️ 信頼性 {reliability_text}</span>
                    <span class="meta-tag">🌐 {article['language'].upper()}</span>
                </div>
                
                <div class="source-link">
                    <a href="{article['url']}" target="_blank" rel="noopener">
                        🔗 元記事を読む: {article['source']}
                    </a>
                </div>
                
                <div class="article-content">{article['content']}</div>
                
                <div class="article-stats">
                    <span class="stat-item">👁️ {stats['views']} 閲覧</span>
                    <span class="stat-item">💬 {stats['comments']} コメント</span>
                    <span class="stat-item">👍 {stats['likes']} いいね</span>
                    <span class="stat-item">📊 {stats['engagement_score']} エンゲージメント</span>
                </div>
                
                {f'<div class="ad-space">📰 記事内広告<br><small>準備中</small></div>' if i == 1 else ''}
                
                <div class="comments-section">
                    <div class="comments-header">
                        <span class="comments-title">💬 コメント ({len(comments)}件)</span>
                    </div>
                    
                    <div class="comments-list">
                        {comments_html}
                        {f'<div style="text-align: center; padding: 10px; color: #666;"><small>他 {len(comments) - 5} 件のコメント</small></div>' if len(comments) > 5 else ''}
                    </div>
                    
                    <div class="comment-form">
                        <h4>💭 この記事にコメント</h4>
                        <div class="form-group">
                            <input type="text" placeholder="お名前（任意・匿名可）" maxlength="50">
                        </div>
                        <div class="form-group">
                            <textarea placeholder="コメントを入力してください..." maxlength="500"></textarea>
                        </div>
                        <button class="submit-btn" onclick="submitComment('{article_id}')">💬 コメント投稿</button>
                    </div>
                </div>
            </div>
            """
        
        return html
    
    def _generate_ranking_html(self, ranking_data, articles):
        """Generate ranking HTML"""
        html = ""
        
        for i, item in enumerate(ranking_data[:5], 1):
            # Find article title
            article_title = "記事が見つかりません"
            for article in articles:
                if article['id'] == item['article_id']:
                    article_title = article['title'][:40] + ("..." if len(article['title']) > 40 else "")
                    break
            
            html += f"""
            <div class="ranking-item">
                <div class="rank-number">{i}</div>
                <div style="flex: 1;">
                    <div style="font-size: 0.9em; font-weight: bold; color: #2c3e50; margin-bottom: 3px;">
                        {article_title}
                    </div>
                    <div style="font-size: 0.8em; color: #7f8c8d;">
                        👁️ {item['views']} | 💬 {item['comments']} | 👍 {item['likes']}
                    </div>
                </div>
            </div>
            """
        
        return html or "<div style='text-align: center; color: #666;'>データを集計中...</div>"
    
    def _get_total_comments(self):
        """Get total number of comments"""
        comments = self.comment_system._load_comments()
        total = sum(len(article_comments) for article_comments in comments.values())
        return total
    
    def _get_average_reliability(self, articles):
        """Calculate average reliability score"""
        if not articles:
            return 0.0
        
        total_reliability = sum(article.get('reliability_score', 0.5) for article in articles)
        return total_reliability / len(articles)
    
    def _get_fallback_articles(self):
        """Fallback articles when RSS feeds fail"""
        return [
            {
                'id': 'fallback_001',
                'title': 'RSS フィード収集システムがメンテナンス中です',
                'content': '現在、ニュースソースからの自動収集システムがメンテナンス中のため、一時的にこのメッセージを表示しています。しばらくお待ちください。',
                'url': '#',
                'source': 'システム通知',
                'source_url': '#',
                'category': 'システム',
                'language': 'ja',
                'reliability_score': 1.0,
                'published': datetime.utcnow().isoformat(),
                'fetch_timestamp': datetime.utcnow().isoformat(),
                'is_real_news': False
            }
        ]


def main():
    """Main execution function"""
    try:
        system = RealNewsSystem()
        system.generate_real_news_website()
        
    except Exception as e:
        logger.error(f"💥 Fatal error: {str(e)}")
        raise


if __name__ == "__main__":
    main()