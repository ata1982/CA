#!/usr/bin/env python3
"""
Extended News Fetcher with SNS Trends, Gossip, and 100+ Categories
Advanced features: Rate limiting, multi-language, trend analysis, viral detection
"""

import os
import sys
import json
import logging
import hashlib
import asyncio
import time
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse, parse_qs
import xml.etree.ElementTree as ET

try:
    import feedparser
    import httpx
    from bs4 import BeautifulSoup
except ImportError:
    feedparser = None
    httpx = None
    BeautifulSoup = None

from news_sources_extended import (
    NEWS_SOURCES, SNS_TREND_SOURCES, GLOBAL_NEWS_SOURCES,
    SPECIAL_CATEGORIES, RELIABILITY_SCORES, SENSITIVE_LEVELS,
    TREND_ANALYSIS_PROMPT
)

logger = logging.getLogger(__name__)

class ExtendedNewsFetcher:
    def __init__(self):
        if httpx is None:
            raise ImportError("httpx library is required")
        
        self.client = httpx.AsyncClient(
            timeout=30.0,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        )
        
        # Rate limiting
        self.rate_limits = {
            'youtube': {'calls': 0, 'reset_time': time.time() + 3600, 'max_calls': 100},
            'twitter': {'calls': 0, 'reset_time': time.time() + 900, 'max_calls': 15},
            'reddit': {'calls': 0, 'reset_time': time.time() + 60, 'max_calls': 60},
            'default': {'calls': 0, 'reset_time': time.time() + 60, 'max_calls': 30}
        }
        
        self.trending_keywords = {}
        self.viral_threshold = 1000  # ソーシャルメトリクス閾値
        
    async def fetch_all_extended_feeds(self, max_per_category: int = 3) -> List[Dict]:
        """
        全拡張カテゴリからニュースを収集
        """
        all_articles = []
        
        # メインニュースソース
        for category, sources in NEWS_SOURCES.items():
            logger.info(f"Fetching {category} news...")
            try:
                category_articles = await self._fetch_category_sources(sources, category, max_per_category)
                all_articles.extend(category_articles)
            except Exception as e:
                logger.error(f"Error fetching {category}: {str(e)}")
        
        # SNSトレンド
        sns_articles = await self._fetch_sns_trends()
        all_articles.extend(sns_articles)
        
        # グローバルニュース
        global_articles = await self._fetch_global_sources()
        all_articles.extend(global_articles)
        
        # 特殊カテゴリ
        special_articles = await self._fetch_special_categories()
        all_articles.extend(special_articles)
        
        # 重複除去とソート
        unique_articles = self._remove_duplicates_advanced(all_articles)
        sorted_articles = self._sort_by_viral_score(unique_articles)
        
        logger.info(f"Collected {len(sorted_articles)} unique articles from 100+ sources")
        return sorted_articles
    
    async def _fetch_category_sources(self, sources: List[Dict], category: str, max_items: int) -> List[Dict]:
        """
        カテゴリ内のソースを並列取得
        """
        tasks = []
        for source in sources[:10]:  # レート制限対策で10ソースまで
            if self._check_rate_limit(self._get_source_type(source['url'])):
                task = self._fetch_single_source(source, category, max_items)
                tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        articles = []
        for result in results:
            if isinstance(result, list):
                articles.extend(result)
            elif isinstance(result, Exception):
                logger.error(f"Source fetch failed: {str(result)}")
        
        return articles
    
    async def _fetch_single_source(self, source: Dict, category: str, max_items: int) -> List[Dict]:
        """
        単一ソースからの記事取得
        """
        try:
            response = await self.client.get(source['url'])
            response.raise_for_status()
            
            articles = []
            if source['url'].endswith('.xml') or 'rss' in source['url']:
                articles = self._parse_rss_feed(response.text, source, category, max_items)
            else:
                # HTMLスクレイピング
                articles = await self._scrape_html_content(response.text, source, category, max_items)
            
            # 信頼性スコアの付与
            for article in articles:
                article['reliability_score'] = self._calculate_reliability_score(source, article)
                article['sensitive_level'] = self._calculate_sensitive_level(article)
                article['viral_score'] = await self._calculate_viral_score(article)
            
            return articles
            
        except Exception as e:
            logger.error(f"Failed to fetch {source['url']}: {str(e)}")
            return []
    
    def _parse_rss_feed(self, xml_content: str, source: Dict, category: str, max_items: int) -> List[Dict]:
        """
        RSS/XMLフィードの解析
        """
        articles = []
        
        try:
            if feedparser:
                feed = feedparser.parse(xml_content)
                entries = feed.entries[:max_items]
                
                for entry in entries:
                    article = {
                        'id': hashlib.md5(f"{entry.get('link', '')}{entry.get('title', '')}".encode()).hexdigest()[:8],
                        'title': entry.get('title', '').strip(),
                        'url': entry.get('link', ''),
                        'content': self._clean_html(entry.get('summary', entry.get('description', ''))),
                        'source': source['name'],
                        'language': source['lang'],
                        'category': category,
                        'published': self._parse_date(entry.get('published', '')),
                        'fetch_timestamp': datetime.utcnow().isoformat(),
                        'needs_translation': source['lang'] != 'ja'
                    }
                    articles.append(article)
            else:
                # フォールバック: 基本XML解析
                articles = self._parse_xml_basic(xml_content, source, category, max_items)
                
        except Exception as e:
            logger.error(f"RSS parsing error: {str(e)}")
            
        return articles
    
    async def _scrape_html_content(self, html: str, source: Dict, category: str, max_items: int) -> List[Dict]:
        """
        HTMLコンテンツのスクレイピング（トレンドサイト対応）
        """
        articles = []
        
        if not BeautifulSoup:
            return articles
            
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # サイト別の解析ロジック
            if 'twitter' in source['url'] or 'trends' in source['url']:
                articles = await self._parse_trend_site(soup, source, category)
            elif 'youtube' in source['url']:
                articles = await self._parse_youtube_trends(soup, source, category)
            elif 'reddit' in source['url']:
                articles = await self._parse_reddit_content(soup, source, category)
            else:
                # 一般的なニュースサイト
                articles = self._parse_generic_news_site(soup, source, category, max_items)
                
        except Exception as e:
            logger.error(f"HTML scraping error for {source['url']}: {str(e)}")
            
        return articles
    
    async def _fetch_sns_trends(self) -> List[Dict]:
        """
        SNSトレンドの収集
        """
        trend_articles = []
        
        # Twitter/Xトレンド
        twitter_trends = await self._fetch_twitter_trends()
        trend_articles.extend(twitter_trends)
        
        # YouTubeトレンド
        youtube_trends = await self._fetch_youtube_trends()
        trend_articles.extend(youtube_trends)
        
        # Redditトレンド
        reddit_trends = await self._fetch_reddit_trends()
        trend_articles.extend(reddit_trends)
        
        # ゴシップサイト
        gossip_articles = await self._fetch_gossip_sources()
        trend_articles.extend(gossip_articles)
        
        return trend_articles
    
    async def _fetch_twitter_trends(self) -> List[Dict]:
        """
        Twitterトレンドの取得（スクレイピング）
        """
        trends = []
        
        if not self._check_rate_limit('twitter'):
            return trends
            
        try:
            # Yahoo!リアルタイム検索をスクレイピング
            url = 'https://search.yahoo.co.jp/realtime'
            response = await self.client.get(url)
            
            if BeautifulSoup:
                soup = BeautifulSoup(response.text, 'html.parser')
                trend_elements = soup.find_all('a', class_='trendword')
                
                for element in trend_elements[:10]:
                    keyword = element.get_text().strip()
                    if keyword:
                        trend_article = {
                            'id': hashlib.md5(f"trend_{keyword}_{datetime.utcnow()}".encode()).hexdigest()[:8],
                            'title': f"【トレンド】{keyword}",
                            'content': f"'{keyword}'がTwitterでトレンド入りしています。",
                            'source': 'Twitter Trends',
                            'language': 'ja',
                            'category': 'sns_trend',
                            'trend_keyword': keyword,
                            'platform': 'twitter',
                            'viral_score': 500,  # トレンド入りは高スコア
                            'reliability_score': 0.6,
                            'sensitive_level': 3,
                            'published': datetime.utcnow().isoformat()
                        }
                        trends.append(trend_article)
                        
        except Exception as e:
            logger.error(f"Twitter trends fetch error: {str(e)}")
            
        return trends
    
    async def _fetch_youtube_trends(self) -> List[Dict]:
        """
        YouTube急上昇動画の取得
        """
        trends = []
        
        if not self._check_rate_limit('youtube'):
            return trends
            
        try:
            # YouTubeチャンネルのRSSフィードから
            youtube_sources = SNS_TREND_SOURCES['youtube_sources']
            
            for source in youtube_sources[:5]:  # レート制限
                response = await self.client.get(source['url'])
                if response.status_code == 200:
                    videos = self._parse_youtube_rss(response.text, source)
                    trends.extend(videos)
                    
        except Exception as e:
            logger.error(f"YouTube trends fetch error: {str(e)}")
            
        return trends
    
    def _parse_youtube_rss(self, xml_content: str, source: Dict) -> List[Dict]:
        """
        YouTubeチャンネルのRSS解析
        """
        videos = []
        
        try:
            root = ET.fromstring(xml_content)
            entries = root.findall('.//{http://www.w3.org/2005/Atom}entry')
            
            for entry in entries[:3]:
                title_elem = entry.find('.//{http://www.w3.org/2005/Atom}title')
                link_elem = entry.find('.//{http://www.w3.org/2005/Atom}link')
                published_elem = entry.find('.//{http://www.w3.org/2005/Atom}published')
                
                if title_elem is not None and link_elem is not None:
                    video_id = self._extract_youtube_id(link_elem.get('href', ''))
                    
                    video_article = {
                        'id': f"yt_{video_id}",
                        'title': title_elem.text,
                        'content': f"{source['name']}の最新動画",
                        'url': link_elem.get('href', ''),
                        'source': source['name'],
                        'language': source['lang'],
                        'category': 'youtube_trend',
                        'platform': 'youtube',
                        'video_id': video_id,
                        'thumbnail_url': f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg",
                        'channel_name': source['name'],
                        'viral_score': 300,  # YouTube動画は中程度
                        'reliability_score': 0.7,
                        'sensitive_level': 2,
                        'published': published_elem.text if published_elem is not None else datetime.utcnow().isoformat()
                    }
                    videos.append(video_article)
                    
        except Exception as e:
            logger.error(f"YouTube RSS parsing error: {str(e)}")
            
        return videos
    
    def _extract_youtube_id(self, url: str) -> str:
        """
        YouTube URLから動画IDを抽出
        """
        try:
            if 'watch?v=' in url:
                return url.split('watch?v=')[1].split('&')[0]
            elif 'youtu.be/' in url:
                return url.split('youtu.be/')[1].split('?')[0]
        except:
            pass
        return ''
    
    async def _fetch_gossip_sources(self) -> List[Dict]:
        """
        ゴシップ・炎上系ソースの取得
        """
        gossip_articles = []
        
        for region, sources in SNS_TREND_SOURCES['gossip_sources'].items():
            for source in sources[:3]:  # 各地域3ソースまで
                try:
                    if self._check_rate_limit('default'):
                        articles = await self._fetch_single_source(source, 'gossip', 3)
                        
                        # ゴシップ系は特別な処理
                        for article in articles:
                            article['gossip_region'] = region
                            article['fact_checked'] = False
                            article['controversy_level'] = self._assess_controversy_level(article)
                            
                        gossip_articles.extend(articles)
                        
                except Exception as e:
                    logger.error(f"Gossip source error: {str(e)}")
                    
        return gossip_articles
    
    async def _calculate_viral_score(self, article: Dict) -> int:
        """
        バイラルスコアの計算
        """
        score = 100  # ベーススコア
        
        # ソース別重み付け
        if 'twitter' in article.get('source', '').lower():
            score += 200
        elif 'youtube' in article.get('source', '').lower():
            score += 150
        elif 'reddit' in article.get('source', '').lower():
            score += 100
        
        # キーワード分析
        title = article.get('title', '').lower()
        content = article.get('content', '').lower()
        
        viral_keywords = ['炎上', '話題', 'トレンド', '急上昇', 'バズ', '大炎上', '物議']
        for keyword in viral_keywords:
            if keyword in title or keyword in content:
                score += 50
        
        # 緊急性キーワード
        urgent_keywords = ['速報', '緊急', '突然', '衝撃', '暴露']
        for keyword in urgent_keywords:
            if keyword in title:
                score += 30
        
        # 時間経過による減衰
        try:
            published = datetime.fromisoformat(article.get('published', '').replace('Z', '+00:00'))
            hours_old = (datetime.utcnow() - published.replace(tzinfo=None)).total_seconds() / 3600
            
            if hours_old < 1:
                score += 100  # 1時間以内
            elif hours_old < 6:
                score += 50   # 6時間以内
            elif hours_old > 24:
                score -= 50   # 24時間以上は減点
                
        except:
            pass
        
        return max(0, min(1000, score))  # 0-1000の範囲
    
    def _calculate_reliability_score(self, source: Dict, article: Dict) -> float:
        """
        信頼性スコアの計算
        """
        base_score = source.get('reliability', 0.7)
        
        # ソースタイプ別調整
        source_name = source.get('name', '').lower()
        
        if any(keyword in source_name for keyword in ['nhk', 'bbc', 'reuters', 'ap']):
            return 0.9  # 大手報道機関
        elif any(keyword in source_name for keyword in ['政府', 'official', '省庁']):
            return 0.95  # 公式発表
        elif any(keyword in source_name for keyword in ['gossip', 'rumor', '爆サイ']):
            return 0.3   # ゴシップ系
        elif 'youtube' in source_name:
            return 0.5   # YouTube系
        
        return base_score
    
    def _calculate_sensitive_level(self, article: Dict) -> int:
        """
        センシティブ度の計算
        """
        level = 1  # ベースレベル
        
        title = article.get('title', '').lower()
        content = article.get('content', '').lower()
        
        # 炎上・対立系キーワード
        controversial_keywords = [
            '炎上', '批判', '謝罪', '物議', '賛否両論', '問題発言',
            '不倫', 'スキャンダル', '暴露', '告発', '訴訟'
        ]
        
        for keyword in controversial_keywords:
            if keyword in title or keyword in content:
                level += 2
        
        # 政治・宗教関連
        political_keywords = ['政治', '選挙', '政権', '総理', '大統領']
        religious_keywords = ['宗教', '神', '仏教', 'キリスト教', 'イスラム']
        
        for keyword in political_keywords + religious_keywords:
            if keyword in title or keyword in content:
                level += 1
        
        return min(10, level)
    
    def _assess_controversy_level(self, article: Dict) -> int:
        """
        論争レベルの評価
        """
        title = article.get('title', '').lower()
        content = article.get('content', '').lower()
        
        controversy_indicators = [
            '大炎上', '総叩き', '猛批判', '大問題', '大騒動',
            '謝罪', '撤回', '削除', '釈明', '弁明'
        ]
        
        level = 0
        for indicator in controversy_indicators:
            if indicator in title:
                level += 3
            elif indicator in content:
                level += 1
        
        return min(10, level)
    
    def _sort_by_viral_score(self, articles: List[Dict]) -> List[Dict]:
        """
        バイラルスコア順でソート
        """
        return sorted(articles, key=lambda x: x.get('viral_score', 0), reverse=True)
    
    def _remove_duplicates_advanced(self, articles: List[Dict]) -> List[Dict]:
        """
        高度な重複除去（タイトル類似度も考慮）
        """
        unique = []
        seen_urls = set()
        seen_titles = set()
        
        for article in articles:
            url = article.get('url', '')
            title = article.get('title', '').lower()
            
            # URL重複チェック
            if url and url in seen_urls:
                continue
                
            # タイトル類似度チェック（簡易版）
            is_similar = False
            for seen_title in seen_titles:
                if self._calculate_title_similarity(title, seen_title) > 0.8:
                    is_similar = True
                    break
            
            if not is_similar:
                unique.append(article)
                if url:
                    seen_urls.add(url)
                seen_titles.add(title)
        
        return unique
    
    def _calculate_title_similarity(self, title1: str, title2: str) -> float:
        """
        タイトル類似度の計算（簡易版）
        """
        words1 = set(title1.split())
        words2 = set(title2.split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _check_rate_limit(self, source_type: str) -> bool:
        """
        レート制限チェック
        """
        current_time = time.time()
        limit_info = self.rate_limits.get(source_type, self.rate_limits['default'])
        
        # リセット時間チェック
        if current_time > limit_info['reset_time']:
            limit_info['calls'] = 0
            limit_info['reset_time'] = current_time + (3600 if source_type == 'youtube' else 900)
        
        # コール数チェック
        if limit_info['calls'] >= limit_info['max_calls']:
            return False
        
        limit_info['calls'] += 1
        return True
    
    def _get_source_type(self, url: str) -> str:
        """
        URLからソースタイプを判定
        """
        if 'youtube' in url:
            return 'youtube'
        elif 'twitter' in url or 'x.com' in url:
            return 'twitter'
        elif 'reddit' in url:
            return 'reddit'
        else:
            return 'default'
    
    def _clean_html(self, html_content: str) -> str:
        """
        HTML内容のクリーニング
        """
        if not html_content:
            return ''
        
        # HTMLタグ除去
        clean = re.sub('<.*?>', '', html_content)
        # 余分な空白除去
        clean = ' '.join(clean.split())
        # 長さ制限
        if len(clean) > 500:
            clean = clean[:497] + '...'
        
        return clean
    
    def _parse_date(self, date_str: str) -> str:
        """
        日付文字列の正規化
        """
        if not date_str:
            return datetime.utcnow().isoformat()
        
        try:
            # 一般的な日付フォーマットを試行
            from dateutil import parser
            parsed_date = parser.parse(date_str)
            return parsed_date.isoformat()
        except:
            return datetime.utcnow().isoformat()
    
    async def close(self):
        """
        クライアントのクローズ
        """
        await self.client.aclose()

# 使用例
async def main():
    fetcher = ExtendedNewsFetcher()
    try:
        articles = await fetcher.fetch_all_extended_feeds(max_per_category=2)
        print(f"Fetched {len(articles)} articles")
        
        # トップ10のバイラル記事を表示
        for i, article in enumerate(articles[:10], 1):
            print(f"{i}. {article['title']} (Score: {article.get('viral_score', 0)})")
            
    finally:
        await fetcher.close()

if __name__ == "__main__":
    asyncio.run(main())