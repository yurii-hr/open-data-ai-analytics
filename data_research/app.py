import pandas as pd
from sklearn.cluster import KMeans, DBSCAN
import sqlite3
import os

def analyze_transport_system():
    db_path = '/app/db_data/lab.db'
    report_dir = '/app/shared_reports'
    report_path = os.path.join(report_dir, 'research_report.txt')
    
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
        report_lines.append("ЗВІТ ПРО ДОСЛІДЖЕННЯ ТРАНСПОРТНОЇ СИСТЕМИ")
        report_lines.append(f"Всього об'єктів: {len(df)}")

        if 'lat' in df.columns and 'lon' in df.columns:
            coords = df[['lat', 'lon']].dropna()

            report_lines.append("\n=== K-MEANS (Зонування) ===")
            kmeans = KMeans(n_clusters=10, random_state=42, n_init=10)
            kmeans.fit(coords)
            
            report_lines.append("Центри кластерів:")
            for i, center in enumerate(kmeans.cluster_centers_):
                report_lines.append(f"  Район {i+1}: {center[0]:.4f}, {center[1]:.4f}")

            report_lines.append("\n=== DBSCAN (Транспортні вузли) ===")
            dbscan = DBSCAN(eps=0.005, min_samples=5)
            labels = dbscan.fit_predict(coords)
            
            n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
            n_noise = list(labels).count(-1)
            
            report_lines.append(f"Кількість транспортних вузлів: {n_clusters}")
            report_lines.append(f"Окремі зупинки (шум): {n_noise}")

        report_lines.append("\n=== ТОП-10 ВУЛИЦЬ ===")
        if 'addressThoroughfare' in df.columns:
            report_lines.append(df['addressThoroughfare'].value_counts().head(10).to_string())

        report_lines.append("\n=== Локалізація зупинок ===")
        if 'addressPostName' in df.columns:
            city_stats = df['addressPostName'].value_counts()
            report_lines.append(city_stats.head(10).to_string())
            
            lviv_count = city_stats.get('Львів', 0)
            total = city_stats.sum()
            report_lines.append(f"\nЧастка зупинок у самому місті: {(lviv_count/total)*100:.1f}%")

        full_report = "\n".join(report_lines)
        
        print(full_report)
      
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(full_report)
            
        print(f"\nЗвіт про дослідження збережено у {report_path}")

    except Exception as e:
        print(f"Помилка при аналізі: {e}")

if __name__ == "__main__":
    analyze_transport_system()