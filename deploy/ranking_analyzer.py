#!/usr/bin/env python3
"""
News Ranking Analyzer
各ニュースサイトの人気記事ランキングを分析し、バイラルパターンを学習
"""

import os
import sys
import json
import logging
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import re

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import httpx
    from bs4 import BeautifulSoup
except ImportError:
    httpx = None
    BeautifulSoup = None

logger = logging.getLogger(__name__)

class NewsRankingAnalyzer:
    def __init__(self):
        self.news_sites = {
            'yahoo_news': {
                'url': 'https://news.yahoo.co.jp/ranking/access/news',
                'ranking_selector': '.newsFeed_item',
                'title_selector': '.newsFeed_item_title',
                'category': '総合'
            },
            'livedoor': {
                'url': 'http://news.livedoor.com/ranking/',
                'ranking_selector': '.rankingList li',
                'title_selector': 'a',
                'category': '総合'
            },
            'oricon': {
                'url': 'https://www.oricon.co.jp/news/rank/',
                'ranking_selector': '.ranking-box li',
                'title_selector': 'a',
                'category': 'エンタメ'
            },
            'modelpress': {
                'url': 'https://mdpr.jp/ranking',
                'ranking_selector': '.p-ranking__item',
                'title_selector': '.p-ranking__title',
                'category': 'エンタメ'
            },
            'itmedia': {
                'url': 'https://www.itmedia.co.jp/news/ranking/',
                'ranking_selector': '.colBoxRanking li',
                'title_selector': 'a',
                'category': 'IT'
            },
            'nlab': {
                'url': 'https://nlab.itmedia.co.jp/nl/subtop/ranking.html',
                'ranking_selector': '.c-ranking__item',
                'title_selector': '.c-ranking__title',
                'category': 'ネット'
            }
        }
        
        self.pattern_analyzer = PatternAnalyzer()
        self.ranking_history = []
        
        if httpx:
            self.client = httpx.Client(
                timeout=30.0,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )
        else:
            self.client = None
    
    def collect_all_rankings(self):
        """全ニュースサイトのランキングを収集"""
        all_rankings = {}
        
        # httpxが利用できない場合はダミーデータを返す
        if not self.client or not BeautifulSoup:
            logger.warning("httpx or BeautifulSoup not available, using dummy data")
            return self._get_dummy_rankings()
        
        for site_name, config in self.news_sites.items():
            try:
                logger.info(f"Collecting rankings from {site_name}")
                rankings = self.scrape_ranking(site_name, config)
                all_rankings[site_name] = rankings
                
                # パターン分析
                if rankings:
                    self.pattern_analyzer.analyze_titles(rankings, config['category'])
                
            except Exception as e:
                logger.error(f"Error scraping {site_name}: {e}")
                continue
        
        # 履歴に保存
        self.ranking_history.append({
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'rankings': all_rankings
        })
        
        return all_rankings
    
    def scrape_ranking(self, site_name, config):
        """個別サイトのランキングをスクレイピング"""
        try:
            response = self.client.get(config['url'])
            if response.status_code != 200:
                logger.error(f"Failed to fetch {site_name}: {response.status_code}")
                return []
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            rankings = []
            items = soup.select(config['ranking_selector'])[:20]  # TOP20
            
            for i, item in enumerate(items):
                title_elem = item.select_one(config['title_selector'])
                if title_elem:
                    title_text = title_elem.text.strip()
                    rankings.append({
                        'rank': i + 1,
                        'title': title_text,
                        'url': title_elem.get('href', ''),
                        'category': config['category']
                    })
            
            return rankings
            
        except Exception as e:
            logger.error(f"Error in scrape_ranking for {site_name}: {e}")
            return []
    
    def _get_dummy_rankings(self):
        """ダミーのランキングデータを生成"""
        dummy_titles = {
            'yahoo_news': [
                "【速報】有名俳優Aが電撃結婚！お相手は20代モデル",
                "【衝撃】人気アイドルBが涙の告白「もう限界でした」",
                "政府が新たな経済対策を発表、総額30兆円規模",
                "【独占】大物芸人Cの不倫疑惑、本人が激白",
                "プロ野球選手Dが年俸5億円で契約更改"
            ],
            'oricon': [
                "【写真20枚】美人女優Eのすっぴん姿が話題",
                "人気俳優Fが熱愛発覚！デート現場を激写",
                "【動画】アイドルGの新曲MVが1000万回再生突破",
                "大物歌手Hが活動休止を発表、ファン騒然",
                "【ランキング】今年最も輝いた俳優TOP10"
            ],
            'itmedia': [
                "【速報】新型iPhone発表、価格は20万円超えか",
                "AI技術で年収1000万円超えエンジニアが急増",
                "【解説】話題のChatGPT最新版、何が変わった？",
                "大手IT企業が大規模リストラを発表",
                "【比較】最新スマホ性能ランキングTOP5"
            ]
        }
        
        all_rankings = {}
        for site, titles in dummy_titles.items():
            rankings = []
            for i, title in enumerate(titles):
                rankings.append({
                    'rank': i + 1,
                    'title': title,
                    'url': f"https://example.com/{site}/{i+1}",
                    'category': self.news_sites.get(site, {}).get('category', '総合')
                })
            all_rankings[site] = rankings
            
            # パターン分析
            self.pattern_analyzer.analyze_titles(
                rankings, 
                self.news_sites.get(site, {}).get('category', '総合')
            )
        
        return all_rankings
    
    def identify_viral_patterns(self):
        """バイラルになりやすい記事パターンを特定"""
        patterns = self.pattern_analyzer.get_viral_patterns()
        
        return {
            'hot_keywords': patterns['keywords'],
            'title_patterns': patterns['patterns'],
            'optimal_length': patterns['length'],
            'emotion_triggers': patterns['emotions']
        }
    
    def save_analysis_data(self):
        """分析データを保存"""
        try:
            data_dir = Path('.')
            analysis_file = data_dir / 'ranking_analysis.json'
            
            analysis_data = {
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'rankings': self.ranking_history[-1]['rankings'] if self.ranking_history else {},
                'viral_patterns': self.identify_viral_patterns(),
                'top_trends': self.pattern_analyzer.get_top_trends()
            }
            
            with open(analysis_file, 'w', encoding='utf-8') as f:
                json.dump(analysis_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Analysis data saved to {analysis_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving analysis data: {e}")
            return False
    
    def close(self):
        """Close HTTP client"""
        if self.client:
            self.client.close()


class PatternAnalyzer:
    def __init__(self):
        self.title_database = []
        self.keyword_frequency = {}
        self.successful_patterns = []
        
    def analyze_titles(self, rankings, category):
        """タイトルパターンを分析"""
        for item in rankings[:10]:  # TOP10のみ分析
            title = item['title']
            
            # キーワード抽出
            keywords = self.extract_keywords(title)
            for keyword in keywords:
                key = f"{category}:{keyword}"
                self.keyword_frequency[key] = self.keyword_frequency.get(key, 0) + (11 - item['rank'])
            
            # パターン抽出
            patterns = self.extract_pattern(title)
            self.successful_patterns.append({
                'pattern': patterns,
                'category': category,
                'rank': item['rank'],
                'original': title
            })
            
            # データベースに追加
            self.title_database.append({
                'title': title,
                'category': category,
                'rank': item['rank'],
                'keywords': keywords,
                'patterns': patterns,
                'length': len(title)
            })
    
    def extract_keywords(self, title):
        """重要キーワードを抽出"""
        # 高頻度で出現する煽りワード
        hot_words = [
            '衝撃', '速報', '緊急', '発覚', '激白', '告白', '暴露',
            '炎上', '批判', '反論', '激怒', '号泣', '涙',
            '結婚', '離婚', '破局', '熱愛', '不倫', 'スキャンダル',
            '逮捕', '書類送検', '起訴', '判決',
            '引退', '卒業', '活動休止', '解散',
            '初', '最後', '限定', '独占', 'スクープ',
            'ヤバい', 'ヤバすぎ', '神', '最強', '最悪',
            '1位', 'ランキング', 'TOP', '最新',
            '美人', 'イケメン', 'かわいい', 'セクシー',
            '年収', '億', '万円', '給料', '資産',
            '激変', '変貌', '激太り', '激やせ', '整形',
            'すっぴん', '私服', 'プライベート', '密着',
            '写真', '動画', '画像', '激写',
            '発表', '決定', '判明', '確定',
            '理由', '真相', '本音', '裏側',
            '悲報', '朗報', '訃報', '吉報'
        ]
        
        found_keywords = []
        for word in hot_words:
            if word in title:
                found_keywords.append(word)
        
        return found_keywords
    
    def extract_pattern(self, title):
        """タイトルの構造パターンを抽出"""
        patterns = []
        
        # 【】の使用
        if '【' in title and '】' in title:
            patterns.append('bracket_emphasis')
        
        # 「」の使用
        if '「' in title and '」' in title:
            patterns.append('quote_usage')
        
        # 数字の使用
        if re.search(r'\d+', title):
            patterns.append('number_usage')
        
        # 疑問形
        if '？' in title or '?' in title or (title and title[-1] == 'か'):
            patterns.append('question_form')
        
        # 感嘆符
        if '！' in title or '!' in title or '!!' in title:
            patterns.append('exclamation')
        
        # 省略形（...、など）
        if '…' in title or '...' in title:
            patterns.append('ellipsis')
        
        # 写真・動画アピール
        if '写真' in title or '画像' in title or '動画' in title:
            patterns.append('visual_content')
        
        # 人名の使用（A、B、アルファベット）
        if re.search(r'[A-Z](?:さん|氏|容疑者|被告)?', title):
            patterns.append('anonymous_person')
        
        return patterns
    
    def get_viral_patterns(self):
        """バイラルパターンを集計"""
        # キーワードランキング
        top_keywords = sorted(
            self.keyword_frequency.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:50]
        
        # パターン統計
        pattern_stats = {}
        for item in self.successful_patterns:
            for pattern in item['pattern']:
                if pattern not in pattern_stats:
                    pattern_stats[pattern] = 0
                pattern_stats[pattern] += (11 - item['rank'])
        
        return {
            'keywords': top_keywords,
            'patterns': pattern_stats,
            'length': self.analyze_title_length(),
            'emotions': self.analyze_emotions()
        }
    
    def analyze_title_length(self):
        """最適なタイトル長を分析"""
        if not self.title_database:
            return {'min': 30, 'max': 50, 'optimal': 40}
        
        lengths = [item['length'] for item in self.title_database if item['rank'] <= 5]
        if lengths:
            return {
                'min': min(lengths),
                'max': max(lengths),
                'optimal': sum(lengths) // len(lengths)
            }
        return {'min': 30, 'max': 50, 'optimal': 40}
    
    def analyze_emotions(self):
        """感情トリガーを分析"""
        emotions = {
            'anger': ['激怒', '批判', '炎上', '暴言', '失言', '反論', '抗議'],
            'sadness': ['涙', '号泣', '悲報', '訃報', '引退', '卒業', '悲しい'],
            'surprise': ['衝撃', '驚愕', 'まさか', '意外', '急展開', '速報', 'びっくり'],
            'joy': ['朗報', '結婚', '妊娠', '復活', '快挙', '祝福', '幸せ'],
            'fear': ['恐怖', '危険', '警告', '注意', '被害', '事故', '怖い'],
            'disgust': ['最悪', '酷い', '批判殺到', '大炎上', '失望', '幻滅']
        }
        
        emotion_scores = {}
        for emotion, words in emotions.items():
            score = 0
            for word in words:
                for category in ['総合', 'エンタメ', 'スポーツ', '社会']:
                    score += self.keyword_frequency.get(f"{category}:{word}", 0)
            emotion_scores[emotion] = score
        
        return emotion_scores
    
    def get_top_trends(self):
        """現在のトップトレンドを取得"""
        # カテゴリ別トップキーワード
        category_trends = {}
        for key, score in self.keyword_frequency.items():
            category, keyword = key.split(':', 1)
            if category not in category_trends:
                category_trends[category] = []
            category_trends[category].append((keyword, score))
        
        # 各カテゴリのトップ5
        for category in category_trends:
            category_trends[category] = sorted(
                category_trends[category], 
                key=lambda x: x[1], 
                reverse=True
            )[:5]
        
        return category_trends


def main():
    """Main execution function"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    try:
        analyzer = NewsRankingAnalyzer()
        
        # ランキング収集
        logger.info("📊 Collecting news rankings...")
        rankings = analyzer.collect_all_rankings()
        
        # パターン分析
        logger.info("🔍 Analyzing viral patterns...")
        patterns = analyzer.identify_viral_patterns()
        
        # データ保存
        analyzer.save_analysis_data()
        
        # 結果表示
        print("\n🔥 Top Viral Keywords:")
        for keyword, score in patterns['hot_keywords'][:10]:
            print(f"  {keyword}: {score}点")
        
        print("\n📊 Title Pattern Statistics:")
        for pattern, score in sorted(patterns['title_patterns'].items(), key=lambda x: x[1], reverse=True):
            print(f"  {pattern}: {score}点")
        
        print("\n😊 Emotion Triggers:")
        for emotion, score in sorted(patterns['emotion_triggers'].items(), key=lambda x: x[1], reverse=True):
            print(f"  {emotion}: {score}点")
        
        print("\n✅ Analysis completed successfully!")
        
    except Exception as e:
        logger.error(f"💥 Fatal error: {str(e)}")
        raise
    finally:
        if 'analyzer' in locals():
            analyzer.close()


if __name__ == "__main__":
    main()