#!/usr/bin/env python3
"""
Real News Fetcher using RSS feeds
Collects news from multiple sources around the world
"""

import os
import sys
import json
import logging
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import xml.etree.ElementTree as ET
from urllib.parse import urlparse

try:
    import feedparser
except ImportError:
    feedparser = None

import httpx
from news_sources import NEWS_SOURCES

logger = logging.getLogger(__name__)

class NewsFetcher:
    def __init__(self):
        self.sources = NEWS_SOURCES['rss_feeds']
        self.client = httpx.Client(
            timeout=30.0,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        )
        self.fetched_articles = []
        self.seen_urls = set()
        
    def fetch_all_feeds(self, max_per_feed: int = 5) -> List[Dict]:
        """
        Fetch news from all configured RSS feeds
        """
        all_articles = []
        
        for feed_info in self.sources:
            try:
                logger.info(f"Fetching from {feed_info['name']}")
                articles = self.fetch_rss_feed(feed_info, max_per_feed)
                all_articles.extend(articles)
                logger.info(f"Fetched {len(articles)} articles from {feed_info['name']}")
            except Exception as e:
                logger.error(f"Error fetching {feed_info['name']}: {str(e)}")
                
        # Remove duplicates
        unique_articles = self._remove_duplicates(all_articles)
        logger.info(f"Total unique articles: {len(unique_articles)}")
        
        return unique_articles
    
    def fetch_rss_feed(self, feed_info: Dict, max_items: int = 5) -> List[Dict]:
        """
        Fetch and parse a single RSS feed
        """
        articles = []
        
        try:
            response = self.client.get(feed_info['url'])
            response.raise_for_status()
            
            if feedparser:
                # Use feedparser if available
                feed = feedparser.parse(response.text)
                
                for entry in feed.entries[:max_items]:
                    article = self._parse_feed_entry(entry, feed_info)
                    if article and article['url'] not in self.seen_urls:
                        articles.append(article)
                        self.seen_urls.add(article['url'])
            else:
                # Fallback to basic XML parsing
                articles = self._parse_rss_xml(response.text, feed_info, max_items)
                
        except Exception as e:
            logger.error(f"Failed to fetch {feed_info['url']}: {str(e)}")
            
        return articles
    
    def _parse_feed_entry(self, entry: Dict, feed_info: Dict) -> Optional[Dict]:
        """
        Parse a single feed entry (feedparser format)
        """
        try:
            # Extract basic information
            title = entry.get('title', '').strip()
            url = entry.get('link', '')
            
            if not title or not url:
                return None
                
            # Get content
            content = ''
            if hasattr(entry, 'summary'):
                content = entry.summary
            elif hasattr(entry, 'description'):
                content = entry.description
                
            # Get publish date
            published = None
            if hasattr(entry, 'published_parsed'):
                published = datetime(*entry.published_parsed[:6])
            elif hasattr(entry, 'updated_parsed'):
                published = datetime(*entry.updated_parsed[:6])
            else:
                published = datetime.utcnow()
                
            # Create article object
            article = {
                'title': title,
                'url': url,
                'content': self._clean_html(content),
                'source': feed_info['name'],
                'language': feed_info['lang'],
                'published': published.isoformat() if published else datetime.utcnow().isoformat(),
                'fetch_timestamp': datetime.utcnow().isoformat(),
                'original_language': feed_info['lang'],
                'needs_translation': feed_info['lang'] != 'ja'
            }
            
            return article
            
        except Exception as e:
            logger.error(f"Error parsing entry: {str(e)}")
            return None
    
    def _parse_rss_xml(self, xml_content: str, feed_info: Dict, max_items: int) -> List[Dict]:
        """
        Fallback XML parser for RSS feeds
        """
        articles = []
        
        try:
            root = ET.fromstring(xml_content)
            
            # Find all items
            items = root.findall('.//item')
            if not items:
                items = root.findall('.//entry')  # Atom format
                
            for item in items[:max_items]:
                title_elem = item.find('title')
                link_elem = item.find('link')
                desc_elem = item.find('description') or item.find('summary')
                pub_elem = item.find('pubDate') or item.find('published')
                
                if title_elem is not None and link_elem is not None:
                    url = link_elem.text or link_elem.get('href', '')
                    
                    if url not in self.seen_urls:
                        article = {
                            'title': title_elem.text or '',
                            'url': url,
                            'content': self._clean_html(desc_elem.text if desc_elem is not None else ''),
                            'source': feed_info['name'],
                            'language': feed_info['lang'],
                            'published': pub_elem.text if pub_elem is not None else datetime.utcnow().isoformat(),
                            'fetch_timestamp': datetime.utcnow().isoformat(),
                            'original_language': feed_info['lang'],
                            'needs_translation': feed_info['lang'] != 'ja'
                        }
                        articles.append(article)
                        self.seen_urls.add(url)
                        
        except Exception as e:
            logger.error(f"XML parsing error: {str(e)}")
            
        return articles
    
    def _clean_html(self, html_content: str) -> str:
        """
        Remove HTML tags and clean content
        """
        import re
        
        if not html_content:
            return ''
            
        # Remove HTML tags
        clean = re.sub('<.*?>', '', html_content)
        # Remove extra whitespace
        clean = ' '.join(clean.split())
        # Limit length
        if len(clean) > 500:
            clean = clean[:497] + '...'
            
        return clean
    
    def _remove_duplicates(self, articles: List[Dict]) -> List[Dict]:
        """
        Remove duplicate articles based on URL and similar titles
        """
        unique = []
        seen_urls = set()
        seen_titles = set()
        
        for article in articles:
            url = article['url']
            title_hash = hashlib.md5(article['title'].lower().encode()).hexdigest()
            
            if url not in seen_urls and title_hash not in seen_titles:
                unique.append(article)
                seen_urls.add(url)
                seen_titles.add(title_hash)
                
        return unique
    
    def filter_recent(self, articles: List[Dict], hours: int = 24) -> List[Dict]:
        """
        Filter articles to only include recent ones
        """
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        recent = []
        
        for article in articles:
            try:
                pub_date = datetime.fromisoformat(article['published'].replace('Z', '+00:00'))
                if pub_date > cutoff:
                    recent.append(article)
            except (ValueError, KeyError, TypeError) as e:
                # If date parsing fails, include the article
                logger.warning(f"Date parsing failed for article: {e}")
                recent.append(article)
                
        return recent
    
    def categorize_articles(self, articles: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Categorize articles by region and topic
        """
        categorized = {
            'by_language': {},
            'by_source': {},
            'all': articles
        }
        
        for article in articles:
            # By language
            lang = article['language']
            if lang not in categorized['by_language']:
                categorized['by_language'][lang] = []
            categorized['by_language'][lang].append(article)
            
            # By source
            source = article['source']
            if source not in categorized['by_source']:
                categorized['by_source'][source] = []
            categorized['by_source'][source].append(article)
            
        return categorized
    
    def close(self):
        """Close HTTP client"""
        self.client.close()