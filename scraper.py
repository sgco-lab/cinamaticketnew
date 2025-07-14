import requests
from datetime import datetime
import os

URL = "https://api.samfaa.ir/admin/report/recent_shows?recently=all&province_id=&screening_id=1404&from=&to="

try:
    response = requests.get(URL)
    data = response.json()
except Exception as e:
    print("Error fetching or decoding JSON:", e)
    exit(1)

movies = data.get("data", [])

html = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>فیلم‌های در حال اکران</title>
    <style>
        body {
            font-family: sans-serif;
            direction: rtl;
            background-color: #f5f5f5;
            margin: 0;
            padding: 30px;
        }
        h1 {
            text-align: center;
            color: #222;
        }
        .container {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 25px;
            max-width: 1400px;
            margin: auto;
        }
        .card {
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            overflow: hidden;
            transition: transform 0.2s;
        }
        .card:hover {
            transform: scale(1.02);
        }
        .poster {
            width: 100%;
            height: 350px;
            object-fit: cover;
        }
        .content {
            padding: 15px;
        }
        .title {
            font-size: 20px;
            color: #0d47a1;
            margin-bottom: 10px;
        }
        .info {
            font-size: 14px;
            margin-bottom: 5px;
        }
    </style>
</head>
<body>
    <h1>فیلم‌های در حال اکران</h1>
    <div class="container">
"""

for movie in movies:
    title = movie.get("fa_name", "بدون عنوان")
    director = movie.get("director", "نامشخص")
    ticket_count = movie.get("ticket_count", "۰")
    cinema_count = movie.get("cinema_count", "۰")
    showtime_count = movie.get("session_count", "۰")
    poster_url = movie.get("poster_url") or "https://via.placeholder.com/350x500?text=No+Image"

    html += f"""
        <div class="card">
            <img src="{poster_url}" alt="{title}" class="poster" />
            <div class="content">
                <div class="title">{title}</div>
                <div class="info">کارگردان: {director}</div>
                <div class="info">تعداد سالن: {cinema_count}</div>
                <div class="info">تعداد سانس: {showtime_count}</div>
                <div class="info">تعداد بلیت: {ticket_count}</div>
            </div>
        </div>
    """

html += """
    </div>
</body>
</html>
"""

# ساخت پوشه public در صورت عدم وجود
os.makedirs("public", exist_ok=True)

# ذخیره فایل در مسیر public/now_showing.html
with open("public/now_showing.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ فایل now_showing.html با موفقیت ساخته شد.")
