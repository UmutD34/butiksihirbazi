import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# --- KONFİGÜRASYON ---
st.set_page_config(page_title="Mutedra: Butik Veri Merkezi v2.0", layout="wide")

# Klinik Tasarım
st.markdown("""
    <style>
    .stApp { background-color: #f4f4f9; }
    .debug-box { background-color: #1e1e1e; color: #00ff00; padding: 15px; font-family: 'Courier New', monospace; border-radius: 5px; }
    .product-card { border: 1px solid #ddd; padding: 20px; border-radius: 10px; background: white; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

def tum_urunleri_tara_v2():
    base_url = "https://www.pasabahcemagazalari.com/butik-koleksiyonlar/"
    # Daha gerçekçi bir User-Agent (Tarayıcı gibi davranmak için)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Referer": "https://www.google.com/"
    }
    
    tum_liste = []
    # Muhtemel ürün kartı sınıfları (Site güncellenmiş olabilir)
    possible_classes = ['product-item', 'product-list-item', 'item-card', 'pr-item', 'product-box']
    
    sayfa = 1
    max_sayfa = 10 # Test aşamasında 10 sayfa yeterlidir

    status_area = st.empty()
    debug_area = st.expander("🔬 Klinik Veri Analizi (Hata Ayıklama)")

    while sayfa <= max_sayfa:
        url = f"{base_url}?pg={sayfa}"
        try:
            response = requests.get(url, headers=headers, timeout=20)
            
            if response.status_code != 200:
                debug_area.write(f"⚠️ Hata: Sunucu {response.status_code} yanıtı döndürdü.")
                break
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Ürünleri Bulma Denemesi (Çoklu Seçici)
            items = []
            for cls in possible_classes:
                items = soup.find_all('div', class_=cls)
                if items:
                    debug_area.write(f"✅ Sınıf Bulundu: `{cls}`")
                    break
            
            # Eğer yukarıdakilerle bulunamazsa, link içeren tüm divleri tara
            if not items:
                items = [div for div in soup.find_all('div') if div.find('h3') or div.find('a', href=True)]

            if not items:
                debug_area.write(f"❌ Sayfa {sayfa}: Ürün konteynerı bulunamadı.")
                break

            for item in items:
                # İsim Ayıklama
                name_tag = item.find('h3') or item.find('div', class_='name') or item.find('a')
                if not name_tag: continue
                
                name = name_tag.text.strip()
                if len(name) < 3: continue # Gereksiz verileri filtrele
                
                # Hikaye/Açıklama Ayıklama
                desc = "Butik koleksiyon parçası."
                desc_tag = item.find('div', class_='product-desc') or item.find('p')
                if desc_tag: desc = desc_tag.text.strip()

                tum_liste.append({"isim": name, "hikaye": desc})
            
            status_area.info(f"📍 Sayfa {sayfa} işlendi. Mevcut Ürün: {len(tum_liste)}")
            sayfa += 1
            time.sleep(1.5) # Sarsılmazlık İlkesi: İstikrar için bekleme

        except Exception as e:
            st.error(f"Sistemsel Hata: {str(e)}")
            break
            
    return pd.DataFrame(tum_liste)

# --- ARAYÜZ ---
st.title("🏛️ Mutedra Butik İstihbarat Merkezi v2.0")
st.write("Veri kazıma başarısı,
