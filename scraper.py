import requests
from bs4 import BeautifulSoup
import pandas as pd


URL = "https://www.nehnutelnosti.sk/bratislava/byty/prenajom"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

response = requests.get(URL, headers=HEADERS)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'html.parser')

listings = soup.find_all('div', class_='MuiBox-root mui-0')

data = []

# Extract information from each card
for listing in listings:
    try:
        # Title
        title_tag = listing.find('h2')
        title = title_tag.get_text(strip=True) if title_tag else "N/A"

        # Price
        price_tag = listing.find('p', class_='MuiTypography-root MuiTypography-h5 mui-aoivfg')
        price = price_tag.get_text(strip=True) if price_tag else "N/A"

        # Location
        location_tag = listing.find('p', class_='MuiTypography-root MuiTypography-body3 MuiTypography-noWrap mui-e9ka76')
        location = location_tag.get_text(strip=True) if location_tag else "N/A"

        if title != "N/A" or price != "N/A" or location != "N/A":
            data.append({
                "Title": title,
                "Price": price,
                "Location": location
            })
            
            
    except Exception as e:
        print(f"Error processing card: {e}")

# Save to CSV
csv_filename = 'bratislava_rentals.csv'
df = pd.DataFrame(data)
df.to_csv(csv_filename, index=False, encoding='utf-8-sig')

print("Scraping completed. Data saved to 'bratislava_rentals.csv'")
print(f"Total number of ads collected: {len(df)}")

# Remove and replace non-breaking spaces (\xa0) from CSV
with open(csv_filename, 'r', encoding='utf-8-sig') as file:
    content = file.read()
cleaned_content = content.replace('\xa0', '')

with open(csv_filename, 'w', encoding='utf-8-sig') as file:
    file.write(cleaned_content)


