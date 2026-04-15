import pandas as pd
import sqlite3
import os

def load_data_to_db():
    input_file = "/app/data/stops.csv"
    db_path = "/app/db_data/lab.db"

    if not os.path.exists(input_file):
        print(f"Помилка: Файл {input_file} не знайдено.")
        return

    df = pd.read_csv(input_file, sep=';')
    print(f"Успішно зчитано {len(df)} рядків.")

    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    conn = sqlite3.connect(db_path)
    
    df.to_sql('stops', conn, if_exists='replace', index=False)
    
    print(f"Дані успішно завантажено в базу даних {db_path}, таблиця 'stops'.")
   
    conn.close()

if __name__ == "__main__":
    load_data_to_db()