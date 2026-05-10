import pandas as pd
import numpy as np

def calculate_cosine_similarity(matrix):
    """
    Cosine similarity formülü: (A . B) / (||A|| * ||B||)
    """
    dot_product = np.dot(matrix, matrix.T)
    norms = np.linalg.norm(matrix, axis=1)
    norms_matrix = np.outer(norms, norms) + 1e-9 # 0'a bölmeyi engellemek için
    return dot_product / norms_matrix

class Recommender:
    """
    Kullanıcı ve İçerik tabanlı öneri motoru.
    """
    def __init__(self, ratings, items, users):
        self.ratings = ratings
        self.items = items
        self.users = users
        self.pivot_table = None
        self.user_similarity = None
        self.item_similarity = None
        self._prepare_matrix()

    def _prepare_matrix(self):
        """
        Pivot tablo oluşturma ve eksik verileri yönetme (Aşama 3).
        """
        self.pivot_table = self.ratings.pivot_table(index='user_id', columns='item_id', values='rating')
        # Eksik değerleri 0 ile dolduruyoruz (Aşama 10: Eksik değer yönetimi)
        self.matrix_filled = self.pivot_table.fillna(0)

    def compute_user_similarity(self):
        """
        Kullanıcı benzerlik matrisi üret (Aşama 4).
        """
        sim_matrix = calculate_cosine_similarity(self.matrix_filled.values)
        self.user_similarity = pd.DataFrame(sim_matrix, index=self.pivot_table.index, columns=self.pivot_table.index)
        return self.user_similarity

    def get_user_recommendations(self, user_id, top_n=5, filter_type=None, filter_category=None):
        """
        Kullanıcı Tabanlı Öneri (Bölüm 6.1) + Filtreleme Özelliği.
        """
        if self.user_similarity is None:
            self.compute_user_similarity()

        if user_id not in self.user_similarity.index:
            return pd.DataFrame()

        # Hedef kullanıcıya en benzer olanlar
        similar_users = self.user_similarity[user_id].sort_values(ascending=False).iloc[1:]
        
        # Kullanıcının henüz puanlamadığı içerikleri bul
        user_ratings = self.pivot_table.loc[user_id]
        unrated_items = user_ratings[user_ratings.isna()].index

        recommendations = []
        for item_id in unrated_items:
            # Filtreleme Kontrolü
            item_info = self.items[self.items['item_id'] == item_id].iloc[0]
            if filter_type and item_info['type'] != filter_type:
                continue
            if filter_category and item_info['category'] != filter_category:
                continue

            # Benzer kullanıcıların bu içeriğe verdiği puanlar
            item_puanlar = self.pivot_table[item_id]
            weighted_sum = 0
            sim_sum = 0
            
            for other_user, similarity in similar_users.items():
                if not np.isnan(item_puanlar[other_user]):
                    weighted_sum += similarity * item_puanlar[other_user]
                    sim_sum += similarity
            
            score = weighted_sum / sim_sum if sim_sum > 0 else 0
            recommendations.append((item_id, score))

        # En iyi N öneriyi seç (Aşama 7)
        top_items = sorted(recommendations, key=lambda x: x[1], reverse=True)[:top_n]
        return self._build_result_df(top_items)

    def get_item_recommendations(self, user_id, top_n=5, filter_type=None, filter_category=None):
        """
        İçerik Tabanlı Öneri (Bölüm 6.2) + Filtreleme Özelliği.
        """
        # İçerik benzerliği için matrisi ters çevir
        item_matrix = self.matrix_filled.T.values
        sim_matrix = calculate_cosine_similarity(item_matrix)
        item_sim_df = pd.DataFrame(sim_matrix, index=self.pivot_table.columns, columns=self.pivot_table.columns)

        # Kullanıcının yüksek puan verdiği içerikler
        user_ratings = self.pivot_table.loc[user_id].dropna()
        liked_items = user_ratings[user_ratings >= 4].index

        scores = {}
        for liked_id in liked_items:
            sim_scores = item_sim_df[liked_id]
            for other_id, sim in sim_scores.items():
                if other_id in user_ratings.index:
                    continue # Zaten puanlanmış
                
                # Filtreleme Kontrolü
                item_info = self.items[self.items['item_id'] == other_id].iloc[0]
                if filter_type and item_info['type'] != filter_type:
                    continue
                if filter_category and item_info['category'] != filter_category:
                    continue

                if other_id not in scores:
                    scores[other_id] = sim
                else:
                    scores[other_id] = max(scores[other_id], sim)

        top_items = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
        return self._build_result_df(top_items)

    def get_genre_based_recommendations(self, user_id, top_n=5):
        """
        Kullanıcının profilindeki 'favori tür' bilgisine göre öneri yapar.
        Özellikle yeni kullanıcılar veya soğuk başlangıç (cold-start) için idealdir.
        """
        user_info = self.users[self.users['user_id'] == user_id].iloc[0]
        fav_genre = user_info['favorite_genre']
        
        # Kullanıcının zaten puanladığı içerikler
        user_rated = self.ratings[self.ratings['user_id'] == user_id]['item_id'].values
        
        # Favori türe sahip ve henüz puanlanmamış içerikleri bul
        matching_items = self.items[
            (self.items['category'] == fav_genre) & 
            (~self.items['item_id'].isin(user_rated))
        ]
        
        # Puan ortalamasına göre sırala (Eğer puan varsa)
        avg_ratings = self.ratings.groupby('item_id')['rating'].mean()
        matching_items = matching_items.merge(avg_ratings, on='item_id', how='left').fillna(0)
        matching_items = matching_items.sort_values(by='rating', ascending=False).head(top_n)
        
        # Formatla
        res = []
        for i, row in enumerate(matching_items.itertuples(), 1):
            res.append({
                'Sıra': i,
                'Önerilen İçerik': row.title,
                'Kategori': row.category,
                'Tür': row.type,
                'Skor': round(row.rating, 2)
            })
        return pd.DataFrame(res)

    def _build_result_df(self, items_with_scores):
        """
        Sonuçları başlık, kategori ve skor ile tabloya dönüştürür (Aşama 8).
        """
        res = []
        for i, (item_id, score) in enumerate(items_with_scores, 1):
            info = self.items[self.items['item_id'] == item_id].iloc[0]
            res.append({
                'Sıra': i,
                'Önerilen İçerik': info['title'],
                'Kategori': info['category'],
                'Tür': info['type'],
                'Skor': round(score, 2)
            })
        return pd.DataFrame(res)
