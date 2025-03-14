# 🌍 Satelitarna vs. Rzeczywista Pogoda  

## 📖 Opis projektu  

Projekt polega na analizie danych pogodowych pozyskiwanych z API satelitarnych oraz rzeczywistych czujników pogodowych w określonych lokalizacjach geograficznych. Celem jest ocena dokładności prognoz satelitarnych w porównaniu do rzeczywistych pomiarów oraz identyfikacja potencjalnych różnic.  

🔬 **Autorzy:**  
- Jakub Wilk  
- Ewa Głowienka, dr inż.  

## 🛰️ Skąd pochodzą dane?  

Dane pochodzą z **API satelitarnych**, które wykorzystują dane z kilku satelit meteorologicznych oraz **rzeczywistych czujników pogodowych**, zlokalizowanych w wybranych punktach geograficznych.  

Porównywane są następujące parametry:  
- 🌡️ **Temperatura** (`temperature_2m`)  
- 💧 **Wilgotność względna** (`relative_humidity_2m`)  
- 🌬️ **Prędkość wiatru** (`wind_speed_10m`)  

Cała analiza jest do przeczytania w pliku ipynb


Korelacja temperatur wynosi 88%, co według mnie jest satysfakcjonującym wynikiem, który pozwala stwierdzić, że korzystanie z satelit jest wystarczająco dokładne.







