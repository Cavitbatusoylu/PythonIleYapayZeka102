import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

class Analysis:
    """
    Veri seti hakkında özet bilgiler ve analizler çıkaran sınıf.
    """
    def __init__(self, ratings, items, users, merged_data):
        self.ratings = ratings
        self.items = items
        self.users = users
        self.merged_data = merged_data
        # Proje kök dizinini bul (src'nin bir üstü)
        self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def run_full_analysis(self):
        """
        Tüm analizleri yapıp ekrana yazdırır.
        """
        user_count = self.ratings['user_id'].nunique()
        item_count = self.items['item_id'].nunique()
        avg_rating = self.ratings['rating'].mean()

        print("\n" + "="*40)
        print("        VERİ SETİ ANALİZ RAPORU")
        print("="*40)
        print(f"Toplam Kullanıcı Sayısı : {user_count}")
        print(f"Toplam İçerik Sayısı   : {item_count}")
        print(f"Genel Puan Ortalaması  : {avg_rating:.2f}")
        
        print("\n--- En Popüler Türler (Puanlamaya Göre) ---")
        pop_types = self.merged_data.groupby('category')['rating'].count().sort_values(ascending=False)
        print(pop_types)

        print("\n--- En Çok Puan Alan 3 İçerik ---")
        top_items = self.merged_data.groupby('title')['rating'].count().sort_values(ascending=False).head(3)
        print(top_items)
        print("="*40 + "\n")

    def export_summary(self, path='outputs/general_stats.csv'):
        """
        Özet bilgileri CSV olarak kaydeder.
        """
        summary = {
            'metric': ['user_count', 'item_count', 'avg_rating'],
            'value': [self.ratings['user_id'].nunique(), self.items['item_id'].nunique(), self.ratings['rating'].mean()]
        }
        pd.DataFrame(summary).to_csv(path, index=False)

    def create_visualizations(self, output_dir=None):
        """
        Veri seti için grafikler oluşturur ve kaydeder.
        """
        if output_dir is None:
            output_dir = os.path.join(self.project_root, 'outputs', 'charts')
            
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # 1. Puan Dağılımı Grafiği
        plt.figure(figsize=(10, 6))
        sns.countplot(x='rating', data=self.ratings, hue='rating', palette='viridis', legend=False)
        plt.title('Puan Dağılımı')
        plt.xlabel('Puan')
        plt.ylabel('Adet')
        plt.savefig(f"{output_dir}/puan_dagilimi.png")
        plt.close()

        # 3. Film vs Kitap Dağılımı (Pasta Grafiği)
        plt.figure(figsize=(8, 8))
        type_counts = self.items['type'].value_counts()
        plt.pie(type_counts, labels=type_counts.index, autopct='%1.1f%%', colors=['lightcoral', 'lightgreen'], startangle=140)
        plt.title('İçerik Türü Dağılımı (Film - Kitap)')
        plt.savefig(f"{output_dir}/film_vs_kitap.png")
        plt.close()

        # 4. Kullanıcı Aktivite Analizi
        plt.figure(figsize=(12, 6))
        user_activity = self.ratings['user_id'].value_counts().sort_index()
        user_activity.plot(kind='line', marker='o', color='purple', linestyle='-')
        plt.title('Kullanıcı Bazlı Puanlama Aktivitesi')
        plt.xlabel('Kullanıcı ID')
        plt.ylabel('Puanlama Sayısı')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.savefig(f"{output_dir}/kullanici_aktivite.png")
        plt.close()

        # 5. En Çok Puanlanan İlk 5 İçerik
        plt.figure(figsize=(10, 6))
        top_5 = self.merged_data.groupby('title')['rating'].count().sort_values(ascending=False).head(5)
        sns.barplot(x=top_5.values, y=top_5.index, hue=top_5.index, palette='magma', legend=False)
        plt.title('En Çok Puanlanan İlk 5 İçerik')
        plt.xlabel('Puanlama Sayısı')
        plt.ylabel('İçerik Başlığı')
        plt.tight_layout()
        plt.savefig(f"{output_dir}/en_populer_5.png")
        plt.close()

        print(f"Toplam 5 farklı grafik '{output_dir}' klasörüne başarıyla kaydedildi.")

    def show_demographic_stats(self):
        """
        Kullanıcı demografik bilgilerini analiz eder ve yazdırır.
        """
        print("\n" + "="*40)
        print("      DEMOGRAFİK ANALİZ RAPORU")
        print("="*40)
        
        print("\n--- Şehirlere Göre Kullanıcı Dağılımı ---")
        city_counts = self.users['city'].value_counts()
        print(city_counts)

        print("\n--- Yaş Ortalaması ---")
        print(f"Sistemdeki kullanıcıların yaş ortalaması: {self.users['age'].mean():.1f}")

        print("\n--- En Çok İlgi Duyulan Türler (Kullanıcı Tercihi) ---")
        genre_counts = self.users['favorite_genre'].value_counts()
        print(genre_counts)
        print("="*40 + "\n")
