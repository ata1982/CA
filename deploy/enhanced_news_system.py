#!/usr/bin/env python3
"""
Enhanced News System with Comments and Ranking
Full-featured news portal with anonymous commenting and engagement tracking
"""

import os
import sys
import json
import logging
import random
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from comment_system import AnonymousCommentSystem, RankingSystem
from comment_generator import CommentGenerator

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class EnhancedNewsSystem:
    def __init__(self, data_dir='/var/www/html'):
        self.data_dir = Path(data_dir)
        self.comment_system = AnonymousCommentSystem(data_dir)
        self.ranking_system = RankingSystem(self.comment_system)
        self.comment_generator = CommentGenerator()
        
        # Sample articles for demonstration
        self.sample_articles = [
            {
                'id': 'article_001',
                'title': '【速報】政府が新税制改革を発表、消費税率変更を検討',
                'content': '政府は本日、新しい税制改革案を発表しました。消費税率の変更や法人税の見直しが含まれており、国民生活への影響が懸念されています。財務省は「経済成長と財政健全化の両立を目指す」と説明していますが、野党からは強い反発の声が上がっています。',
                'category': '政治',
                'published': datetime.now(timezone.utc).isoformat(),
                'source': 'ニュース通信社'
            },
            {
                'id': 'article_002', 
                'title': '人気俳優の不倫疑惑が発覚、事務所は否定コメント',
                'content': '人気俳優のA氏に不倫疑惑が浮上しました。週刊誌が密会の瞬間を撮影したと報じており、ファンの間では衝撃が広がっています。所属事務所は「事実無根」と否定していますが、SNS上では様々な憶測が飛び交っています。',
                'category': '芸能',
                'published': (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat(),
                'source': '芸能ニュース'
            },
            {
                'id': 'article_003',
                'title': '新型コロナワクチンの副反応について厚労省が見解発表',
                'content': '厚生労働省は新型コロナワクチンの副反応に関する最新データを公表しました。専門家は「重篤な副反応は極めて稀」と説明していますが、一部では安全性への懸念の声も上がっています。接種の判断は個人に委ねられており、医師との相談が推奨されています。',
                'category': '健康',
                'published': (datetime.now(timezone.utc) - timedelta(hours=4)).isoformat(),
                'source': '医療ニュース'
            },
            {
                'id': 'article_004',
                'title': '若者の車離れが深刻化、自動車業界に激震',
                'content': '若者の車への関心低下が止まらず、自動車業界では危機感が高まっています。カーシェアリングの普及や都市部での交通利便性向上が背景にあるとされ、従来の販売戦略の見直しが急務となっています。',
                'category': '経済',
                'published': (datetime.now(timezone.utc) - timedelta(hours=6)).isoformat(),
                'source': '経済新聞'
            },
            {
                'id': 'article_005',
                'title': '高校生の学力低下が問題に、教育現場では対策を模索',
                'content': '全国学力テストの結果から、高校生の基礎学力低下が明らかになりました。スマートフォンの普及による学習時間の減少が一因とされ、教育関係者は対策に頭を悩ませています。「ゆとり教育の弊害」との指摘もあり、議論が活発化しています。',
                'category': '教育',
                'published': (datetime.now(timezone.utc) - timedelta(hours=8)).isoformat(),
                'source': '教育新聞'
            }
        ]
    
    def generate_full_website(self):
        """コメント機能付きの完全なニュースサイトを生成"""
        try:
            logger.info("🚀 Enhanced news system starting...")
            
            # Initialize articles with comments if not already present
            self._initialize_articles_with_comments()
            
            # Track views for ranking
            for article in self.sample_articles:
                # Simulate some views
                for _ in range(random.randint(10, 100)):
                    self.comment_system.track_view(article['id'])
            
            # Generate HTML content
            html_content = self._generate_enhanced_html()
            
            # Save to website directory
            html_path = self.data_dir / 'index.html'
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"✅ Enhanced website saved to {html_path}")
            
            # Generate rankings
            self._update_rankings()
            
            logger.info("🎉 Enhanced news system update completed!")
            
        except Exception as e:
            logger.error(f"💥 Error in enhanced news system: {str(e)}")
            raise
    
    def _initialize_articles_with_comments(self):
        """記事に初期コメントを生成"""
        existing_comments = self.comment_system._load_comments()
        
        for article in self.sample_articles:
            article_id = article['id']
            
            # Skip if comments already exist
            if article_id in existing_comments and len(existing_comments[article_id]) > 0:
                continue
            
            logger.info(f"Generating comments for {article_id}")
            
            # Generate initial comments
            num_comments = random.randint(10, 25)
            initial_comments = self.comment_generator.generate_initial_comments(
                article['content'], num_comments
            )
            
            # Post comments to the system
            for comment_data in initial_comments:
                # Create realistic timestamps
                minutes_ago = random.randint(5, 300)
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
            
            # Save comments
            self.comment_system._save_comments(existing_comments)
    
    def _generate_enhanced_html(self):
        """拡張HTML生成"""
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
    <meta name="description" content="最新ニュースを最速でお届け！政治・芸能・経済・社会のニュースとリアルタイムコメント">
    <meta name="keywords" content="ニュース,速報,政治,芸能,経済,コメント,まとめ">
    <meta http-equiv="refresh" content="300">
    
    <!-- OGP Tags -->
    <meta property="og:title" content="【速報】ニュースまとめ速">
    <meta property="og:description" content="最新ニュースを最速でお届け！">
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
            border-left: 4px solid #3498db;
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
        }}
        
        .meta-tag {{
            background: #ecf0f1;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 0.8em;
        }}
        
        .article-content {{
            color: #555;
            margin-bottom: 20px;
            line-height: 1.7;
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
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="container">
            <h1>🔥 【速報】ニュースまとめ速</h1>
            <div class="subtitle">最新ニュースを最速でお届け！</div>
            <div class="live-indicator">
                <span class="live-dot"></span>
                <span>リアルタイム更新中</span>
            </div>
        </div>
    </div>
    
    <div class="container">
        <div class="update-info">
            <strong>📅 最終更新:</strong> {jst_time.strftime('%Y年%m月%d日 %H:%M:%S')} (JST)<br>
            <strong>🔄 次回更新:</strong> 約5分後 | <strong>📊 総記事数:</strong> {len(self.sample_articles)}件
        </div>
        
        <div class="main-content">
            <div class="articles-section">
                <h2 style="margin-bottom: 25px; color: #2c3e50;">📰 最新ニュース</h2>
                {self._generate_articles_html()}
            </div>
            
            <div class="sidebar">
                <div class="ranking-box">
                    <div class="ranking-title">🔥 注目ランキング</div>
                    {self._generate_ranking_html(hourly_ranking)}
                </div>
                
                <div class="ad-space">
                    💰 広告スペース<br>
                    <small>収益化準備中</small>
                </div>
                
                <div class="ranking-box">
                    <div class="ranking-title">📊 サイト統計</div>
                    <div style="font-size: 0.9em; line-height: 1.8;">
                        • 総記事数: {len(self.sample_articles)}件<br>
                        • 総コメント数: {self._get_total_comments()}件<br>
                        • アクティブユーザー: {random.randint(50, 200)}人<br>
                        • 今日の訪問者: {random.randint(500, 2000)}人
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="footer">
        <div class="container">
            <p>© 2025 【速報】ニュースまとめ速 - 最新ニュースをお届け</p>
            <p style="font-size: 0.9em; margin-top: 10px; color: #bbb;">
                当サイトは様々なニュースソースから情報を収集し、読者の皆様にお届けしています
            </p>
        </div>
    </div>
    
    <script>
        // Auto-refresh page every 5 minutes
        setTimeout(() => {{
            location.reload();
        }}, 300000);
        
        // Comment functionality
        function likeComment(articleId, commentId) {{
            // In a real implementation, this would make an API call
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
        
        // Smooth scrolling for better UX
        document.addEventListener('click', function(e) {{
            if (e.target.tagName === 'A' && e.target.getAttribute('href').startsWith('#')) {{
                e.preventDefault();
                const target = document.querySelector(e.target.getAttribute('href'));
                if (target) {{
                    target.scrollIntoView({{ behavior: 'smooth' }});
                }}
            }}
        }});
    </script>
</body>
</html>"""
        
        return html_content
    
    def _generate_articles_html(self):
        """記事HTML生成"""
        html = ""
        
        for i, article in enumerate(self.sample_articles):
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
            published_time = datetime.fromisoformat(article['published'].replace('Z', '+00:00'))
            jst_published = published_time + timedelta(hours=9)
            
            html += f"""
            <div class="article" id="{article_id}">
                <div class="article-title">{article['title']}</div>
                <div class="article-meta">
                    <span class="meta-tag">📂 {article['category']}</span>
                    <span class="meta-tag">📰 {article['source']}</span>
                    <span class="meta-tag">🕐 {jst_published.strftime('%m/%d %H:%M')}</span>
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
                        <h4>💭 コメントを投稿</h4>
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
    
    def _generate_ranking_html(self, ranking_data):
        """ランキングHTML生成"""
        html = ""
        
        for i, item in enumerate(ranking_data[:5], 1):
            # Find article title
            article_title = "記事が見つかりません"
            for article in self.sample_articles:
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
    
    def _update_rankings(self):
        """ランキングデータの更新"""
        hourly_ranking = self.ranking_system.get_hourly_ranking(100)
        daily_ranking = self.ranking_system.get_daily_ranking(100)
        viral_ranking = self.ranking_system.get_viral_ranking(50)
        
        rankings_data = {
            'hourly': hourly_ranking,
            'daily': daily_ranking,
            'viral': viral_ranking,
            'updated_at': datetime.now(timezone.utc).isoformat()
        }
        
        rankings_file = self.data_dir / 'rankings.json'
        with open(rankings_file, 'w', encoding='utf-8') as f:
            json.dump(rankings_data, f, ensure_ascii=False, indent=2)
    
    def _get_total_comments(self):
        """総コメント数を取得"""
        comments = self.comment_system._load_comments()
        total = sum(len(article_comments) for article_comments in comments.values())
        return total


def main():
    """メイン実行関数"""
    try:
        system = EnhancedNewsSystem()
        system.generate_full_website()
        
    except Exception as e:
        logger.error(f"💥 Fatal error: {str(e)}")
        raise


if __name__ == "__main__":
    main()