import requests
import json

url = "https://samfaa.ir/api/recent_shows?recently=all&province_id=&screening_id=1404&from=&to="

headers = {
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0"
}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()

    # چاپ داده خام برای بررسی ساختار
    print("✅ اطلاعات دریافتی از API:")
    print(json.dumps(data[:2], indent=2, ensure_ascii=False))  # فقط ۲ مورد اول برای خوانایی

except Exception as e:
    print("❌ خطا در دریافت اطلاعات:", e)
