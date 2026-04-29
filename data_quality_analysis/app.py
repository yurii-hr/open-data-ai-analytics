import pandas as pd
import sqlite3
import os

def check_data_quality():
    db_path = '/app/db_data/lab.db'
    report_dir = '/app/shared_reports'
    report_path = os.path.join(report_dir, 'quality_report.txt')
    
    os.makedirs(report_dir, exist_ok=True)

    if not os.path.exists(db_path):
        error_msg = f"Помилка: Базу даних {db_path} не знайдено."
        print(error_msg)
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(error_msg)
        return

    
    try:
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query("SELECT * FROM stops", conn)
        conn.close()
        
        report_lines = []
        report_lines.append("ЗВІТ ПРО ЯКІСТЬ ДАНИХ")
        report_lines.append(f"Всього рядків: {len(df)}")
        report_lines.append(f"Всього колонок: {len(df.columns)}")
        
        report_lines.append("\n--- Пропущені значення (NaN) ---")
        missing = df.isnull().sum()
        missing_filtered = missing[missing > 0]
        if not missing_filtered.empty:
            report_lines.append(missing_filtered.to_string())
        else:
            report_lines.append("Пропущених значень немає.")
        
        duplicates = df.duplicated().sum()
        report_lines.append(f"\n--- Дублікати ---")
        report_lines.append(f"Кількість повних дублікатів: {duplicates}")
        
        report_lines.append("\n--- Типи даних ---")
        report_lines.append(df.dtypes.to_string())

        full_report = "\n".join(report_lines)
        
        print(full_report)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(full_report)
            
        print(f"\nЗвіт успішно збережено у {report_path}")

    except Exception as e:
        print(f"Помилка при аналізі: {e}")

if __name__ == "__main__":
    check_data_quality()