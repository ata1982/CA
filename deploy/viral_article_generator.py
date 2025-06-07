#!/usr/bin/env python3
"""
Viral Article Generator
ランキング分析結果に基づいてバイラルになりやすい記事を自動生成
"""

import os
import sys
import json
import logging
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import random
import hashlib

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ranking_analyzer import NewsRankingAnalyzer

try:
    from deepseek_processor import DeepSeekProcessor
except ImportError:
    DeepSeekProcessor = None

logger = logging.getLogger(__name__)

class ViralArticleGenerator:
    def __init__(self):
        self.ranking_analyzer = NewsRankingAnalyzer()
        self.deepseek_client = DeepSeekProcessor() if DeepSeekProcessor else None
        self.generated_articles = []
        
    def generate_trending_articles(self, num_articles: int = 5) -> List[Dict]:
        """トレンドに基づいた記事を自動生成"""
        
        logger.info("🔥 Starting viral article generation...")
        
        # 現在のランキング収集
        current_rankings = self.ranking_analyzer.collect_all_rankings()
        
        # バイラルパターン分析
        viral_patterns = self.ranking_analyzer.identify_viral_patterns()
        
        # 各カテゴリのトップトレンドから記事生成
        generated_articles = []
        categories = ['エンタメ', 'スポーツ', '総合', '社会', 'IT']
        
        for i in range(min(num_articles, len(categories))):
            category = categories[i]
            
            # そのカテゴリで最も人気のキーワード取得
            hot_keywords = [
                kw.split(':', 1)[1] for kw, score in viral_patterns['hot_keywords'] 
                if kw.startswith(f"{category}:")
            ][:5]
            
            if not hot_keywords:
                # カテゴリ固有のキーワードがない場合は汎用キーワードを使用
                hot_keywords = ['速報', '衝撃', '話題', '注目', '発表']
            
            # 記事生成
            try:
                article = self.generate_viral_article(category, hot_keywords, viral_patterns)
                if article:
                    generated_articles.append(article)
                    logger.info(f"✅ Generated article for {category}: {article['title']}")
            except Exception as e:
                logger.error(f"Error generating article for {category}: {e}")
                continue
        
        self.generated_articles = generated_articles
        return generated_articles
    
    def generate_viral_article(self, category: str, keywords: List[str], patterns: Dict) -> Optional[Dict]:
        """カテゴリとキーワードに基づいて記事を生成"""
        
        # プロンプト作成
        prompt = self.create_viral_prompt(category, keywords, patterns)
        
        # DeepSeekで記事生成（クライアントがない場合はダミー記事を生成）
        try:
            if self.deepseek_client:
                article_data = self.deepseek_client.process_news(prompt)
                
                if article_data and 'articles' in article_data and article_data['articles']:
                    article = article_data['articles'][0]
                    
                    # 記事IDとメタデータを追加
                    article['id'] = self._generate_article_id(article['title'])
                    article['category'] = category
                    article['generated_at'] = datetime.now(timezone.utc).isoformat()
                    article['viral_keywords'] = keywords
                    article['is_generated'] = True
                    article['source'] = 'AI Generated (Viral Pattern Analysis)'
                    article['url'] = f"#article-{article['id']}"
                    article['reliability_score'] = 0.7  # AI生成記事なので中程度の信頼性
                    
                    return article
                else:
                    logger.warning(f"No article generated for {category}")
                    return None
            else:
                # DeepSeekクライアントがない場合はダミー記事を生成
                return self._generate_dummy_article(category, keywords)
                
        except Exception as e:
            logger.error(f"Error in generate_viral_article: {e}")
            return None
    
    def create_viral_prompt(self, category: str, keywords: List[str], patterns: Dict) -> str:
        """バイラル記事生成用プロンプト"""
        
        # パターン統計から最も効果的なパターンを選択
        top_patterns = []
        if patterns['title_patterns']:
            pattern_items = sorted(patterns['title_patterns'].items(), key=lambda x: x[1], reverse=True)
            top_patterns = [p[0] for p in pattern_items[:3]]
        
        # 感情トリガーの上位を取得
        top_emotions = []
        if patterns['emotion_triggers']:
            emotion_items = sorted(patterns['emotion_triggers'].items(), key=lambda x: x[1], reverse=True)
            top_emotions = [e[0] for e in emotion_items[:2]]
        
        # タイトル長の推奨
        title_length = patterns['optimal_length']
        optimal_length = title_length.get('optimal', 40) if title_length else 40
        
        prompt = f"""
以下の条件で{category}カテゴリのバイラルになりやすいニュース記事を1つ作成してください。

【必須条件】
- カテゴリ: {category}
- 使用すべきキーワード: {', '.join(keywords[:3])}
- タイトル文字数: {optimal_length-5}〜{optimal_length+5}文字

【タイトル作成ルール】
"""
        
        if 'bracket_emphasis' in top_patterns:
            prompt += "- 必ず【】で重要部分を強調する\n"
        if 'number_usage' in top_patterns:
            prompt += "- 具体的な数字を含める（年齢、金額、順位、％など）\n"
        if 'quote_usage' in top_patterns:
            prompt += "- 「」で印象的な発言を引用する\n"
        if 'question_form' in top_patterns:
            prompt += "- 疑問形で読者の興味を引く\n"
        
        prompt += f"""
- 感情を揺さぶる（特に{', '.join(top_emotions)}の感情）
- 今話題になりそうな内容にする

【成功パターン例】
"""
        
        # カテゴリ別の成功パターン例
        if category == 'エンタメ':
            prompt += """
- 【衝撃】俳優A(28)が電撃結婚！お相手は20代モデル
- 【速報】人気アイドルBが涙の告白「もう限界でした」
- 【独占】大物芸人Cの不倫疑惑、本人が激白
"""
        elif category == 'スポーツ':
            prompt += """
- 【速報】日本代表選手Dが海外移籍！年俸は推定5億円
- 【衝撃】人気選手Eが引退表明「体力の限界」
- 【歓喜】日本チームが歴史的勝利！監督が涙
"""
        elif category == 'IT':
            prompt += """
- 【革命】新AI技術で年収1000万円プログラマーが急増
- 【警告】人気アプリに重大な脆弱性！個人情報流出の恐れ
- 【独占】大手IT企業が新サービス発表、業界激震
"""
        else:
            prompt += """
- 【速報】政府が新制度を発表、国民生活に大きな影響
- 【衝撃】有名企業が倒産危機、従業員1万人の運命は
- 【独占】話題の事件、関係者が真相を激白
"""
        
        prompt += f"""

【記事内容の構成】
1. リード文（100-150文字）
   - 冒頭で最も衝撃的な事実を提示
   - 読者を引き込む強いフック
   
2. 本文（1000-1500文字）
   - 事実と推測を織り交ぜる
   - 関係者のコメント（架空でOK）を含める
   - 具体的な数字やデータを使う
   - 時系列で展開を説明
   
3. 今後の展望（200文字）
   - 読者が気になる今後の展開を示唆
   - 続報への期待を持たせる

【注意事項】
- 実在の人物名は使わず、A、B、Cなどで表現
- 断定的な表現を使い、説得力を持たせる
- SNSでの反応も含める
- 現在の日付: {(datetime.now(timezone.utc) + timedelta(hours=9)).strftime('%Y年%m月%d日')}

必ずJSON形式で以下の構造で返してください：
{{
    "articles": [{{
        "title": "記事タイトル",
        "content": "記事本文",
        "summary": "100文字程度の要約",
        "tags": ["タグ1", "タグ2", "タグ3"],
        "published": "2024-03-15T10:00:00Z",
        "language": "ja",
        "tone": "sensational"
    }}]
}}
"""
        
        return prompt
    
    def _generate_dummy_article(self, category: str, keywords: List[str]) -> Dict:
        """ダミーのバイラル記事を生成"""
        # カテゴリ別のダミータイトルテンプレート
        title_templates = {
            'エンタメ': [
                "【衝撃】人気俳優A(28)が電撃結婚！お相手は20代モデル",
                "【速報】大物歌手Bが活動休止を発表、ファン騒然",
                "【独占】美人女優Cの不倫疑惑、関係者が激白",
                "【悲報】人気アイドルDが涙の告白「限界でした」"
            ],
            'スポーツ': [
                "【速報】日本代表エースが海外移籍！年俸は推定5億円",
                "【衝撃】人気選手Fが引退表明「体力の限界」涙の会見",
                "【歓喜】日本チームが歴史的勝利！監督「信じられない」",
                "【独占】スター選手Gの移籍交渉、舞台裏を関係者が激白"
            ],
            'IT': [
                "【革命】新AI技術で年収1000万円エンジニアが急増中",
                "【警告】人気アプリに重大脆弱性！個人情報流出の恐れ",
                "【独占】大手IT企業が新サービス発表、業界に激震",
                "【速報】話題のAIサービスが突然停止、ユーザー大混乱"
            ],
            '総合': [
                "【速報】政府が新制度発表、国民生活に大きな影響か",
                "【衝撃】有名企業が突然倒産、従業員1000人の運命は",
                "【独占】話題の事件、関係者が衝撃の真相を激白",
                "【緊急】大型台風接近、専門家「過去最大級の警戒を」"
            ],
            '社会': [
                "【発覚】大企業の不正会計、損失額は100億円規模",
                "【速報】有名政治家に汚職疑惑、検察が本格捜査開始",
                "【衝撃】人気レストランで食中毒、原因は従業員の衛生管理",
                "【独占】社会問題化する事件、被害者家族が心境を語る"
            ]
        }
        
        # ランダムにタイトルを選択
        templates = title_templates.get(category, title_templates['総合'])
        title = random.choice(templates)
        
        # キーワードを含めてタイトルを調整
        if keywords:
            keyword = random.choice(keywords)
            if keyword not in title:
                # 【】内にキーワードを追加
                if '【' in title and '】' in title:
                    bracket_content = title.split('【')[1].split('】')[0]
                    title = title.replace(f'【{bracket_content}】', f'【{keyword}】')
        
        # ダミー記事内容を生成
        content = self._generate_dummy_content(category, title, keywords)
        
        article = {
            'id': self._generate_article_id(title),
            'title': title,
            'content': content,
            'summary': content[:100] + '...',
            'tags': keywords[:3] if keywords else ['ニュース', category],
            'published': datetime.now(timezone.utc).isoformat(),
            'language': 'ja',
            'tone': 'sensational',
            'category': category,
            'generated_at': datetime.now(timezone.utc).isoformat(),
            'viral_keywords': keywords,
            'is_generated': True,
            'source': 'AI Generated (Pattern Analysis - Demo)',
            'url': f"#article-{self._generate_article_id(title)}",
            'reliability_score': 0.6
        }
        
        return article
    
    def _generate_dummy_content(self, category: str, title: str, keywords: List[str]) -> str:
        """ダミーの記事内容を生成"""
        category_contexts = {
            'エンタメ': [
                "芸能界に衝撃が走っている。",
                "関係者によると、この発表は予想外だったという。",
                "ファンからは祝福と驚きの声が相次いでいる。",
                "所属事務所も正式にコメントを発表した。"
            ],
            'スポーツ': [
                "スポーツ界で大きな話題となっている。",
                "チーム関係者は「予想していなかった展開」と語る。",
                "ファンや関係者からは様々な反応が寄せられている。",
                "今後の動向に注目が集まっている。"
            ],
            'IT': [
                "IT業界で大きな動きが見られている。",
                "専門家は「これまでにない画期的な技術」と評価。",
                "ユーザーからは期待と不安の声が混在している。",
                "競合他社も対応策を検討し始めているという。"
            ],
            '総合': [
                "この発表により、社会全体に大きな影響が予想される。",
                "専門家は「慎重な対応が必要」と指摘している。",
                "国民からは様々な意見が寄せられている。",
                "政府も詳細な検討を進めているとのことだ。"
            ]
        }
        
        contexts = category_contexts.get(category, category_contexts['総合'])
        
        content_parts = [
            f"【{title.split('【')[1].split('】')[0] if '【' in title else 'ニュース'}】として注目を集めている今回の件について、詳細が明らかになった。",
            "",
            random.choice(contexts),
            "",
            "関係者の話によると、この動きは以前から水面下で進められていたという。「多くの人に影響を与える重要な決定」として、慎重に検討が重ねられてきた経緯がある。",
            "",
            "特に注目されているのは、今後の展開についてである。専門家は「これまでの常識を覆す可能性がある」と分析しており、業界全体への波及効果が期待されている。",
            "",
            "一方で、課題も指摘されている。「解決すべき問題がまだ残っている」との声もあり、関係者は慎重な対応を続けている状況だ。",
            "",
            "SNS上では様々な反応が見られており、「驚いた」「期待している」「心配だ」など、多様な意見が交わされている。",
            "",
            "今後の動向について、関係者は「適切な時期に詳細を発表する予定」としており、続報が待たれている状況である。"
        ]
        
        return "\n".join(content_parts)
    
    def _generate_article_id(self, title: str) -> str:
        """タイトルからユニークなIDを生成"""
        timestamp = datetime.now().isoformat()
        hash_input = f"{title}{timestamp}"
        return hashlib.md5(hash_input.encode()).hexdigest()[:12]
    
    def save_generated_articles(self) -> bool:
        """生成した記事を保存"""
        try:
            data_dir = Path('.')
            articles_file = data_dir / 'viral_articles.json'
            
            # 既存の記事を読み込む
            existing_articles = []
            if articles_file.exists():
                with open(articles_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    existing_articles = data.get('articles', [])
            
            # 新しい記事を追加
            existing_articles.extend(self.generated_articles)
            
            # 最新の50記事のみ保持
            existing_articles = existing_articles[-50:]
            
            # 保存
            save_data = {
                'last_updated': datetime.now(timezone.utc).isoformat(),
                'total_articles': len(existing_articles),
                'articles': existing_articles
            }
            
            with open(articles_file, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Saved {len(self.generated_articles)} new articles to {articles_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving generated articles: {e}")
            return False
    
    def get_article_performance_prediction(self, article: Dict) -> Dict:
        """記事のパフォーマンス予測"""
        score = 0
        factors = []
        
        title = article.get('title', '')
        
        # キーワードスコア
        viral_keywords = article.get('viral_keywords', [])
        keyword_score = len([kw for kw in viral_keywords if kw in title]) * 20
        score += keyword_score
        if keyword_score > 0:
            factors.append(f"バイラルキーワード使用 (+{keyword_score})")
        
        # パターンスコア
        if '【' in title and '】' in title:
            score += 15
            factors.append("【】強調使用 (+15)")
        
        if any(char in title for char in ['！', '!', '？', '?']):
            score += 10
            factors.append("感嘆符/疑問符使用 (+10)")
        
        # 数字の使用
        import re
        if re.search(r'\d+', title):
            score += 10
            factors.append("数字使用 (+10)")
        
        # タイトル長
        title_length = len(title)
        if 35 <= title_length <= 45:
            score += 15
            factors.append("最適なタイトル長 (+15)")
        
        # 予測結果
        performance_level = "低"
        if score >= 60:
            performance_level = "非常に高い"
        elif score >= 45:
            performance_level = "高い"
        elif score >= 30:
            performance_level = "中"
        
        return {
            'score': score,
            'level': performance_level,
            'factors': factors,
            'recommendation': self._get_recommendation(score)
        }
    
    def _get_recommendation(self, score: int) -> str:
        """スコアに基づいた改善提案"""
        if score >= 60:
            return "このタイトルは高いバイラル性が期待できます。SNSでの拡散を狙いましょう。"
        elif score >= 45:
            return "良いタイトルです。画像や動画を追加することでさらに効果的になります。"
        elif score >= 30:
            return "もう少しインパクトのあるキーワードを追加すると良いでしょう。"
        else:
            return "より感情に訴えるキーワードと【】での強調を検討してください。"


def main():
    """Main execution function"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    try:
        generator = ViralArticleGenerator()
        
        # ランキング分析に基づいて記事生成
        logger.info("🚀 Generating viral articles based on ranking analysis...")
        articles = generator.generate_trending_articles(num_articles=5)
        
        if articles:
            # 記事を保存
            generator.save_generated_articles()
            
            # 結果表示
            print(f"\n✅ Generated {len(articles)} viral articles:")
            for article in articles:
                print(f"\n📰 {article['title']}")
                print(f"   Category: {article['category']}")
                print(f"   Keywords: {', '.join(article.get('viral_keywords', []))}")
                
                # パフォーマンス予測
                prediction = generator.get_article_performance_prediction(article)
                print(f"   Performance: {prediction['level']} (Score: {prediction['score']})")
                print(f"   Factors: {', '.join(prediction['factors'])}")
            
            print("\n🎉 Viral article generation completed!")
        else:
            print("\n❌ No articles were generated")
            
    except Exception as e:
        logger.error(f"💥 Fatal error: {str(e)}")
        raise


if __name__ == "__main__":
    main()