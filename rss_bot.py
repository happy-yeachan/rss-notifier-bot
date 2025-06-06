import feedparser
import requests
import os

WEBHOOK_URL = os.environ['WEBHOOK_URL']

# 블로그 닉네임과 RSS 주소 목록
BLOGS = [
    ('예찬', 'https://yeachan.tistory.com/rss'),
    ('영재', 'https://v2.velog.io/rss/yjl8628'),
    ('준호', 'https://se-juno.tistory.com/rss'),
]

# 캐시 디렉토리 (최근 글 기록용)
CACHE_DIR = 'cache'
os.makedirs(CACHE_DIR, exist_ok=True)

for name, url in BLOGS:
    cache_file = os.path.join(CACHE_DIR, f'{name}.txt')

    try:
        with open(cache_file, 'r') as f:
            last_link = f.read().strip()
    except FileNotFoundError:
        last_link = ''

    feed = feedparser.parse(url)
    if not feed.entries:
        continue  # 피드가 비어있을 경우 skip

    latest = feed.entries[0]

    if latest.link != last_link:
        message = f"📢 **[{name}] 블로그 새 글이 올라왔어요!**\n**{latest.title}**\n{latest.link}"
        requests.post(WEBHOOK_URL, json={"content": message})

        with open(cache_file, 'w') as f:
            f.write(latest.link)
