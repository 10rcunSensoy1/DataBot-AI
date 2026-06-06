import pandas as pd
import os
import requests

# Proje dosya yapısı yönetimi
DATA_DIR = "data"

def get_holidays_info():
    """Excel tabanlı resmi/dini tatil takvimine erişim sağlar."""
    file_path = os.path.join(DATA_DIR, "holidays.xlsx")
    try:
        # Excel motoru üzerinden veri bütünlüğü korunarak okuma yapılır
        df = pd.read_excel(file_path)
        return df.to_string(index=False)
    except Exception as e:
        return f"Veri erişim hatası ({file_path}): {str(e)}"

def get_vehicle_info():
    """Araç teknik özelliklerini ve yakıt tüketim verilerini döndürür."""
    file_path = os.path.join(DATA_DIR, "vehicles.xlsx")
    try:
        df = pd.read_excel(file_path)
        return df.to_string(index=False)
    except Exception as e:
        return f"Veri seti yükleme hatası: {str(e)}"

def get_historical_weather_info():
    """Geçmiş yıllara ait istatistiksel hava verilerini analiz için sunar."""
    file_path = os.path.join(DATA_DIR, "weather.xlsx")
    try:
        df = pd.read_excel(file_path)
        return df.to_string(index=False)
    except Exception as e:
        return f"Hava durumu verisi okunurken hata oluştu: {str(e)}"

def get_current_weather_forecast(city="Istanbul"):
    """
    Dinamik veri ihtiyacı için Open-Meteo API entegrasyonu.
    Excel'de bulunmayan anlık ve gelecek zamanlı verileri sisteme dahil eder.
    """
    lat, lon = 41.0082, 28.9784 # Koordinat bazlı sorgulama
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min&timezone=auto"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        daily = data.get("daily", {})
        times = daily.get("time", [])
        max_temps = daily.get("temperature_2m_max", [])
        min_temps = daily.get("temperature_2m_min", [])
        
        result_text = f"{city} için 7 günlük hava tahmini:\n"
        for i in range(len(times)):
            result_text += f"- {times[i]}: Max {max_temps[i]}°C, Min {min_temps[i]}°C\n"
            
        return result_text
    except Exception as e:
        return f"Harici API bağlantı hatası: {str(e)}"

if __name__ == "__main__":
    # Unit test: Veri erişim katmanının doğrulanması
    print("--- ARAÇ VERİLERİ ---")
    print(get_vehicle_info())
    print("\n--- GÜNCEL HAVA DURUMU (API) ---")
    print(get_current_weather_forecast())