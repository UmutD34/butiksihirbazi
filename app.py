import streamlit as st
import json
import time
import random

# --- 1. YAPILANDIRMA VE SAYFA AYARLARI ---
st.set_page_config(
    page_title="Mutedra | Alegorik Ürün İstihbaratı",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ESTETİK OTORİTE (CSS MANİPÜLASYONU) ---
st.markdown("""
    <style>
    /* Ana Arka Plan */
    .stApp {
        background-color: #0e1117;
        color: #c9d1d9;
    }
    
    /* Kart Tasarımı (Ürün Kutuları) */
    div[data-testid="column"] {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 15px;
        transition: transform 0.2s;
    }
    div[data-testid="column"]:hover {
        border-color: #d4af37;
        transform: translateY(-5px);
    }

    /* Başlıklar */
    h1, h2, h3 {
        font-family: 'Helvetica Neue', sans-serif;
        color: #ffffff;
        font-weight: 300;
        letter-spacing: 1px;
    }
    
    /* Vurgulu Metinler (Altın Sarısı) */
    .gold-text {
        color: #d4af37;
        font-weight: bold;
    }

    /* Alegori Kutusu */
    .allegory-box {
        background: linear-gradient(135deg, #1e2130 0%, #161b22 100%);
        border-left: 5px solid #d4af37;
        padding: 25px;
        margin-top: 20px;
        border-radius: 0 10px 10px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }

    /* Buton Tasarımı */
    .stButton>button {
        width: 100%;
        background-color: #21262d;
        color: #d4af37;
        border: 1px solid #d4af37;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #d4af37;
        color: #0e1117;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. VERİ MOTORU ---
@st.cache_data
def load_data():
    try:
        with open('urunler.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Veri temizliği: ID ataması yapalım (seçim için gerekli)
            for i, item in enumerate(data):
                item['id'] = i
            return data
    except FileNotFoundError:
        return []

# --- 4. ARAYÜZ MİMARİSİ ---

# Yan Panel (Arama ve Filtreleme)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/5360/5360936.png", width=50)
    st.title("MUTEDRA")
    st.caption("Alegorik Analiz Protokolü v2.0")
    st.divider()
    
    # Arama Motoru
    search_query = st.text_input("🔍 Varlık Taraması:", placeholder="Örn: Füreya, Vazo, Nude...")
    
    st.info("Sistem Durumu: 🟢 Aktif\nVeritabanı: Entegre")

# Ana Ekran
products = load_data()

if not products:
    st.error("⚠️ KRİTİK HATA: 'urunler.json' bulunamadı.")
    st.warning("Lütfen scraper.py dosyasını çalıştırarak veriyi çekin.")
    st.stop()

# --- Arama Mantığı ---
if search_query:
    filtered_products = [p for p in products if search_query.lower() in p['name'].lower()]
else:
    filtered_products = products[:12] # Arama yoksa ilk 12 ürünü göster (Vitrin)

# --- Session State (Seçilen Ürünü Hatırlama) ---
if 'selected_product' not in st.session_state:
    st.session_state.selected_product = None

# --- Ürün Seçimi Fonksiyonu ---
def select_product(product):
    st.session_state.selected_product = product

# --- GÖRÜNÜM MODLARI ---

# MOD 1: VİTRİN (Ürün seçilmediyse veya yeni arama yapıldıysa)
if st.session_state.selected_product is None or (search_query and st.session_state.selected_product['name'].lower() not in search_query.lower()):
    
    st.subheader(f"📂 Sonuçlar ({len(filtered_products)})")
    
    # Grid Sistemi (3 Sütunlu)
    cols = st.columns(3)
    
    for idx, p in enumerate(filtered_products):
        with cols[idx % 3]:
            # Resim (Hata korumalı)
            if p.get('image'):
                st.image(p['image'], use_container_width=True)
            else:
                st.markdown("📷 *Görsel Yok*")
            
            # İsim
            st.markdown(f"**{p['name']}**")
            
            # Seçim Butonu
            if st.button("İncele & Analiz Et", key=f"btn_{p['id']}"):
                select_product(p)
                st.rerun()

# MOD 2: ANALİZ MASASI (Bir ürün seçildiğinde)
else:
    p = st.session_state.selected_product
    
    # Geri Dön Butonu
    if st.button("← Listeye Dön"):
        st.session_state.selected_product = None
        st.rerun()

    st.divider()

    # İki Sütunlu Detay Görünümü
    col_left, col_right = st.columns([1, 2])

    with col_left:
        st.image(p['image'], use_container_width=True)
        # Fiyat Bilgisi (Hata Korumalı)
        fiyat = p.get('price', 'Fiyat Bilgisi Gizli')
        st.caption(f"🏷️ Fiyat Endeksi: {fiyat}")
        if p.get('link'):
            st.link_button("🌐 Resmi Siteye Git", p['link'])

    with col_right:
        st.title(p['name'])
        
        # Eğer JSON dosyasında temizlenmiş veri (short_story vb.) varsa onu kullan
        # Yoksa (henüz işlemediysek) raw_story kullan
        hikaye = p.get('short_story', p.get('raw_story', 'Hikaye verisi işleniyor...'))
        
        st.markdown(f"*{hikaye}*")
        
        st.markdown("### 👁️ Mutedra Analizi")
        
        # Simülasyon Efekti (Yapay Zeka düşünüyor gibi)
        with st.spinner('Alegorik katmanlar çözümleniyor...'):
            time.sleep(0.8) 
        
        # Alegori Kutusu
        alegori = p.get('allegory', "Bu nesne, maddenin ötesinde bir anlam taşır. Camın kırılganlığı ile tarihin kalıcılığı arasındaki tezatı temsil eder.")
        
        st.markdown(f"""
            <div class="allegory-box">
                <span class="gold-text">DERİN ANLAM:</span><br>
                {alegori}
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Satış Stratejisi
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### 🎯 Kime Satılır?")
            # Eğer sales_tips liste ise madde madde yaz, değilse düz yaz
            tips = p.get('sales_tips', ["Prestij arayanlara.", "Hikayesi olan objeleri sevenlere."])
            if isinstance(tips, list):
                for tip in tips:
                    st.success(f"✓ {tip}")
            else:
                st.success(tips)

        with c2:
            st.markdown("#### 🧠 Psikolojik Kanca")
            st.info("Bu bir satın alma değil, bir kültürel mirasa ortak olma eylemidir.")

# Footer
st.markdown("---")
st.caption("Mutedra © 2026 | Sarsılmazlık İlkesi ile kodlanmıştır.")
