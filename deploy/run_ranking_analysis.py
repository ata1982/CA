#!/usr/bin/env python3
"""
Ranking Analysis Runner
ニュースランキング分析とバイラル記事生成を実行
"""

import os
import sys
import logging
from datetime import datetime, timezone
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ranking_analyzer import NewsRankingAnalyzer
from viral_article_generator import ViralArticleGenerator

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_complete_analysis():
    """完全なランキング分析とバイラル記事生成を実行"""
    try:
        logger.info("🚀 Starting complete ranking analysis and viral article generation...")
        
        # Phase 1: ランキング分析
        logger.info("📊 Phase 1: Collecting and analyzing news rankings...")
        analyzer = NewsRankingAnalyzer()
        
        # ランキング収集
        rankings = analyzer.collect_all_rankings()
        logger.info(f"✅ Collected rankings from {len(rankings)} sites")
        
        # パターン分析
        viral_patterns = analyzer.identify_viral_patterns()
        logger.info("✅ Viral pattern analysis completed")
        
        # 分析データ保存
        analyzer.save_analysis_data()
        logger.info("✅ Analysis data saved")
        
        # Phase 2: バイラル記事生成
        logger.info("🔥 Phase 2: Generating viral articles...")
        generator = ViralArticleGenerator()
        
        # 記事生成
        articles = generator.generate_trending_articles(num_articles=5)
        logger.info(f"✅ Generated {len(articles)} viral articles")
        
        # 記事保存
        if articles:
            generator.save_generated_articles()
            logger.info("✅ Viral articles saved")
        
        # Phase 3: 結果サマリー表示
        logger.info("📋 Phase 3: Displaying results summary...")
        display_summary(viral_patterns, articles)
        
        print("\n🎉 Complete analysis finished successfully!")
        print("📊 View the dashboard: ranking_dashboard.html")
        
    except Exception as e:
        logger.error(f"💥 Fatal error in complete analysis: {str(e)}")
        raise
    finally:
        # Cleanup
        if 'analyzer' in locals():
            analyzer.close()

def display_summary(viral_patterns, articles):
    """結果サマリーを表示"""
    print("\n" + "="*60)
    print("📊 RANKING ANALYSIS SUMMARY")
    print("="*60)
    
    # Top Keywords
    print("\n🔥 TOP 10 VIRAL KEYWORDS:")
    for i, (keyword, score) in enumerate(viral_patterns['hot_keywords'][:10], 1):
        category, word = keyword.split(':', 1)
        print(f"  {i:2d}. {word} ({category}) - {score}点")
    
    # Pattern Statistics
    print("\n📊 TITLE PATTERN STATISTICS:")
    pattern_names = {
        'bracket_emphasis': '【】強調',
        'number_usage': '数字使用',
        'quote_usage': '「」引用',
        'question_form': '疑問形',
        'exclamation': '感嘆符',
        'ellipsis': '省略形',
        'visual_content': '写真・動画',
        'anonymous_person': '匿名人物'
    }
    
    sorted_patterns = sorted(viral_patterns['title_patterns'].items(), key=lambda x: x[1], reverse=True)
    for pattern, score in sorted_patterns[:6]:
        name = pattern_names.get(pattern, pattern)
        print(f"  • {name}: {score}点")
    
    # Emotion Analysis
    print("\n😊 EMOTION TRIGGER ANALYSIS:")
    emotion_names = {
        'anger': '怒り', 'sadness': '悲しみ', 'surprise': '驚き',
        'joy': '喜び', 'fear': '恐れ', 'disgust': '嫌悪'
    }
    
    sorted_emotions = sorted(viral_patterns['emotion_triggers'].items(), key=lambda x: x[1], reverse=True)
    for emotion, score in sorted_emotions:
        name = emotion_names.get(emotion, emotion)
        print(f"  • {name}: {score}点")
    
    # Generated Articles
    if articles:
        print(f"\n🚀 GENERATED VIRAL ARTICLES ({len(articles)}):")
        for i, article in enumerate(articles, 1):
            print(f"  {i}. {article['title']}")
            print(f"     Category: {article['category']}")
            
            # Performance prediction
            from viral_article_generator import ViralArticleGenerator
            temp_generator = ViralArticleGenerator()
            prediction = temp_generator.get_article_performance_prediction(article)
            print(f"     Performance: {prediction['level']} (Score: {prediction['score']})")
            print()
    
    print("="*60)

def run_quick_analysis():
    """クイック分析（ランキング収集のみ）"""
    try:
        logger.info("⚡ Running quick ranking analysis...")
        
        analyzer = NewsRankingAnalyzer()
        rankings = analyzer.collect_all_rankings()
        analyzer.save_analysis_data()
        
        print(f"\n⚡ Quick analysis completed!")
        print(f"📊 Collected data from {len(rankings)} news sites")
        
    except Exception as e:
        logger.error(f"💥 Error in quick analysis: {str(e)}")
        raise
    finally:
        if 'analyzer' in locals():
            analyzer.close()

def run_article_generation_only():
    """記事生成のみ実行"""
    try:
        logger.info("📝 Running article generation only...")
        
        generator = ViralArticleGenerator()
        articles = generator.generate_trending_articles(num_articles=3)
        
        if articles:
            generator.save_generated_articles()
            print(f"\n📝 Generated {len(articles)} articles:")
            for article in articles:
                print(f"  • {article['title']}")
        else:
            print("\n❌ No articles were generated")
            
    except Exception as e:
        logger.error(f"💥 Error in article generation: {str(e)}")
        raise

def main():
    """Main function with command line options"""
    import argparse
    
    parser = argparse.ArgumentParser(description='News Ranking Analysis System')
    parser.add_argument('--mode', choices=['full', 'quick', 'articles'], default='full',
                       help='Analysis mode: full (default), quick, articles')
    parser.add_argument('--articles', type=int, default=5,
                       help='Number of articles to generate (default: 5)')
    
    args = parser.parse_args()
    
    print("🔥 News Ranking Analysis System")
    print(f"Mode: {args.mode}")
    print(f"Time: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("-" * 50)
    
    try:
        if args.mode == 'full':
            run_complete_analysis()
        elif args.mode == 'quick':
            run_quick_analysis()
        elif args.mode == 'articles':
            run_article_generation_only()
            
    except KeyboardInterrupt:
        print("\n⚠️  Analysis interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()