from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Ustawienia przeglądarki
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)

# Zakres dat: 4 do 20 lipca 2024
dates = pd.date_range("2024-07-04", "2024-07-20").strftime("%Y-%m-%d").tolist()
weather_data = []

for date in dates:
    url = f"https://www.wunderground.com/history/daily/EPKK/date/{date}"
    driver.get(url)

    # Czekaj na załadowanie tabeli
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.mat-table")))

    # Pobierz nagłówki tabeli
    header_row = driver.find_element(By.CSS_SELECTOR, "table.mat-table tr")
    headers = [col.text for col in header_row.find_elements(By.TAG_NAME, "th")]

    # Pobierz indeksy potrzebnych kolumn
    time_idx = headers.index("Time")
    temp_idx = headers.index("Temperature")
    humidity_idx = headers.index("Humidity")
    wind_speed_idx = headers.index("Wind Speed")

    # Pobierz wszystkie wiersze (pomijamy pierwszy - nagłówek)
    rows = driver.find_elements(By.CSS_SELECTOR, "table.mat-table tr")[1:]

    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) > 1:
            time_str = cols[time_idx].text.strip()  # np. "12:00 AM"
            temperature_str = cols[temp_idx].text.strip()  # np. "59 °F"
            humidity_str = cols[humidity_idx].text.strip()  # np. "82 %"
            wind_speed_str = cols[wind_speed_idx].text.strip()  # np. "4 mph"

            # Filtruj tylko pełne godziny (sprawdzamy czy minuty to "00")
            if ":" in time_str:
                minutes = time_str.split(":")[1].split()[0]
                if minutes == "00":
                    # Łączenie daty i czasu, konwersja do datetime z formatem 12-godzinnym
                    timestamp = pd.to_datetime(f"{date} {time_str}", format='%Y-%m-%d %I:%M %p')
                    # Ustawienie strefy czasowej na UTC
                    timestamp = timestamp.tz_localize('UTC')

                    # Konwersja temperatury z °F na °C (dokładność do 6 miejsc)
                    temperature = (float(temperature_str.replace('°F', '').strip()) - 32) * 5.0 / 9.0
                    temperature = round(temperature, 6)

                    # Konwersja wilgotności (usuwamy znak %)
                    humidity = float(humidity_str.replace('%', '').strip())

                    # Konwersja prędkości wiatru z mph na m/s (zaokrąglenie do 1 miejsca)
                    wind_speed = float(wind_speed_str.replace('mph', '').strip()) * 0.44704
                    wind_speed = round(wind_speed, 1)

                    weather_data.append([
                        timestamp,
                        temperature,
                        humidity,
                        wind_speed
                    ])

driver.quit()

# Tworzenie DataFrame z nowymi nazwami kolumn
df = pd.DataFrame(weather_data, columns=["date", "temperature_2m", "relative_humidity_2m", "wind_speed_10m"])
print(df)

df.to_csv("pobieranie_wunder.csv", index=False)
