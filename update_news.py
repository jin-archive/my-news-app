import feedparser
import json
import datetime

# 💡 수정됨: 각 주소별로 우리가 보여줄 '깔끔한 언론사 이름'을 짝지어(Dictionary) 지정해 줍니다.
rss_sources = {
    "https://news.sbs.co.kr/news/TopicRssFeed.do?plink=RSSREADER": "SBS",
    "https://news-ex.jtbc.co.kr/v1/get/rss/issue": "JTBC",
    "https://www.yna.co.kr/rss/news.xml": "연합뉴스",
    "https://rss.donga.com/total.xml": "동아일보",
    "https://www.chosun.com/arc/outboundfeeds/rss/?outputType=xml": "조선일보",
    "https://www.hankyung.com/feed/all-news": "한국경제",
    "https://www.mk.co.kr/rss/40300001/": "매일경제",
    "https://www.khan.co.kr/rss/rssdata/total_news.xml": "경향신문",
    "https://www.hani.co.kr/rss/": "한겨레",
    "https://www.newsis.com/RSS/sokbo.xml": "뉴시스",
    "http://www.kookje.co.kr/news2011/rss/newslist.xml": "국제신문",
    "https://www.imaeil.com/rss": "매일신문",
    "https://www.mediatoday.co.kr/rss/allArticle.xml": "미디어오늘",
    "http://rss.etnews.com/Section903.xml": "전자신문"
}

news_data = []

# 짝지어둔 주소(url)와 언론사 이름(source_name)을 하나씩 꺼내서 반복
for url, source_name in rss_sources.items():
    try:
        feed = feedparser.parse(url)
        
        # 각 언론사별 최신 뉴스 50개 가져오기
        for entry in feed.entries[:50]:
            news_data.append({
                "title": entry.title,
                "link": entry.link,
                "published": getattr(entry, 'published', ''),
                "source": source_name # 원본 이름 대신 우리가 지정한 깔끔한 이름을 넣습니다.
            })
    except Exception as e:
        print(f"[{url}] 파싱 중 에러 발생: {e}")

# 업데이트 시간 및 뉴스 데이터 구조화
output_data = {
    "updated_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "news": news_data
}

# news.json 파일로 저장
with open("news.json", "w", encoding="utf-8") as f:
    json.dump(output_data, f, ensure_ascii=False, indent=4)
