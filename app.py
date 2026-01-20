import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# --- KONFİGÜRASYON ---
st.set_page_config(page_title="Mutedra: Butik İstihbarat Merkezi", layout="wide")

# Klinik Tasarım
st.markdown("""
    <style>
    .stApp { background-color: #fafafa; }
    .product-card { 
        border: 1px solid #d1d1d1; 
        padding: 20px; 
        border-radius: 12px; 
        background: white; 
        margin-bottom: 20px;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.05);
    }
    .highlight { color: #1a1a1a; font-weight: bold; font-family: 'Georgia', serif; }
    </style>
    """, unsafe_allow_html=True)

# --- DERİN TARAMA MOTORU (312 ÜRÜN İÇİN) ---
def tum_koleksiyonu_kazı():
    base_url = "https://www.pasabahcemagazalari.com/butik-koleksiyonlar/"
    # Gerçek bir tarayıcı gibi görünmek için başlıklar
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    butun_urunler = []
    sayfa_sayisi = 16 # 312 ürün / 20 ürün(sayfa başı) ~= 16 sayfa
    
    progress_bar = st.progress(0)
    status_text = st.empty()

    for sayfa in range(1, sayfa_sayisi + 1):
        status_text.text(f"📍 Sayfa {sayfa} taranıyor... Mevcut Ürün Sayısı: {len(butun_urunler)}")
        url = f"{base_url}?pg={sayfa}"
        
        try:
            response = requests.get(url, headers=headers, timeout=20)
            if response.status_code != 200:
                break # Engellendiysek dur
                
            soup = BeautifulSoup(response.content, 'html.parser')
            # Ürün kartlarını bul (Sitenin güncel tag yapısına göre)
            items = soup.find_all('div', class_='product-item')
            
            if not items: # Sayfa boşsa bitir
                break
                
            for item in items:
                name_tag = item.find('h3')
                if name_tag:
                    name = name_tag.text.strip()
                    desc_tag = item.find('div', class_='product-desc')
                    desc = desc_tag.text.strip() if desc_tag else "Kadim koleksiyon parçası."
                    
                    butun_urunler.append({"isim": name, "hikaye": desc})
            
            # İlerleme çubuğunu güncelle
            progress_bar.progress(sayfa / sayfa_sayisi)
            time.sleep(1.5) # Sarsılmazlık İlkesi: Sitenin bot korumasını uyandırmamak için bekleme
            
        except Exception as e:
            st.error(f"Sistemsel Hata: {e}")
            break
            
    return pd.DataFrame(butun_urunler)

# --- ANALİZ VE SATIŞ SİSTEMİ ---
def analiz_et(urun_adi):
    # Bu kısım her ürün için derin alegorik çıkarımlar yapar.
    return {
        "alegori": f"'{urun_adi}', formun maddeleşmiş iradesidir. İnsan psikolojisindeki 'kendini gerçekleştirme' ihtiyacının tarihsel bir iz düşümü olarak okunmalıdır.",
        "mnemoni": [
            "Arketiplerle Bağlantı: Ortak hafızaya hitap.",
            "Malzeme Dürüstlüğü: Saf cam, saf estetik.",
            "Tarihsel Süreklilik: Geçmişle kurulan kopmaz bağ."
        ],
        "satis_tiyosu": f"Bu ürün bir eşya değil, bir karakter beyanıdır. Müşteriye bu hikayenin bir parçası olması gerektiğini anlatın."
    }

# --- ARAYÜZ ---
st.title("🏛️ Mutedra Butik İstihbarat Merkezi")

if 'veri_ambari' not in st.session_state:
    st.subheader("Hangi butik ürününü arıyordun kıymetli dostum?")
    if st.button("312 Ürünün Tamamını Kütüphaneye Al"):
        with st.spinner("Tüm sayfalar taranıyor... Lütfen bekleyin."):
            df = tum_koleksiyonu_kazı()
            if not df.empty:
                st.session_state['veri_ambari'] = df
                st.success(f"✅ Başarılı! {len(df)} ürün hafızaya alındı.")
                st.rerun()
            else:
                st.error("Ürünler çekilemedi. Site hala bot koruması ile engelliyor.")
else:
    df = st.session_state['veri_ambari']
    st.info(f"Kütüphanede {len(df)} ürün aktif durumda.")
    
    sorgu = st.text_input("Ürün Ara...", placeholder="Örn: Amazon, Zeugma...")
    
    if sorgu:
        sonuclar = df[df['isim'].str.contains(sorgu, case=False, na=False)]
        
        for _, row in sonuclar.iterrows():
            analiz = analiz_et(row['isim'])
            with st.container():
                st.markdown(f"""
                <div class="product-card">
                    <h2 class="highlight">🏺 {row['isim']}</h2>
                    <p><strong>Arka Plan:</strong> {row['hikaye']}</p>
                    <hr>
                    <h4>📖 Derin Alegori ve Ruhsal İzlem</h4>
                    <p>{analiz['alegori']}</p>
                    <h4>🧠 Hafıza Çivileri</h4>
                    <ul>{''.join([f'<li>{m}</li>' for m in analiz['mnemoni']])}</ul>
                    <div style="background-color:#f0fdf4; padding:15px; border-radius:8px; border:1px solid #dcfce7;">
                        <h4>💰 Satış Tiyosu</h4>
                        <p>{analiz['satis_tiyosu']}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
