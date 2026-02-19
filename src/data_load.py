import pandas as pd
import os

def load_local_data():
    input_file = "stops.csv"
    
    if not os.path.exists(input_file):
        print(f"Помилка: Файл {input_file} не знайдено.")
        return

    df = pd.read_csv(input_file, sep=';')
    
    output_dir = 'data/raw'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'stops_lviv.csv')
    
    df.to_csv(output_path, index=False)
    print(f"Дані переміщено та збережено у {output_path}")

if __name__ == "__main__":
    load_local_data()