#!/usr/bin/env python3
"""
Viral News Frontend Generator
Advanced UI with trending keywords, viral meter, YouTube embeds, SNS metrics
"""

import json
import re
from datetime import datetime, timezone
from typing import Dict, List

def generate_viral_frontend(articles: List[Dict], trending_keywords: List[str] = None) -> str:
    """
    バイラル対応フロントエンドの生成
    """
    if trending_keywords is None:
        trending_keywords = extract_trending_keywords(articles)
    
    # 統計情報の計算
    stats = calculate_viral_stats(articles)
    
    html_content = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔥 Viral News Portal - トレンド＆炎上ニュース</title>
    <meta http-equiv="refresh" content="180">
    <style>
        :root {{
            --viral-red: #ff4757;
            --trend-blue: #3742fa;
            --gossip-purple: #5f27cd;
            --safe-green: #00d2d3;
            --warning-orange: #ff9f43;
            --dark-bg: #1e1e2e;
            --card-bg: #2d2d44;
            --text-light: #f8f8f2;
            --text-muted: #6272a4;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, var(--dark-bg) 0%, #44475a 100%);
            color: var(--text-light);
            min-height: 100vh;
            line-height: 1.6;
        }}
        
        .header {{
            background: rgba(30, 30, 46, 0.95);
            backdrop-filter: blur(10px);
            border-bottom: 2px solid var(--viral-red);
            padding: 20px 0;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 4px 20px rgba(255, 71, 87, 0.3);
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 20px;
        }}
        
        .main-title {{
            font-size: 3em;
            background: linear-gradient(45deg, var(--viral-red), var(--trend-blue), var(--gossip-purple));
            background-clip: text;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-bottom: 10px;
            animation: pulse 2s infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(1.05); }}
        }}
        
        .subtitle {{
            text-align: center;
            color: var(--text-muted);
            margin-bottom: 15px;
            font-size: 1.2em;
        }}
        
        .live-indicator {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            margin-bottom: 20px;
        }}
        
        .live-dot {{
            width: 12px;
            height: 12px;
            background: var(--viral-red);
            border-radius: 50%;
            animation: blink 1s infinite;
        }}
        
        @keyframes blink {{
            0%, 50% {{ opacity: 1; }}
            51%, 100% {{ opacity: 0.3; }}
        }}
        
        .trending-bar {{
            background: var(--card-bg);
            border-radius: 15px;
            padding: 15px;
            margin-bottom: 20px;
            border: 1px solid var(--trend-blue);
        }}
        
        .trending-title {{
            color: var(--trend-blue);
            font-weight: bold;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .trending-keywords {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }}
        
        .trending-keyword {{
            background: linear-gradient(45deg, var(--trend-blue), var(--gossip-purple));
            color: white;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.9em;
            animation: float 3s ease-in-out infinite;
        }}
        
        .trending-keyword:nth-child(odd) {{
            animation-delay: 0.5s;
        }}
        
        @keyframes float {{
            0%, 100% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-5px); }}
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: var(--card-bg);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            border: 1px solid;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }}
        
        .stat-card.viral {{ border-color: var(--viral-red); }}
        .stat-card.trend {{ border-color: var(--trend-blue); }}
        .stat-card.gossip {{ border-color: var(--gossip-purple); }}
        .stat-card.safe {{ border-color: var(--safe-green); }}
        
        .stat-value {{
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        
        .stat-card.viral .stat-value {{ color: var(--viral-red); }}
        .stat-card.trend .stat-value {{ color: var(--trend-blue); }}
        .stat-card.gossip .stat-value {{ color: var(--gossip-purple); }}
        .stat-card.safe .stat-value {{ color: var(--safe-green); }}
        
        .stat-label {{
            color: var(--text-muted);
            font-size: 0.9em;
        }}
        
        .filter-tabs {{
            display: flex;
            gap: 10px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }}
        
        .filter-tab {{
            background: var(--card-bg);
            color: var(--text-light);
            border: 2px solid transparent;
            padding: 10px 20px;
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 500;
        }}
        
        .filter-tab:hover, .filter-tab.active {{
            border-color: var(--trend-blue);
            background: linear-gradient(45deg, var(--trend-blue), var(--gossip-purple));
            transform: translateY(-2px);
        }}
        
        .articles-grid {{
            display: grid;
            gap: 25px;
            margin-bottom: 50px;
        }}
        
        .article-card {{
            background: var(--card-bg);
            border-radius: 20px;
            padding: 25px;
            border: 2px solid;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }}
        
        .article-card:hover {{
            transform: translateY(-8px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.4);
        }}
        
        .article-card.viral {{ border-color: var(--viral-red); }}
        .article-card.trending {{ border-color: var(--trend-blue); }}
        .article-card.gossip {{ border-color: var(--gossip-purple); }}
        .article-card.normal {{ border-color: var(--safe-green); }}
        
        .viral-indicator {{
            position: absolute;
            top: 15px;
            right: 15px;
            display: flex;
            align-items: center;
            gap: 5px;
        }}
        
        .viral-flames {{
            font-size: 1.2em;
            animation: flicker 1.5s infinite;
        }}
        
        @keyframes flicker {{
            0%, 100% {{ opacity: 1; }}
            25%, 75% {{ opacity: 0.7; }}
            50% {{ opacity: 0.4; }}
        }}
        
        .viral-score {{
            background: var(--viral-red);
            color: white;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 0.8em;
            font-weight: bold;
        }}
        
        .article-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 15px;
        }}
        
        .article-title {{
            font-size: 1.6em;
            color: var(--text-light);
            margin-bottom: 10px;
            margin-right: 80px;
            line-height: 1.3;
        }}
        
        .article-meta {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 15px;
        }}
        
        .meta-tag {{
            padding: 4px 12px;
            border-radius: 15px;
            font-size: 0.85em;
            font-weight: 500;
        }}
        
        .meta-tag.source {{
            background: var(--trend-blue);
            color: white;
        }}
        
        .meta-tag.platform {{
            background: var(--gossip-purple);
            color: white;
        }}
        
        .meta-tag.language {{
            background: var(--warning-orange);
            color: white;
        }}
        
        .meta-tag.reliability {{
            background: var(--safe-green);
            color: white;
        }}
        
        .meta-tag.reliability.low {{
            background: var(--viral-red);
        }}
        
        .meta-tag.reliability.medium {{
            background: var(--warning-orange);
        }}
        
        .viral-meter {{
            background: var(--dark-bg);
            border-radius: 10px;
            padding: 10px;
            margin: 15px 0;
        }}
        
        .viral-meter-label {{
            font-size: 0.9em;
            color: var(--text-muted);
            margin-bottom: 5px;
        }}
        
        .viral-meter-bar {{
            height: 8px;
            background: #44475a;
            border-radius: 4px;
            overflow: hidden;
            position: relative;
        }}
        
        .viral-meter-fill {{
            height: 100%;
            border-radius: 4px;
            transition: width 1s ease;
            position: relative;
        }}
        
        .viral-meter-fill::after {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            animation: shimmer 2s infinite;
        }}
        
        @keyframes shimmer {{
            0% {{ transform: translateX(-100%); }}
            100% {{ transform: translateX(100%); }}
        }}
        
        .article-content {{
            color: var(--text-muted);
            line-height: 1.7;
            margin-bottom: 15px;
        }}
        
        .youtube-embed {{
            margin: 15px 0;
            border-radius: 12px;
            overflow: hidden;
            position: relative;
            background: #000;
        }}
        
        .youtube-thumbnail {{
            width: 100%;
            height: 200px;
            object-fit: cover;
            cursor: pointer;
            transition: transform 0.3s ease;
        }}
        
        .youtube-thumbnail:hover {{
            transform: scale(1.05);
        }}
        
        .play-button {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 60px;
            height: 60px;
            background: rgba(255, 255, 255, 0.9);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5em;
            color: var(--dark-bg);
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        
        .play-button:hover {{
            background: white;
            transform: translate(-50%, -50%) scale(1.1);
        }}
        
        .sns-metrics {{
            display: flex;
            gap: 15px;
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #44475a;
        }}
        
        .sns-metric {{
            display: flex;
            align-items: center;
            gap: 5px;
            color: var(--text-muted);
            font-size: 0.9em;
        }}
        
        .controversy-alert {{
            background: linear-gradient(45deg, var(--viral-red), #ff6b6b);
            color: white;
            padding: 10px;
            border-radius: 10px;
            margin: 15px 0;
            display: flex;
            align-items: center;
            gap: 8px;
            animation: pulse 2s infinite;
        }}
        
        .timestamp {{
            text-align: center;
            color: var(--text-muted);
            margin-top: 40px;
            font-size: 0.9em;
        }}
        
        .live-update {{
            background: var(--safe-green);
            color: white;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 0.8em;
            animation: pulse 1.5s infinite;
        }}
        
        @media (max-width: 768px) {{
            .main-title {{
                font-size: 2em;
            }}
            
            .stats-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
            
            .filter-tabs {{
                justify-content: center;
            }}
            
            .article-card {{
                padding: 20px;
            }}
            
            .article-title {{
                font-size: 1.3em;
                margin-right: 60px;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="container">
            <h1 class="main-title">🔥 Viral News Portal</h1>
            <div class="subtitle">リアルタイム トレンド＆炎上ニュース配信</div>
            <div class="live-indicator">
                <div class="live-dot"></div>
                <span>LIVE</span>
                <span class="live-update">自動更新中</span>
            </div>
            
            <div class="trending-bar">
                <div class="trending-title">
                    🚀 今のトレンドワード
                </div>
                <div class="trending-keywords">
                    {generate_trending_keywords_html(trending_keywords)}
                </div>
            </div>
            
            <div class="stats-grid">
                <div class="stat-card viral">
                    <div class="stat-value">{stats['viral_count']}</div>
                    <div class="stat-label">🔥 炎上中</div>
                </div>
                <div class="stat-card trend">
                    <div class="stat-value">{stats['trend_count']}</div>
                    <div class="stat-label">📈 トレンド</div>
                </div>
                <div class="stat-card gossip">
                    <div class="stat-value">{stats['gossip_count']}</div>
                    <div class="stat-label">💬 ゴシップ</div>
                </div>
                <div class="stat-card safe">
                    <div class="stat-value">{stats['youtube_count']}</div>
                    <div class="stat-label">📺 動画</div>
                </div>
            </div>
            
            <div class="filter-tabs">
                <div class="filter-tab active" data-filter="all">🌟 すべて</div>
                <div class="filter-tab" data-filter="viral">🔥 炎上中</div>
                <div class="filter-tab" data-filter="trending">📈 トレンド</div>
                <div class="filter-tab" data-filter="youtube">📺 動画</div>
                <div class="filter-tab" data-filter="gossip">💬 ゴシップ</div>
                <div class="filter-tab" data-filter="global">🌍 海外</div>
            </div>
        </div>
    </div>
    
    <div class="container">
        <div class="articles-grid" id="articles-grid">
            {generate_articles_html(articles)}
        </div>
        
        <div class="timestamp">
            最終更新: {datetime.now(timezone.utc).strftime('%Y年%m月%d日 %H:%M:%S UTC')}<br>
            次回更新: 3分後 | 収集ソース: {len(set(a.get('source', '') for a in articles))}個
        </div>
    </div>
    
    <script>
        // フィルタリング機能
        document.querySelectorAll('.filter-tab').forEach(tab => {{
            tab.addEventListener('click', () => {{
                // アクティブタブの切り替え
                document.querySelectorAll('.filter-tab').forEach(t => t.classList.remove('active'));
                tab.classList.add('active');
                
                // 記事のフィルタリング
                const filter = tab.dataset.filter;
                const articles = document.querySelectorAll('.article-card');
                
                articles.forEach(article => {{
                    if (filter === 'all' || article.classList.contains(filter)) {{
                        article.style.display = 'block';
                    }} else {{
                        article.style.display = 'none';
                    }}
                }});
            }});
        }});
        
        // YouTube動画再生
        document.querySelectorAll('.youtube-thumbnail').forEach(thumb => {{
            thumb.addEventListener('click', (e) => {{
                const videoId = e.target.dataset.videoId;
                if (videoId) {{
                    const iframe = document.createElement('iframe');
                    iframe.src = `https://www.youtube.com/embed/${{videoId}}?autoplay=1`;
                    iframe.width = '100%';
                    iframe.height = '200';
                    iframe.frameBorder = '0';
                    iframe.allowFullscreen = true;
                    
                    e.target.parentElement.innerHTML = '';
                    e.target.parentElement.appendChild(iframe);
                }}
            }});
        }});
        
        // リアルタイム更新表示
        setInterval(() => {{
            document.querySelector('.live-dot').style.animation = 'blink 0.5s infinite';
            setTimeout(() => {{
                document.querySelector('.live-dot').style.animation = 'blink 1s infinite';
            }}, 2000);
        }}, 30000);
        
        // バイラルメーターアニメーション
        window.addEventListener('load', () => {{
            document.querySelectorAll('.viral-meter-fill').forEach(fill => {{
                const width = fill.dataset.width;
                setTimeout(() => {{
                    fill.style.width = width + '%';
                }}, 500);
            }});
        }});
    </script>
</body>
</html>"""
    
    return html_content

def generate_trending_keywords_html(keywords: List[str]) -> str:
    """
    トレンドキーワードのHTML生成
    """
    if not keywords:
        keywords = ["DeepSeek-R1", "AI技術", "トレンド分析", "バイラルニュース", "グローバル配信"]
    
    html = ""
    for keyword in keywords[:8]:  # 最大8個まで表示
        html += f'<span class="trending-keyword">{keyword}</span>'
    
    return html

def generate_articles_html(articles: List[Dict]) -> str:
    """
    記事一覧のHTML生成
    """
    html = ""
    
    for article in articles:
        # 記事の分類
        article_class = classify_article(article)
        viral_score = article.get('viral_score', 0)
        reliability = article.get('reliability_score', 0.5)
        
        # バイラルフレーム数
        flame_count = min(5, max(1, viral_score // 200))
        flames = "🔥" * flame_count
        
        # 信頼性レベル
        reliability_class = get_reliability_class(reliability)
        reliability_text = get_reliability_text(reliability)
        
        # YouTube埋め込み
        youtube_embed = ""
        if article.get('platform') == 'youtube' and article.get('video_id'):
            youtube_embed = f"""
            <div class="youtube-embed">
                <img src="{article.get('thumbnail_url', '')}" 
                     alt="YouTube thumbnail" 
                     class="youtube-thumbnail"
                     data-video-id="{article.get('video_id')}">
                <div class="play-button">▶️</div>
            </div>
            """
        
        # 論争アラート
        controversy_alert = ""
        controversy_level = article.get('controversy_level', 0)
        if controversy_level >= 5:
            controversy_alert = f"""
            <div class="controversy-alert">
                ⚠️ 議論を呼ぶ内容が含まれています (レベル: {controversy_level}/10)
            </div>
            """
        
        # バイラルメーター
        viral_meter_color = get_viral_meter_color(viral_score)
        viral_meter_width = min(100, viral_score // 10)
        
        html += f"""
        <div class="article-card {article_class}" data-category="{article.get('category', '')}">
            <div class="viral-indicator">
                <span class="viral-flames">{flames}</span>
                <span class="viral-score">{viral_score}</span>
            </div>
            
            <div class="article-header">
                <h2 class="article-title">{article.get('title', 'タイトルなし')}</h2>
            </div>
            
            <div class="article-meta">
                <span class="meta-tag source">📰 {article.get('source', 'Unknown')}</span>
                {f'<span class="meta-tag platform">📱 {article.get("platform", "").upper()}</span>' if article.get('platform') else ''}
                <span class="meta-tag language">🌐 {article.get('language', '').upper()}</span>
                <span class="meta-tag reliability {reliability_class}">🛡️ {reliability_text}</span>
            </div>
            
            {controversy_alert}
            
            <div class="viral-meter">
                <div class="viral-meter-label">🔥 バイラル度: {viral_score}/1000</div>
                <div class="viral-meter-bar">
                    <div class="viral-meter-fill" 
                         style="background: {viral_meter_color};" 
                         data-width="{viral_meter_width}"></div>
                </div>
            </div>
            
            {youtube_embed}
            
            <div class="article-content">
                {article.get('content', '')[:200]}...
            </div>
            
            <div class="sns-metrics">
                <div class="sns-metric">
                    ⏰ {format_time_ago(article.get('published', ''))}
                </div>
                {f'<div class="sns-metric">🔗 <a href="{article.get("url", "#")}" target="_blank" style="color: inherit;">元記事</a></div>' if article.get('url') else ''}
                <div class="sns-metric">
                    📊 信頼度: {int(reliability * 100)}%
                </div>
                {f'<div class="sns-metric">🎯 {article.get("trend_keyword", "")}</div>' if article.get('trend_keyword') else ''}
            </div>
        </div>
        """
    
    return html

def classify_article(article: Dict) -> str:
    """
    記事の分類
    """
    viral_score = article.get('viral_score', 0)
    category = article.get('category', '')
    platform = article.get('platform', '')
    
    if viral_score >= 800:
        return 'viral'
    elif platform == 'youtube':
        return 'youtube'
    elif 'gossip' in category:
        return 'gossip'
    elif viral_score >= 400:
        return 'trending'
    else:
        return 'normal'

def get_reliability_class(score: float) -> str:
    """
    信頼性クラスの取得
    """
    if score >= 0.8:
        return 'high'
    elif score >= 0.5:
        return 'medium'
    else:
        return 'low'

def get_reliability_text(score: float) -> str:
    """
    信頼性テキストの取得
    """
    if score >= 0.8:
        return '高'
    elif score >= 0.5:
        return '中'
    else:
        return '低'

def get_viral_meter_color(score: int) -> str:
    """
    バイラルメーターの色取得
    """
    if score >= 800:
        return 'linear-gradient(90deg, #ff4757, #ff3838)'
    elif score >= 600:
        return 'linear-gradient(90deg, #ff9f43, #ff6348)'
    elif score >= 400:
        return 'linear-gradient(90deg, #feca57, #ff9ff3)'
    elif score >= 200:
        return 'linear-gradient(90deg, #48dbfb, #0abde3)'
    else:
        return 'linear-gradient(90deg, #1dd1a1, #10ac84)'

def format_time_ago(timestamp: str) -> str:
    """
    相対時間の表示
    """
    try:
        from datetime import datetime
        pub_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        now = datetime.utcnow().replace(tzinfo=pub_time.tzinfo)
        diff = now - pub_time
        
        if diff.days > 0:
            return f"{diff.days}日前"
        elif diff.seconds > 3600:
            return f"{diff.seconds // 3600}時間前"
        elif diff.seconds > 60:
            return f"{diff.seconds // 60}分前"
        else:
            return "たった今"
    except:
        return "不明"

def extract_trending_keywords(articles: List[Dict]) -> List[str]:
    """
    記事からトレンドキーワードを抽出
    """
    keywords = {}
    
    for article in articles:
        # タイトルからキーワード抽出
        title = article.get('title', '')
        words = re.findall(r'[ァ-ヶー]+|[a-zA-Z]+', title)
        
        for word in words:
            if len(word) >= 2:
                keywords[word] = keywords.get(word, 0) + 1
        
        # トレンドキーワードがある場合は優先
        if article.get('trend_keyword'):
            keywords[article['trend_keyword']] = keywords.get(article['trend_keyword'], 0) + 10
    
    # 出現頻度順でソート
    sorted_keywords = sorted(keywords.items(), key=lambda x: x[1], reverse=True)
    return [kw[0] for kw in sorted_keywords[:10]]

def calculate_viral_stats(articles: List[Dict]) -> Dict:
    """
    バイラル統計の計算
    """
    stats = {
        'viral_count': 0,
        'trend_count': 0,
        'gossip_count': 0,
        'youtube_count': 0
    }
    
    for article in articles:
        viral_score = article.get('viral_score', 0)
        category = article.get('category', '')
        platform = article.get('platform', '')
        
        if viral_score >= 800:
            stats['viral_count'] += 1
        elif viral_score >= 400:
            stats['trend_count'] += 1
        
        if 'gossip' in category:
            stats['gossip_count'] += 1
            
        if platform == 'youtube':
            stats['youtube_count'] += 1
    
    return stats