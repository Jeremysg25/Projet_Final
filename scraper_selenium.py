from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = Options()
options.binary_location = "/usr/bin/google-chrome"
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service("/home/jeremysegui2003/scraper/Projet_Final/chromedriver-linux64/chromedriver-linux64/chromedriver")
driver = webdriver.Chrome(service=service, options=options)


URL = "https://horloge-de-la-dette-publique.com/"
driver.get(URL)

wait = WebDriverWait(driver, 10) 

try:
    wait.until(EC.visibility_of_element_located((By.ID, "custom-counter-value-dette")))
    wait.until(EC.visibility_of_element_located((By.ID, "custom-counter-value-habitant")))
    wait.until(EC.visibility_of_element_located((By.ID, "custom-counter-value-dettesecu")))
    time.sleep(2)
except:
    print("")

page_source = driver.page_source
with open("source.html", "w", encoding="utf-8") as file:
    file.write(page_source)

with open("debug_headless.html", "w", encoding="utf-8") as f:
    f.write(driver.page_source)
