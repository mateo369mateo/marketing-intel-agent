import re
import html
import requests
import feedparser
from bs4 import BeautifulSoup
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

from sources import NEWS_SOURCES
from config import MAX_ARTICLES_PER_FEED

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept": "application/rss+xml, application/rdf+xml, application/atom+xml, application/xml;q=0.9, text/xml;q=0.8, */*;q=0.1"
}


def clean_html(text: str) -> str:
    """Strip HTML tags and unescape HTML entities to clean text."""
    if not text:
        return ""
    # Use BeautifulSoup to parse and extract text
    soup = BeautifulSoup(text, "html.parser")
    # Remove script and style tags
    for s in soup(["script", "style"]):
        s.extract()
    cleaned = soup.get_text(separator=" ")
    cleaned = html.unescape(cleaned)
    # Collapse multiple spaces and newlines
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def normalize_title(title: str) -> str:
    """Normalize title for deduplication."""
    clean = re.sub(r"[^\w\s]", "", title.lower())
    return " ".join(clean.split())


def fetch_single_feed(source: dict) -> list:
    """Fetch and parse a single RSS/Atom feed."""
    name = source["name"]
    url = source["url"]
    category = source["category"]
    articles = []

    try:
        session = requests.Session()
        session.headers.update(HEADERS)
        response = session.get(url, timeout=12)
        if response.status_code != 200:
            print(f"[Fetcher] ⚠️  {name}: HTTP status {response.status_code}")
            return []

        feed = feedparser.parse(response.content)
        entries = feed.entries[:MAX_ARTICLES_PER_FEED]

        for entry in entries:
            title = clean_html(entry.get("title", ""))
            if not title:
                continue

            link = entry.get("link", "")
            
            # Extract summary or description
            summary_raw = entry.get("summary", "") or entry.get("description", "")
            if not summary_raw and "content" in entry and entry["content"]:
                summary_raw = entry["content"][0].get("value", "")
            
            summary = clean_html(summary_raw)
            # If summary is too short or identical to title, try fallback
            if len(summary) < 20:
                summary = f"Latest report from {name} regarding {title}."
            elif len(summary) > 350:
                summary = summary[:347] + "..."

            # Published date
            pub_date = None
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                pub_date = datetime(*entry.published_parsed[:6])
            elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
                pub_date = datetime(*entry.updated_parsed[:6])
            else:
                pub_date = datetime.now()

            articles.append({
                "title": title,
                "url": link,
                "source": name,
                "category": category,
                "summary": summary,
                "published": pub_date.strftime("%b %d, %Y"),
                "timestamp": pub_date.timestamp(),
                "priority": source.get("priority", 2)
            })

        print(f"[Fetcher] ✅ {name}: Fetched {len(articles)} articles")

    except Exception as e:
        print(f"[Fetcher] ❌ {name}: Failed with error: {e}")

    return articles


def fetch_all_marketing_news() -> list:
    """Fetch all sources in parallel and return deduplicated articles."""
    all_articles = []
    print(f"\n[Fetcher] Scanning {len(NEWS_SOURCES)} top marketing, branding & advertising sources...")

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(fetch_single_feed, src): src for src in NEWS_SOURCES}
        for future in as_completed(futures):
            try:
                res = future.result()
                all_articles.extend(res)
            except Exception as e:
                src = futures[future]
                print(f"[Fetcher] Error processing {src['name']}: {e}")

    # Deduplicate based on title similarity
    unique_articles = []
    seen_titles = set()

    # Sort primarily by source priority and recency
    all_articles.sort(key=lambda a: (a.get("priority", 2), -a.get("timestamp", 0)))

    for art in all_articles:
        norm = normalize_title(art["title"])
        # Check if already seen or very close
        if norm not in seen_titles and len(norm) > 10:
            seen_titles.add(norm)
            unique_articles.append(art)

    print(f"[Fetcher] Total unique articles curated: {len(unique_articles)}")
    return unique_articles
