"""Скачивает фото со свободной лицензией с Wikimedia Commons в папки сайтов.

picsum.photos и Unsplash из России недоступны, поэтому картинки лежат в самом репозитории.
Берём только CC0 / Public domain / CC BY / CC BY-SA, авторов пишем в credits.json.
Запуск: python _tools/fetch_images.py
"""
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UA = {"User-Agent": "web-demos-portfolio/1.0 (github.com/Slomi/web-demos)"}
OK_LICENSE = re.compile(r"^(CC0|Public domain|PD|CC BY(-SA)? [234]\.0)", re.I)

# (папка, имя файла, поисковый запрос, ширина)
WANT = [
    ("coffee", "hero", "latte art cup cafe", 900),
    ("coffee", "g1", "empty cafe interior chairs", 900),
    ("coffee", "g2", "barista espresso machine", 1100),
    ("coffee", "g3", "croissant bakery", 700),
    ("coffee", "g4", "coffee beans roasted", 700),
    ("coffee", "g5", "cafe table window plants", 1100),
    ("photo", "hero", "mountain lake landscape sunrise", 1800),
    ("photo", "p1", "iceland waterfall", 900),
    ("photo", "p2", "portrait woman natural light", 900),
    ("photo", "p3", "wedding couple", 900),
    ("photo", "p4", "georgia mountains caucasus", 900),
    ("photo", "p5", "studio portrait man", 900),
    ("photo", "p6", "altai mountains river", 900),
    ("photo", "p7", "wedding bouquet bride", 900),
    ("photo", "p8", "portrait young man smiling outdoors", 900),
    ("photo", "p9", "karelia lake forest", 900),
    ("photo", "me", "vintage film camera leica", 900),
]


def get(url: str) -> bytes:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read()


def search(query: str, width: int) -> dict | None:
    params = {
        "action": "query", "format": "json", "generator": "search", "gsrsearch": f"{query} filetype:bitmap",
        "gsrnamespace": "6", "gsrlimit": "20", "prop": "imageinfo",
        "iiprop": "url|size|extmetadata|mime", "iiurlwidth": str(width),
    }
    data = json.loads(get("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)))
    pages = sorted(data.get("query", {}).get("pages", {}).values(), key=lambda p: p.get("index", 99))
    for p in pages:
        ii = (p.get("imageinfo") or [{}])[0]
        meta = ii.get("extmetadata", {})
        lic = meta.get("LicenseShortName", {}).get("value", "")
        if ii.get("mime") != "image/jpeg" or not OK_LICENSE.search(lic):
            continue
        if ii.get("width", 0) < width or ii.get("width", 0) < ii.get("height", 1) * 0.5:
            continue
        artist = re.sub(r"<[^>]+>", "", meta.get("Artist", {}).get("value", "")).strip()
        return {"thumb": ii["thumburl"], "page": ii["descriptionurl"], "license": lic,
                "author": artist[:80] or "неизвестен", "title": p["title"]}
    return None


def main() -> None:
    credits: dict[str, list] = {}
    for folder in {w[0] for w in WANT}:
        cf = ROOT / folder / "img" / "credits.json"
        if cf.exists():
            credits[folder] = json.loads(cf.read_text(encoding="utf-8"))
    for folder, name, query, width in WANT:
        out = ROOT / folder / "img" / f"{name}.jpg"
        out.parent.mkdir(parents=True, exist_ok=True)
        if out.exists():
            continue
        time.sleep(5)
        try:
            hit = search(query, width)
        except Exception as e:  # noqa: BLE001
            print("ошибка поиска", query, e)
            continue
        if not hit:
            print("не найдено", query)
            continue
        out.write_bytes(get(hit["thumb"]))
        credits.setdefault(folder, []).append({"file": f"img/{name}.jpg", **hit})
        print("✓", folder, name, hit["license"], hit["author"][:40])
        time.sleep(1)
    for folder, items in credits.items():
        (ROOT / folder / "img" / "credits.json").write_text(
            json.dumps(items, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
