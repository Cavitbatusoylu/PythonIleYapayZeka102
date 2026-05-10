import pandas as pd
import os

class DataLoader:
    """
    Veri dosyalarini (CSV) yükleyen ve birlestiren sinif.
    """
    def __init__(self, data_path=None):
        if data_path is None:
            # Script'in bulunduğu klasörden bir üst seviyeye çıkıp data klasörüne ulaş
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.data_path = os.path.join(base_dir, 'data')
        else:
            self.data_path = data_path
            
        self.ratings_file = os.path.join(self.data_path, 'ratings.csv')
        self.items_file = os.path.join(self.data_path, 'items.csv')
        self.users_file = os.path.join(self.data_path, 'users.csv')

    def load_and_merge(self):
        """
        Dosyalari okur, kontrol eder ve birlestirir.
        """
        if not all(os.path.exists(f) for f in [self.ratings_file, self.items_file, self.users_file]):
            raise FileNotFoundError(f"Hata: {self.data_path} klasöründe gerekli CSV dosyalari eksik.")

        self.ratings = pd.read_csv(self.ratings_file)
        self.items = pd.read_csv(self.items_file)
        self.users = pd.read_csv(self.users_file)

        # ratings ve items tablolarını birleştir
        self.merged_data = pd.merge(self.ratings, self.items, on='item_id')
        # Kullanıcı bilgilerini de ekle
        self.merged_data = pd.merge(self.merged_data, self.users, on='user_id')
        
        return self.ratings, self.items, self.users, self.merged_data

if __name__ == "__main__":
    # Test
    loader = DataLoader('../data')
    r, i, m = loader.load_and_merge()
    print("Veri yüklendi, ilk 5 satir:")
    print(m.head())
