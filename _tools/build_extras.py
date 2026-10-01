"""1) credits.html по credits.json для сайтов с фото;
2) режим #shot для скриншотов: блоки с анимацией появления показываются сразу.
Запуск: python _tools/build_extras.py (повторный запуск ничего не ломает)."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITES = ["priceradar", "aidays", "coffee", "habitly", "photo"]
MARK = "<!--shot-mode-->"
SHOT = (MARK + "<style>html.shot .reveal{opacity:1!important;transform:none!important;transition:none!important}"
        "html.shot .hero.is-full{height:900px!important;min-height:0!important}</style>"
        "<script>if(location.hash==='#shot')document.documentElement.classList.add('shot')</script>\n")

for site in SITES:
    page = ROOT / site / "index.html"
    text = page.read_text(encoding="utf-8")
    if MARK not in text:
        text = text.replace("</head>", SHOT + "</head>", 1)
        page.write_text(text, encoding="utf-8")

    cf = ROOT / site / "img" / "credits.json"
    if not cf.exists():
        continue
    rows = "".join(
        f'<tr><td><img src="{c["file"]}" alt=""></td><td><a href="{html.escape(c["page"])}">'
        f'{html.escape(c["title"].removeprefix("File:"))}</a></td><td>{html.escape(c["author"])}</td>'
        f'<td>{html.escape(c["license"])}</td></tr>'
        for c in json.loads(cf.read_text(encoding="utf-8")))
    (ROOT / site / "credits.html").write_text(f"""<!doctype html><html lang="ru"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Фото: авторы и лицензии</title>
<style>body{{font-family:system-ui,sans-serif;margin:0;padding:32px 16px;background:#faf8f4;color:#222}}
main{{max-width:900px;margin:auto}}table{{width:100%;border-collapse:collapse;font-size:14px}}
td{{padding:8px;border-bottom:1px solid #ddd;vertical-align:middle}}img{{width:90px;height:60px;object-fit:cover;border-radius:6px}}
a{{color:#2e6bff}}</style></head><body><main><p><a href="./">← назад к сайту</a></p>
<h1>Фото: авторы и лицензии</h1><p>Все фотографии взяты с Wikimedia Commons под свободными лицензиями
(CC0, Public domain, CC BY, CC BY-SA). Изображения уменьшены, в остальном не изменялись.</p>
<table>{rows}</table></main></body></html>""", encoding="utf-8")
    print("credits:", site)
print("ok")
