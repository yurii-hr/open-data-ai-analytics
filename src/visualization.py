import matplotlib
matplotlib.use('Agg') 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans, DBSCAN
import os

def visualize_all():
    file_path = 'data/raw/stops_lviv.csv'
    output_dir = 'reports/figures'
    os.makedirs(output_dir, exist_ok=True)
    
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (12, 8)

    if not os.path.exists(file_path):
        print("Файл даних не знайдено.")
        return

    df = pd.read_csv(file_path)
    coords = df[['lat', 'lon']].dropna()
    print(f"Дані завантажено. Всього точок: {len(coords)}")

    kmeans = KMeans(n_clusters=6, random_state=42, n_init=10)
    labels_kmeans = kmeans.fit_predict(coords)
    
    plt.figure()
    scatter = plt.scatter(coords['lon'], coords['lat'], c=labels_kmeans, cmap='viridis', s=10, alpha=0.6)
    centers = kmeans.cluster_centers_
    plt.scatter(centers[:, 1], centers[:, 0], c='red', s=150, marker='X', label='Центри')
    plt.title('K-Means')
    plt.xlabel('Довгота'); plt.ylabel('Широта')
    plt.legend()
    plt.savefig(f'{output_dir}/kmeans_map.png', dpi=300)
    plt.close()

    
    dbscan = DBSCAN(eps=0.005, min_samples=3)
    labels_db = dbscan.fit_predict(coords)
    
    plt.figure()
    unique_labels = set(labels_db)
    colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]
    df_plot = coords.copy()
    df_plot['cluster'] = labels_db
    
    noise = df_plot[df_plot['cluster'] == -1]
    hubs = df_plot[df_plot['cluster'] != -1]
    
    plt.scatter(noise['lon'], noise['lat'], c='lightgray', s=5, label='Окремі зупинки (Шум)')
    plt.scatter(hubs['lon'], hubs['lat'], c=hubs['cluster'], cmap='tab20', s=10, label='Транспортні Хаби')
    
    plt.title('DBSCAN')
    plt.legend()
    plt.savefig(f'{output_dir}/dbscan_map.png', dpi=300)
    plt.close()

  
    if 'addressThoroughfare' in df.columns:
        top_streets = df['addressThoroughfare'].value_counts().head(10)
        
        plt.figure(figsize=(12, 6))
        sns.barplot(x=top_streets.values, y=top_streets.index, palette='viridis')
        plt.title('Топ-10 вулиць за кількістю зупинок')
        plt.xlabel('Кількість зупинок')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/streets_bar.png', dpi=300)
        plt.close()

    
    if 'addressPostName' in df.columns:
        top_cities = df['addressPostName'].value_counts().head(10)
        
        plt.figure(figsize=(12, 6))
        sns.barplot(x=top_cities.values, y=top_cities.index, palette='magma')
        plt.title('Розподіл зупинок по населених пунктах')
        plt.xlabel('Кількість зупинок')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/cities_bar.png', dpi=300)
        plt.close()



if __name__ == "__main__":
    visualize_all()