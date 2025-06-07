#!/usr/bin/env python3
"""
Test DeepSeek News Generation
Generate today's news with 2000-character articles
"""

import os
import json
import requests
from datetime import datetime

def test_deepseek_news():
    api_key = os.getenv("DEEPSEEK_API_KEY", "sk-9689ac1bcc6248cf842cc16816cd2829")
    api_url = "https://api.deepseek.com/v1/chat/completions"
    
    today = datetime.now().strftime("%Y年%m月%d日")
    
    prompt = f"""
    {today}の最新ニュースを生成してください。
    
    テクノロジー分野で最も注目すべきニュースを1つ選び、以下の構成で2000文字の詳細記事を作成してください：
    
    1. タイトル（30文字以内）
    2. リード文（200文字）- なぜこのニュースが重要かを説明
    3. 背景説明（500文字）- このニュースに至る経緯や関連する歴史
    4. 詳細分析（800文字）- 技術的詳細、影響範囲、専門家の視点を含む深い分析
    5. 今後の展望（400文字）- このニュースがもたらす未来への影響
    6. 関連情報（100文字）- 読者が更に知るべき情報
    
    現実的で具体的な内容にしてください。
    必ず指定された文字数に近い長さで各セクションを書いてください。
    
    JSON形式で返答：
    {{
        "title": "タイトル",
        "lead": "リード文",
        "background": "背景説明",
        "analysis": "詳細分析",
        "outlook": "今後の展望",
        "related_info": "関連情報",
        "total_characters": 全体の文字数
    }}
    """
    
    print(f"Generating news for {today}...")
    
    try:
        response = requests.post(
            api_url,
            json={
                "model": "deepseek-reasoner",
                "messages": [
                    {"role": "system", "content": "あなたは優秀なテクノロジージャーナリストです。"},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 4000
            },
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            timeout=60.0
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            # Extract JSON
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]
            
            article = json.loads(content.strip())
            
            # Display the article
            print("\n" + "="*60)
            print(f"📰 {article['title']}")
            print("="*60)
            
            print(f"\n【リード文】")
            print(article['lead'])
            
            print(f"\n【背景説明】")
            print(article['background'])
            
            print(f"\n【詳細分析】")
            print(article['analysis'])
            
            print(f"\n【今後の展望】")
            print(article['outlook'])
            
            print(f"\n【関連情報】")
            print(article['related_info'])
            
            print(f"\n総文字数: {article.get('total_characters', 'N/A')}")
            
            # Save to file
            with open('deepseek_news_test.json', 'w', encoding='utf-8') as f:
                json.dump(article, f, ensure_ascii=False, indent=2)
            
            print("\n✅ Article saved to deepseek_news_test.json")
            
        else:
            print(f"❌ API Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_deepseek_news()