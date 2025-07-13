import requests
from bs4 import BeautifulSoup
import os

# دریافت HTML از سامفا
url = "https://www.samfaa.ir/"
headers = {
    "User-Agent": "Mozilla/5.0"
}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

# استخراج فیلم‌ها
movies = soup.select("div.card")

# ساخت HTML خروجی
output_html = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>فیلم‌های در حال اکران</title>
    <style>
        body { font-family: sans-serif; background: #f5f5f5; padding: 20px; direction: rtl; }
        .movie { background: white; border-radius: 8px; padding: 10px; margin-bottom: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        img { max-width: 100%; border-radius: 8px; }
        .title { font-size: 18px; font-weight: bold; margin-top: 10px; }
        .desc { font-size: 14px; color: #444; margin-top: 5px; }
    </style>
</head>
<body>
    <h2>فیلم‌های در حال اکران</h2>
"""

for movie in movies:
    title = movie.select_one(".card-title").get_text(strip=True) if movie.select_one(".card-title") else "بدون عنوان"
    desc = movie.select_one(".card-text").get_text(strip=True) if movie.select_one(".card-text") else ""
    img_tag = movie.select_one("img")
    img = img_tag["src"] if img_tag and "src" in img_tag.attrs else ""

    output_html += f"""
    <div class="movie">
        <img src="{img}" alt="{title}">
        <div class="title">{title}</div>
        <div class="desc">{desc}</div>
    </div>
    """

output_html += """
</body>
</html>
"""

# ذخیره در فایل public
os.makedirs("public", exist_ok=True)
with open("public/now_showing.html", "w", encoding="utf-8") as f:
    f.write(output_html)

print(f"تعداد فیلم‌ها: {len(movies)}")
