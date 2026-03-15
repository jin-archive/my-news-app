import feedparser
import json
import datetime

# 14개 언론사 RSS 주소 목록
rss_urls = [
    "https://news.sbs.co.kr/news/TopicRssFeed.do?plink=RSSREADER",
    "https://news-ex.jtbc.co.kr/v1/get/rss/issue",
    "https://www.yna.co.kr/rss/news.xml",
    "https://rss.donga.com/total.xml",
    "https://www.chosun.com/arc/outboundfeeds/rss/?outputType=xml",
    "https://www.hankyung.com/feed/all-news",
    "https://www.mk.co.kr/rss/40300001/",
    "https://www.khan.co.kr/rss/rssdata/total_news.xml",
    "https://www.hani.co.kr/rss/",
    "https://www.newsis.com/RSS/sokbo.xml",
    "http://www.kookje.co.kr/news2011/rss/newslist.xml",
    "https://www.imaeil.com/rss",
    "https://www.mediatoday.co.kr/rss/allArticle.xml",
    "http://rss.etnews.com/Section903.xml"
]

news_data = []

for url in rss_urls:
    try:
        feed = feedparser.parse(url)
        # 피드에 제목이 없으면 URL 도메인을 출처로 사용
        source_name = feed.feed.title if hasattr(feed, 'feed') and hasattr(feed.feed, 'title') else url.split('/')[2]
        
        # 💡 수정됨: 각 언론사별 최신 뉴스를 5개에서 10개로 변경!
        for entry in feed.entries[:10]:
            news_data.append({
                "title": entry.title,
                "link": entry.link,
                "published": getattr(entry, 'published', ''),
                "source": source_name
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
