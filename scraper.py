import requests
import json
import os
from datetime import datetime

OUTPUT_HTML = "public/now_showing.html"
OUTPUT_JSON = "output.json"
URL = "https://iranopen.sbs/api/v1/recent_shows?recently=all&province_id=&screening_id=1404&from=&to="

response = requests.get(URL)
data = response.json()

# ذخیره JSON برای دیباگ
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✅ اطلاعات دریافتی از API:")
print(json.dumps(data, indent=2, ensure_ascii=False))

# تولید HTML
os.makedirs("public", exist_ok=True)
with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write("""
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>فیلم‌های در حال اکران</title>
    <style>
        body { font-family: sans-serif; background: #f2f2f2; text-align: center; }
        h1 { color: #222; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 20px; padding: 20px; }
        .card { background: white; border-radius: 10px; padding: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); direction: rtl; }
        .card img { width: 100%; height: 200px; object-fit: cover; border-radius: 8px; }
    </style>
</head>
<body>
    <h1>فیلم‌های در حال اکران</h1>
    <div class="grid">
""")

    for item in data.get("data", []):
        title = item.get("title", "بدون عنوان")
        director = item.get("director", "")
        poster = item.get("poster_url") or ""
        tickets = item.get("ticket_count") or "؟"
        halls = item.get("hall_count") or "؟"
        screenings = item.get("screening_count") or "؟"

        f.write(f"""
        <div class="card">
            <img src="{poster}" alt="{title}">
            <h3>{title}</h3>
            <p>کارگردان: {director}</p>
            <p>تعداد سانس: {screenings}</p>
            <p>تعداد سالن: {halls}</p>
            <p>تعداد بلیت: {tickets}</p>
        </div>
        """)

    f.write("""
    </div>
</body>
</html>
""")

print("✅ فایل HTML با موفقیت ساخته شد.")
