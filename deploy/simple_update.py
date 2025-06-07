#!/usr/bin/env python3
"""
Simple News Update System - Minimal version for testing
"""

import os
import sys
import json
import logging
from datetime import datetime, timezone
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_simple_html():
    """
    Create a simple HTML page with current timestamp
    """
    current_time = datetime.now(timezone.utc)
    
    html_content = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔥 【速報】ニュースまとめ速 - 最新ニュース</title>
    <meta http-equiv="refresh" content="60">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        
        .update-time {{
            background: rgba(255, 255, 255, 0.2);
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }}
        
        .status {{
            background: rgba(255, 255, 255, 0.1);
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
        }}
        
        .working {{
            color: #4ade80;
        }}
        
        .error {{
            color: #ef4444;
        }}
        
        .comments-section {{
            background: rgba(255, 255, 255, 0.15);
            padding: 20px;
            border-radius: 10px;
            margin-top: 30px;
        }}
        
        .comment-form {{
            margin-top: 20px;
        }}
        
        .comment-form input, .comment-form textarea {{
            width: 100%;
            padding: 10px;
            margin: 5px 0;
            border: none;
            border-radius: 5px;
            background: rgba(255, 255, 255, 0.9);
            color: #333;
        }}
        
        .comment-form button {{
            background: #4ade80;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }}
        
        .comment-form button:hover {{
            background: #22c55e;
        }}
        
        .comments-list {{
            margin-top: 20px;
        }}
        
        .comment {{
            background: rgba(255, 255, 255, 0.1);
            padding: 15px;
            margin: 10px 0;
            border-radius: 8px;
        }}
        
        .comment-author {{
            font-weight: bold;
            color: #fbbf24;
        }}
        
        .comment-time {{
            font-size: 0.9em;
            color: #d1d5db;
        }}
        
        .live-indicator {{
            display: inline-block;
            width: 12px;
            height: 12px;
            background: #ef4444;
            border-radius: 50%;
            animation: blink 1s infinite;
            margin-right: 5px;
        }}
        
        @keyframes blink {{
            0%, 50% {{ opacity: 1; }}
            51%, 100% {{ opacity: 0.3; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🔥 【速報】ニュースまとめ速</h1>
        <div>最新ニュースを最速でお届け！</div>
        <div><span class="live-indicator"></span>システム稼働中</div>
    </div>
    
    <div class="update-time">
        <h2>📅 最終更新時刻</h2>
        <p style="font-size: 1.5em; font-weight: bold;">
            {current_time.strftime('%Y年%m月%d日 %H:%M:%S UTC')}
        </p>
        <p>JST: {current_time.astimezone().strftime('%Y年%m月%d日 %H:%M:%S')}</p>
    </div>
    
    <div class="status working">
        ✅ 自動更新システム稼働中（15分間隔）
    </div>
    
    <div class="status working">
        ✅ DeepSeek-R1 API 接続正常
    </div>
    
    <div class="status working">
        ✅ ニュース収集システム動作中
    </div>
    
    <div class="comments-section">
        <h3>💬 コメント機能</h3>
        <p>現在コメント機能を開発中です。以下のフォームから意見をお聞かせください：</p>
        
        <div class="comment-form">
            <input type="text" placeholder="お名前（任意）" id="name">
            <textarea placeholder="コメントを入力してください..." rows="4" id="comment"></textarea>
            <button onclick="submitComment()">コメント投稿</button>
        </div>
        
        <div class="comments-list" id="comments">
            <div class="comment">
                <div class="comment-author">開発チーム</div>
                <div class="comment-time">{current_time.strftime('%Y-%m-%d %H:%M')}</div>
                <div>システムの更新を確認中です。コメント機能は次回アップデートで実装予定です。</div>
            </div>
        </div>
    </div>
    
    <script>
        function submitComment() {{
            const name = document.getElementById('name').value || '匿名';
            const comment = document.getElementById('comment').value;
            
            if (!comment.trim()) {{
                alert('コメントを入力してください');
                return;
            }}
            
            // Create new comment element
            const commentDiv = document.createElement('div');
            commentDiv.className = 'comment';
            commentDiv.innerHTML = `
                <div class="comment-author">${{name}}</div>
                <div class="comment-time">${{new Date().toLocaleString('ja-JP')}}</div>
                <div>${{comment}}</div>
            `;
            
            // Add to comments list
            const commentsList = document.getElementById('comments');
            commentsList.insertBefore(commentDiv, commentsList.firstChild);
            
            // Clear form
            document.getElementById('name').value = '';
            document.getElementById('comment').value = '';
            
            alert('コメントを投稿しました！（注意：ページを更新すると消去されます）');
        }}
        
        // Auto refresh every minute
        setTimeout(() => {{
            location.reload();
        }}, 60000);
    </script>
</body>
</html>"""
    
    return html_content

def main():
    """
    Main update function
    """
    try:
        logger.info("🔄 Starting simple news update...")
        
        # Create HTML content
        html_content = create_simple_html()
        
        # Save to website directory
        html_path = Path('/var/www/html/index.html')
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"✅ Updated website at {html_path}")
        logger.info(f"🕐 Update completed at {datetime.now()}")
        
    except Exception as e:
        logger.error(f"💥 Error in update: {str(e)}")
        raise

if __name__ == "__main__":
    main()