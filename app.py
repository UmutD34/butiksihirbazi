import streamlit as st
import json
import time
import random

# --- 1. YAPILANDIRMA ---
st.set_page_config(
    page_title="Mutedra | Premium Envanter",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. APPLE-VARI MODERN CSS (ESTETİK OTORİTE) ---
st.markdown("""
    <style>
    /* 1. GENEL ZEMİN (Soft Gri - Apple Style) */
    .stApp {
        background-color: #fbfbfd; /* Apple web sitesi arka plan tonu */
        color: #1d1d1f; /* Apple standart metin rengi (Tam siyah değil) */
        font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* 2. SOL MENÜ (Clean White) */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #d2d2d7; /* İnce ayırıcı çizgi */
    }
    
    /* Sidebar Metinleri */
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3 {
        color: #1d1d1f !important;
    }

    /* 3. ÜRÜN KARTLARI (Kutu Tasarımı) */
    div[data-testid="column"] {
        background-color: #ffffff; /* Kartlar bembeyaz */
        border-radius: 18px; /* Apple tarzı yuvarlak köşeler */
        padding: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05); /* Çok hafif, lüks gölge */
        border: 1px solid #f0f0f0; /* Çok silik sınır */
        transition: all 0.3s ease;
        text-align: center;
    }
    
    div[data-testid="column"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1); /* Hover'da belirginleşen gölge */
        border-color: #d4af37; /* Sadece hover'da ince altın dokunuş */
    }

    /* 4. RESİMLER */
    div[data-testid="stImage"] {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 220px; /* Sabit yükseklik */
        margin-bottom: 15px;
    }
    
    div[data-testid="stImage"] img {
        max-height: 210px !important;
        object-fit: contain !important;
        mix-blend-mode: multiply; /* Beyaz arka planda resim kenarlarını yumuşatır */
    }

    /* 5. METİNLER VE BAŞLIKLAR */
    h1 { 
        color: #1d1d1f; 
        font-weight: 600; 
        letter-spacing: -0.5px; 
    }
    
    .product-title {
        font-size: 16px;
        font-weight: 500;
        color: #1d1d1f;
        margin-bottom: 5px;
        height: 45px;
        display: flex;
        align-items: center;
        justify-content: center;
        line-height: 1.2;
    }
    
    .price-tag {
        color: #86868b; /* Apple gri */
        font-size: 13px;
        margin-bottom: 15px;
        font-weight: 400;
    }

    /* 6. ARAMA KUTUSU (Minimalist) */
    .stTextInput > div > div > input {
        background-color: #ffffff;
        color: #1d1d1f;
        border: 1px solid #d2d2d7;
        border-radius: 12px;
        padding: 12px 15px;
        font-size: 16px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.02);
    }
    .stTextInput > div > div > input:focus {
        border-color: #0071e3; /* Apple mavisi odaklanma */
        box-shadow: 0 0 0 4px rgba(0,113,227,0.1);
    }

    /* 7. BUTONLAR (Soft & Clean) */
    .stButton > button {
        background-color: #f5f5f7;
        color: #1d1d1f;
        border: none;
        border-radius: 20px;
        padding: 8px 20px;
        font-weight: 500;
        width: 100%;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        background-color: #1d1d1f; /* Üzerine gelince siyah */
        color: #ffffff; /* Yazı beyaz */
    }

    /* 8. DETAY SAYFASI ÖZELLERİ */
    .story-box {
        background-color: #ffffff;
        border-left: 4px solid #d4af37;
        padding: 20px;
        border-radius: 0 12px 12px 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        color: #424245;
        font-style: italic;
    }
    
    .allegory-section {
        background-color: #f5f5f7;
        padding: 25px;
        border-radius: 18px;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. VERİ MOTORU ---
@st.cache_data
def load_data():
    try:
        with open('urunler.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            for i, item in enumerate(data):
                item['id'] = i
            return data
    except FileNotFoundError:
        return []

products = load_data()

# --- 4. SOL MENÜ (Clean Sidebar) ---
with st.sidebar:
    # Logo yerine temiz bir ikon veya başlık
    st.markdown("<h2 style='text-align: center; color: #1d1d1f;'>MUTEDRA</h2>", unsafe_allow_html=True)
    st.caption("Alegorik Analiz Protokolü v5.0")
    st.markdown("---")
    
    menu = st.radio("Navigasyon", ["Koleksiyon", "Hakkımızda", "İletişim"])
    
    st.markdown("---")
    
    if menu == "İletişim":
        st.info("📍 İstanbul, TR\n📧 contact@mutedra.com")
    
    # Alt Bilgi
    st.markdown("<div style='margin-top: 50px; text-align: center; color: #86868b; font-size: 12px;'>Designed by Umut<br>Powered by Sarsılmazlık</div>", unsafe_allow_html=True)

# --- 5. ANA EKRAN MANTIĞI ---

if 'selected_product' not in st.session_state:
    st.session_state.selected_product = None

def select_product(product):
    st.session_state.selected_product = product

# --- MOD 1: VİTRİN (GALLERY) ---
if st.session_state.selected_product is None:
    
    # Büyük Başlık ve Arama (Ortalanmış)
    c1, c2, c3 = st.columns([1, 6, 1])
    with c2:
        st.markdown("<h1 style='text-align: center; font-size: 40px;'>Koleksiyonu Keşfet.</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #86868b; font-size: 18px;'>Her nesnenin anlatacak bir hikayesi vardır.</p>", unsafe_allow_html=True)
        search_query = st.text_input("", placeholder="Ara: Vazo, Lale, Güç, Huzur...", label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)

    # Filtreleme
    if search_query:
        display_items = [p for p in products if search_query.lower() in p['name'].lower() or search_query.lower() in p.get('short_story', '').lower()]
        st.markdown(f"### 🔎 Sonuçlar ({len(display_items)})")
    else:
        # Rastgele Öneri
        sample_size = min(len(products), 8)
        display_items = random.sample(products, sample_size)
        st.markdown("### ✨ Sizin İçin Seçilenler")

    # GRID SİSTEMİ (4 Sütunlu)
    cols = st.columns(4)
    
    for idx, p in enumerate(display_items):
        with cols[idx % 4]:
            # Resim Alanı
            if p.get('image'):
                st.image(p['image'], use_container_width=True)
            else:
                st.markdown("<div style='height:200px; display:flex; align-items:center; justify-content:center; color:#ccc;'>Görsel Yok</div>", unsafe_allow_html=True)
            
            # Ürün Bilgisi
            st.markdown(f"<div class='product-title'>{p['name']}</div>", unsafe_allow_html=True)
            
            # İncele Butonu
            if st.button("İncele", key=f"btn_{p['id']}"):
                select_product(p)
                st.rerun()

# --- MOD 2: DETAY SAYFASI (PRODUCT PAGE) ---
else:
    p = st.session_state.selected_product
    
    # Geri Butonu (Sol Üst)
    if st.button("← Koleksiyona Dön", use_container_width=False):
        st.session_state.selected_product = None
        st.rerun()
        
    st.markdown("<br>", unsafe_allow_html=True)

    # İki Sütunlu Düzen (Sol: Görsel, Sağ: Hikaye)
    col_left, col_right = st.columns([1, 1.2])

    with col_left:
        # Büyük Görsel (Kutulu)
        st.markdown("""
            <div style="background: white; padding: 20px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.08);">
        """, unsafe_allow_html=True)
        st.image(p['image'], use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        if p.get('link'):
            st.markdown("<br>", unsafe_allow_html=True)
            st.link_button("🌐 Resmi Sitede Görüntüle", p['link'], use_container_width=True)

    with col_right:
        # Başlık ve Fiyat
        st.markdown(f"<h1 style='margin-bottom: 0;'>{p['name']}</h1>", unsafe_allow_html=True)
        if p.get('price'):
            st.markdown(f"<h3 style='color: #86868b; margin-top: 0;'>{p['price']}</h3>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)

        # Hikaye Kutusu
        hikaye = p.get('short_story', p.get('raw_story', '...'))
        st.markdown(f"""
            <div class="story-box">
                <span style="font-size: 20px;">❝</span><br>
                {hikaye}
            </div>
        """, unsafe_allow_html=True)

        # Alegori Analizi (Gri Alan)
        st.markdown("<br>", unsafe_allow_html=True)
        with st.spinner('Analiz ediliyor...'):
            time.sleep(0.3)
            
        alegori = p.get('allegory', "Derin anlam yükleniyor...")
        
        st.markdown(f"""
            <div class="allegory-section">
                <h4 style="color: #d4af37; margin-top:0;">👁️ DERİN ANLAM (ALEGORİ)</h4>
                <p style="color: #1d1d1f; font-size: 15px; line-height: 1.6;">{alegori}</p>
            </div>
        """, unsafe_allow_html=True)

        # Satış Tiyoları
        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        tips = p.get('sales_tips', ["Özel bir parça.", "Hikayesini anlatın."])
        if isinstance(tips, str): tips = [tips]
        
        with c1:
            st.success(f"**Hedef Kitle:** {tips[0]}")
        with c2:
            if len(tips) > 1:
                st.info(f"**Strateji:** {tips[1]}")

# Footer
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; color: #d2d2d7; font-size: 12px;'>Mutedra © 2026 | Sarsılmazlık İlkesi</div>", unsafe_allow_html=True)
