import requests
import json
import os

URL = "https://api.samfaa.ir/admin/report/recent_shows?recently=all&province_id=&screening_id=1404&from=&to="

response = requests.get(URL)
data = response.json()

# اطمینان از اینکه 'data' کلید 'data' دارد و آن هم لیست است
movies = data.get("data", []) if isinstance(data, dict) else []

html_output = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>فیلم‌های در حال اکران</title>
    <style>
        body { font-family: sans-serif; background: #f9f9f9; direction: rtl; }
        .movie { border: 1px solid #ccc; border-radius: 10px; padding: 10px; margin: 10px; background: white; max-width: 600px; }
        img { max-width: 100%; border-radius: 5px; }
        .title { font-size: 18px; font-weight: bold; color: #333; margin-top: 5px; }
        .desc { font-size: 14px; color: #666; }
    </style>
</head>
<body>
    <h2>فیلم‌های در حال اکران</h2>
"""

for movie in movies:
    if isinstance(movie, dict):
        title = movie.get("fa_name", "بدون عنوان")
        image_url = movie.get("poster_url", "")
        desc = movie.get("directors_fa", "")

        html_output += f"""
        <div class="movie">
            <img src="{image_url}" alt="{title}">
            <div class="title">{title}</div>
            <div class="desc">کارگردان: {desc}</div>
        </div>
        """

html_output += """
</body>
</html>
"""

# ذخیره خروجی
output_path = os.path.join("public", "now_showing.html")
os.makedirs("public", exist_ok=True)
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html_output)

print(f"✅ تعداد فیلم‌ها: {len(movies)}")
