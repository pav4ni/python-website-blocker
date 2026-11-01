"""Web scraping: fetch a page and pull out the text used for pattern matching."""
import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0 (website-blocker learning project)"}


def scrape(url: str, timeout: int = 8) -> str:
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    resp = requests.get(url, headers=HEADERS, timeout=timeout)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    parts = [soup.title.get_text(" ", strip=True) if soup.title else ""]
    for meta in soup.find_all("meta", attrs={"name": ["description", "keywords"]}):
        parts.append(meta.get("content", ""))
    for h in soup.find_all(["h1", "h2", "h3"]):
        parts.append(h.get_text(" ", strip=True))
    parts.append(soup.get_text(" ", strip=True)[:5000])
    return " ".join(parts).lower()
