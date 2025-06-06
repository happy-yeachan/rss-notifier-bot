import feedparser
import requests
import os

WEBHOOK_URL = os.environ['WEBHOOK_URL']

# 블로그 닉네임과 RSS 주소 목록
BLOGS = [
    ('예찬', 'https://yeachan.tistory.com/rss'),
    ('영재', 'https://velog.io/rss/@yjl8628'),  # 최신 RSS 주소로 업데이트
    ('준호', 'https://se-juno.tistory.com/rss'),
    ('진포', 'https://medium.com/feed/@Jinpyo-An')
]

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
        print(f"[{name}] RSS 피드가 비어있음.")
        continue

    latest = feed.entries[0]

    # Medium RSS는 link가 객체일 수 있음
    if isinstance(latest.link, dict):
        link = latest.link.get('href')
    else:
        link = latest.link

    if link != last_link:
        message = f"📢 **[{name}] 블로그 새 글이 올라왔어요!**\n**{latest.title}**\n{link}"
        try:
            requests.post(WEBHOOK_URL, json={"content": message})
            print(f"[{name}] Webhook 전송 완료.")
        except Exception as e:
            print(f"[{name}] Webhook 전송 실패: {e}")

        with open(cache_file, 'w') as f:
            f.write(link)
    else:
        print(f"[{name}] 새 글 없음.")
