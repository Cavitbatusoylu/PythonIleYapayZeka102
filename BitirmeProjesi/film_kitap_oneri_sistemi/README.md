# Film / Kitap Öneri Sistemi

Bu proje, Hamit MIZRAK tarafından hazırlanan bitirme projesi föyüne uygun olarak geliştirilmiştir. Kullanıcıların verdiği puanlara dayanarak onlara en uygun film veya kitapları önermeyi amaçlar.

## 📁 Proje Yapısı
```
film_kitap_oneri_sistemi/
|-- data/
|   |-- ratings.csv
|   |-- items.csv
|   |-- users.csv
|-- src/
|   |-- main.py
|   |-- data_loader.py
|   |-- recommender.py
|   |-- analysis.py
|-- outputs/
|   |-- recommendations.csv    # Öneri sonuçları (Örnek)
|   |-- charts/              # Analiz grafikleri (PNG)
|-- README.md
```

## 🛠️ Kullanılan Yöntemler
1.  **Kullanıcı Tabanlı Öneri (User-Based):** Hedef kullanıcıya benzer beğeni profili olan kullanıcıların yüksek puan verdiği ancak hedef kullanıcının henüz keşfetmediği içerikleri önerir.
2.  **İçerik Tabanlı Öneri (Item-Based):** Kullanıcının daha önce yüksek puan verdiği (4+) içeriklere benzerlik skoru en yüksek olan diğer içerikleri önerir.
3.  **Cosine Similarity:** İki vektör arasındaki yön benzerliğini ölçmek için kullanılmıştır. Projede kütüphane bağımlılığını azaltmak adına NumPy ile manuel olarak implement edilmiştir.

## 🚀 Çalıştırma Talimatları
Programı başlatmak için terminalde proje ana dizinindeyken şu komutu çalıştırın:
```bash
python src/main.py
```

## ✨ Gelişmiş Özellikler (Bonus)
- **Tür Filtreleme:** Sadece "Film" veya "Kitap" önerisi alabilme.
- **Grafik Üretimi:** Veri seti istatistiklerini `outputs/charts/` klasörüne kaydetme.
- **Kıyaslama Modu:** İki farklı algoritmanın sonuçlarını karşılaştırma.
- **Dışa Aktarım:** Sonuçları CSV olarak kaydetme.

## 📊 Örnek Çıktı Tablosu
| Sıra | Önerilen İçerik | Kategori | Skor |
| :--- | :--- | :--- | :--- |
| 1 | Interstellar | Bilim Kurgu | 0.91 |
| 2 | Inception | Bilim Kurgu | 0.88 |

## 👨‍💻 Hazırlayan
**Cavit**
**Antigravity (AI Assistant)**
