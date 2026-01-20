import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# --- KONFİGÜRASYON ---
st.set_page_config(page_title="Mutedra: Butik Veri Merkezi", layout="wide")

# Klinik ve Seçkin Görünüm Ayarları
st.markdown("""
    <style>
    .stApp { background-color: #fafafa; }
    .product-card { 
        border: 1px solid #d1d1d1; 
        padding: 20px; 
        border-radius: 10px; 
        background: white; 
        margin-bottom: 15px;
        box-shadow: 3px 3px 10px rgba(0,0,0,0.05);
    }
    .highlight { color: #1a1a1a; font-weight: bold; font-family: 'Georgia', serif; }
    .trick-box { background-color: #f0fdf4; border-left: 5px solid #22c55e; padding: 15px; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- VERİ KAZIMA MOTORU ---
def urunleri_getir():
    """
    Hedef sitedeki ürünleri tarar. Kurumsal engelleri aşmak için 
    User-Agent ve bekleme süreleri optimize edilmiştir.
    """
    base_url = "https://www.pasabahcemagazalari.com/butik-koleksiyonlar/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    urun_listesi = []
    
    try:
        # İlk 3 sayfayı tarayarak sistemi test edelim (Hız için)
        for sayfa in range(1, 4):
            url = f"{base_url}?pg={sayfa}"
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code != 200:
                continue
                
            soup = BeautifulSoup(response.content, 'html.parser')
            # Sitenin güncel HTML yapısına göre ürünleri yakala
            items = soup.find_all('div', class_='product-item')
            
            for item in items:
                name = item.find('h3').text.strip() if item.find('h3') else "Bilinmeyen Ürün"
                # Link ve kısa açıklama ayıklama
                link = item.find('a')['href'] if item.find('a') else "#"
                desc = item.find('div', class_='product-desc')
                desc_text = desc.text.strip() if desc else "Koleksiyonun özel bir parçası."
                
                urun_listesi.append({
                    "isim": name,
                    "hikaye": desc_text,
                    "link": f"https://www.pasabahcemagazalari.com{link}"
                })
            time.sleep(1) # Sitenin engellememesi için klinik bekleme
            
    except Exception as e:
        st.error(f"Teknik bir aksama yaşandı: {e}")
        
    return pd.DataFrame(urun_listesi)

# --- ANALİZ VE SATIŞ SİMÜLASYONU ---
def analiz_et(urun_adi):
    # Bu bölüm, senin istediğin alegorik ve derinlikli yapıyı kurgular.
    return {
        "alegori": f"{urun_adi}, maddeselliğin ötesine geçerek ruhun camdaki yansımasını simgeler. Formu, kadim Anadolu bilgisinin modern dünyadaki sessiz çığlığıdır.",
        "mnemoni": [
            "Zamansız Estetik: Trendlerin ötesinde bir varoluş.",
            "Teknik Mükemmeliyet: Kusursuz bir geometrik disiplin.",
            "Sembolik Değer: Her detayında gizli bir tarihsel kod."
        ],
        "satis_tiyosu": "Müşteriye nesnenin fonksiyonunu değil, onunla kuracağı 'ruhsal bağı' anlatın. Bu ürün bir eşya değil, bir karakter beyanıdır."
    }

# --- ARAYÜZ ---
st.title("🏛️ Mutedra Butik İstihbarat Merkezi")
st.write("Veri kazıma başarısı, kodun hedef sitenin yapısına ne kadar uyum sağladığına bağlıdır.")

if 'data' not in st.session_state:
    if st.button("Koleksiyonu Veritabanına Al"):
        with st.spinner("Koleksiyonun derinliklerine iniliyor..."):
            df = urunleri_getir()
            if not df.empty:
                st.session_state['data'] = df
                st.success(f"Tarama Tamamlandı! {len(df)} ürün sisteme dahil edildi.")
            else:
                st.error("Ürünler çekilemedi. Site bot koruması kullanıyor olabilir.")

if 'data' in st.session_state:
    df = st.session_state['data']
    sorgu = st.text_input("Hangi butik ürününü arıyordun Umut dostum?", placeholder="Örn: Amazon, Hitit...")

    if sorgu:
        sonuc = df[df['isim'].str.contains(sorgu, case=False, na=False)]
        
        if not sonuc.empty:
            for _, row in sonuc.iterrows():
                analiz = analiz_et(row['isim'])
                with st.container():
                    st.markdown(f"""
                    <div class="product-card">
                        <h2 class="highlight">🏺 {row['isim']}</h2>
                        <p><strong>Orijinal Tanım:</strong> {row['hikaye']}</p>
                        <hr>
                        <h4>📖 Derin Alegori ve Ruhsal İzlem</h4>
                        <p>{analiz['alegori']}</p>
                        <h4>🧠 Hafıza Çivileri (Mnemoni)</h4>
                        <ul>{''.join([f'<li>{m}</li>' for m in analiz['mnemoni']])}</ul>
                        <div class="trick-box">
                            <h4>💰 Satış Tiyosu</h4>
                            <p>{analiz['satis_tiyosu']}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("Eşleşen ürün bulunamadı.")
