#!/usr/bin/env python3
"""
Extended News Sources Configuration
100+ categories and genres including SNS trends, gossip, and global coverage
"""

# 🌍 メインニュースソース（100+カテゴリ）
NEWS_SOURCES = {
    # 🌍 国際ニュース
    'international': [
        {'url': 'https://news.google.com/rss?hl=ja&gl=JP&ceid=JP:ja', 'name': 'Google News Japan', 'lang': 'ja'},
        {'url': 'https://feeds.bbci.co.uk/news/world/rss.xml', 'name': 'BBC World', 'lang': 'en'},
        {'url': 'https://rss.nytimes.com/services/xml/rss/nyt/World.xml', 'name': 'NY Times World', 'lang': 'en'},
        {'url': 'https://www.aljazeera.com/xml/rss/all.xml', 'name': 'Al Jazeera', 'lang': 'en'},
        {'url': 'https://feeds.reuters.com/reuters/topNews', 'name': 'Reuters', 'lang': 'en'},
        {'url': 'https://www.theguardian.com/world/rss', 'name': 'The Guardian', 'lang': 'en'},
        {'url': 'https://feeds.washingtonpost.com/rss/world', 'name': 'Washington Post', 'lang': 'en'},
        {'url': 'https://feeds.foxnews.com/foxnews/world', 'name': 'Fox News World', 'lang': 'en'},
        {'url': 'https://www.france24.com/en/rss', 'name': 'France 24', 'lang': 'en'},
        {'url': 'https://www.dw.com/rss/en/news/rss.xml', 'name': 'Deutsche Welle', 'lang': 'en'},
        {'url': 'https://feeds.skynews.com/feeds/rss/world.xml', 'name': 'Sky News', 'lang': 'en'},
        {'url': 'https://www3.nhk.or.jp/rss/news/cat0.xml', 'name': 'NHK News', 'lang': 'ja'}
    ],
    
    # 🎭 エンタメ・芸能
    'entertainment': [
        {'url': 'https://news.yahoo.co.jp/rss/categories/entertainment', 'name': 'Yahoo!ニュース芸能', 'lang': 'ja'},
        {'url': 'https://www.oricon.co.jp/rss/news.xml', 'name': 'ORICON NEWS', 'lang': 'ja'},
        {'url': 'https://www.cinematoday.jp/rss/news', 'name': 'シネマトゥデイ', 'lang': 'ja'},
        {'url': 'https://natalie.mu/music/feed/news', 'name': '音楽ナタリー', 'lang': 'ja'},
        {'url': 'https://natalie.mu/eiga/feed/news', 'name': '映画ナタリー', 'lang': 'ja'},
        {'url': 'https://natalie.mu/comic/feed/news', 'name': 'コミックナタリー', 'lang': 'ja'},
        {'url': 'https://www.billboard-japan.com/rss/news', 'name': 'Billboard JAPAN', 'lang': 'ja'},
        {'url': 'https://www.hollywoodreporter.com/feed', 'name': 'Hollywood Reporter', 'lang': 'en'},
        {'url': 'https://variety.com/feed/', 'name': 'Variety', 'lang': 'en'},
        {'url': 'https://deadline.com/feed/', 'name': 'Deadline', 'lang': 'en'},
        {'url': 'https://www.eonline.com/syndication/feeds/rssfeeds/topstories.xml', 'name': 'E! Online', 'lang': 'en'},
        {'url': 'https://www.tmz.com/rss.xml', 'name': 'TMZ', 'lang': 'en'},
        {'url': 'https://pagesix.com/feed/', 'name': 'Page Six', 'lang': 'en'}
    ],
    
    # ⚽ スポーツ
    'sports': [
        {'url': 'https://news.yahoo.co.jp/rss/categories/sports', 'name': 'Yahoo!スポーツ', 'lang': 'ja'},
        {'url': 'https://www3.nhk.or.jp/rss/news/cat7.xml', 'name': 'NHKスポーツ', 'lang': 'ja'},
        {'url': 'https://www.nikkansports.com/rss/sports.xml', 'name': '日刊スポーツ', 'lang': 'ja'},
        {'url': 'https://www.sponichi.co.jp/rss/sports.xml', 'name': 'スポニチ', 'lang': 'ja'},
        {'url': 'https://rss.espn.com/espn/topheadlines', 'name': 'ESPN', 'lang': 'en'},
        {'url': 'https://www.skysports.com/rss/12040', 'name': 'Sky Sports', 'lang': 'en'},
        {'url': 'https://www.marca.com/rss/portada.xml', 'name': 'Marca', 'lang': 'es'},
        {'url': 'https://feeds.foxsports.com/foxsports/latest', 'name': 'Fox Sports', 'lang': 'en'},
        {'url': 'https://www.sportingnews.com/rss', 'name': 'Sporting News', 'lang': 'en'},
        {'url': 'https://bleacherreport.com/articles/feed', 'name': 'Bleacher Report', 'lang': 'en'}
    ],
    
    # 💻 テクノロジー
    'technology': [
        {'url': 'https://techcrunch.com/feed/', 'name': 'TechCrunch', 'lang': 'en'},
        {'url': 'https://feeds.arstechnica.com/arstechnica/technology-lab', 'name': 'Ars Technica', 'lang': 'en'},
        {'url': 'https://www.theverge.com/rss/index.xml', 'name': 'The Verge', 'lang': 'en'},
        {'url': 'https://www.wired.com/feed/rss', 'name': 'WIRED', 'lang': 'en'},
        {'url': 'https://www.engadget.com/rss.xml', 'name': 'Engadget', 'lang': 'en'},
        {'url': 'https://gizmodo.com/rss', 'name': 'Gizmodo', 'lang': 'en'},
        {'url': 'https://www.techmeme.com/feed.xml', 'name': 'Techmeme', 'lang': 'en'},
        {'url': 'https://news.ycombinator.com/rss', 'name': 'Hacker News', 'lang': 'en'},
        {'url': 'https://www.itmedia.co.jp/rss/20/index.xml', 'name': 'ITmedia', 'lang': 'ja'},
        {'url': 'https://gigazine.net/news/rss_2.0/', 'name': 'GIGAZINE', 'lang': 'ja'},
        {'url': 'https://jp.techcrunch.com/feed/', 'name': 'TechCrunch Japan', 'lang': 'ja'},
        {'url': 'https://www.gizmodo.jp/index.xml', 'name': 'ギズモード', 'lang': 'ja'}
    ],
    
    # 💰 経済・ビジネス
    'business': [
        {'url': 'https://feeds.bloomberg.com/markets/news.rss', 'name': 'Bloomberg', 'lang': 'en'},
        {'url': 'https://feeds.reuters.com/reuters/businessNews', 'name': 'Reuters Business', 'lang': 'en'},
        {'url': 'https://www.wsj.com/xml/rss/3_7085.xml', 'name': 'Wall Street Journal', 'lang': 'en'},
        {'url': 'https://www.forbes.com/real-time/feed2/', 'name': 'Forbes', 'lang': 'en'},
        {'url': 'https://fortune.com/feed', 'name': 'Fortune', 'lang': 'en'},
        {'url': 'https://www.businessinsider.com/rss', 'name': 'Business Insider', 'lang': 'en'},
        {'url': 'https://www.nikkei.com/rss/news.rdf', 'name': '日経新聞', 'lang': 'ja'},
        {'url': 'https://toyokeizai.net/list/feed/rss', 'name': '東洋経済', 'lang': 'ja'},
        {'url': 'https://diamond.jp/feed/all', 'name': 'ダイヤモンド', 'lang': 'ja'},
        {'url': 'https://president.jp/list/rss', 'name': 'プレジデント', 'lang': 'ja'}
    ],
    
    # 🔬 科学・研究
    'science': [
        {'url': 'https://www.nature.com/nature.rss', 'name': 'Nature', 'lang': 'en'},
        {'url': 'https://www.science.org/rss/news_current.xml', 'name': 'Science', 'lang': 'en'},
        {'url': 'https://feeds.newscientist.com/science-news', 'name': 'New Scientist', 'lang': 'en'},
        {'url': 'https://www.scientificamerican.com/feed', 'name': 'Scientific American', 'lang': 'en'},
        {'url': 'https://www.sciencedaily.com/rss/all.xml', 'name': 'Science Daily', 'lang': 'en'},
        {'url': 'https://phys.org/rss-feed/', 'name': 'Phys.org', 'lang': 'en'},
        {'url': 'https://www.livescience.com/feeds/all', 'name': 'Live Science', 'lang': 'en'},
        {'url': 'https://www.eurekalert.org/rss.xml', 'name': 'EurekAlert!', 'lang': 'en'},
        {'url': 'https://feeds.nationalgeographic.com/ng/News/News_Main', 'name': 'National Geographic', 'lang': 'en'},
        {'url': 'https://news.mit.edu/rss/feed', 'name': 'MIT News', 'lang': 'en'},
        {'url': 'https://www.jst.go.jp/pr/rss/press.xml', 'name': 'JST', 'lang': 'ja'}
    ],
    
    # 🏥 健康・医療
    'health': [
        {'url': 'https://www.webmd.com/xml/rss/RSSFeeds.xml', 'name': 'WebMD', 'lang': 'en'},
        {'url': 'https://www.medicalnewstoday.com/rss/news.xml', 'name': 'Medical News Today', 'lang': 'en'},
        {'url': 'https://www.healthline.com/rss', 'name': 'Healthline', 'lang': 'en'},
        {'url': 'https://www.mayoclinic.org/rss/all-news', 'name': 'Mayo Clinic', 'lang': 'en'},
        {'url': 'https://feeds.harvard.edu/rss/hub_health_medicine.xml', 'name': 'Harvard Health', 'lang': 'en'},
        {'url': 'https://www.nih.gov/news-events/news-releases/feed', 'name': 'NIH', 'lang': 'en'},
        {'url': 'https://www.who.int/feeds/entity/mediacentre/news/en/rss.xml', 'name': 'WHO', 'lang': 'en'},
        {'url': 'https://www.m3.com/news/rss/general', 'name': 'm3.com', 'lang': 'ja'},
        {'url': 'https://medical.nikkeibp.co.jp/inc/all/rss/facebook.xml', 'name': '日経メディカル', 'lang': 'ja'}
    ],
    
    # 🎮 ゲーム・eスポーツ
    'gaming': [
        {'url': 'https://www.4gamer.net/rss/index.xml', 'name': '4Gamer', 'lang': 'ja'},
        {'url': 'https://www.famitsu.com/rss/fcom_news.xml', 'name': 'ファミ通', 'lang': 'ja'},
        {'url': 'https://game.watch.impress.co.jp/data/rss/1.0/gmw/feed.rdf', 'name': 'Game Watch', 'lang': 'ja'},
        {'url': 'https://www.gamespark.jp/rss/index.xml', 'name': 'GameSpark', 'lang': 'ja'},
        {'url': 'https://automaton-media.com/feed/', 'name': 'AUTOMATON', 'lang': 'ja'},
        {'url': 'https://www.ign.com/rss/articles', 'name': 'IGN', 'lang': 'en'},
        {'url': 'https://www.gamespot.com/feeds/news/', 'name': 'GameSpot', 'lang': 'en'},
        {'url': 'https://www.polygon.com/rss/index.xml', 'name': 'Polygon', 'lang': 'en'},
        {'url': 'https://kotaku.com/rss', 'name': 'Kotaku', 'lang': 'en'},
        {'url': 'https://www.pcgamer.com/rss/', 'name': 'PC Gamer', 'lang': 'en'}
    ],
    
    # 👗 ファッション・美容
    'fashion': [
        {'url': 'https://www.fashion-press.net/rss/news.xml', 'name': 'Fashion Press', 'lang': 'ja'},
        {'url': 'https://www.fashionsnap.com/rss/index.xml', 'name': 'Fashionsnap', 'lang': 'ja'},
        {'url': 'https://www.wwdjapan.com/rss/feed', 'name': 'WWD JAPAN', 'lang': 'ja'},
        {'url': 'https://www.vogue.co.jp/rss/fashion.xml', 'name': 'VOGUE JAPAN', 'lang': 'ja'},
        {'url': 'https://www.elle.com/jp/rss/fashion.xml', 'name': 'ELLE JAPAN', 'lang': 'ja'},
        {'url': 'https://www.beautynewstokyo.jp/feed', 'name': 'Beauty News Tokyo', 'lang': 'ja'},
        {'url': 'https://www.cosme.net/rss/news.xml', 'name': '@cosme', 'lang': 'ja'}
    ],
    
    # 🚗 自動車・バイク
    'automotive': [
        {'url': 'https://response.jp/rss/index.xml', 'name': 'Response', 'lang': 'ja'},
        {'url': 'https://car.watch.impress.co.jp/data/rss/1.0/car/feed.rdf', 'name': 'Car Watch', 'lang': 'ja'},
        {'url': 'https://carview.yahoo.co.jp/rss/news/', 'name': 'carview!', 'lang': 'ja'},
        {'url': 'https://www.webcg.net/rss/index.xml', 'name': 'webCG', 'lang': 'ja'},
        {'url': 'https://motor-fan.jp/rss/article', 'name': 'Motor-Fan', 'lang': 'ja'},
        {'url': 'https://jp.autoblog.com/rss.xml', 'name': 'Autoblog JP', 'lang': 'ja'},
        {'url': 'https://bikebros.co.jp/rss/news.xml', 'name': 'BikeJIN', 'lang': 'ja'},
        {'url': 'https://young-machine.com/feed/', 'name': 'ヤングマシン', 'lang': 'ja'}
    ],
    
    # 🏛️ 政治・政策
    'politics': [
        {'url': 'https://www3.nhk.or.jp/rss/news/cat4.xml', 'name': 'NHK政治', 'lang': 'ja'},
        {'url': 'https://www.jiji.com/rss/ranking.xml', 'name': '時事通信', 'lang': 'ja'},
        {'url': 'https://feeds.reuters.com/reuters/JPPoliticsNews', 'name': 'Reuters 政治', 'lang': 'ja'},
        {'url': 'https://www.asahi.com/rss/politics.rdf', 'name': '朝日新聞政治', 'lang': 'ja'},
        {'url': 'https://rss.mainichi.jp/rss/etc/mainichi-seiji.rss', 'name': '毎日新聞政治', 'lang': 'ja'},
        {'url': 'https://feeds.cnn.com/rss/edition_politics.rss', 'name': 'CNN Politics', 'lang': 'en'},
        {'url': 'https://feeds.foxnews.com/foxnews/politics', 'name': 'Fox Politics', 'lang': 'en'},
        {'url': 'https://www.politico.com/rss/politics.xml', 'name': 'Politico', 'lang': 'en'}
    ],
    
    # 🌿 環境・エコロジー
    'environment': [
        {'url': 'https://www.env.go.jp/press/index.xml', 'name': '環境省', 'lang': 'ja'},
        {'url': 'https://sustainablejapan.jp/feed', 'name': 'Sustainable Japan', 'lang': 'ja'},
        {'url': 'https://www.alterna.co.jp/feed/', 'name': 'オルタナ', 'lang': 'ja'},
        {'url': 'https://www.kankyo-business.jp/rss/news.xml', 'name': '環境ビジネス', 'lang': 'ja'},
        {'url': 'https://www.theguardian.com/environment/rss', 'name': 'Guardian Environment', 'lang': 'en'},
        {'url': 'https://e360.yale.edu/feed', 'name': 'Yale E360', 'lang': 'en'},
        {'url': 'https://insideclimatenews.org/feed/', 'name': 'Inside Climate News', 'lang': 'en'},
        {'url': 'https://grist.org/feed/', 'name': 'Grist', 'lang': 'en'}
    ],
    
    # 🏫 教育・学習
    'education': [
        {'url': 'https://www.mext.go.jp/b_menu/news/index.xml', 'name': '文部科学省', 'lang': 'ja'},
        {'url': 'https://resemom.jp/rss/index.rdf', 'name': 'リセマム', 'lang': 'ja'},
        {'url': 'https://kyoiku.yomiuri.co.jp/rss/index.xml', 'name': '読売教育', 'lang': 'ja'},
        {'url': 'https://univ-journal.jp/feed/', 'name': '大学ジャーナル', 'lang': 'ja'},
        {'url': 'https://edtechzine.jp/rss/index.xml', 'name': 'EdTechZine', 'lang': 'ja'},
        {'url': 'https://ict-enews.net/feed/', 'name': 'ICT教育ニュース', 'lang': 'ja'}
    ],
    
    # 🎬 映画
    'movies': [
        {'url': 'https://eiga.com/rss/news/', 'name': '映画.com', 'lang': 'ja'},
        {'url': 'https://www.cinematoday.jp/rss/news', 'name': 'シネマトゥデイ', 'lang': 'ja'},
        {'url': 'https://moviewalker.jp/rss/news.xml', 'name': 'MovieWalker', 'lang': 'ja'},
        {'url': 'https://filmaga.filmarks.com/rss', 'name': 'Filmaga', 'lang': 'ja'},
        {'url': 'https://theriver.jp/feed/', 'name': 'THE RIVER', 'lang': 'ja'},
        {'url': 'https://www.hollywoodreporter.com/movies/feed', 'name': 'Hollywood Reporter Movies', 'lang': 'en'},
        {'url': 'https://variety.com/v/film/feed/', 'name': 'Variety Movies', 'lang': 'en'},
        {'url': 'https://deadline.com/v/film/feed/', 'name': 'Deadline Movies', 'lang': 'en'}
    ],
    
    # 🎵 音楽
    'music': [
        {'url': 'https://rockinon.com/rss/news', 'name': 'rockinon.com', 'lang': 'ja'},
        {'url': 'https://www.barks.jp/rss/news100.xml', 'name': 'BARKS', 'lang': 'ja'},
        {'url': 'https://natalie.mu/music/feed/news', 'name': '音楽ナタリー', 'lang': 'ja'},
        {'url': 'https://www.musicman.co.jp/rss/news.xml', 'name': 'MUSICMAN', 'lang': 'ja'},
        {'url': 'https://www.billboard-japan.com/rss/news', 'name': 'Billboard JAPAN', 'lang': 'ja'},
        {'url': 'https://realsound.jp/feed', 'name': 'Real Sound', 'lang': 'ja'},
        {'url': 'https://pitchfork.com/rss/news/', 'name': 'Pitchfork', 'lang': 'en'},
        {'url': 'https://www.rollingstone.com/music/feed/', 'name': 'Rolling Stone', 'lang': 'en'},
        {'url': 'https://www.nme.com/news/music/feed', 'name': 'NME', 'lang': 'en'}
    ]
}

