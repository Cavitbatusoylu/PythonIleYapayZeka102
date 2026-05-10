import pandas as pd
import os

class DataManager:
    """
    Veri seti üzerinde ekleme ve silme işlemlerini yöneten sınıf.
    """
    def __init__(self, loader):
        self.loader = loader

    def add_new_item(self, title, category, itype, year):
        """Yeni bir film veya kitap ekler."""
        new_id = self.loader.items['item_id'].max() + 1
        new_row = {
            'item_id': new_id,
            'title': title,
            'category': category,
            'type': itype,
            'year': year
        }
        self.loader.items = pd.concat([self.loader.items, pd.DataFrame([new_row])], ignore_index=True)
        self.loader.items.to_csv(self.loader.items_file, index=False)
        return new_id

    def delete_item(self, item_id):
        """Bir içeriği ve ona bağlı tüm puanları siler."""
        if item_id not in self.loader.items['item_id'].values:
            return False
        
        # İçeriği sil
        self.loader.items = self.loader.items[self.loader.items['item_id'] != item_id]
        self.loader.items.to_csv(self.loader.items_file, index=False)
        
        # Bağlı puanları da sil (Veri tutarlılığı için)
        self.loader.ratings = self.loader.ratings[self.loader.ratings['item_id'] != item_id]
        self.loader.ratings.to_csv(self.loader.ratings_file, index=False)
        return True

    def add_rating(self, user_id, item_id, rating):
        """Bir kullanıcı için puan ekler."""
        if item_id not in self.loader.items['item_id'].values:
            return False, "İçerik ID bulunamadı."
        
        new_row = {
            'user_id': user_id,
            'item_id': item_id,
            'rating': rating,
            'timestamp': pd.Timestamp.now().strftime('%Y-%m-%d')
        }
        
        # Eğer kullanıcı zaten bu içeriğe puan verdiyse güncelle, yoksa ekle
        mask = (self.loader.ratings['user_id'] == user_id) & (self.loader.ratings['item_id'] == item_id)
        if not self.loader.ratings[mask].empty:
            self.loader.ratings.loc[mask, 'rating'] = rating
            msg = "Mevcut puan güncellendi."
        else:
            self.loader.ratings = pd.concat([self.loader.ratings, pd.DataFrame([new_row])], ignore_index=True)
            msg = "Yeni puan başarıyla eklendi."
            
        self.loader.ratings.to_csv(self.loader.ratings_file, index=False)
        return True, msg
