import pandas as pd
import os

def check_data_quality():
    file_path = 'data/raw/stops_lviv.csv'
    
    if not os.path.exists(file_path):
        print(f"Помилка: Файл {file_path} не знайдено.")
        return

    print("ЗВІТ ПРО ЯКІСТЬ ДАНИХ")
    
    try:
        df = pd.read_csv(file_path)
        
        print(f"Всього рядків: {len(df)}")
        print(f"Всього колонок: {len(df.columns)}")
        
        print("\n--- Пропущені значення (NaN) ---")
        missing = df.isnull().sum()
        print(missing[missing > 0])
        
        duplicates = df.duplicated().sum()
        print(f"\n--- Дублікати ---")
        print(f"Кількість повних дублікатів: {duplicates}")
        
        print("\n--- Типи даних ---")
        print(df.dtypes)

    except Exception as e:
        print(f"Помилка при аналізі: {e}")

if __name__ == "__main__":
    check_data_quality()