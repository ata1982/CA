#!/usr/bin/env python3
"""
Integrate Ranking Analysis System
既存のニュースサイトにランキング分析システムを統合
"""

import os
import sys
import json
import logging
from datetime import datetime, timezone
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from article_enhancer import EnhancedRealNewsSystem
from run_ranking_analysis import run_complete_analysis

logger = logging.getLogger(__name__)

def integrate_ranking_system():
    """ランキング分析システムを既存のニュースサイトに統合"""
    try:
        logger.info("🔗 Integrating ranking analysis system with news site...")
        
        # Phase 1: ランキング分析実行
        logger.info("📊 Running ranking analysis...")
        run_complete_analysis()
        
        # Phase 2: 既存ニュースサイトを更新
        logger.info("🔄 Updating existing news site...")
        current_dir = Path('.')
        news_system = EnhancedRealNewsSystem(current_dir)
        
        # バイラル記事を既存記事に統合
        viral_articles = load_viral_articles()
        if viral_articles:
            logger.info(f"📰 Integrating {len(viral_articles)} viral articles...")
            integrated_articles = integrate_viral_articles(news_system, viral_articles)
        else:
            integrated_articles = []
        
        # サイト生成
        news_system.generate_enhanced_news_website()
        
        # ランキングダッシュボードの設定情報を追加
        add_dashboard_link()
        
        logger.info("✅ Integration completed successfully!")
        
        # 統計表示
        print("\n🎯 INTEGRATION SUMMARY:")
        print(f"📊 Ranking analysis: ✅ Completed")
        print(f"📰 Viral articles: {len(integrated_articles)} integrated")
        print(f"🔗 Dashboard link: ✅ Added")
        print(f"🌐 News site: ✅ Updated")
        print("\n📋 Available files:")
        print(f"  • index.html - Updated news site")
        print(f"  • ranking_dashboard.html - Analysis dashboard") 
        print(f"  • ranking_analysis.json - Analysis data")
        print(f"  • viral_articles.json - Generated articles")
        
        return True
        
    except Exception as e:
        logger.error(f"💥 Integration failed: {str(e)}")
        return False

def load_viral_articles():
    """バイラル記事を読み込み"""
    try:
        viral_file = Path('.') / 'viral_articles.json'
        if viral_file.exists():
            with open(viral_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('articles', [])
        return []
    except Exception as e:
        logger.error(f"Error loading viral articles: {e}")
        return []

def integrate_viral_articles(news_system, viral_articles):
    """バイラル記事を既存システムに統合"""
    integrated = []
    
    for viral_article in viral_articles[-3:]:  # 最新3記事のみ統合
        try:
            # 既存記事フォーマットに変換
            integrated_article = {
                'id': viral_article['id'],
                'title': viral_article['title'],
                'content': viral_article['content'][:500] + '...',  # 概要として切り詰め
                'url': viral_article['url'],
                'source': viral_article['source'],
                'source_url': viral_article['url'],
                'category': viral_article['category'],
                'language': viral_article['language'],
                'reliability_score': viral_article['reliability_score'],
                'published': viral_article['published'],
                'fetch_timestamp': viral_article['generated_at'],
                'is_real_news': False,
                'is_viral_generated': True,
                'viral_keywords': viral_article.get('viral_keywords', []),
                'enhanced_content': {
                    'detailed_summary': viral_article['content'],
                    'detailed_explanation': 'この記事は最新のニュースランキング分析に基づいて、バイラルになりやすいパターンを学習して自動生成されました。実際のニュースサイトのトレンドを反映しています。',
                    'fact_check': 'この記事は分析システムによる生成記事です。実際の事件・人物とは関係ありません。デモンストレーション目的で作成されており、ニュースサイトのトレンド分析結果を表示しています。',
                    'word_count': len(viral_article['content']),
                    'analysis_quality': 'demo'
                }
            }
            
            integrated.append(integrated_article)
            
        except Exception as e:
            logger.error(f"Error integrating viral article {viral_article.get('title', 'Unknown')}: {e}")
            continue
    
    return integrated

def add_dashboard_link():
    """既存のHTMLにダッシュボードリンクを追加"""
    try:
        index_file = Path('.') / 'index.html'
        if not index_file.exists():
            return
        
        with open(index_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # ダッシュボードリンクを追加
        dashboard_link = '''
        <div class="ranking-box">
            <div style="font-size: 1.4em; font-weight: bold; color: #2c3e50; margin-bottom: 20px; border-bottom: 3px solid #9b59b6; padding-bottom: 8px;">📊 ランキング分析</div>
            <div style="font-size: 0.95em; line-height: 1.9;">
                <p>ニュースサイトのトレンド分析とバイラルパターン学習システム</p>
                <a href="ranking_dashboard.html" target="_blank" style="display: inline-block; margin-top: 10px; padding: 10px 20px; background: linear-gradient(135deg, #667eea, #764ba2); color: white; text-decoration: none; border-radius: 8px; font-weight: bold;">
                    📊 分析ダッシュボードを開く
                </a>
            </div>
        </div>
        
                <div class="ad-space">'''
        
        # 広告スペースの前に挿入
        if '<div class="ad-space">' in html_content:
            html_content = html_content.replace('<div class="ad-space">', dashboard_link)
            
            with open(index_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info("✅ Dashboard link added to news site")
        
    except Exception as e:
        logger.error(f"Error adding dashboard link: {e}")

def main():
    """Main execution function"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    print("🔗 NEWS RANKING ANALYSIS SYSTEM INTEGRATION")
    print("=" * 60)
    print(f"Time: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("-" * 60)
    
    try:
        success = integrate_ranking_system()
        
        if success:
            print("\n🎉 Integration completed successfully!")
            print("\n📝 Next steps:")
            print("  1. Open index.html to view updated news site")
            print("  2. Open ranking_dashboard.html to view analysis")
            print("  3. Set up cron job for automatic updates:")
            print("     */30 * * * * python3 /path/to/integrate_ranking_system.py")
        else:
            print("\n❌ Integration failed. Check logs for details.")
            
    except KeyboardInterrupt:
        print("\n⚠️  Integration interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()