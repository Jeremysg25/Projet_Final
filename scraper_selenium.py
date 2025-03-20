from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

CHROMEDRIVER_PATH = "C:/Users/jerem/OneDrive/Documents/ESILV/A4 bis/S8/PGL/Projet_Final/chromedriver-win64/chromedriver-win64/chromedriver.exe"
#CHROMEDRIVER_PATH = ""

options = webdriver.ChromeOptions()
options.add_argument("--headless") 
service = Service(CHROMEDRIVER_PATH)
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
    print("Les valeurs dynamiques ne se sont pas chargées correctement.")

page_source = driver.page_source
with open("source.html", "w", encoding="utf-8") as file:
    file.write(page_source)

print("Code source enregistré dans 'source.html'.")

driver.quit()