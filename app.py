import streamlit as st
import json
import time
import random

# --- 1. YAPILANDIRMA ---
st.set_page_config(
    page_title="Mutedra | Alegorik Ürün İstihbaratı",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded" # Menü açık başlasın
)

# --- 2. ESTETİK OTORİTE (PREMIUM CSS) ---
st.markdown("""
    <style>
    /* ANA ZEMİN */
    .stApp {
        background: linear-gradient(to bottom, #0f1116, #161b22); /* Profesyonel Koyu Ton */
        color: #e6e6e6;
    }

    /* SOL MENÜ (SIDEBAR) */
    section[data-testid="stSidebar"] {
        background-color: #1c1f26; /* Daha açık gri-siyah */
        border-right: 1px solid #2d333b;
    }

    /* ÜRÜN KARTLARI (KUTULAR) */
    div[data-testid="column"] {
        background-color: #21262d; /* Kart Rengi */
        border: 1px solid #30363d;
        border-radius: 12px; /* Yuvarlak köşeler */
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3); /* Derinlik Gölgesi */
        transition: transform 0.2s, border-color 0.2s;
        text-align: center;
        height: 100%;
    }
    
    div[data-testid="column"]:hover {
        transform: translateY(-5px); /* Üzerine gelince yukarı kalksın */
        border-color: #d4af37; /* Altın sarısı kenar */
        box-shadow: 0 8px 15px rgba(212, 175, 55, 0.15);
    }

    /* RESİMLER (PROFESYONEL GÖRÜNÜM) */
    div[data-testid="stImage"] {
        border-radius: 8px;
        overflow: hidden;
        margin-bottom: 10px;
        background-color: #ffffff; /* Resim arkası beyaz olsun ki ürün parlasın */
        padding: 5px;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 200px; /* Sabit yükseklik */
    }
    
    div[data-testid="stImage"] img {
        max-height: 190px !important;
        object-fit: contain !important; /* Resmi kesme, sığdır */
    }

    /* BAŞLIKLAR VE METİNLER */
    h1 { color: #d4af37; font-family: 'Helvetica Neue', sans-serif; font-weight: 300; letter-spacing: 2px; }
    h3 { color: #ffffff; font-weight: 400; }
    .product-title {
        font-size: 15px;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 8px;
        height: 40px; /* İsimler için sabit alan */
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
    }

    /* ARAMA KUTUSU (GOOGLE STYLE) */
    .stTextInput > div > div > input {
        border-radius: 50px;
        border: 2px solid #30363d;
        background-color: #0d1117;
        color: white;
        padding: 12px 20px;
        text-align: center;
        font-size: 16px;
    }
    .stTextInput > div > div > input:focus {
        border-color: #d4af37;
        box-shadow: 0 0 10px rgba(212, 175, 55, 0.4);
    }

    /* BUTONLAR */
    .stButton > button {
        border-radius: 8px;
        border: 1px solid #d4af37;
        background-color: transparent;
        color: #d4af37;
        width: 100%;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #d4af37;
        color: #000000;
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

# --- 4. SOL MENÜ (SIDEBAR) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/5360/5360936.png", width=80)
    st.title("MUTEDRA")
    st.caption("Alegorik Ürün İstihbaratı v4.0")
    
    st.divider()
    
    # Navigasyon
    menu = st.radio("MENÜ", ["🏠 Ana Sayfa", "ℹ️ Hakkımızda", "📞 İletişim"], index=0)
    
    st.divider()
    
    # İletişim / Bilgi Kartı
    if menu == "📞 İletişim":
        st.info("📧 info@mutedra.com\n📍 İstanbul, Türkiye")
    elif menu == "ℹ️ Hakkımızda":
        st.info("Mutedra, nesnelerin görünen yüzeyinin ötesindeki derin anlamı ve satış hikayesini ortaya çıkaran yapay zeka destekli bir analiz protokolüdür.")
    
    st.markdown("---")
    st.markdown("**Geliştirici:** Umut")
    st.caption("© 2026 Mutedra Protocol")

# --- 5. ANA SAYFA MİMARİSİ ---

# State Yönetimi
if 'selected_product' not in st.session_state:
    st.session_state.selected_product = None

def select_product(product):
    st.session_state.selected_product = product

# -- ARAMA VE BAŞLIK (ORTA ALAN) --
if st.session_state.selected_product is None:
    
    # Logo ve Başlık Ortalı
    c1, c2, c3 = st.columns([1, 6, 1])
    with c2:
        st.markdown("<h1 style='text-align: center;'>MUTEDRA</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #8b949e;'>Nesnelerin ruhunu keşfedin.</p>", unsafe_allow_html=True)
        
        # Google Tarzı Arama
        search_query = st.text_input("", placeholder="🔍 Ürün, hikaye veya duygu arayın...", label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)

    # -- VİTRİN --
    if search_query:
        display_items = [p for p in products if search_query.lower() in p['name'].lower() or search_query.lower() in p.get('short_story', '').lower()]
        st.markdown(f"### 📂 Arama Sonuçları ({len(display_items)})")
    else:
        # Rastgele Öneri (Keşfet Modu)
        sample_size = min(len(products), 12) # 12 Ürün gösterelim
        display_items = random.sample(products, sample_size)
        st.markdown("### ✨ Sizin İçin Seçtiklerimiz")

    # Grid Sistemi (4 Sütun)
    # Mobilde otomatik teklenir, masaüstünde 4'lü olur
    cols = st.columns(4)
    
    for idx, p in enumerate(display_items):
        with cols[idx % 4]:
            # --- KART YAPISI BAŞLANGICI ---
            # Resim
            if p.get('image'):
                st.image(p['image'], use_container_width=True)
            else:
                st.markdown("<div style='height:200px; display:flex; align-items:center; justify-content:center; background:#333; color:#777;'>Görsel Yok</div>", unsafe_allow_html=True)
            
            # Ürün İsmi
            st.markdown(f"<div class='product-title'>{p['name']}</div>", unsafe_allow_html=True)
            
            # Fiyat (Varsa)
            if p.get('price'):
                st.caption(f"🏷️ {p['price']}")
            
            # İncele Butonu
            if st.button("İncele", key=f"btn_{p['id']}"):
                select_product(p)
                st.rerun()
            # --- KART SONU ---

# -- DETAY SAYFASI --
else:
    p = st.session_state.selected_product
    
    # Üst Bar (Geri Dön)
    c_back, c_title = st.columns([1, 5])
    with c_back:
        if st.button("← Geri"):
            st.session_state.selected_product = None
            st.rerun()
    
    st.divider()

    # Ürün Detayları
    col_img, col_info = st.columns([1, 1.5])
    
    with col_img:
        st.image(p['image'], use_container_width=True)
        if p.get('link'):
            st.link_button("🌐 Ürünü Sitesinde Gör", p['link'], use_container_width=True)

    with col_info:
        st.title(p['name'])
        
        # Vurucu Hikaye
        hikaye = p.get('short_story', p.get('raw_story', 'Analiz bekleniyor...'))
        st.info(f"📖 {hikaye}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Mutedra Analizi
        with st.spinner('Alegorik katmanlar işleniyor...'):
            time.sleep(0.5)
            
        # Alegori
        alegori = p.get('allegory', "Bu nesne, maddenin ötesinde derin bir anlam taşır.")
        st.markdown(f"""
            <div style="background: #1c1f26; border-left: 5px solid #d4af37; padding: 20px; border-radius: 8px;">
                <h4 style="color: #d4af37; margin:0;">👁️ DERİN ANLAM (ALEGORİ)</h4>
                <p style="margin-top: 10px; color: #ddd;">{alegori}</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)

        # Satış Tiyoları (Grid)
        t1, t2 = st.columns(2)
        tips = p.get('sales_tips', ["Koleksiyonluk bir parça.", "Hikayesiyle etkileyin."])
        if isinstance(tips, str): tips = [tips]
        
        with t1:
            st.success(f"🎯 **Hedef Kitle:**\n{tips[0]}")
        with t2:
            if len(tips) > 1:
                st.warning(f"💡 **Satış Tiyosu:**\n{tips[1]}")
            else:
                st.warning("💡 **Tiyo:** Duygusal bağ kurun.")

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; color: #555;'>Mutedra Alegorik Analizör © 2026</div>", unsafe_allow_html=True)
