from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

CHROMEDRIVER_PATH = "C:/Users/jerem/OneDrive/Documents/ESILV/A4 bis/S8/PGL/Projet_Final/chromedriver-win64/chromedriver-win64/chromedriver.exe"

options = webdriver.ChromeOptions()
options.add_argument("--headless")
service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

URL = "https://horloge-de-la-dette-publique.com/"
driver.get(URL)

wait = WebDriverWait(driver, 10)

try:
    dette_publique = wait.until(EC.visibility_of_element_located((By.ID, "custom-counter-value-dette"))).text
except:
    dette_publique = "Non trouvé"

try:
    dette_pib = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[contains(@id,'tooltip-text') and contains(text(), 'Dette publique/PIB')]/following-sibling::p"))).text
except:
    dette_pib = "Non trouvé"

try:
    deficit_2024 = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[contains(@id,'tooltip-text') and contains(text(), 'Déficit budgétaire 2024')]/following-sibling::p"))).text
except:
    deficit_2024 = "Non trouvé"

try:
    dette_habitant = wait.until(EC.visibility_of_element_located((By.ID, "custom-counter-value-habitant"))).text
except:
    dette_habitant = "Non trouvé"

try:
    deficit_secu = wait.until(EC.visibility_of_element_located((By.ID, "custom-counter-value-dettesecu"))).text
except:
    deficit_secu = "Non trouvé"

with open("data.txt", "w", encoding="utf-8") as file:
    file.write(f"Dette publique: {dette_publique} €\n")
    file.write(f"Dette/PIB: {dette_pib} %\n")
    file.write(f"Déficit budgétaire 2024: {deficit_2024} %\n")
    file.write(f"Dette par habitant: {dette_habitant} €\n")
    file.write(f"Déficit Sécurité sociale: {deficit_secu} €\n")

print("Données économiques mises à jour et enregistrées dans 'data.txt'")

driver.quit()
