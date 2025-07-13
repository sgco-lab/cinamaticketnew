import requests
import json
from datetime import datetime

URL = "https://www.samfaa.ir/api/v1/show/recent_shows?recently=all&province=0"

def fetch_and_generate():
    response = requests.get(URL)
    data = response.json()

    movies = data.get("data", [])
    print(f"📽️ تعداد فیلم‌ها: {len(movies)}")

    html = "<!DOCTYPE html><html lang='fa' dir='rtl'><head><meta charset='utf-8'><title>فیلم‌های در حال اکران</title></head><body>"
    html += f"<h2>فیلم‌های فعال ({len(movies)} مورد)</h2><ul>"

    for movie in movies:
        name = movie.get("movie", {}).get("title", "بدون نام")
        poster = movie.get("movie", {}).get("poster_url", "")
        description = movie.get("movie", {}).get("summary", "")
        html += f"<li><h3>{name}</h3><img src='{poster}' width='200'/><p>{description}</p></li>"

    html += "</ul></body></html>"

    with open("now_showing.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    fetch_and_generate()
