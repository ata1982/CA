#!/usr/bin/env python3
"""
News Sources Configuration
Real news feeds from around the world
"""

NEWS_SOURCES = {
    'rss_feeds': [
        # Japanese
        {'url': 'https://news.google.com/rss?hl=ja&gl=JP&ceid=JP:ja', 'name': 'Google News Japan', 'lang': 'ja'},
        {'url': 'https://www3.nhk.or.jp/rss/news/cat0.xml', 'name': 'NHK General', 'lang': 'ja'},
        
        # English - Global
        {'url': 'https://feeds.bbci.co.uk/news/world/rss.xml', 'name': 'BBC World', 'lang': 'en'},
        {'url': 'https://rss.nytimes.com/services/xml/rss/nyt/World.xml', 'name': 'NY Times World', 'lang': 'en'},
        {'url': 'https://www.aljazeera.com/xml/rss/all.xml', 'name': 'Al Jazeera', 'lang': 'en'},
        {'url': 'https://feeds.bloomberg.com/markets/news.rss', 'name': 'Bloomberg Markets', 'lang': 'en'},
        
        # Technology
        {'url': 'https://feeds.arstechnica.com/arstechnica/index', 'name': 'Ars Technica', 'lang': 'en'},
        {'url': 'https://techcrunch.com/feed/', 'name': 'TechCrunch', 'lang': 'en'},
        
        # Regional
        {'url': 'https://rss.cnn.com/rss/edition_world.rss', 'name': 'CNN World', 'lang': 'en'},
        {'url': 'https://www.reuters.com/rssFeed/worldNews', 'name': 'Reuters World', 'lang': 'en'},
    ],
    
    'regions': {
        'asia': {
            'countries': ['japan', 'china', 'korea', 'india', 'singapore'],
            'languages': ['ja', 'zh', 'ko', 'hi', 'en']
        },
        'europe': {
            'countries': ['uk', 'france', 'germany', 'italy', 'spain'],
            'languages': ['en', 'fr', 'de', 'it', 'es']
        },
        'americas': {
            'countries': ['usa', 'canada', 'brazil', 'mexico', 'argentina'],
            'languages': ['en', 'fr', 'pt', 'es']
        },
        'middle_east': {
            'countries': ['uae', 'saudi', 'israel', 'egypt'],
            'languages': ['ar', 'en', 'he']
        },
        'africa': {
            'countries': ['south_africa', 'egypt', 'nigeria', 'kenya'],
            'languages': ['en', 'ar', 'fr']
        },
        'oceania': {
            'countries': ['australia', 'new_zealand'],
            'languages': ['en']
        }
    },
    
    'categories': [
        'technology',
        'business',
        'politics',
        'science',
        'health',
        'environment',
        'sports',
        'culture'
    ],
    
    'language_names': {
        'ja': '日本語',
        'en': '英語',
        'zh': '中国語',
        'ko': '韓国語',
        'es': 'スペイン語',
        'fr': 'フランス語',
        'de': 'ドイツ語',
        'ar': 'アラビア語',
        'pt': 'ポルトガル語',
        'hi': 'ヒンディー語',
        'it': 'イタリア語',
        'he': 'ヘブライ語'
    }
}