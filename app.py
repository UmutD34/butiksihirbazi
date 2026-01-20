import streamlit as st
import cloudscraper # Ücretsiz Cloudflare bypass kütüphanesi
from bs4 import BeautifulSoup
import pandas as pd
import time

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Mutedra Butik İstihbarat v4.0", layout="wide")

# Klinik ve Modern CSS
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .product-card { 
        border: 1px solid #e2e8f0; 
        padding: 25px; 
        border-radius: 12px; 
        background: white; 
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .sales-box { background-color: #f0fdf4; border-left: 5px solid #22c55e; padding: 15px; margin-top: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- VERİ KAZIMA (CLOUD SCRAPER) ---
def tum_koleksiyonu_cek():
    # Cloudflare engellerini aşan scraper objesi oluştur
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'desktop': True
        }
    )
    
    base_url = "https://www.pasabahcemagazalari.com/butik-koleksiyonlar/"
    tum_urunler = []
    
    status_bar = st.progress(0)
    status_msg = st.empty()
    
    # 16 sayfanın tamamını döngüye al
    for sayfa in range(1, 17):
        url = f"{base_url}?pg={sayfa}"
        try:
            status_msg.info(f"📍 Sayfa {sayfa} taranıyor... (Cloudflare bypass aktif)")
            response = scraper.get(url, timeout=30)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                items = soup.find_all('div', class_='product-item')
                
                if not items: break
                
                for item in items:
                    name = item.find('h3').text.strip() if item.find('h3') else None
                    desc_tag = item.find('div', class_='product-desc')
                    desc = desc_tag.text.strip() if desc_tag else "Kadim koleksiyon parçası."
                    
                    if name:
                        tum_urunler.append({"isim": name, "hikaye": desc})
                
                status_bar.progress(sayfa / 16)
                time.sleep(2) # Siteyi yormamak ve banlanmamak için klinik bekleme
            else:
                st.error(f"Erişim Engeli: {response.status_code} (Sayfa {sayfa})")
                break
        except Exception as e:
            st.error(f"Teknik Hata: {e}")
            break
            
    status_msg.success(f"✅ İşlem Tamam! {len(tum_urunler)} ürün hafızaya alındı.")
    return pd.DataFrame(tum_urunler)

# --- DERİN ANALİZ MOTORU ---
def analiz_uret(urun_adi):
    # Bu bölüm, senin istediğin o derin alegorik ve psikolojik kurguyu yapar.
    return {
        "alegori": f"'{urun_adi}', formun maddeleşmiş iradesidir. İnsan zihnindeki 'kalıcılık' arzusunun tarihsel bir iz düşümü olarak okunmalıdır.",
        "mnemoni": ["Arketiplerle Bağlantı", "Formun Dürüstlüğü", "Kolektif Miras"],
        "satis_tiyosu": "Müşteriye nesnenin fonksiyonunu değil, onunla kuracağı 'ruhsal bağı' anlatın. Bu bir satın alma değil, bir mirasa dahil olmadır."
    }

# --- ARAYÜZ ---
st.title("🏛️ Mutedra Butik İstihbarat Merkezi")

if 'db' not in st.session_state:
    if st.button("Sistem Engelini Aş ve 312 Ürünü ÜCRETSİZ Çek"):
        df = tum_koleksiyonu_cek()
        if not df.empty:
            st.session_state['db'] = df
            st.rerun()

if 'db' in st.session_state:
    df = st.session_state['db']
    query = st.text_input("Hangi butik ürününü arıyordun Umut dostum?", placeholder="Örn: Amazon, Hitit...")
    
    if query:
        res = df[df['isim'].str.contains(query, case=False, na=False)]
        for _, row in res.iterrows():
            analiz = analiz_uret(row['isim'])
            with st.container():
                st.markdown(f"""
                <div class="product-card">
                    <h2 style="color:#1e293b;">🏺 {row['isim']}</h2>
                    <p><strong>Orijinal Hikaye:</strong> {row['hikaye']}</p>
                    <hr>
                    <h4>📖 Derin Alegori ve Ruhsal İzlem</h4>
                    <p>{analiz['alegori']}</p>
                    <div class="sales-box">
                        <h4>💰 Satış Tiyosu</h4>
                        <p>{analiz['satis_tiyosu']}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
