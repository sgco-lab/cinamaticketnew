import requests
import os

# مسیر ذخیره HTML
output_dir = "public"
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, "now_showing.html")

# آدرس API سمفا برای نمایش فیلم‌های در حال اکران
url = "https://samfaa.ir/api/recent_shows?recently=all&province_id=&screening_id=1404&from=&to="

# هدر ساده برای شبیه‌سازی مرورگر
headers = {
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0"
}

# دریافت داده‌ها
try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
except Exception as e:
    print("❌ خطا در دریافت اطلاعات از API:", e)
    data = []

# ساخت HTML
html = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>فیلم‌های در حال اکران</title>
    <style>
        body { font-family: sans-serif; background: #f4f4f4; padding: 20px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 20px; }
        .card { background: white; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); padding: 15px; }
        .title { font-weight: bold; font-size: 18px; margin-bottom: 5px; color: #222; }
        .info { font-size: 14px; color: #555; margin-bottom: 5px; }
    </style>
</head>
<body>
    <h2>🎬 فیلم‌های در حال اکران (بر اساس اطلاعات سامفا)</h2>
    <div class="grid">
"""

# اضافه کردن فیلم‌ها به HTML
if data:
    for item in data:
        movie_name = item.get("movie", {}).get("name", "بدون عنوان")
        director = item.get("movie", {}).get("director", "نامشخص")
        theaters = len(item.get("cinemas", []))
        ticket_count = item.get("ticket_count", 0)
        session_count = item.get("session_count", 0)

        html += f"""
        <div class="card">
            <div class="title">{movie_name}</div>
            <div class="info">🎬 کارگردان: {director}</div>
            <div class="info">🏢 تعداد سینماها: {theaters}</div>
            <div class="info">🎟️ تعداد بلیت فروخته‌شده: {ticket_count}</div>
            <div class="info">🕒 تعداد سانس: {session_count}</div>
        </div>
        """
else:
    html += "<p>هیچ اطلاعاتی یافت نشد.</p>"

# پایان HTML
html += """
    </div>
</body>
</html>
"""

# ذخیره فایل نهایی
with open(output_file, "w", encoding="utf-8") as f:
    f.write(html)

print("✅ فایل HTML با موفقیت ایجاد شد.")
