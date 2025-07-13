from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def fetch_and_generate():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # ساخت سرویس
    service = Service(ChromeDriverManager().install())
    
    # ساخت مرورگر با سرویس و آپشن
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # ادامه کد...