# 🔥 SNSトレンド・ゴシップ・炎上系ニュースソース
SNS_TREND_SOURCES = {
    # 🐦 Twitter/X トレンド
    'twitter_trends': {
        'realtime_search': [
            {'url': 'https://search.yahoo.co.jp/realtime', 'name': 'Yahoo!リアルタイム検索', 'lang': 'ja', 'type': 'scraping'},
            {'url': 'https://twittrend.jp/', 'name': 'ついっトレンド', 'lang': 'ja', 'type': 'scraping'},
            {'url': 'https://trends24.in/japan/', 'name': 'Trends24 Japan', 'lang': 'ja', 'type': 'scraping'},
            {'url': 'https://getdaytrends.com/japan/', 'name': 'GetDayTrends Japan', 'lang': 'ja', 'type': 'scraping'},
            {'url': 'https://www.google.com/trends/trendingsearches/realtime?geo=JP', 'name': 'Google Trends JP', 'lang': 'ja', 'type': 'api'},
            {'url': 'https://www.google.com/trends/trendingsearches/realtime?geo=US', 'name': 'Google Trends US', 'lang': 'en', 'type': 'api'},
            {'url': 'https://www.google.com/trends/trendingsearches/realtime?geo=KR', 'name': 'Google Trends KR', 'lang': 'ko', 'type': 'api'}
        ]
    },
    
    # 📺 YouTube トレンド・ニュース
    'youtube_sources': [
        # 日本のニュース系YouTuber
        {'url': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCFCkHhKmwsRnqhmCS-UClmw', 'name': 'ABEMA NEWS', 'lang': 'ja'},
        {'url': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCGCZAYq5Xxojl_tSXcVJhiQ', 'name': 'FNN', 'lang': 'ja'},
        {'url': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCkKVQ_GNjd8FbAuT6xDcWgg', 'name': 'TBS NEWS', 'lang': 'ja'},
        {'url': 'https://www.youtube.com/feeds/videos.xml?channel_id=UC8WYZ7hG8IxvS7Y0WKtvEJQ', 'name': 'ANNnews', 'lang': 'ja'},
        
        # エンタメ・ゴシップ系
        {'url': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCQ_iBh8Rt0sFqUlwUSU6Cgw', 'name': '文春オンライン', 'lang': 'ja'},
        {'url': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCOyV2bdKJcEGrZ2fZPvFo5A', 'name': 'Friday', 'lang': 'ja'},
        {'url': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCjlB8xHgmKfgD0UZU7fXHaA', 'name': '東スポ', 'lang': 'ja'},
        
        # 炎上・議論系（注意：センシティブなコンテンツの可能性）
        {'url': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCjV1HabiEMwWHADj4DiAHKg', 'name': 'コレコレ', 'lang': 'ja'},
        
        # 韓国エンタメ
        {'url': 'https://www.youtube.com/feeds/videos.xml?channel_id=UC5BMQOsAB8hKUyHu9KI6yig', 'name': 'SBS News', 'lang': 'ko'},
        {'url': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCF4Wxdo3inmxP-Y59wXDsFw', 'name': 'MBC News', 'lang': 'ko'},
        {'url': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCcQTRi69dsVYHN3exePtZ1A', 'name': 'KBS News', 'lang': 'ko'},
        
        # アメリカ
        {'url': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCeY0bbntWzzVIaj2z3QigXg', 'name': 'NBC News', 'lang': 'en'},
        {'url': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCW1bfNu6gzUcFqh3qJlQ7ig', 'name': 'TMZ', 'lang': 'en'},
        {'url': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCdtXPiqI2cLorKaPrfpKc4g', 'name': 'Entertainment Tonight', 'lang': 'en'}
    ],
    
    # 🔥 炎上・ゴシップ専門サイト
    'gossip_sources': {
        'japanese': [
            {'url': 'https://girlschannel.net/rss/feed.rss', 'name': 'ガールズちゃんねる', 'lang': 'ja', 'reliability': 0.4},
            {'url': 'https://bakusai.com/rss/feed.xml', 'name': '爆サイ', 'lang': 'ja', 'reliability': 0.3},
            {'url': 'https://matomedane.jp/feed', 'name': 'まとめダネ', 'lang': 'ja', 'reliability': 0.5},
            {'url': 'https://togetter.com/rss/index', 'name': 'Togetter', 'lang': 'ja', 'reliability': 0.6},
            {'url': 'https://b.hatena.ne.jp/hotentry/all.rss', 'name': 'はてブ総合', 'lang': 'ja', 'reliability': 0.7},
            {'url': 'https://b.hatena.ne.jp/hotentry/entertainment.rss', 'name': 'はてブ芸能', 'lang': 'ja', 'reliability': 0.7},
            {'url': 'https://nogizaka-journal.com/feed/', 'name': '乃木坂ジャーナル', 'lang': 'ja', 'reliability': 0.5},
            {'url': 'https://johnnys-watcher.net/feed/', 'name': 'ジャニーズウォッチャー', 'lang': 'ja', 'reliability': 0.4}
        ],
        'korean': [
            {'url': 'https://www.dispatch.co.kr/rss/allArticle.xml', 'name': 'Dispatch', 'lang': 'ko', 'reliability': 0.6},
            {'url': 'https://www.allkpop.com/feed', 'name': 'allkpop', 'lang': 'en', 'reliability': 0.5},
            {'url': 'https://www.koreaboo.com/feed/', 'name': 'Koreaboo', 'lang': 'en', 'reliability': 0.5},
            {'url': 'https://www.soompi.com/feed/', 'name': 'Soompi', 'lang': 'en', 'reliability': 0.7},
            {'url': 'https://kbizoom.com/feed', 'name': 'Kbizoom', 'lang': 'en', 'reliability': 0.4},
            {'url': 'https://www.knetizen.com/feed/', 'name': 'Knetizen', 'lang': 'en', 'reliability': 0.4},
            {'url': 'https://netizenbuzz.blogspot.com/feeds/posts/default', 'name': 'Netizen Buzz', 'lang': 'en', 'reliability': 0.5},
            {'url': 'https://www.kstarlive.com/rss', 'name': 'KStarLive', 'lang': 'en', 'reliability': 0.5}
        ],
        'american': [
            {'url': 'https://www.tmz.com/rss.xml', 'name': 'TMZ', 'lang': 'en', 'reliability': 0.6},
            {'url': 'https://pagesix.com/feed/', 'name': 'Page Six', 'lang': 'en', 'reliability': 0.6},
            {'url': 'https://www.thecut.com/rss.xml', 'name': 'The Cut', 'lang': 'en', 'reliability': 0.7},
            {'url': 'https://www.justjared.com/feed/', 'name': 'Just Jared', 'lang': 'en', 'reliability': 0.5},
            {'url': 'https://www.eonline.com/syndication/feeds/rssfeeds/topstories.xml', 'name': 'E! Online', 'lang': 'en', 'reliability': 0.6},
            {'url': 'https://hollywoodlife.com/feed/', 'name': 'Hollywood Life', 'lang': 'en', 'reliability': 0.4},
            {'url': 'https://radaronline.com/feed/', 'name': 'Radar Online', 'lang': 'en', 'reliability': 0.3},
            {'url': 'https://blindgossip.com/feed/', 'name': 'Blind Gossip', 'lang': 'en', 'reliability': 0.3},
            {'url': 'https://dlisted.com/feed/', 'name': 'Dlisted', 'lang': 'en', 'reliability': 0.4}
        ]
    },
    
    # 📊 リアルタイムトレンド収集
    'realtime_trends': {
        'reddit': [
            {'url': 'https://www.reddit.com/r/all/hot/.rss', 'name': 'Reddit All', 'lang': 'en', 'reliability': 0.6},
            {'url': 'https://www.reddit.com/r/worldnews/hot/.rss', 'name': 'Reddit WorldNews', 'lang': 'en', 'reliability': 0.7},
            {'url': 'https://www.reddit.com/r/entertainment/hot/.rss', 'name': 'Reddit Entertainment', 'lang': 'en', 'reliability': 0.6},
            {'url': 'https://www.reddit.com/r/SubredditDrama/hot/.rss', 'name': 'Reddit Drama', 'lang': 'en', 'reliability': 0.5},
            {'url': 'https://www.reddit.com/r/PublicFreakout/hot/.rss', 'name': 'Reddit PublicFreakout', 'lang': 'en', 'reliability': 0.4},
            {'url': 'https://www.reddit.com/r/LivestreamFail/hot/.rss', 'name': 'Reddit LivestreamFail', 'lang': 'en', 'reliability': 0.5}
        ]
    },
    
    # 🎭 芸能事務所・公式
    'entertainment_official': {
        'japan': [
            {'url': 'https://www.johnnys-net.jp/rss/feed.xml', 'name': 'ジャニーズ', 'lang': 'ja', 'reliability': 0.9},
            {'url': 'https://avex.jp/rss/news.xml', 'name': 'エイベックス', 'lang': 'ja', 'reliability': 0.9},
            {'url': 'https://www.amuse.co.jp/rss/news.xml', 'name': 'アミューズ', 'lang': 'ja', 'reliability': 0.9},
            {'url': 'https://www.horipro.co.jp/rss/news.xml', 'name': 'ホリプロ', 'lang': 'ja', 'reliability': 0.9},
            {'url': 'https://www.watanabepro.co.jp/rss/news.xml', 'name': 'ワタナベプロ', 'lang': 'ja', 'reliability': 0.9}
        ],
        'korea': [
            {'url': 'https://www.smtown.com/rss/news.xml', 'name': 'SM Entertainment', 'lang': 'ko', 'reliability': 0.9},
            {'url': 'https://www.jype.com/rss/news.xml', 'name': 'JYP Entertainment', 'lang': 'ko', 'reliability': 0.9},
            {'url': 'https://www.ygfamily.com/rss/news.xml', 'name': 'YG Entertainment', 'lang': 'ko', 'reliability': 0.9},
            {'url': 'https://www.bighitmusic.com/rss/news.xml', 'name': 'HYBE (Big Hit)', 'lang': 'ko', 'reliability': 0.9}
        ]
    },
    
    # 💬 掲示板・フォーラム
    'forums': {
        'japanese': [
            {'url': 'https://www.2nn.jp/rss/news.xml', 'name': '2NN', 'lang': 'ja', 'reliability': 0.5},
            {'url': 'https://newsoku.blog/feed', 'name': 'ニュー速', 'lang': 'ja', 'reliability': 0.4},
            {'url': 'https://vippers.jp/feed', 'name': 'VIPPERSブログ', 'lang': 'ja', 'reliability': 0.4},
            {'url': 'https://world-fusigi.net/feed', 'name': '不思議.net', 'lang': 'ja', 'reliability': 0.4},
            {'url': 'https://alfalfalfa.com/index.rdf', 'name': 'アルファルファモザイク', 'lang': 'ja', 'reliability': 0.4}
        ]
    },
    
    # 🎬 ストリーミング配信ニュース
    'streaming': {
        'twitch': [
            {'url': 'https://blog.twitch.tv/en/feed/', 'name': 'Twitch Blog', 'lang': 'en', 'reliability': 0.8},
            {'url': 'https://www.dexerto.com/entertainment/feed/', 'name': 'Dexerto', 'lang': 'en', 'reliability': 0.6},
            {'url': 'https://streamerscharts.com/feed', 'name': 'StreamersCharts', 'lang': 'en', 'reliability': 0.7}
        ]
    }
}

# 🌐 地域別グローバルニュースソース
GLOBAL_NEWS_SOURCES = {
    'north_america': [
        {'url': 'https://rss.cbc.ca/lineup/topstories.xml', 'name': 'CBC Canada', 'lang': 'en'},
        {'url': 'https://feeds.npr.org/1001/rss.xml', 'name': 'NPR', 'lang': 'en'},
        {'url': 'https://feeds.latimes.com/latimes/news', 'name': 'LA Times', 'lang': 'en'},
        {'url': 'https://rss.chicagotribune.com/news/feed', 'name': 'Chicago Tribune', 'lang': 'en'},
        {'url': 'https://www.seattletimes.com/feed/', 'name': 'Seattle Times', 'lang': 'en'},
        {'url': 'https://rss.miami.com/news/', 'name': 'Miami Herald', 'lang': 'en'}
    ],
    'south_america': [
        {'url': 'https://rss.uol.com.br/feed/noticias.xml', 'name': 'UOL Brasil', 'lang': 'pt'},
        {'url': 'https://www.clarin.com/rss/lo-ultimo/', 'name': 'Clarín Argentina', 'lang': 'es'},
        {'url': 'https://elcomercio.pe/feed/lima.xml', 'name': 'El Comercio Perú', 'lang': 'es'},
        {'url': 'https://www.eltiempo.com/rss/mundo.xml', 'name': 'El Tiempo Colombia', 'lang': 'es'},
        {'url': 'https://www.emol.com/rss/noticias.xml', 'name': 'Emol Chile', 'lang': 'es'}
    ],
    'europe': [
        {'url': 'https://www.lemonde.fr/rss/une.xml', 'name': 'Le Monde', 'lang': 'fr'},
        {'url': 'https://www.spiegel.de/schlagzeilen/index.rss', 'name': 'Der Spiegel', 'lang': 'de'},
        {'url': 'https://www.corriere.it/rss/homepage.xml', 'name': 'Corriere della Sera', 'lang': 'it'},
        {'url': 'https://elpais.com/rss/elpais/portada.xml', 'name': 'El País', 'lang': 'es'},
        {'url': 'https://www.svd.se/rss.xml', 'name': 'Svenska Dagbladet', 'lang': 'sv'}
    ],
    'middle_east': [
        {'url': 'https://www.haaretz.com/cmlink/1.4463960', 'name': 'Haaretz', 'lang': 'en'},
        {'url': 'https://www.dailysabah.com/rss', 'name': 'Daily Sabah', 'lang': 'en'},
        {'url': 'https://english.alarabiya.net/tools/rss', 'name': 'Al Arabiya', 'lang': 'en'},
        {'url': 'https://www.thenationalnews.com/rss', 'name': 'The National', 'lang': 'en'},
        {'url': 'https://www.tehrantimes.com/rss', 'name': 'Tehran Times', 'lang': 'en'}
    ],
    'africa': [
        {'url': 'https://ewn.co.za/RSS%20Feeds/Latest%20News', 'name': 'EWN South Africa', 'lang': 'en'},
        {'url': 'https://www.herald.co.zw/feed/', 'name': 'The Herald Zimbabwe', 'lang': 'en'},
        {'url': 'https://nairobinews.nation.co.ke/feed', 'name': 'Nairobi News', 'lang': 'en'},
        {'url': 'https://www.vanguardngr.com/feed/', 'name': 'Vanguard Nigeria', 'lang': 'en'}
    ],
    'asia_pacific': [
        {'url': 'https://www.straitstimes.com/news/singapore/rss.xml', 'name': 'Straits Times', 'lang': 'en'},
        {'url': 'https://www.bangkokpost.com/rss/latest', 'name': 'Bangkok Post', 'lang': 'en'},
        {'url': 'https://vietnamnews.vn/rss/home.rss', 'name': 'Vietnam News', 'lang': 'en'},
        {'url': 'https://www.thejakartapost.com/feed', 'name': 'Jakarta Post', 'lang': 'en'},
        {'url': 'https://www.nzherald.co.nz/arc/outboundfeeds/rss/', 'name': 'NZ Herald', 'lang': 'en'}
    ],
    'russia_cis': [
        {'url': 'https://tass.ru/rss/v2.xml', 'name': 'TASS', 'lang': 'ru'},
        {'url': 'https://www.rt.com/rss/', 'name': 'RT', 'lang': 'en'},
        {'url': 'https://www.pravda.com.ua/rss/view_news/', 'name': 'Pravda Ukraine', 'lang': 'uk'},
        {'url': 'https://akipress.com/rss/all/', 'name': 'AKIpress', 'lang': 'en'}
    ]
}

# 🎯 特殊カテゴリ
SPECIAL_CATEGORIES = {
    # 🎰 ギャンブル・宝くじ
    'gambling': [
        {'url': 'https://www.jra.go.jp/news/rss/index.xml', 'name': 'JRA', 'lang': 'ja'},
        {'url': 'https://www.keiba.go.jp/rss/news.xml', 'name': '地方競馬', 'lang': 'ja'},
        {'url': 'https://news.netkeiba.com/?pid=rss', 'name': 'netkeiba', 'lang': 'ja'},
        {'url': 'https://www.boatrace.jp/rss/index.xml', 'name': 'ボートレース', 'lang': 'ja'},
        {'url': 'https://takarakuji-official.jp/rss/index.xml', 'name': '宝くじ公式', 'lang': 'ja'}
    ],
    
    # 🚀 宇宙・天文
    'space': [
        {'url': 'https://www.jaxa.jp/rss/index.xml', 'name': 'JAXA', 'lang': 'ja'},
        {'url': 'https://www.nao.ac.jp/rss/index.xml', 'name': '国立天文台', 'lang': 'ja'},
        {'url': 'https://sorae.info/feed', 'name': 'sorae', 'lang': 'ja'},
        {'url': 'https://www.astroarts.co.jp/rss/index.xml', 'name': 'AstroArts', 'lang': 'ja'},
        {'url': 'https://www.nasa.gov/rss/dyn/breaking_news.rss', 'name': 'NASA', 'lang': 'en'},
        {'url': 'https://www.space.com/feeds/all', 'name': 'Space.com', 'lang': 'en'},
        {'url': 'https://spaceflightnow.com/feed/', 'name': 'Spaceflight Now', 'lang': 'en'},
        {'url': 'https://www.universetoday.com/feed', 'name': 'Universe Today', 'lang': 'en'}
    ],
    
    # 🏛️ 歴史・考古学
    'history': [
        {'url': 'https://www.nabunken.go.jp/rss/index.xml', 'name': '奈良文化財研究所', 'lang': 'ja'},
        {'url': 'https://www.bunka.go.jp/rss/index.xml', 'name': '文化庁', 'lang': 'ja'},
        {'url': 'https://bushoojapan.com/feed', 'name': '武将ジャパン', 'lang': 'ja'},
        {'url': 'https://sengoku-his.com/feed', 'name': '戦国ヒストリー', 'lang': 'ja'},
        {'url': 'https://intojapanwaraku.com/feed/', 'name': '和樂web', 'lang': 'ja'}
    ],
    
    # 🕍 宗教・スピリチュアル
    'religion': [
        {'url': 'https://www.jinja-honcho.or.jp/rss/index.xml', 'name': '神社本庁', 'lang': 'ja'},
        {'url': 'https://www.bukkyo-times.co.jp/rss/index.xml', 'name': '仏教タイムス', 'lang': 'ja'},
        {'url': 'https://www.christiantoday.co.jp/rss/index.xml', 'name': 'クリスチャントゥデイ', 'lang': 'ja'},
        {'url': 'https://www.el-aura.com/feed/', 'name': 'ELALRA', 'lang': 'ja'},
        {'url': 'https://trinity-jp.com/feed/', 'name': 'Trinity', 'lang': 'ja'}
    ]
}

# 📊 信頼性・センシティブ度スコア定義
RELIABILITY_SCORES = {
    'official': 0.9,      # 政府機関、公式発表
    'mainstream': 0.8,    # 大手メディア
    'specialized': 0.7,   # 専門メディア
    'entertainment': 0.6, # エンタメ系メディア
    'social': 0.5,       # SNS、掲示板
    'gossip': 0.4,       # ゴシップ系
    'rumor': 0.3         # 噂・未確認情報
}

SENSITIVE_LEVELS = {
    'low': 1,      # 一般的なニュース
    'medium': 5,   # 議論を呼ぶ可能性
    'high': 8,     # 炎上・対立を含む
    'extreme': 10  # 非常にセンシティブ
}

# 🎯 DeepSeekプロンプト（トレンド・炎上対応版）
TREND_ANALYSIS_PROMPT = """
以下のSNSトレンド・炎上系ニュースを分析し、2000文字の記事を作成してください。

トレンド情報：
- ソース: {source_type} ({platform})
- トレンドワード/動画: {trend_title}
- 関連情報: {related_info}
- 言語: {original_language}
- 地域: {region}
- 信頼性スコア: {reliability_score}/10
- センシティブ度: {sensitive_level}/10

記事作成時の注意点：
1. ゴシップ・炎上系の場合は、事実と推測を明確に区別
2. 複数の視点を含める（賛否両論）
3. SNSの反応も含める
4. 文化的背景の説明（特に海外ニュース）
5. 炎上の経緯と現在の状況を時系列で整理
6. プライバシーや人権に配慮した表現

構成：
1. タイトル（キャッチーだが誇張しない、30文字以内）
2. 概要（何が起きているか、200文字）
3. 経緯説明（なぜ話題になったか、500文字）
4. 各方面の反応（SNS、メディア、当事者、800文字）
5. 影響と今後（炎上の社会的影響、400文字）
6. 関連情報（過去の類似事例など、100文字）

必ずJSON形式で返答：
{{
    "title_ja": "記事タイトル",
    "lead_ja": "概要",
    "background_ja": "経緯説明", 
    "analysis_ja": "各方面の反応",
    "outlook_ja": "影響と今後",
    "related_info_ja": "関連情報",
    "fact_check": "事実確認済み部分",
    "speculation": "推測・噂の部分",
    "social_impact": "社会的影響度（1-10）"
}}
"""

# 💡 トレンド収集用関数のプロトタイプ
def collect_twitter_trends():
    """Twitter/Xのトレンドを収集"""
    pass

def collect_youtube_trending():
    """YouTube急上昇動画からニュース価値のあるものを抽出"""
    pass

def process_gossip_content(content):
    """ゴシップ・炎上系コンテンツの処理"""
    pass

def analyze_sns_sentiment(content):
    """SNS上の感情分析"""
    pass

def detect_trending_keywords(sources):
    """複数ソースからトレンドキーワードを検出"""
    pass