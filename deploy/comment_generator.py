#!/usr/bin/env python3
"""
Middle-aged Know-it-all Comment Generator
Generates authentic-sounding comments from middle-aged users with strong opinions
"""

import random
from datetime import datetime, timezone, timedelta
from typing import Dict, List

class CommentGenerator:
    def __init__(self):
        self.comment_patterns = {
            'know_it_all': [
                "私が若い頃はこんなことはなかった。日本も落ちたものだ",
                "これは明らかに政府の陰謀ですね。調べればすぐ分かることです",
                "マスコミは真実を報道しない。私は実際に現場を知っている",
                "昔から言われていることですが、若い人は知らないでしょうね",
                "私の知人の医者も同じことを言っていました",
                "これは経済学の基本です。少し勉強すれば分かることですが",
                "私は以前この業界にいたので内情をよく知っています",
                "テレビでは言えない真実があるんですよ",
                "これは氷山の一角に過ぎません。本当の闇はもっと深い",
                "私もそうなるんじゃないかと思っていました。予想通りです",
                "現場を知らない人の意見ですね。実際は全然違います",
                "これについては専門家の間でも意見が分かれているんです"
            ],
            'political': [
                "また税金の無駄遣いか。我々の血税が",
                "野党は批判ばかりで対案を出さない。いつものことだが",
                "これだから今の政治家は信用できない",
                "選挙前だけいいことを言う。国民を馬鹿にしている",
                "官僚の天下りがまた始まった。利権の温床だ",
                "マスコミと政府は裏で繋がっている。報道規制は明らか",
                "この国の未来は暗い。若者が可哀想だ",
                "また増税か。取りやすいところから取る。卑怯な手だ",
                "政治献金の見返りに便宜を図っている。癒着は明らか",
                "これも選挙対策でしょう。国民のことなど考えていない",
                "公約違反も甚だしい。有権者を騙している",
                "既得権益を守るために必死ですね。分かりやすい"
            ],
            'nostalgic': [
                "昭和の時代は良かった。今の若者は甘やかされすぎ",
                "私達の世代は苦労して今の日本を作った",
                "最近の若い人は礼儀を知らない。親の教育がなっていない",
                "バブルの頃を知っている世代としては今の不景気が信じられない",
                "昔は近所付き合いがあった。今は人情が失われた",
                "私の若い頃は月給3万円で頑張った。今の若者は贅沢だ",
                "高度経済成長期を支えた我々世代の努力を無駄にしないでほしい",
                "昔は家族の絆が強かった。今は個人主義で寂しい時代",
                "私達の時代は終身雇用が当たり前だった。今は不安定で気の毒",
                "戦後復興を成し遂げた先人達の苦労を若い人は知らない",
                "昔は職人が尊敬されていた。今は技術が軽視されている"
            ],
            'health_conscious': [
                "これは体に悪い。私は健康のために絶対に避けている",
                "医者に聞いたが、これは危険だそうだ",
                "私は毎朝ウォーキングをしているが、最近の若者は運動不足だ",
                "添加物まみれの食品ばかり。昔の食べ物は安全だった",
                "ワクチンについては賛否両論ある。私は慎重派だ",
                "最近の医療は金儲け主義。昔の医者は患者のことを考えていた",
                "健康食品に月10万使っているが、病院には行かない",
                "化学調味料は体に毒。天然のものしか摂取しません",
                "農薬まみれの野菜は危険。有機栽培しか買わない",
                "電磁波の健康被害について、もっと研究すべき",
                "薬に頼らず自然治癒力を高めることが大切"
            ],
            'condescending': [
                "まあ、若い人にはまだ分からないでしょうが",
                "経験不足な人の意見ですね。もう少し社会を知ってから発言すべき",
                "私も若い頃は同じように考えていました。今思えば恥ずかしい",
                "これは常識ですよ。知らないのは勉強不足では？",
                "私の長年の経験から言わせてもらうと",
                "素人考えですね。プロの目から見れば明らか",
                "もっと視野を広げて物事を見るべきです",
                "表面的な情報に惑わされているようですね",
                "もう少し人生経験を積めば理解できるようになりますよ",
                "理想論では世の中は動きません。現実を見なさい",
                "若い方の純粋な気持ちは分かりますが、世間はそんなに甘くない"
            ],
            'conspiracy': [
                "メディアは真実を隠している。裏には巨大な組織が",
                "これは表向きの理由。本当の目的は別にある",
                "ネットで調べれば真実が分かる。テレビは嘘ばかり",
                "某国の工作員が日本を破壊しようとしている",
                "これは人口削減計画の一環だ。気づいている人は少ない",
                "5Gの電波で健康被害が。政府は隠蔽している",
                "グローバリストの陰謀だ。日本が狙われている",
                "製薬会社とWHOは癒着している。利益のためなら何でもする",
                "気象兵器による人工的な災害。偶然ではありえない",
                "報道されない真実がある。自分で情報を集めないと騙される",
                "このタイミングでこのニュース。仕組まれている"
            ],
            'passive_aggressive': [
                "まあ、人それぞれ考え方がありますからね（笑）",
                "若い方の意見も参考になります（苦笑）",
                "なるほど、そういう見方もあるんですね（呆）",
                "最近はこういう意見が主流なんでしょうか？時代ですね",
                "私は違うと思いますが、まあいいでしょう",
                "そうですか。勉強になりました（棒）",
                "面白い意見ですね。私なら違う結論になりますが",
                "へぇ〜、そうなんですか（遠い目）",
                "お若いっていいですね。何でも信じられて",
                "そういう考え方もあるんですね。知りませんでした（白目）",
                "なるほど〜。深いですね〜（棒読み）"
            ],
            'angry': [
                "ふざけるなよ！いい加減にしろ！",
                "もうウンザリだ。この国はどうなってしまうんだ",
                "許せない！絶対に許せない！",
                "もう我慢の限界だ。黙っていられない",
                "こんなことが許されていいのか！",
                "税金返せ！詐欺と同じだろこれ",
                "いつまで国民を舐めてるんだ",
                "責任取れよ！誰が責任取るんだ！",
                "最低だな。人として最低",
                "頭に来る！本当に頭に来る！"
            ],
            'sad': [
                "悲しすぎます。涙が出ます",
                "こんな世の中で子供を育てるのが不安",
                "日本の将来が心配でなりません",
                "昔の良き時代が懐かしい",
                "こんなはずじゃなかった。残念です",
                "希望が持てない。絶望的な気持ち",
                "孫の世代が心配。どうなってしまうのか",
                "もう疲れました。何もかも嫌になる",
                "虚しいです。何のために働いてきたのか",
                "この国に未来はあるのでしょうか"
            ]
        }
        
        self.names = [
            "匿名希望", "一市民", "納税者", "主婦", "会社員",
            "元会社員", "年金生活者", "自営業", "パート", "元公務員",
            "子育て終了組", "団塊世代", "昭和生まれ", "還暦過ぎ", "定年退職者",
            "中年男性", "おばちゃん", "おじさん", "ベテラン", "経験者",
            "先輩", "年上", "人生の先輩", "社会人", "働く母"
        ]
        
        # Battle phrases for reply comments
        self.battle_phrases = [
            "何言ってるんだ？理解力がないね",
            "あなたこそ間違ってる。勉強し直せ",
            "そんな考えだから日本がダメになる",
            "もっと現実を見ろよ。世間知らず",
            "典型的な○○脳だな。洗脳されてる",
            "そういう考えが一番危険なんだよ",
            "あなたには理解できないでしょうね",
            "レベルが違いすぎて話にならない",
            "もう少し大人になってから発言しろ",
            "議論する価値もない意見ですね"
        ]
    
    def generate_middle_aged_comment(self, article_content, comment_number):
        """中高年風のコメント生成"""
        
        # 記事内容に応じてコメントタイプを選択
        content_lower = article_content.lower()
        
        if any(word in content_lower for word in ["政治", "政府", "総理", "大臣", "選挙"]):
            types = ['political', 'know_it_all', 'conspiracy', 'angry']
        elif any(word in content_lower for word in ["若者", "世代", "教育", "子供"]):
            types = ['nostalgic', 'condescending', 'know_it_all']
        elif any(word in content_lower for word in ["健康", "医療", "病院", "薬", "ワクチン"]):
            types = ['health_conscious', 'know_it_all', 'conspiracy']
        elif any(word in content_lower for word in ["経済", "給料", "税金", "年金"]):
            types = ['political', 'nostalgic', 'angry']
        elif any(word in content_lower for word in ["芸能", "スキャンダル", "不倫"]):
            types = ['condescending', 'passive_aggressive', 'angry']
        elif any(word in content_lower for word in ["事故", "災害", "死亡", "被害"]):
            types = ['sad', 'conspiracy', 'know_it_all']
        else:
            types = ['know_it_all', 'condescending', 'passive_aggressive']
        
        # 感情に基づく重み付け（炎上しやすい話題は強い感情）
        if any(word in content_lower for word in ["炎上", "批判", "問題", "疑惑"]):
            types.extend(['angry', 'conspiracy'] * 2)  # 重み付けで追加
        
        # コメントタイプを選択
        comment_type = random.choice(types)
        base_comment = random.choice(self.comment_patterns[comment_type])
        
        # 長文にする確率（中高年は長文を書きがち）
        if random.random() < 0.7:
            additions = [
                "\n\n私の若い頃の経験から言うと、" + self.generate_personal_anecdote(),
                "\n\nちなみに私の知り合いの" + self.generate_friend_story(),
                "\n\n最近のニュースを見ていると本当に心配になります。",
                "\n\n長文失礼しました。言いたいことがあると、つい。",
                "\n\n補足ですが、" + random.choice(self.comment_patterns['know_it_all']),
                "\n\n追記：" + random.choice(self.comment_patterns[comment_type]),
                "\n\nあと、これも関係あるんですが、" + self.generate_related_complaint()
            ]
            base_comment += random.choice(additions)
        
        # さらに追加の可能性
        if random.random() < 0.4:
            base_comment += "\n\n" + random.choice([
                "もうこの国は終わりですね。",
                "私達の税金がこんなことに使われるなんて。",
                "マスコミはこういうことは報道しない。",
                "若い人はもっと勉強すべき。",
                "昔はこんなことはなかった。"
            ])
        
        # たまに絵文字や顔文字を使う（不慣れな感じ）
        if random.random() < 0.4:
            emojis = ["(^_^;)", "(^^;)", "(´･_･`)", "(-_-;)", "(･_･;", "^^;", "...", "(呆)", "(怒)", "(涙)"]
            base_comment += " " + random.choice(emojis)
        
        return base_comment
    
    def generate_personal_anecdote(self):
        """個人的な体験談を生成"""
        anecdotes = [
            "バブルの頃は本当に景気が良かった。あの頃を知らない世代は可哀想",
            "昔勤めていた会社では考えられないことです。時代が変わりました",
            "子供が小さい頃はこんな心配はなかった。今の親御さんは大変",
            "私も同じような経験があります。あの時は本当に大変でした",
            "実は私も被害に遭ったことがあるんです。警察も動いてくれなかった",
            "父の時代はもっと厳しかった。でも筋が通っていた",
            "昔の上司はこう言っていました。『最近の若い者は』と",
            "私の母が生きていたら何と言うだろうか",
            "戦争を体験した祖父の話を思い出します",
            "昔住んでいた街では考えられないことです"
        ]
        return random.choice(anecdotes)
    
    def generate_friend_story(self):
        """知り合いの話を生成"""
        stories = [
            "医者がこれは危険だと言っていました。",
            "弁護士も同じ意見でした。法的にも問題があるそうです。",
            "大手企業の役員も、裏では全く違うことを言っています。",
            "元官僚も、これは表に出せない事情があると。",
            "大学教授も首を傾げていました。学問的にもおかしいと。",
            "看護師が実情を教えてくれました。",
            "教師をしている友人も同じことを言っています。",
            "警察官の知り合いから聞いた話では、",
            "銀行員の息子が、金融業界の裏事情を話してくれました。",
            "農家の親戚が言うには、実際の状況は違うそうです。"
        ]
        return random.choice(stories)
    
    def generate_related_complaint(self):
        """関連する愚痴を生成"""
        complaints = [
            "最近の電車のマナーも悪くなった",
            "コンビニの店員の態度も気になります",
            "若い政治家は頼りない",
            "テレビ番組の質も下がった",
            "食べ物の味も昔より落ちている",
            "近所付き合いも希薄になった",
            "職場の人間関係も変わった",
            "病院の待ち時間も長くなった",
            "年金制度も不安だし",
            "子供の教育も心配です"
        ]
        return random.choice(complaints)
    
    def generate_reply_comment(self, target_num, target_comment):
        """レスバトル用の返信コメント生成"""
        
        # 元コメントの感情を分析
        if any(word in target_comment for word in ["若い", "甘い", "理想"]):
            reply_type = "condescending"
        elif any(word in target_comment for word in ["政府", "政治", "税金"]):
            reply_type = "political"
        elif any(word in target_comment for word in ["間違い", "違う", "おかしい"]):
            reply_type = "angry"
        else:
            reply_type = random.choice(["condescending", "passive_aggressive", "know_it_all"])
        
        base_replies = [
            f">>>{target_num}\nあなたはまだお若いようですね。私の年齢になれば分かりますよ。",
            f">>>{target_num}\nそれは表面的な見方です。もっと深く考える必要があります。",
            f">>>{target_num}\n私は実際に経験していますから。机上の空論では困ります。",
            f">>>{target_num}\nマスコミの情報を鵜呑みにしているようですね。真実は違います。",
            f">>>{target_num}\n若い方の意見も大切ですが、経験がものを言う場合もあります。",
            f">>>{target_num}\nその考えは甘いですね。社会の厳しさを知らない。",
            f">>>{target_num}\n私も昔はそう思っていました。でも現実は違うんです。",
            f">>>{target_num}\n" + random.choice(self.battle_phrases)
        ]
        
        reply = random.choice(base_replies)
        
        # さらに長文で反論する確率
        if random.random() < 0.6:
            additional_content = random.choice(self.comment_patterns[reply_type])
            reply += "\n\n" + additional_content
        
        # 追い打ちをかける
        if random.random() < 0.3:
            reply += "\n\n" + random.choice([
                "まあ、理解できない人に説明しても無駄でしょうが。",
                "もう少し人生経験を積んでから発言することをお勧めします。",
                "現実を知らない人との議論は時間の無駄ですね。",
                "あなたのような考えの人がいるから日本がダメになる。",
                "これ以上は時間の無駄なので終わりにします。"
            ])
        
        return reply
    
    def get_random_name(self):
        """中高年風の名前"""
        base_name = random.choice(self.names)
        
        # 年齢や地域を付ける
        if random.random() < 0.3:
            age = random.randint(45, 75)
            base_name += f"（{age}歳）"
        
        if random.random() < 0.2:
            regions = ["東京", "大阪", "名古屋", "福岡", "北海道", "地方都市", "田舎", "関東", "関西", "九州"]
            base_name += f"・{random.choice(regions)}在住"
        
        if random.random() < 0.1:
            occupations = ["会社員", "主婦", "自営業", "公務員", "無職"]
            base_name += f"・{random.choice(occupations)}"
        
        return base_name
    
    def generate_initial_comments(self, article_content, num_comments=15):
        """記事用の初期コメント群を生成"""
        comments = []
        
        for i in range(num_comments):
            comment_text = self.generate_middle_aged_comment(article_content, i + 1)
            
            # たまに返信コメントを生成
            if i > 3 and random.random() < 0.3:
                target_comment_idx = random.randint(0, len(comments) - 1)
                target_comment = comments[target_comment_idx]
                comment_text = self.generate_reply_comment(target_comment_idx + 1, target_comment['text'])
            
            comment = {
                'name': self.get_random_name(),
                'text': comment_text,
                'timestamp': (datetime.now() - timedelta(minutes=random.randint(5, 180))).strftime('%Y/%m/%d %H:%M:%S'),
                'likes': random.randint(0, 25),
                'dislikes': random.randint(0, 8)
            }
            
            comments.append(comment)
        
        return comments


# Usage example
if __name__ == "__main__":
    generator = CommentGenerator()
    
    # Generate comments for a political article
    article_content = "政府が新しい税制改革を発表しました。消費税の増税が検討されています。"
    
    comments = generator.generate_initial_comments(article_content, 10)
    
    for i, comment in enumerate(comments, 1):
        print(f"\n--- コメント {i} ---")
        print(f"名前: {comment['name']}")
        print(f"内容: {comment['text']}")
        print(f"時刻: {comment['timestamp']}")
        print(f"👍 {comment['likes']} 👎 {comment['dislikes']}")