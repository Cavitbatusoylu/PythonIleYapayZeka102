
# 🎬📚 Film & Kitap Tavsiye Sistemi (Recommendation Engine)

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg?logo=python&logoColor=white)](https://www.python.org)
[![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-150458.svg?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Machine Learning](https://img.shields.io/badge/Machine_Learning-Recommendation_Systems-FF6F00.svg)](https://en.wikipedia.org/wiki/Recommender_system)

Modern, konsol tabanlı ve interaktif bir **Film ve Kitap Tavsiye Sistemi**! Bu proje, kullanıcıların ilgi alanlarına ve geçmiş puanlamalarına göre en uygun içerikleri sunmayı amaçlayan hibrit (User-Based & Item-Based) bir öneri motorudur. Veri bilimi ve algoritmik yaklaşımların gerçek dünya senaryolarına nasıl uygulanabileceğini göstermek amacıyla geliştirilmiştir.

## 🚀 Proje Hakkında (Motivasyon)

Günümüzde dijital içeriklerin artmasıyla beraber kullanıcıların doğru içeriğe ulaşması zorlaşmıştır. Bu proje, temel bir **Tavsiye Sistemi (Recommender System)** mantığının nasıl kurgulanacağını, veri manipülasyonunun ve temel makine öğrenimi mantığının (Cosine Similarity) kütüphanelere bağımlı kalmadan nasıl sıfırdan inşa edilebileceğini göstermektedir.

**Öne Çıkan Özellikler:**
- **Kullanıcı Tabanlı (User-Based) Öneriler:** Benzer zevklere sahip kullanıcıların davranışlarını analiz ederek yeni içerikler keşfetmenizi sağlar.
- **İçerik Tabanlı (Item-Based) Öneriler:** Beğendiğiniz bir içeriğe en çok benzeyen diğer içerikleri bulur.
- **Dinamik Veri Yönetimi:** Yeni film/kitap ekleyebilir, puanlamaları güncelleyebilir ve silebilirsiniz.
- **Görsel Analiz Raporları:** Veri seti üzerinden yaş dağılımları, popüler kategoriler gibi istatistikleri görselleştirir.
- **Kıyaslama Modu:** Farklı algoritmaların (User-Based vs Item-Based) ürettiği sonuçları yan yana karşılaştırma imkanı sunar.

## ⚙️ Kullanılan Teknolojiler ve Yöntemler

- **Dil:** Python
- **Veri Manipülasyonu:** Pandas (Verilerin birleştirilmesi, filtrelenmesi, analizi)
- **Matematiksel Modeller:** Cosine Similarity (Kosinüs Benzerliği) - Projede NumPy ve temel Python yetenekleriyle kurgulanmıştır.
- **Veri Görselleştirme:** Matplotlib / Seaborn (Kullanıcı demografisi ve içerik analizleri için)

## 📂 Proje Mimarisi

```text
film_kitap_oneri_sistemi/
├── assets/                  # Proje görselleri ve banner
├── data/                    # Veri setleri (ratings.csv, items.csv, users.csv)
├── outputs/                 
│   ├── charts/              # Analiz çıktıları (.png grafikleri)
│   └── recommendations.csv  # Çıktı olarak alınan öneri listeleri
├── src/                     # Kaynak Kodlar
│   ├── main.py              # Uygulama ana giriş noktası
│   ├── recommender.py       # Öneri algoritmaları motoru
│   ├── data_loader.py       # Veri yükleme işlemleri
│   ├── data_manager.py      # Veri yönetimi (Ekle/Sil)
│   └── analysis.py          # Veri analizi ve görselleştirme
└── README.md
```

## 💻 Kurulum ve Kullanım

Projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyebilirsiniz:

1. Depoyu klonlayın:
   ```bash
   git clone https://github.com/Cavitbatusoylu/PythonIleYapayZeka102.git
   ```
2. Proje dizinine gidin:
   ```bash
   cd PythonIleYapayZeka102/BitirmeProjesi/film_kitap_oneri_sistemi
   ```
3. Gerekli kütüphaneleri yükleyin:
   ```bash
   pip install pandas numpy matplotlib seaborn
   ```
4. Ana uygulamayı başlatın:
   ```bash
   python src/main.py
   ```

## 📈 Örnek Çıktılar

| Sıra | Önerilen İçerik | Kategori | Skor | Algoritma |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Interstellar | Bilim Kurgu | 0.91 | User-Based |
| 2 | Inception | Bilim Kurgu | 0.88 | User-Based |
| 3 | 1984 | Distopya | 0.85 | Item-Based |

---
*Geliştirici:* **Cavit**  
*Projeye katkı sağlamak veya geri bildirimde bulunmak için GitHub üzerinden issue açabilir veya Pull Request gönderebilirsiniz.*
