import os
import pandas as pd
from data_loader import DataLoader
from analysis import Analysis
from recommender import Recommender
from data_manager import DataManager

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    print("\n" + "="*50)
    print(f"{title:^50}")
    print("="*50)

def main():
    # Klasör kontrolü (Dinamik yol ayarı)
    src_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(src_dir)
    os.chdir(project_root) # Çalışma dizinini proje köküne çek

    if not os.path.exists('outputs/charts'):
        os.makedirs('outputs/charts')

    # 1. Veri Yükleme
    loader = DataLoader()
    try:
        ratings, items, users, merged_data = loader.load_and_merge()
    except Exception as e:
        print(f"Hata: {e}")
        return

    # 2. Modülleri Hazırla
    analysis = Analysis(ratings, items, users, merged_data)
    engine = Recommender(ratings, items, users)
    manager = DataManager(loader)

    while True:
        clear_console()
        print_header("FİLM / KİTAP TAVSİYE SİSTEMİ ULTIMATE")
        print("1. Veri Yönetimi (Ekle/Sil)")
        print("2. Veri Seti Analiz Raporu")
        print("3. Analiz Grafiklerini Oluştur")
        print("4. Kullanıcı Demografik İstatistikleri")
        print("5. Kullanıcı Tabanlı Öneri Sistemi (User-Based)")
        print("6. İçerik Tabanlı Öneri Sistemi (Item-Based)")
        print("7. Favori Türüne Göre Akıllı Öneri")
        print("8. Öneri Yöntemlerini Karşılaştır")
        print("0. Çıkış")
        print("-" * 50)
        
        choice = input("Seçiminiz: ")

        if choice == '1':
            while True:
                clear_console()
                print_header("VERİ YÖNETİM PANELİ")
                print("1. Yeni Film/Kitap Ekle")
                print("2. Mevcut İçeriği Sil")
                print("3. Yeni Puan Ekle / Güncelle")
                print("0. Ana Menüye Dön")
                m_choice = input("\nSeçiminiz: ")

                if m_choice == '1':
                    title = input("Başlık: ")
                    cat = input("Kategori: ")
                    itype = input("Tür (Film/Kitap): ")
                    year = input("Yıl: ")
                    new_id = manager.add_new_item(title, cat, itype, year)
                    print(f"\n[OK] '{title}' başarıyla eklendi. Atanan ID: {new_id}")
                    input("\nDevam...")

                elif m_choice == '2':
                    try:
                        i_id = int(input("Silinecek İçerik ID: "))
                        if manager.delete_item(i_id):
                            print(f"\n[OK] ID: {i_id} olan içerik ve tüm puanları silindi.")
                        else:
                            print("\n[!] Hata: ID bulunamadı.")
                    except: print("\n[!] Hata: Geçersiz ID.")
                    input("\nDevam...")

                elif m_choice == '3':
                    try:
                        u_id = int(input("Kullanıcı ID: "))
                        i_id = int(input("İçerik ID: "))
                        rating = float(input("Puan (1-5): "))
                        if 1 <= rating <= 5:
                            success, msg = manager.add_rating(u_id, i_id, rating)
                            print(f"\n[{'OK' if success else '!'}] {msg}")
                        else:
                            print("\n[!] Puan 1-5 arasında olmalıdır.")
                    except: print("\n[!] Hata: Geçersiz giriş.")
                    input("\nDevam...")

                elif m_choice == '0':
                    # Verileri tekrar yükle ki değişiklikler her yere yansısın
                    ratings, items, users, merged_data = loader.load_and_merge()
                    analysis = Analysis(ratings, items, users, merged_data)
                    engine = Recommender(ratings, items, users)
                    break

        elif choice == '2':
            analysis.run_full_analysis()
            input("\nDevam etmek için Enter'a basın...")
        
        elif choice == '3':
            print("\nGrafikler hazırlanıyor...")
            try:
                analysis.create_visualizations()
            except Exception as e:
                print(f"Grafik oluşturma hatası: {e}")
            input("\nDevam etmek için Enter'a basın...")

        elif choice == '4':
            analysis.show_demographic_stats()
            input("\nDevam etmek için Enter'a basın...")

        elif choice == '5' or choice == '6':
            try:
                u_id = int(input("\nKullanıcı ID (1-10): "))
                if u_id not in users['user_id'].unique():
                    print("Hata: Kullanıcı bulunamadı!")
                    input("\nDevam...")
                    continue
                
                # Kullanıcı Bilgisini Göster
                u_info = users[users['user_id'] == u_id].iloc[0]
                print(f"\n>>> Kullanıcı: {u_id} | Yaş: {u_info.age} | Şehir: {u_info.city} | Favori: {u_info.favorite_genre}")

                # Filtreleme
                print("\n--- Filtreleme ---")
                print("1. Hepsi | 2. Film | 3. Kitap")
                f_choice = input("Seçim (1-3): ")
                f_type = 'Film' if f_choice == '2' else 'Kitap' if f_choice == '3' else None

                if choice == '5':
                    results = engine.get_user_recommendations(u_id, filter_type=f_type)
                    method = "User-Based"
                else:
                    results = engine.get_item_recommendations(u_id, filter_type=f_type)
                    method = "Item-Based"

                if not results.empty:
                    print(f"\n--- {method} Önerileri ---")
                    print(results.to_string(index=False))
                    
                    save = input("\nSonuçları kaydetmek ister misiniz? (e/h): ")
                    if save.lower() == 'e':
                        csv_path = os.path.join(project_root, 'outputs', 'recommendations.csv')
                        results.to_csv(csv_path, index=False)
                        print(f"Başarıyla kaydedildi: {csv_path}")
                else:
                    print("\nEşleşen öneri bulunamadı.")

            except ValueError:
                print("Hata: Geçersiz giriş.")
            input("\nDevam etmek için Enter'a basın...")

        elif choice == '7':
            try:
                u_id = int(input("\nKullanıcı ID (1-10): "))
                if u_id in users['user_id'].unique():
                    u_info = users[users['user_id'] == u_id].iloc[0]
                    print(f"\nFavori Türünüz: {u_info.favorite_genre}")
                    results = engine.get_genre_based_recommendations(u_id)
                    print(results.to_string(index=False))

                    save = input("\nSonuçları kaydetmek ister misiniz? (e/h): ")
                    if save.lower() == 'e':
                        csv_path = os.path.join(project_root, 'outputs', 'recommendations.csv')
                        results.to_csv(csv_path, index=False)
                        print(f"Başarıyla kaydedildi: {csv_path}")
                else:
                    print("Kullanıcı bulunamadı.")
            except Exception as e:
                print(f"Hata: {e}")
            input("\nDevam etmek için Enter'a basın...")

        elif choice == '8':
            try:
                u_id = int(input("\nKarşılaştırma için Kullanıcı ID (1-10): "))
                if u_id in users['user_id'].unique():
                    ub = engine.get_user_recommendations(u_id, top_n=3)
                    ib = engine.get_item_recommendations(u_id, top_n=3)
                    print("\n" + "-"*15 + f" KULLANICI {u_id} KIYASLAMA " + "-"*15)
                    print("\n[USER-BASED]")
                    print(ub[['Önerilen İçerik', 'Skor']] if not ub.empty else "Boş")
                    print("\n[ITEM-BASED]")
                    print(ib[['Önerilen İçerik', 'Skor']] if not ib.empty else "Boş")
                else:
                    print("Kullanıcı bulunamadı.")
            except Exception as e:
                print(f"Hata: {e}")
            input("\nDevam etmek için Enter'a basın...")

        elif choice == '0':
            break
        else:
            input("\nHatalı seçim. Devam...")

if __name__ == "__main__":
    main()
