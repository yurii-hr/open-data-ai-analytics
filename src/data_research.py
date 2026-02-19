import pandas as pd
from sklearn.cluster import KMeans, DBSCAN
import os

def analyze_transport_system():
    file_path = 'data/raw/stops_lviv.csv'
    
    if not os.path.exists(file_path):
        print("Помилка: Файл даних не знайдено.")
        return

    df = pd.read_csv(file_path)
    print(f"Всього об'єктів: {len(df)}")

    coords = df[['lat', 'lon']].dropna()

    print("\n K-MEANS")
    kmeans = KMeans(n_clusters=10, random_state=42, n_init=10)
    kmeans.fit(coords)
    
    print("Центри кластерів:")
    for i, center in enumerate(kmeans.cluster_centers_):
        print(f"  Район {i+1}: {center[0]:.4f}, {center[1]:.4f}")

    print("\n DBSCAN")

    dbscan = DBSCAN(eps=0.005, min_samples=5)
    labels = dbscan.fit_predict(coords)
    
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise = list(labels).count(-1)
    
    print(f"Кількість транспортних вузлів: {n_clusters}")
    print(f"Окремі зупинки (шум): {n_noise}")

    print("\n  ТОП-10 ВУЛИЦЬ")
    if 'addressThoroughfare' in df.columns:
        print(df['addressThoroughfare'].value_counts().head(10))

    print("\n Львів та прилеглі населені пункти")
    if 'addressPostName' in df.columns:
        city_stats = df['addressPostName'].value_counts()
        print(city_stats.head(10))
        
        lviv_count = city_stats.get('Львів', 0)
        total = city_stats.sum()
        print(f"\nЧастка зупинок у самому Львові: {(lviv_count/total)*100:.1f}%")

if __name__ == "__main__":
    analyze_transport_system()