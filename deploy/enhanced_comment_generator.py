#!/usr/bin/env python3
"""
Enhanced Comment Generator with Threading and News-Related Content
Generates high-quality, news-related comments with reply threads and proper rating system
"""

import random
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional

class EnhancedCommentGenerator:
    def __init__(self):
        # News-related comment patterns by category
        self.news_related_patterns = {
            'politics': {
                'expert': [
                    "政策立案プロセスの観点から分析すると、{specific_point}は従来の手法から大きく逸脱している。特に行政法の原則である比例性・適正手続きの観点で検討が必要だ。",
                    "憲法学の立場から申し上げると、今回の{legal_aspect}は憲法第{constitution_article}条との整合性に疑義がある。最高裁判例との関係も慎重に検討すべきだ。",
                    "公共政策の効果測定において、今回の施策は{policy_analysis}という点で評価できる。ただし、EBPM（証拠に基づく政策立案）の観点では{evidence_concern}が不足している。",
                    "国際比較の観点では、OECD諸国の中で日本の{policy_field}は{international_position}に位置する。特にドイツの{german_model}やスウェーデンの{swedish_approach}と比較すると{comparison_result}。",
                    "財政学の理論から見ると、この政策の{fiscal_impact}は中長期的に{fiscal_sustainability}への懸念を生じさせる。特に社会保障費の増加を考慮すると{budget_projection}。",
                    "行政学の観点から、今回の政策実施体制は{administrative_structure}という問題を内包している。NPM（新公共管理）理論に基づく{efficiency_concern}の改善が急務だ。",
                ],
                'constructive': [
                    "この政策については以前から議論があったが、今回の決定は{specific_point}という点で注目すべきだ。",
                    "過去の{related_case}と比較すると、今回のアプローチは{difference}が異なる。",
                    "専門家の間では{expert_view}という見方が主流だが、実際の影響は{practical_impact}だろう。",
                    "この件について、私の選挙区では{local_impact}という声が多い。",
                    "法的な観点から見ると{legal_aspect}が問題になる可能性がある。",
                    "予算的には{budget_concern}が懸念される。財源をどう確保するかが課題だ。",
                    "野党の{opposition_point}という指摘は的を射ている。与党はもっと説明すべきだ。",
                    "この政策の実施には{implementation_challenge}という課題がある。",
                ],
                'critical': [
                    "また選挙対策の{election_strategy}か。国民を舐めるのもいい加減にしろ。",
                    "これでは{negative_outcome}になるのは目に見えている。過去に学ばない政治家たち。",
                    "税金の無駄遣いだ。{waste_example}に使うべき予算がこんなことに。",
                    "官僚の{bureaucracy_problem}がまた露呈した。責任を取る者は誰もいない。",
                    "マスコミは{media_criticism}を報道しろ。都合の悪いことは隠すな。",
                    "利権が絡んでいるのは明らか。{interest_group}の圧力に屈した結果だ。",
                ]
            },
            'economics': {
                'expert': [
                    "マクロ経済学の観点から、今回の{economic_policy}はIS-LM分析では{is_lm_effect}をもたらすと考えられる。特に金利政策との相互作用において{monetary_interaction}が重要だ。",
                    "計量経済学の手法で過去データを分析すると、{statistical_analysis}という結果が得られる。GDP成長率への影響は{gdp_impact}程度と推計される。",
                    "産業組織論の視点では、今回の{market_structure}変化は{competition_effect}を引き起こす可能性がある。特に{industry_concentration}への影響が懸念される。",
                    "国際経済学の理論に基づくと、{trade_theory}の観点から{comparative_advantage}に変化が生じる。貿易収支への影響は{trade_balance_effect}と予測される。",
                    "労働経済学の研究では、類似の政策による{employment_effect}が報告されている。特に{skill_biased}技術変化との関連で{wage_inequality}への影響を注視すべきだ。",
                    "金融工学の観点から、今回の{financial_innovation}はリスク管理において{risk_assessment}が必要だ。VaR（バリューアットリスク）の再計算が急務である。",
                ],
                'constructive': [
                    "経済指標を見ると{economic_indicator}が改善している。ただし{concern}には注意が必要。",
                    "この業界では{industry_trend}という傾向が続いている。今回の発表は{impact}を意味する。",
                    "株式市場の反応は{market_reaction}だった。投資家は{investor_sentiment}を示している。",
                    "中小企業への影響が{sme_impact}だ。特に{specific_sector}では深刻だろう。",
                    "為替の動きを考えると{forex_impact}が予想される。輸出企業には{export_impact}。",
                    "消費者にとっては{consumer_impact}だ。家計への影響は{household_effect}になりそう。",
                ],
                'critical': [
                    "またアベノミクスの失敗を隠すための{cover_up}か。数字を操作するな。",
                    "庶民の生活は{living_condition}なのに、政府は現実を見ていない。",
                    "大企業だけが{corporate_benefit}で、労働者は{worker_situation}のまま。",
                    "増税の前に{priority_spending}を削減しろ。順序が間違っている。",
                ]
            },
            'technology': {
                'expert': [
                    "コンピュータサイエンスの観点から、今回の{algorithm_analysis}はアルゴリズムの計算複雑性において{complexity_class}に分類される。特にP vs NP問題との関連で{computational_implications}が重要だ。",
                    "情報セキュリティの専門家として、このシステムの{security_architecture}は従来の{encryption_standard}と比較して{security_improvement}を実現している。ただし{vulnerability_concern}への対策が不十分だ。",
                    "機械学習の理論では、今回のモデルは{ml_approach}を採用しており、{training_data}に対する{generalization_performance}が期待される。過学習の問題は{overfitting_analysis}で解決可能だ。",
                    "ソフトウェア工学の品質保証において、{software_metrics}による評価では{quality_assessment}という結果が得られる。特にMcCabe複雑度や{maintainability_index}の観点で改善が必要だ。",
                    "データベース理論の正規化において、今回の{database_design}は第{normal_form}正規形を満たしている。しかし{performance_optimization}の観点では{denormalization_strategy}も検討すべきだ。",
                    "ネットワーク工学の視点では、{network_topology}による{latency_analysis}が重要だ。特にOSI参照モデルの{layer_analysis}において{bottleneck_identification}が急務である。",
                ],
                'constructive': [
                    "この技術は{tech_advantage}という利点がある。ただし{security_concern}が心配だ。",
                    "以前から{related_technology}を使っているが、今回の{improvement}は画期的だ。",
                    "IT業界では{industry_standard}が標準になりつつある。今回の発表は{significance}。",
                    "プライバシーの観点から{privacy_concern}が問題になりそう。規制が必要だ。",
                    "中国の{china_tech}と比較すると、日本は{japan_position}にある。",
                    "技術者として見ると{technical_aspect}が興味深い。実装は{implementation}だろう。",
                ],
                'critical': [
                    "また外国製品に依存するのか。日本の技術力はどこに行った。",
                    "セキュリティが{security_risk}だ。個人情報が{data_concern}になる。",
                    "IT音痴の政治家が決めた{poor_decision}だろう。現場を知らない。",
                ]
            },
            'health': {
                'expert': [
                    "循環器内科の専門医として、今回の{cardiovascular_aspect}はACC/AHA（米国心臓病学会/米国心臓協会）のガイドラインに照らすと{guideline_compliance}という評価になる。特に{risk_stratification}が重要だ。",
                    "薬剤疫学の観点から、{pharmacoepidemiology}による大規模コホート研究では{cohort_results}が報告されている。NNT（治療必要数）は{nnt_value}程度と推計される。",
                    "医療経済学の分析では、QALY（質調整生存年）による{qaly_analysis}は{cost_effectiveness}という結果になる。ICER（増分費用効果比）の観点で{health_economics_assessment}が妥当だ。",
                    "感染症学の専門家として、今回の{infectious_disease_aspect}は基本再生産数R0が{r0_value}であり、{transmission_dynamics}という感染動態を示している。",
                    "公衆衛生学の立場から、{population_health}に対する影響は{epidemiological_impact}と評価される。特にDALY（障害調整生命年）の観点で{disease_burden}への対策が急務だ。",
                    "精神医学の診断基準DSM-5において、今回の{psychiatric_classification}は{diagnostic_criteria}を満たしている。認知行動療法の適応については{cbt_indication}と判断される。",
                ],
                'constructive': [
                    "医療従事者として、この{medical_aspect}は{professional_view}だと思う。",
                    "過去の{similar_case}と比較すると、今回は{difference}が異なる。",
                    "この治療法は{treatment_benefit}があるが、{side_effect}も考慮すべきだ。",
                    "高齢者への影響が{elderly_impact}だ。特に{specific_condition}の方は注意が必要。",
                    "医療費の観点から{cost_benefit}を検討する必要がある。",
                    "海外では{overseas_practice}が一般的だが、日本では{japan_situation}だ。",
                ],
                'critical': [
                    "また製薬会社の{pharma_interest}か。患者のことを考えているのか。",
                    "厚労省の{ministry_failure}がまた露呈した。責任を取れ。",
                    "医師会の{medical_association}に振り回される政治。国民の健康はどうでもいいのか。",
                ]
            },
            'general': {
                'expert': [
                    "社会学の理論から分析すると、今回の{social_phenomenon}はブルデューの{bourdieu_concept}理論で説明できる。特にハビトゥスと{field_analysis}の相互作用が重要だ。",
                    "統計学的手法による{statistical_method}では、信頼区間95%で{confidence_interval}という結果が得られる。p値は{p_value}で統計的有意性が確認される。",
                    "組織行動学の観点では、{organizational_behavior}はハーズバーグの{motivation_theory}で説明可能だ。特に{hygiene_factors}と動機要因の区別が重要である。",
                    "教育心理学の研究によると、{learning_theory}に基づく{educational_approach}は{learning_effectiveness}という効果を示している。ブルームの教育目標分類学では{bloom_taxonomy}に相当する。",
                    "環境科学の専門家として、{environmental_impact}はライフサイクルアセスメント（LCA）による{lca_analysis}の結果、{carbon_footprint}のCO2削減効果が期待される。",
                ],
                'constructive': [
                    "この問題については{specific_angle}から考える必要がある。",
                    "過去の事例を見ると{historical_perspective}だった。今回は{current_difference}。",
                    "専門家の{expert_opinion}という意見は参考になる。",
                    "地域によって{regional_variation}があるのも事実だ。",
                    "長期的な視点で見ると{long_term_view}が重要だ。",
                ],
                'critical': [
                    "いつものパターンだ。{typical_pattern}で終わるだろう。",
                    "責任のなすりつけ合いが始まる。{blame_game}の構図だ。",
                    "結局は{usual_outcome}になる。期待するだけ無駄。",
                ]
            },
            'sports': {
                'expert': [
                    "スポーツ科学の観点から、今回の{performance_analysis}は生理学的に{physiological_aspect}を示している。特に乳酸閾値と{vo2_max}の関係において{training_effect}が重要だ。",
                    "戦術分析として、今回の{tactical_formation}は4-3-3システムの{positional_play}に基づいている。特にティキタカとゲーゲンプレッシングの{tactical_combination}が効果的だった。",
                    "バイオメカニクスの研究では、{biomechanical_analysis}による動作解析で{kinematic_data}という結果が得られる。関節角度と{force_vector}の最適化が課題だ。",
                    "スポーツ心理学の理論では、{psychological_factor}がパフォーマンスに{mental_impact}を与える。特にフロー状態と{concentration_level}の関係が重要だ。",
                ],
                'constructive': [
                    "この選手は{technical_skill}が素晴らしい。特に{specific_technique}の精度が高い。",
                    "戦術的に見ると{tactical_insight}が興味深い。コーチの{strategy}が効いている。",
                    "今季の{team_performance}は期待以上だ。来季に向けて{future_prospect}が楽しみ。",
                    "この記録は{record_significance}という点で評価できる。過去の{comparison_data}と比較しても優秀だ。",
                ],
                'critical': [
                    "また審判の{referee_mistake}か。公正なジャッジをしろ。",
                    "選手の{player_attitude}が悪い。プロ意識が足りない。",
                    "監督の{coaching_failure}だろう。戦術が古すぎる。",
                ]
            },
            'entertainment': {
                'expert': [
                    "エンターテインメント産業の経済学的分析では、{market_analysis}による収益構造は{revenue_model}を示している。特にロングテール理論との関連で{distribution_strategy}が重要だ。",
                    "メディア理論の観点から、{media_theory}はマクルーハンの{mcluhan_concept}で説明できる。特にホット・メディアとクール・メディアの{media_classification}が興味深い。",
                    "映像技術の専門家として、今回の{visual_technology}は色彩心理学の{color_psychology}を効果的に活用している。特にHDR技術と{dynamic_range}の組み合わせが秀逸だ。",
                    "音響工学の分析では、{acoustic_analysis}による周波数特性が{frequency_response}を示している。特に空間音響と{surround_technology}の実装が優れている。",
                ],
                'constructive': [
                    "この作品は{artistic_quality}が高い。特に{creative_aspect}に注目したい。",
                    "キャストの{acting_skill}が素晴らしい。{character_development}も丁寧だった。",
                    "演出の{direction_style}が印象的だった。{visual_presentation}も美しい。",
                    "音楽の{musical_score}が物語を引き立てている。{emotional_impact}も十分だ。",
                ],
                'critical': [
                    "また同じような{repetitive_content}か。新鮮味がない。",
                    "事務所の{agency_politics}が見え見えだ。実力で勝負しろ。",
                    "視聴率のための{rating_strategy}が露骨すぎる。質を重視しろ。",
                ]
            },
            'food': {
                'expert': [
                    "食品科学の観点から、{food_science}はメイラード反応の{maillard_reaction}によって{flavor_development}が生成される。特にアミノ酸と還元糖の{chemical_reaction}が重要だ。",
                    "栄養学の専門家として、{nutritional_analysis}による栄養価は{nutrient_profile}を示している。特にGI値と{glycemic_response}の関係で{health_impact}が注目される。",
                    "調理科学の理論では、{culinary_science}による熱伝導は{heat_transfer}のメカニズムで説明できる。特に対流と伝導の{thermal_dynamics}が料理の仕上がりを左右する。",
                    "フードペアリングの研究によると、{flavor_pairing}は分子ガストロノミーの{molecular_gastronomy}理論に基づいている。共通する香気成分の{aroma_compounds}が重要だ。",
                ],
                'constructive': [
                    "この料理は{taste_profile}が絶妙だ。特に{flavor_balance}が素晴らしい。",
                    "食材の{ingredient_quality}が良い。{cooking_technique}も丁寧で好感が持てる。",
                    "お店の{restaurant_atmosphere}も含めて満足度が高い。{service_quality}も良かった。",
                    "この地域の{local_cuisine}として評価できる。{cultural_significance}も感じられる。",
                ],
                'critical': [
                    "また{trend_following}だけの店か。個性がない。",
                    "価格に対して{value_proposition}が見合わない。コスパが悪い。",
                    "SNS映えばかり狙って{instagram_focus}、味は二の次だ。",
                ]
            },
            'viral': {
                'expert': [
                    "デジタル社会学の観点から、{viral_phenomenon}はネットワーク理論の{network_theory}で説明できる。特にスモールワールド現象と{six_degrees}の法則が重要だ。",
                    "情報理論の専門家として、{information_theory}による拡散パターンは{diffusion_model}を示している。特にバズの閾値と{tipping_point}の関係が興味深い。",
                    "メディア心理学の研究では、{media_psychology}による感情的伝染は{emotional_contagion}のメカニズムで説明される。特にミラーニューロンと{empathy_response}が関与している。",
                    "デジタルマーケティングの分析では、{engagement_metrics}によるリーチ効果は{reach_analysis}という結果になる。CTRと{conversion_rate}の最適化が課題だ。",
                ],
                'constructive': [
                    "この現象は{social_impact}という意味で興味深い。{discussion_value}もある。",
                    "拡散の{spread_pattern}を見ると{viral_mechanism}が分かる。勉強になる。",
                    "炎上の{controversy_aspect}だけでなく、{positive_message}も含んでいる。",
                    "この議論は{social_discourse}として価値がある。{awareness_raising}に貢献している。",
                ],
                'critical': [
                    "また{fake_news}に踊らされている。情報リテラシーがない。",
                    "炎上商法の{attention_seeking}だろう。質の悪いコンテンツだ。",
                    "ネットの{mob_mentality}が酷い。冷静になれ。",
                ]
            },
            'youtuber': {
                'expert': [
                    "動画コンテンツ分析の専門家として、{content_analysis}はエンゲージメント理論の{engagement_theory}に基づいている。特に視聴維持率と{audience_retention}の相関が重要だ。",
                    "デジタルメディア研究では、{platform_algorithm}によるレコメンデーションは機械学習の{ml_recommendation}システムで最適化されている。特にCTRと{user_behavior}の学習が鍵となる。",
                    "インフルエンサーマーケティングの理論では、{influencer_impact}はパラソーシャル関係の{parasocial_relationship}で説明できる。特にオーセンティシティと{authenticity_factor}が信頼構築に重要だ。",
                    "動画技術の観点から、{video_technology}による画質向上は{encoding_optimization}とCDNの{content_delivery}が効果的に機能している結果だ。",
                ],
                'constructive': [
                    "この動画の{content_quality}は高い。{editing_skill}も上達している。",
                    "企画の{creative_concept}が面白い。{entertainment_value}もある。",
                    "チャンネルの{channel_growth}が順調だ。{subscriber_engagement}も良い。",
                    "コラボ企画の{collaboration_effect}が成功している。{synergy}も感じられる。",
                ],
                'critical': [
                    "また{clickbait_title}か。中身がない動画だ。",
                    "再生数稼ぎの{view_farming}が露骨すぎる。質を重視しろ。",
                    "炎上狙いの{controversy_baiting}だろう。品がない。",
                ]
            }
        }
        
        # Reply patterns for threading
        self.reply_patterns = {
            'agreement': [
                ">>#{reply_to}\n{commenter_name}さんの意見に同感です。特に{specific_point}については全くその通りだと思います。",
                ">>#{reply_to}\nそれは私も感じていました。{additional_point}も含めて考えると、やはり{conclusion}ですね。",
                ">>#{reply_to}\n貴重な意見をありがとうございます。{support_reason}という理由で賛成します。",
            ],
            'disagreement': [
                ">>#{reply_to}\n{commenter_name}さんの意見も分かりますが、{counter_point}という視点もあるのではないでしょうか。",
                ">>#{reply_to}\nちょっと待ってください。{objection_reason}という問題があります。",
                ">>#{reply_to}\nその考えは{problem_with_view}だと思います。もう少し{suggestion}を考慮すべきです。",
            ],
            'question': [
                ">>#{reply_to}\n{question_point}について詳しく教えていただけませんか？",
                ">>#{reply_to}\nなるほど。ところで{related_question}はどうお考えですか？",
                ">>#{reply_to}\n興味深い指摘ですね。{follow_up_question}という点はいかがでしょう？",
            ],
            'additional_info': [
                ">>#{reply_to}\n補足ですが、{additional_fact}という情報もあります。",
                ">>#{reply_to}\n関連して、{related_information}というニュースも見ました。",
                ">>#{reply_to}\n{source}でも似たような{similar_report}が報道されていました。",
            ]
        }
        
        # Low-quality comment patterns (will get more downvotes)
        self.low_quality_patterns = [
            "は？意味わからん",
            "くだらない",
            "どうでもいい",
            "つまらん",
            "はいはい",
            "で？",
            "知らんがな",
            "勝手にしろ",
            "馬鹿馬鹿しい",
            "時間の無駄",
            "もうええわ",
            "そんなことより",
            "関係ない",
            "どうせ",
            "無理無理",
        ]
        
        self.names = [
            "匿名希望", "一市民", "納税者", "主婦", "会社員",
            "元会社員", "年金生活者", "自営業", "パート", "元公務員",
            "子育て終了組", "団塊世代", "昭和生まれ", "還暦過ぎ", "定年退職者",
            "中年男性", "おばちゃん", "おじさん", "ベテラン", "経験者",
            "先輩", "年上", "人生の先輩", "社会人", "働く母", "元教師",
            "医療関係者", "元公務員", "地方在住", "都市部在住"
        ]
    
    def generate_news_related_comments(self, article_title: str, article_content: str, article_category: str, num_comments: int = 15) -> List[Dict]:
        """Generate news-related comments with threading"""
        comments = []
        
        # Determine article focus for more relevant comments
        article_keywords = self._extract_keywords(article_title + " " + article_content)
        category = self._determine_category(article_category, article_keywords)
        
        # Generate initial comments (40% expert-level, 35% constructive, 20% critical, 5% low-quality)
        initial_count = max(5, int(num_comments * 0.7))
        
        for i in range(initial_count):
            comment_type = self._determine_comment_type(i, initial_count)
            comment = self._generate_single_comment(article_title, article_content, category, comment_type, i + 1)
            comments.append(comment)
        
        # Generate reply threads
        reply_count = num_comments - initial_count
        for i in range(reply_count):
            if comments:  # Only if there are comments to reply to
                target_comment = random.choice(comments)
                reply = self._generate_reply_comment(target_comment, article_title, category, len(comments) + 1)
                comments.append(reply)
        
        return comments
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from article for relevance"""
        important_words = []
        
        # Political keywords
        if any(word in text for word in ['政府', '政治', '首相', '大臣', '政策', '法案', '選挙', '国会']):
            important_words.extend(['政策', '政府', '国会'])
        
        # Economic keywords  
        if any(word in text for word in ['経済', '金融', '税金', '企業', '株価', '市場', '予算']):
            important_words.extend(['経済', '市場', '企業'])
        
        # Technology keywords
        if any(word in text for word in ['AI', 'IT', '技術', 'デジタル', 'システム', 'アプリ']):
            important_words.extend(['技術', 'システム', 'デジタル'])
        
        # Health keywords
        if any(word in text for word in ['医療', '健康', '病院', 'ワクチン', '治療', '薬']):
            important_words.extend(['医療', '健康', '治療'])
        
        return important_words
    
    def _determine_category(self, article_category: str, keywords: List[str]) -> str:
        """Determine comment category based on article"""
        category_mapping = {
            '政治': 'politics',
            '総合': 'politics',
            '経済': 'economics', 
            'ビジネス': 'economics',
            'テクノロジー': 'technology',
            'IT': 'technology',
            '健康': 'health',
            '医療': 'health',
            'スポーツ': 'sports',
            '芸能': 'entertainment',
            'エンタメ': 'entertainment',
            'グルメ': 'food',
            '料理': 'food',
            'フード': 'food',
            '炎上': 'viral',
            'バズ': 'viral',
            'SNS': 'viral',
            'ユーチューバー': 'youtuber',
            'YouTube': 'youtuber',
            '配信': 'youtuber',
            '国際': 'politics'
        }
        
        return category_mapping.get(article_category, 'general')
    
    def _determine_comment_type(self, index: int, total: int) -> str:
        """Determine comment type based on position and randomness"""
        rand = random.random()
        
        # 40% expert-level, 35% constructive, 20% critical, 5% low-quality
        if rand < 0.40:
            return 'expert'
        elif rand < 0.75:  # 0.40 + 0.35
            return 'constructive'
        elif rand < 0.95:  # 0.75 + 0.20
            return 'critical'
        else:
            return 'low_quality'
    
    def _generate_single_comment(self, article_title: str, article_content: str, category: str, comment_type: str, comment_number: int) -> Dict:
        """Generate a single news-related comment"""
        
        if comment_type == 'low_quality':
            return self._generate_low_quality_comment(comment_number)
        
        # Get patterns for the category
        patterns = self.news_related_patterns.get(category, self.news_related_patterns['general'])
        comment_patterns = patterns.get(comment_type, patterns['constructive'])
        
        base_comment = random.choice(comment_patterns)
        
        # Fill in specific details based on article content
        enhanced_comment = self._enhance_comment_with_specifics(base_comment, article_title, article_content, category)
        
        # Determine ratings based on quality
        if comment_type == 'expert':
            likes = random.randint(15, 45)  # Expert comments get high likes
            dislikes = random.randint(0, 2)
        elif comment_type == 'constructive':
            likes = random.randint(5, 25)
            dislikes = random.randint(0, 3)
        elif comment_type == 'critical':
            likes = random.randint(2, 15)
            dislikes = random.randint(1, 8)
        else:  # low_quality
            likes = random.randint(0, 3)
            dislikes = random.randint(8, 25)
        
        return {
            'name': self._get_contextual_name(category, comment_type),
            'text': enhanced_comment,
            'timestamp': (datetime.now() - timedelta(minutes=random.randint(5, 180))).strftime('%Y/%m/%d %H:%M:%S'),
            'likes': likes,
            'dislikes': dislikes,
            'comment_number': comment_number,
            'reply_to': None,
            'quality': comment_type
        }
    
    def _generate_low_quality_comment(self, comment_number: int) -> Dict:
        """Generate low-quality comment that gets downvoted"""
        base_comment = random.choice(self.low_quality_patterns)
        
        # Sometimes add random unrelated content
        if random.random() < 0.4:
            additions = [
                "。お腹空いた",
                "。今日寒いな",
                "。テレビつまらん",
                "。早く家帰りたい",
                "。疲れた",
                "。眠い"
            ]
            base_comment += random.choice(additions)
        
        return {
            'name': random.choice(['通りすがり', '名無し', '匿名', 'ななし', '774']),
            'text': base_comment,
            'timestamp': (datetime.now() - timedelta(minutes=random.randint(1, 30))).strftime('%Y/%m/%d %H:%M:%S'),
            'likes': random.randint(0, 2),
            'dislikes': random.randint(10, 30),  # Lots of downvotes
            'comment_number': comment_number,
            'reply_to': None,
            'quality': 'low_quality'
        }
    
    def _enhance_comment_with_specifics(self, base_comment: str, article_title: str, article_content: str, category: str) -> str:
        """Enhance comment with specific details from the article"""
        
        # Extract specific elements from article for more realistic comments
        specifics = {
            'specific_point': self._extract_specific_point(article_title, article_content),
            'related_case': self._get_related_case(category),
            'difference': self._get_difference_point(category),
            'expert_view': self._get_expert_view(category),
            'practical_impact': self._get_practical_impact(category),
            'local_impact': self._get_local_impact(),
            'legal_aspect': self._get_legal_aspect(category),
            'budget_concern': self._get_budget_concern(),
            'opposition_point': self._get_opposition_point(),
            'implementation_challenge': self._get_implementation_challenge(),
            'election_strategy': self._get_election_strategy(),
            'negative_outcome': self._get_negative_outcome(category),
            'waste_example': self._get_waste_example(),
            'bureaucracy_problem': self._get_bureaucracy_problem(),
            'media_criticism': self._get_media_criticism(),
            'interest_group': self._get_interest_group(category),
        }
        
        # Fill in the template
        try:
            enhanced = base_comment.format(**specifics)
        except KeyError:
            # If some keys are missing, use the base comment
            enhanced = base_comment
        
        return enhanced
    
    def _generate_reply_comment(self, target_comment: Dict, article_title: str, category: str, comment_number: int) -> Dict:
        """Generate a reply comment"""
        
        reply_type = random.choice(['agreement', 'disagreement', 'question', 'additional_info'])
        reply_patterns = self.reply_patterns[reply_type]
        base_reply = random.choice(reply_patterns)
        
        # Create reply-specific content
        reply_specifics = {
            'reply_to': target_comment['comment_number'],
            'commenter_name': target_comment['name'].split('（')[0],  # Remove age/location
            'specific_point': self._extract_specific_point(target_comment['text'], ''),
            'additional_point': self._get_additional_point(category),
            'conclusion': self._get_conclusion(category),
            'support_reason': self._get_support_reason(),
            'counter_point': self._get_counter_point(category),
            'objection_reason': self._get_objection_reason(),
            'problem_with_view': self._get_problem_with_view(),
            'suggestion': self._get_suggestion(category),
            'question_point': self._get_question_point(category),
            'related_question': self._get_related_question(category),
            'follow_up_question': self._get_follow_up_question(),
            'additional_fact': self._get_additional_fact(category),
            'related_information': self._get_related_information(),
            'source': self._get_news_source(),
            'similar_report': self._get_similar_report(),
        }
        
        try:
            enhanced_reply = base_reply.format(**reply_specifics)
        except KeyError:
            enhanced_reply = base_reply
        
        # Adjust ratings based on reply type and target comment quality
        if reply_type == 'agreement' and target_comment.get('quality') == 'constructive':
            likes = random.randint(3, 15)
            dislikes = random.randint(0, 2)
        elif reply_type == 'disagreement':
            likes = random.randint(1, 8)
            dislikes = random.randint(2, 10)
        else:
            likes = random.randint(2, 10)
            dislikes = random.randint(0, 5)
        
        return {
            'name': self._get_contextual_name(category, 'reply'),
            'text': enhanced_reply,
            'timestamp': (datetime.now() - timedelta(minutes=random.randint(1, 120))).strftime('%Y/%m/%d %H:%M:%S'),
            'likes': likes,
            'dislikes': dislikes,
            'comment_number': comment_number,
            'reply_to': target_comment['comment_number'],
            'quality': 'reply'
        }
    
    def _get_contextual_name(self, category: str, comment_type: str = 'constructive') -> str:
        """Get name appropriate for the category and comment type"""
        if comment_type == 'expert':
            if category == 'politics':
                names = ["政治学博士", "元官僚", "行政法専門家", "憲法学者", "公共政策専門家", "政治学教授", "元国会議員秘書", "行政学研究者"]
            elif category == 'economics':
                names = ["経済学博士", "金融アナリスト", "マクロ経済専門家", "元日銀職員", "経済学教授", "計量経済学者", "金融工学博士", "産業組織論専門家"]
            elif category == 'technology':
                names = ["情報工学博士", "セキュリティ専門家", "機械学習研究者", "ソフトウェア工学者", "データサイエンティスト", "AI研究者", "システムアーキテクト", "情報セキュリティ専門家"]
            elif category == 'health':
                names = ["医学博士", "循環器専門医", "疫学研究者", "公衆衛生専門家", "薬剤疫学者", "医療経済学者", "精神科専門医", "感染症専門医"]
            else:
                names = ["社会学博士", "統計学専門家", "環境科学博士", "教育心理学者", "組織行動学専門家", "データ分析専門家"]
        else:
            if category == 'politics':
                names = ["有権者", "元公務員", "政治関心者", "納税者", "地方議員経験者"]
            elif category == 'economics':
                names = ["投資家", "会社員", "自営業者", "元銀行員", "経済学部卒"]
            elif category == 'technology':
                names = ["IT関係者", "エンジニア", "システム管理者", "元SE", "技術者"]
            elif category == 'health':
                names = ["医療関係者", "看護師", "薬剤師", "介護士", "元病院勤務"]
            else:
                names = self.names
        
        base_name = random.choice(names)
        
        # Add credentials for experts, age for others
        if comment_type == 'expert':
            if random.random() < 0.4:
                credentials = ["（大学教授）", "（研究所勤務）", "（博士）", "（専門家）"]
                base_name += random.choice(credentials)
        else:
            if random.random() < 0.3:
                age = random.randint(35, 70)
                base_name += f"（{age}歳）"
        
        return base_name
    
    # Helper methods for generating specific content
    def _extract_specific_point(self, title: str, content: str) -> str:
        if '政策' in title or '政策' in content:
            return "政策の実効性"
        elif '経済' in title or '経済' in content:
            return "経済効果"
        elif '技術' in title or '技術' in content:
            return "技術的な課題"
        else:
            return "今回の内容"
    
    def _get_related_case(self, category: str) -> str:
        cases = {
            'politics': ["前回の法改正", "昨年の政策変更", "過去の同様事例"],
            'economics': ["リーマンショック時", "バブル崩壊時", "前回の不況時"],
            'technology': ["過去のシステム導入", "類似技術の事例", "先行事例"],
            'health': ["SARS対応時", "過去のパンデミック", "類似の医療問題"]
        }
        return random.choice(cases.get(category, ["過去の事例", "類似案件", "前例"]))
    
    def _get_difference_point(self, category: str) -> str:
        differences = {
            'politics': ["法的根拠", "実施手順", "予算規模"],
            'economics': ["市場環境", "金融政策", "財政状況"],
            'technology': ["技術仕様", "セキュリティ対策", "導入方法"],
            'health': ["治療方針", "予防策", "対象範囲"]
        }
        return random.choice(differences.get(category, ["アプローチ", "手法", "方向性"]))
    
    def _get_expert_view(self, category: str) -> str:
        views = {
            'politics': ["慎重な対応が必要", "段階的な実施が望ましい", "より詳細な検討が必要"],
            'economics': ["市場への影響は限定的", "長期的な効果に期待", "リスク管理が重要"],
            'technology': ["セキュリティ対策が急務", "段階的導入が現実的", "国際標準との整合性が必要"],
            'health': ["安全性の確認が最優先", "慎重な運用が必要", "継続的な監視が重要"]
        }
        return random.choice(views.get(category, ["より慎重な検討が必要", "専門的な議論が必要", "多角的な検証が重要"]))
    
    def _get_practical_impact(self, category: str) -> str:
        impacts = {
            'politics': ["地方自治体への負担増加", "行政手続きの複雑化", "市民サービスへの影響"],
            'economics': ["中小企業への負担", "雇用への影響", "家計への負担"],
            'technology': ["現場での混乱", "運用コストの増加", "習熟期間の必要性"],
            'health': ["医療現場への負担", "患者への影響", "医療費への影響"]
        }
        return random.choice(impacts.get(category, ["現場への影響", "実務への負担", "運用上の課題"]))
    
    def _get_local_impact(self) -> str:
        return random.choice([
            "高齢者からは不安の声",
            "商店街では歓迎する声",
            "子育て世代には好評",
            "農家からは反対意見",
            "地元企業は様子見",
            "住民は賛否両論"
        ])
    
    def _get_legal_aspect(self, category: str) -> str:
        aspects = {
            'politics': ["憲法との整合性", "既存法との矛盾", "法的手続きの妥当性"],
            'economics': ["独占禁止法の観点", "税法上の問題", "労働法への影響"],
            'technology': ["個人情報保護法", "著作権法", "電気通信事業法"],
            'health': ["薬事法", "医師法", "個人情報保護"  ]
        }
        return random.choice(aspects.get(category, ["法的な問題", "規制との関係", "コンプライアンス"]))
    
    def _get_budget_concern(self) -> str:
        return random.choice([
            "予算の裏付けが不透明",
            "財源の確保が困難",
            "他の予算を削減する必要",
            "将来世代への負担",
            "費用対効果が疑問",
            "維持費用が膨大"
        ])
    
    def _get_opposition_point(self) -> str:
        return random.choice([
            "手続きの透明性不足",
            "国民への説明不足",
            "拙速な決定",
            "利害関係者の排除",
            "代替案の検討不足",
            "影響評価の甘さ"
        ])
    
    def _get_implementation_challenge(self) -> str:
        return random.choice([
            "人材の確保",
            "システムの構築",
            "関係機関との調整",
            "現場での理解",
            "予算の執行",
            "スケジュールの管理"
        ])
    
    def _get_election_strategy(self) -> str:
        return random.choice([
            "人気取り政策",
            "票集めの道具",
            "支持率回復の手段",
            "選挙対策の一環",
            "有権者への目くらまし",
            "政治的パフォーマンス"
        ])
    
    def _get_negative_outcome(self, category: str) -> str:
        outcomes = {
            'politics': ["行政の混乱", "国民の不信", "政策の破綻"],
            'economics': ["景気の悪化", "失業の増加", "格差の拡大"],
            'technology': ["システム障害", "情報漏洩", "セキュリティ事故"],
            'health': ["医療崩壊", "健康被害", "医療格差"  ]
        }
        return random.choice(outcomes.get(category, ["問題の深刻化", "状況の悪化", "混乱の拡大"]))
    
    def _get_waste_example(self) -> str:
        return random.choice([
            "教育予算",
            "医療費",
            "インフラ整備",
            "災害対策",
            "子育て支援",
            "高齢者福祉"
        ])
    
    def _get_bureaucracy_problem(self) -> str:
        return random.choice([
            "責任逃れ",
            "縦割り行政",
            "前例主義",
            "保身体質",
            "情報隠蔽",
            "先送り体質"
        ])
    
    def _get_media_criticism(self) -> str:
        return random.choice([
            "政府の癒着",
            "利権構造",
            "隠蔽工作",
            "責任の所在",
            "真の問題",
            "裏の事情"
        ])
    
    def _get_interest_group(self, category: str) -> str:
        groups = {
            'politics': ["政治団体", "業界団体", "圧力団体"],
            'economics': ["経済界", "大企業", "既得権益"],
            'technology': ["IT業界", "通信会社", "外資系企業"],
            'health': ["製薬会社", "医師会", "保険会社"]
        }
        return random.choice(groups.get(category, ["利益団体", "既得権益", "特定組織"]))
    
    # Reply-specific helper methods
    def _get_additional_point(self, category: str) -> str:
        points = {
            'politics': ["予算面での課題", "地方への影響", "長期的な視点"],
            'economics': ["国際競争力", "雇用への配慮", "中小企業支援"],
            'technology': ["セキュリティ対策", "プライバシー保護", "デジタル格差"],
            'health': ["安全性の確保", "アクセシビリティ", "費用対効果"]
        }
        return random.choice(points.get(category, ["関連する課題", "付随する問題", "見落としがちな点"]))
    
    def _get_conclusion(self, category: str) -> str:
        conclusions = {
            'politics': ["慎重な対応が必要", "透明性の確保が重要", "国民の理解が不可欠"],
            'economics': ["段階的な実施が現実的", "リスク管理が重要", "持続可能性を重視すべき"],
            'technology': ["安全性を最優先すべき", "段階的導入が妥当", "国際標準に準拠すべき"],
            'health': ["患者の安全が最優先", "科学的根拠に基づくべき", "継続的な監視が必要"]
        }
        return random.choice(conclusions.get(category, ["バランスの取れた対応が必要", "多角的な検討が重要", "慎重な判断が求められる"]))
    
    def _get_support_reason(self) -> str:
        return random.choice([
            "実体験があるから",
            "専門知識があるから",
            "過去の事例を知っているから",
            "現場の声を聞いているから",
            "データを確認したから",
            "類似の成功例があるから"
        ])
    
    def _get_counter_point(self, category: str) -> str:
        points = {
            'politics': ["財政負担の問題", "実効性への疑問", "公平性の観点"],
            'economics': ["市場への悪影響", "競争力の低下", "雇用への懸念"],
            'technology': ["セキュリティリスク", "プライバシー侵害", "技術的制約"],
            'health': ["副作用のリスク", "費用対効果", "アクセシビリティ"]
        }
        return random.choice(points.get(category, ["異なる視点", "別の考え方", "反対の立場"]))
    
    def _get_objection_reason(self) -> str:
        return random.choice([
            "過去の失敗例がある",
            "データが不十分",
            "リスクが高すぎる",
            "代替案がある",
            "時期尚早",
            "前提条件が不明"
        ])
    
    def _get_problem_with_view(self) -> str:
        return random.choice([
            "一面的すぎる",
            "楽観的すぎる",
            "現実的でない",
            "根拠が薄弱",
            "偏見がある",
            "情報不足"
        ])
    
    def _get_suggestion(self, category: str) -> str:
        suggestions = {
            'politics': ["段階的実施", "試験運用", "国民対話"],
            'economics': ["市場調査", "影響評価", "段階的導入"],
            'technology': ["セキュリティ監査", "プライバシー影響評価", "ユーザビリティテスト"],
            'health': ["臨床試験", "安全性評価", "倫理審査"]
        }
        return random.choice(suggestions.get(category, ["慎重な検討", "専門家の意見", "多角的な分析"]))
    
    def _get_question_point(self, category: str) -> str:
        questions = {
            'politics': ["予算の詳細", "実施スケジュール", "責任の所在"],
            'economics': ["具体的な効果", "影響範囲", "費用対効果"],
            'technology': ["セキュリティ対策", "運用体制", "障害時の対応"],
            'health': ["安全性データ", "適用条件", "副作用情報"]
        }
        return random.choice(questions.get(category, ["詳細な内容", "具体的な方法", "実施体制"]))
    
    def _get_related_question(self, category: str) -> str:
        questions = {
            'politics': ["他の政策との整合性", "地方自治体の対応", "国際的な動向"],
            'economics': ["他業界への影響", "国際競争力", "長期的な効果"],
            'technology': ["既存システムとの連携", "国際標準への対応", "将来の拡張性"],
            'health': ["他の治療法との比較", "海外での事例", "保険適用の可能性"]
        }
        return random.choice(questions.get(category, ["関連する課題", "波及効果", "今後の展開"]))
    
    def _get_follow_up_question(self) -> str:
        return random.choice([
            "実現可能性",
            "スケジュール",
            "費用負担",
            "責任体制",
            "評価方法",
            "見直し時期"
        ])
    
    def _get_additional_fact(self, category: str) -> str:
        facts = {
            'politics': ["過去の統計データでは", "他国の事例では", "専門機関の報告によると"],
            'economics': ["市場データによると", "経済指標を見ると", "業界団体の調査では"],
            'technology': ["技術動向調査では", "セキュリティ報告書によると", "国際標準では"],
            'health': ["臨床データでは", "疫学調査によると", "WHO報告では"]
        }
        return random.choice(facts.get(category, ["調査結果によると", "データを見ると", "専門家によると"]))
    
    def _get_related_information(self) -> str:
        return random.choice([
            "類似の取り組み",
            "関連する動き",
            "同様の議論",
            "参考になる事例",
            "注目すべき動向",
            "興味深い報告"
        ])
    
    def _get_news_source(self) -> str:
        return random.choice([
            "NHK", "読売新聞", "朝日新聞", "毎日新聞", "日経新聞",
            "共同通信", "時事通信", "産経新聞", "東京新聞", "地方紙"
        ])
    
    def _get_similar_report(self) -> str:
        return random.choice([
            "同様の内容",
            "関連する報道",
            "追加情報",
            "詳細な分析",
            "専門家のコメント",
            "現場の声"
        ])
    
    # Expert-specific helper methods
    def _get_constitution_article(self) -> str:
        return random.choice(["14", "19", "20", "21", "22", "25", "41", "73", "76", "94"])
    
    def _get_policy_analysis(self) -> str:
        return random.choice([
            "効果測定の明確性",
            "実証的根拠の充実",
            "定量的評価指標",
            "因果関係の明確化",
            "統計的有意性"
        ])
    
    def _get_international_position(self) -> str:
        return random.choice([
            "中位",
            "上位",
            "下位",
            "平均的な位置",
            "特異な位置"
        ])
    
    def _get_fiscal_sustainability(self) -> str:
        return random.choice([
            "財政持続可能性",
            "債務残高比率",
            "プライマリーバランス",
            "世代間公平性"
        ])
    
    def _get_is_lm_effect(self) -> str:
        return random.choice([
            "金利低下効果",
            "投資促進効果",
            "クラウディングアウト",
            "流動性の罠"
        ])
    
    def _get_complexity_class(self) -> str:
        return random.choice([
            "P",
            "NP",
            "NP完全",
            "PSPACE",
            "多項式時間"
        ])
    
    def _get_security_improvement(self) -> str:
        return random.choice([
            "暗号強度の向上",
            "脆弱性の削減",
            "認証機能の強化",
            "アクセス制御の改善"
        ])
    
    def _get_nnt_value(self) -> str:
        return random.choice(["10", "15", "20", "25", "50", "100"])
    
    def _get_r0_value(self) -> str:
        return random.choice(["1.2", "1.5", "2.1", "2.8", "3.5", "0.8"])


# Usage example
if __name__ == "__main__":
    generator = EnhancedCommentGenerator()
    
    # Test with a political article
    article_title = "政府が新税制改革を発表、消費税率変更を検討"
    article_content = "政府は本日、新しい税制改革案を発表しました。消費税率の変更や法人税の見直しが含まれており、国民生活への影響が懸念されています。"
    article_category = "政治"
    
    comments = generator.generate_news_related_comments(article_title, article_content, article_category, 12)
    
    for i, comment in enumerate(comments, 1):
        print(f"\n--- コメント {i} ---")
        if comment.get('reply_to'):
            print(f"[返信 → #{comment['reply_to']}]")
        print(f"名前: {comment['name']}")
        print(f"内容: {comment['text']}")
        print(f"時刻: {comment['timestamp']}")
        print(f"👍 {comment['likes']} 👎 {comment['dislikes']} (品質: {comment.get('quality', 'unknown')})")