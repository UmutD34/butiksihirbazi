import streamlit as st
import json
import time
import random

# --- 1. YAPILANDIRMA ---
st.set_page_config(
    page_title="Mutedra | Alegorik Arama Motoru",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="collapsed" # Mobilde menü kapalı başlar, yer kaplamaz
)

# --- 2. ESTETİK OTORİTE (CSS) ---
st.markdown("""
    <style>
    /* Genel Arka Plan */
    .stApp {
        background-color: #0e1117;
        color: #c9d1d9;
    }

    /* Arama Kutusu Stili (Google Gibi) */
    .stTextInput > div > div > input {
        background-color: #161b22;
        color: #ffffff;
        border: 1px solid #30363d;
        border-radius: 24px; /* Yuvarlak hatlar */
        padding: 10px 20px;
        font-size: 16px;
        text-align: center;
    }
    .stTextInput > div > div > input:focus {
        border-color: #d4af37;
        box-shadow: 0 0 10px rgba(212, 175, 55, 0.3);
    }

    /* Ürün Kartı Resim Ayarı (Kocaman resimleri engeller) */
    div[data-testid="stImage"] img {
        height: 180px;          /* Sabit yükseklik */
        width: 100%;            /* Genişlik sığsın */
        object-fit: contain;    /* Resmi kesmeden sığdır */
        margin-bottom: 10px;
    }

    /* Kart Kutusu */
    div[data-testid="column"] {
        background-color: #161b22;
        border: 1px solid #21262d;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        transition: all 0.3s ease;
    }
    div[data-testid="column"]:hover {
        border-color: #d4af37;
        transform: translateY(-5px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.5);
    }

    /* Butonlar */
    .stButton > button {
        width: 100%;
        border-radius: 20px;
        background-color: #21262d;
        color: #d4af37;
        border: 1px solid #30363d;
    }
    .stButton > button:hover {
        background-color: #d4af37;
        color: #0e1117;
        border-color: #d4af37;
    }
    
    /* Metinler */
    h1, h2, h3 { font-family: 'Helvetica Neue', sans-serif; font-weight: 300; }
    .product-title { font-size: 14px; font-weight: 600; min-height: 40px; display: flex; align-items: center; justify-content: center; }
    .price-tag { color: #8b949e; font-size: 12px; margin-bottom: 10px; }
    
    /* Alegori Kutusu */
    .allegory-box {
        background: linear-gradient(135deg, #1e2130 0%, #0d1117 100%);
        border-left: 4px solid #d4af37;
        padding: 20px;
        margin-top: 20px;
        border-radius: 0 8px 8px 0;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. VERİ MOTORU ---
@st.cache_data
def load_data():
    try:
        with open('urunler.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Her ürüne bir ID verelim
            for i, item in enumerate(data):
                item['id'] = i
            return data
    except FileNotFoundError:
        return []

products = load_data()

# --- 4. SOL MENÜ (Sistem Bilgileri) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/5360/5360936.png", width=60)
    st.markdown("### MUTEDRA")
    st.caption("v3.0 | Alegorik Arama Motoru")
    
    st.divider()
    
    st.markdown("**Sistem Durumu**")
    st.success("🟢 Aktif")
    
    st.markdown("**Veritabanı**")
    st.info(f"💾 {len(products)} Ürün Entegre")
    
    st.divider()
    st.markdown("### 🛠️ Emeği Geçenler")
    st.markdown("""
    **Developer:** Umut  
    **AI Core:** Mutedra Protocol  
    **Vizyon:** Sarsılmazlık İlkesi
    """)

# --- 5. ANA EKRAN MİMARİSİ ---

# State Yönetimi (Seçilen Ürün)
if 'selected_product' not in st.session_state:
    st.session_state.selected_product = None

def select_product(product):
    st.session_state.selected_product = product

# -- HEADER & ARAMA (Google Style) --
if st.session_state.selected_product is None:
    # Boşluk bırakarak ortala
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown("<h1 style='text-align: center; color: #d4af37;'>MUTEDRA</h1>", unsafe_allow_html=True)
        search_query = st.text_input("", placeholder="🔍 Alegorik bir şeyler arayın... (Örn: Vazo, Lale, Güç)", label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)

    # -- VİTRİN MANTIĞI --
    
    # 1. Filtreleme veya Rastgele Seçim
    if search_query:
        # Arama varsa filtrele
        display_items = [p for p in products if search_query.lower() in p['name'].lower() or search_query.lower() in p.get('raw_story', '').lower()]
        header_text = f"Bulunan Sonuçlar ({len(display_items)})"
    else:
        # Arama yoksa RASTGELE 8 ürün göster (Keşfet Modu)
        # Eğer ürün sayısı 8'den azsa hepsini göster
        sample_size = min(len(products), 8)
        display_items = random.sample(products, sample_size)
        header_text = "✨ Mutedra'nın Seçtikleri (Bugünün İlhamı)"

    st.subheader(header_text)
    
    # 2. Grid Gösterimi (4 Sütunlu - Mobilde otomatik teklenir)
    # Ürünleri 4'erli gruplara bölüyoruz
    cols = st.columns(4)
    
    for idx, p in enumerate(display_items):
        with cols[idx % 4]:
            # Resim
            if p.get('image'):
                st.image(p['image'], use_container_width=True)
            else:
                st.markdown("📷 *Görsel Yok*")
            
            # İsim (Uzunsa kes)
            short_name = (p['name'][:25] + '..') if len(p['name']) > 25 else p['name']
            st.markdown(f"<div class='product-title'>{short_name}</div>", unsafe_allow_html=True)
            
            # Buton
            if st.button("İncele", key=f"btn_{p['id']}"):
                select_product(p)
                st.rerun()

# -- DETAY SAYFASI (Ürün Seçilince) --
else:
    p = st.session_state.selected_product
    
    # Geri Dön
    if st.button("← Aramaya Dön", use_container_width=False):
        st.session_state.selected_product = None
        st.rerun()
    
    st.divider()
    
    # Detay Düzeni
    c1, c2 = st.columns([1, 1.5])
    
    with c1:
        st.image(p['image'], use_container_width=True)
        # Resmi siteye git butonu
        if p.get('link'):
            st.link_button("🌐 Ürünü Sitede Gör", p['link'], use_container_width=True)

    with c2:
        st.title(p['name'])
        
        # Fiyat varsa göster
        if p.get('price'):
            st.markdown(f"<div class='price-tag'>{p['price']}</div>", unsafe_allow_html=True)

        # Hikaye (İşlenmiş veri varsa onu, yoksa ham veriyi göster)
        hikaye = p.get('short_story', p.get('raw_story', 'Analiz ediliyor...'))
        st.info(hikaye)
        
        # Alegori Analizi (Simülasyon)
        with st.spinner('Mutedra Derin Analiz Yapıyor...'):
            time.sleep(0.7) # Yapay zeka düşünme efekti
            
        alegori = p.get('allegory', "Bu nesne, maddenin ötesinde bir anlam taşır. Camın kırılganlığı ile tarihin kalıcılığı arasındaki tezatı temsil eder.")
        
        st.markdown(f"""
            <div class="allegory-box">
                <strong style="color:#d4af37">DERİN ANLAM (ALEGORİ):</strong><br>
                {alegori}
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🧠 Satış Stratejisi")
        col_tip1, col_tip2 = st.columns(2)
        
        tips = p.get('sales_tips', ["Koleksiyonerlere önerin.", "Hikayesinden bahsedin."])
        if isinstance(tips, str): tips = [tips]
        
        with col_tip1:
            st.success(f"🎯 **Hedef:** {tips[0]}")
        with col_tip2:
            if len(tips) > 1:
                st.warning(f"💡 **Tiyo:** {tips[1]}")

# Footer
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; color: #30363d; font-size: 12px;'>Mutedra © 2026 | Sarsılmazlık İlkesi</div>", unsafe_allow_html=True)
