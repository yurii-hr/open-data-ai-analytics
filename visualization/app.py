import matplotlib
matplotlib.use('Agg')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans, DBSCAN
import sqlite3
import os

def visualize_all():
    db_path = '/app/db_data/lab.db'
    output_dir = '/app/shared_reports'
    os.makedirs(output_dir, exist_ok=True)
    
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (12, 8)

    if not os.path.exists(db_path):
        print(f"Помилка: Базу даних {db_path} не знайдено.")
        return

    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM stops", conn)
    conn.close()

    coords = df[['lat', 'lon']].dropna()
    print(f"Дані успішно завантажено. Всього точок: {len(coords)}")

    print("Генеруємо графік K-Means...")
    kmeans = KMeans(n_clusters=6, random_state=42, n_init=10)
    labels_kmeans = kmeans.fit_predict(coords)
    
    plt.figure()
    plt.scatter(coords['lon'], coords['lat'], c=labels_kmeans, cmap='viridis', s=10, alpha=0.6)
    centers = kmeans.cluster_centers_
    plt.scatter(centers[:, 1], centers[:, 0], c='red', s=150, marker='X', label='Centers')
    plt.title('K-Means Clustering: Lviv Transit Stops')
    plt.xlabel('Longitude'); plt.ylabel('Latitude')
    plt.legend()
    plt.savefig(f'{output_dir}/kmeans_map.png', dpi=300)
    plt.close()

    print("Генеруємо графік DBSCAN...")
    dbscan = DBSCAN(eps=0.005, min_samples=3)
    labels_db = dbscan.fit_predict(coords)
    
    plt.figure()
    df_plot = coords.copy()
    df_plot['cluster'] = labels_db
    
    noise = df_plot[df_plot['cluster'] == -1]
    hubs = df_plot[df_plot['cluster'] != -1]
    
    plt.scatter(noise['lon'], noise['lat'], c='lightgray', s=5, label='Noise (Isolated Stops)')
    plt.scatter(hubs['lon'], hubs['lat'], c=hubs['cluster'], cmap='tab20', s=10, label='Transport Hubs')
    
    plt.title('DBSCAN Clustering: Identification of Hubs')
    plt.xlabel('Longitude'); plt.ylabel('Latitude')
    plt.legend()
    plt.savefig(f'{output_dir}/dbscan_map.png', dpi=300)
    plt.close()

    print("Генеруємо графік вулиць...")
    if 'addressThoroughfare' in df.columns:
        top_streets = df['addressThoroughfare'].value_counts().head(10)
        plt.figure(figsize=(12, 6))
        sns.barplot(x=top_streets.values, y=top_streets.index, palette='viridis')
        plt.title('Top 10 Streets by Number of Stops')
        plt.xlabel('Stops Count')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/streets_bar.png', dpi=300)
        plt.close()

    print("Генеруємо графік населених пунктів...")
    if 'addressPostName' in df.columns:
        top_cities = df['addressPostName'].value_counts().head(10)
        plt.figure(figsize=(12, 6))
        sns.barplot(x=top_cities.values, y=top_cities.index, palette='magma')
        plt.title('Stops Distribution by Settlement')
        plt.xlabel('Stops Count')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/cities_bar.png', dpi=300)
        plt.close()

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Аналіз транспортної системи Львова</title>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background: #f4f4f4; }}
            .container {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            h1 {{ color: #333; }}
            .chart {{ margin-bottom: 40px; text-align: center; }}
            img {{ max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 4px; }}
            .report-text {{ background: #eee; padding: 15px; border-radius: 5px; white-space: pre-wrap; text-align: left; font-family: monospace; }}
        </style>
    </head>
    <body>
        <div class="container">
 
            <div class="chart">
                <h3>K-Means Clustering</h3>
                <img src="kmeans_map.png" alt="K-Means">
            </div>
            
            <div class="chart">
                <h3>DBSCAN Hub Identification</h3>
                <img src="dbscan_map.png" alt="DBSCAN">
            </div>
            
            <div class="chart">
                <h3>Top Streets</h3>
                <img src="streets_bar.png" alt="Streets">
            </div>

            <div class="chart">
                <h3>Settlement Distribution</h3>
                <img src="cities_bar.png" alt="Settlements">
            </div>
        </div>
    </body>
    </html>
    """
    
    with open(f'{output_dir}/index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Візуалізацію завершено. Артефакти збережено у {output_dir}")

if __name__ == "__main__":
    visualize_all()