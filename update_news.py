import feedparser
import json
import datetime
import re # HTML 태그 제거를 위한 모듈 추가

# 언론사 분류 맵핑
rss_sources = {
    "https://news.sbs.co.kr/news/TopicRssFeed.do?plink=RSSREADER": "SBS",
    "https://news-ex.jtbc.co.kr/v1/get/rss/issue": "JTBC",
    "https://www.yna.co.kr/rss/news.xml": "연합뉴스",
    "https://www.newsis.com/RSS/sokbo.xml": "뉴시스",
    "https://www.chosun.com/arc/outboundfeeds/rss/?outputType=xml": "조선일보",
    "https://rss.donga.com/total.xml": "동아일보",
    "https://www.khan.co.kr/rss/rssdata/total_news.xml": "경향신문",
    "https://www.hani.co.kr/rss/": "한겨레",
    "https://www.mk.co.kr/rss/40300001/": "매일경제",
    "https://www.hankyung.com/feed/all-news": "한국경제",
    "http://rss.etnews.com/Section903.xml": "전자신문",
    "https://www.imaeil.com/rss": "매일신문",
    "http://www.kookje.co.kr/news2011/rss/newslist.xml": "국제신문",
    "https://www.mediatoday.co.kr/rss/allArticle.xml": "미디어오늘"
}

news_data = []

for url, source_name in rss_sources.items():
    try:
        feed = feedparser.parse(url)
        
        for entry in feed.entries[:50]:
            # 💡 추가됨: 기사 요약본 가져오기 (HTML 태그가 섞여있을 수 있어 제거 처리)
            raw_summary = getattr(entry, 'description', getattr(entry, 'summary', '요약이 제공되지 않는 기사입니다.'))
            clean_summary = re.sub('<[^<]+>', '', raw_summary).strip() # 깔끔한 텍스트만 추출
            if not clean_summary:
                clean_summary = "이 기사는 언론사에서 요약본을 제공하지 않습니다."

            news_data.append({
                "title": entry.title,
                "link": entry.link,
                "published": getattr(entry, 'published', ''),
                "source": source_name,
                "summary": clean_summary # JSON 데이터에 추가
            })
    except Exception as e:
        print(f"[{url}] 파싱 중 에러 발생: {e}")

output_data = {
    "updated_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "news": news_data
}

with open("news.json", "w", encoding="utf-8") as f:
    json.dump(output_data, f, ensure_ascii=False, indent=4)
