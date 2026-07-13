import requests
from bs4 import BeautifulSoup

URL = "https://forest.mponline.gov.in/Search.aspx?park=3"

EXPECTED_TO_DT = "9/30/2026 11:59:59 PM"

print("Downloading page...")

response = requests.get(URL, timeout=30)

print("Status:", response.status_code)

response.raise_for_status()

soup = BeautifulSoup(response.text, "lxml")

to_dt = soup.find(id="To_dt")

if not to_dt:
    raise Exception("Could not locate To_dt field.")

current = to_dt["value"]

print()
print("Expected :", EXPECTED_TO_DT)
print("Current  :", current)
print()

if current != EXPECTED_TO_DT:
    print("🚨 CHANGE DETECTED!")
else:
    print("No change.")
