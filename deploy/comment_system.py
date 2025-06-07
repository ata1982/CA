#!/usr/bin/env python3
"""
Anonymous Comment System for News Portal
2ch-style anonymous commenting with automatic engagement features
"""

import json
import os
import random
import hashlib
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List, Optional

class AnonymousCommentSystem:
    def __init__(self, data_dir=None):
        if data_dir is None:
            try:
                from config import DATA_DIR
                self.data_dir = DATA_DIR
            except ImportError:
                # Fallback if config module is not available
                self.data_dir = Path('/var/www/html') if Path('/var/www/html').exists() else Path('.')
        else:
            self.data_dir = Path(data_dir)
        self.comments_file = self.data_dir / 'comments.json'
        self.reactions_file = self.data_dir / 'reactions.json'
        self.views_file = self.data_dir / 'views.json'
        
        # Ensure data files exist
        self._init_data_files()
    
    def _init_data_files(self):
        """Initialize JSON data files if they don't exist"""
        for file_path in [self.comments_file, self.reactions_file, self.views_file]:
            if not file_path.exists():
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump({}, f, ensure_ascii=False, indent=2)
    
    def generate_comment_id(self):
        """Generate unique comment ID"""
        timestamp = datetime.now().timestamp()
        random_str = ''.join(random.choices('0123456789abcdef', k=8))
        return f"{int(timestamp)}_{random_str}"
    
    def get_random_name(self):
        """Get random anonymous name"""
        names = [
            '名無しさん', '匿名', '通りすがり', 'ななし', '774', 
            '匿名希望', '一市民', '納税者', '主婦', '会社員',
            '元会社員', '年金生活者', '自営業', 'パート', '元公務員',
            '子育て終了組', '団塊世代', '昭和生まれ', '還暦過ぎ', '定年退職者'
        ]
        base_name = random.choice(names)
        
        # Sometimes add age or location
        if random.random() < 0.3:
            age = random.randint(25, 75)
            base_name += f"（{age}歳）"
        
        if random.random() < 0.2:
            regions = ["東京", "大阪", "名古屋", "福岡", "北海道", "地方都市", "田舎"]
            base_name += f"・{random.choice(regions)}在住"
        
        return base_name
    
    def get_next_number(self, article_id):
        """Get next comment number for article"""
        comments = self._load_comments()
        article_comments = comments.get(article_id, [])
        return len(article_comments) + 1
    
    def get_timestamp(self):
        """Get formatted timestamp"""
        now = datetime.now(timezone.utc)
        return {
            'iso': now.isoformat(),
            'display': now.strftime('%Y/%m/%d %H:%M:%S'),
            'jst_display': (now + timedelta(hours=9)).strftime('%Y/%m/%d %H:%M:%S')
        }
    
    def post_comment(self, article_id: str, text: str, reply_to: Optional[int] = None) -> Dict:
        """Post a new comment"""
        comments = self._load_comments()
        
        if article_id not in comments:
            comments[article_id] = []
        
        comment = {
            'id': self.generate_comment_id(),
            'name': self.get_random_name(),
            'text': text.strip(),
            'timestamp': self.get_timestamp(),
            'number': self.get_next_number(article_id),
            'reply_to': reply_to,
            'likes': 0,
            'dislikes': 0
        }
        
        comments[article_id].append(comment)
        self._save_comments(comments)
        
        return comment
    
    def add_reaction(self, article_id: str, comment_id: str, reaction_type: str) -> bool:
        """Add reaction to comment (heart/heartbreak)"""
        if reaction_type not in ['like', 'dislike']:
            return False
        
        reactions = self._load_reactions()
        
        if article_id not in reactions:
            reactions[article_id] = {}
        
        if comment_id not in reactions[article_id]:
            reactions[article_id][comment_id] = {'likes': 0, 'dislikes': 0}
        
        # Allow unlimited clicking (no IP restriction)
        reactions[article_id][comment_id][reaction_type + 's'] += 1
        
        self._save_reactions(reactions)
        
        # Update comment data
        comments = self._load_comments()
        if article_id in comments:
            for comment in comments[article_id]:
                if comment['id'] == comment_id:
                    comment['likes'] = reactions[article_id][comment_id]['likes']
                    comment['dislikes'] = reactions[article_id][comment_id]['dislikes']
                    break
            self._save_comments(comments)
        
        return True
    
    def get_comments(self, article_id: str) -> List[Dict]:
        """Get all comments for an article"""
        comments = self._load_comments()
        return comments.get(article_id, [])
    
    def track_view(self, article_id: str):
        """Track article view"""
        views = self._load_views()
        
        if article_id not in views:
            views[article_id] = {
                'total_views': 0,
                'hourly_views': {},
                'daily_views': {}
            }
        
        # Increment total views
        views[article_id]['total_views'] += 1
        
        # Track hourly views
        current_hour = datetime.now().strftime('%Y-%m-%d-%H')
        if current_hour not in views[article_id]['hourly_views']:
            views[article_id]['hourly_views'][current_hour] = 0
        views[article_id]['hourly_views'][current_hour] += 1
        
        # Track daily views
        current_day = datetime.now().strftime('%Y-%m-%d')
        if current_day not in views[article_id]['daily_views']:
            views[article_id]['daily_views'][current_day] = 0
        views[article_id]['daily_views'][current_day] += 1
        
        self._save_views(views)
    
    def get_article_stats(self, article_id: str) -> Dict:
        """Get article statistics"""
        views = self._load_views()
        comments = self._load_comments()
        reactions = self._load_reactions()
        
        article_views = views.get(article_id, {'total_views': 0})
        article_comments = comments.get(article_id, [])
        article_reactions = reactions.get(article_id, {})
        
        total_likes = sum(r.get('likes', 0) for r in article_reactions.values())
        total_dislikes = sum(r.get('dislikes', 0) for r in article_reactions.values())
        
        return {
            'views': article_views['total_views'],
            'comments': len(article_comments),
            'likes': total_likes,
            'dislikes': total_dislikes,
            'engagement_score': len(article_comments) * 10 + total_likes * 2 + total_dislikes
        }
    
    def _load_comments(self) -> Dict:
        """Load comments from file"""
        try:
            with open(self.comments_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def _save_comments(self, comments: Dict):
        """Save comments to file"""
        with open(self.comments_file, 'w', encoding='utf-8') as f:
            json.dump(comments, f, ensure_ascii=False, indent=2)
    
    def _load_reactions(self) -> Dict:
        """Load reactions from file"""
        try:
            with open(self.reactions_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def _save_reactions(self, reactions: Dict):
        """Save reactions to file"""
        with open(self.reactions_file, 'w', encoding='utf-8') as f:
            json.dump(reactions, f, ensure_ascii=False, indent=2)
    
    def _load_views(self) -> Dict:
        """Load views from file"""
        try:
            with open(self.views_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def _save_views(self, views: Dict):
        """Save views to file"""
        with open(self.views_file, 'w', encoding='utf-8') as f:
            json.dump(views, f, ensure_ascii=False, indent=2)


class RankingSystem:
    def __init__(self, comment_system: AnonymousCommentSystem):
        self.comment_system = comment_system
    
    def get_hourly_ranking(self, limit=100) -> List[Dict]:
        """Get hourly ranking based on recent engagement"""
        views = self.comment_system._load_views()
        current_hour = datetime.now().strftime('%Y-%m-%d-%H')
        
        rankings = []
        for article_id, data in views.items():
            hourly_views = data.get('hourly_views', {}).get(current_hour, 0)
            stats = self.comment_system.get_article_stats(article_id)
            
            score = hourly_views * 5 + stats['engagement_score']
            rankings.append({
                'article_id': article_id,
                'score': score,
                'views': hourly_views,
                'comments': stats['comments'],
                'likes': stats['likes']
            })
        
        return sorted(rankings, key=lambda x: x['score'], reverse=True)[:limit]
    
    def get_daily_ranking(self, limit=100) -> List[Dict]:
        """Get daily ranking"""
        views = self.comment_system._load_views()
        current_day = datetime.now().strftime('%Y-%m-%d')
        
        rankings = []
        for article_id, data in views.items():
            daily_views = data.get('daily_views', {}).get(current_day, 0)
            stats = self.comment_system.get_article_stats(article_id)
            
            score = daily_views * 3 + stats['engagement_score']
            rankings.append({
                'article_id': article_id,
                'score': score,
                'views': daily_views,
                'comments': stats['comments'],
                'likes': stats['likes']
            })
        
        return sorted(rankings, key=lambda x: x['score'], reverse=True)[:limit]
    
    def get_viral_ranking(self, limit=50) -> List[Dict]:
        """Get viral ranking based on engagement rate"""
        views = self.comment_system._load_views()
        
        rankings = []
        for article_id, data in views.items():
            total_views = data.get('total_views', 0)
            stats = self.comment_system.get_article_stats(article_id)
            
            if total_views > 0:
                engagement_rate = (stats['comments'] * 100 + stats['likes'] * 10) / total_views
                viral_score = engagement_rate * stats['engagement_score']
                
                rankings.append({
                    'article_id': article_id,
                    'viral_score': viral_score,
                    'engagement_rate': engagement_rate,
                    'views': total_views,
                    'comments': stats['comments'],
                    'likes': stats['likes']
                })
        
        return sorted(rankings, key=lambda x: x['viral_score'], reverse=True)[:limit]


# Usage example
if __name__ == "__main__":
    # Initialize system
    comment_system = AnonymousCommentSystem()
    ranking_system = RankingSystem(comment_system)
    
    # Test posting a comment
    article_id = "test_article_001"
    comment = comment_system.post_comment(article_id, "これは素晴らしいニュースですね！")
    print(f"Posted comment: {comment}")
    
    # Test reaction
    comment_system.add_reaction(article_id, comment['id'], 'like')
    
    # Test view tracking
    comment_system.track_view(article_id)
    
    # Get stats
    stats = comment_system.get_article_stats(article_id)
    print(f"Article stats: {stats}")
    
    # Get rankings
    hourly = ranking_system.get_hourly_ranking(10)
    print(f"Hourly ranking: {hourly}")