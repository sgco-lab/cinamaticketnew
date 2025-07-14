import requests
import os

try:
    # فراخوانی API سمفا
    url = "https://api.samfaa.ir/admin/report/recent_shows?recently=all&province_id=&screening_id=1404&from=&to="
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # بررسی خطاهای HTTP
    data = response.json()
    movies = data.get("data", [])

    html_content = """
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
        html_content += f"""
        <div class="card">
            <img src="{movie.get("poster")}" class="poster" alt="{movie.get("fa_name")}">
            <div class="content">
                <div class="title">{movie.get("fa_name")}</div>
                <div class="info">کارگردان: {movie.get("director", "ندارد")}</div>
                <div class="info">تعداد بلیت: {movie.get("ticket_count", "۰")}</div>
                <div class="info">تعداد سالن: {movie.get("cinema_count", "۰")}</div>
                <div class="info">تعداد سانس: {movie.get("screening_count", "۰")}</div>
            </div>
        </div>
        """

    html_content += """
    </div>
</body>
</html>
"""

    os.makedirs("public", exist_ok=True)

    with open("public/now_showing.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print("✅ فایل HTML با موفقیت ایجاد شد.")

except Exception as e:
    print("❌ خطا در اجرای scraper.py:", str(e))
