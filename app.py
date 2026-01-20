import streamlit as st
import json
import time
import random

# --- 1. YAPILANDIRMA ---
st.set_page_config(
    page_title="Butik Sihirbazı | Alegorik Ürün İstihbaratı",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ESTETİK OTORİTE (APPLE-VARI MODERN CSS) ---
st.markdown("""
    <style>
    /* 1. GENEL ZEMİN */
    .stApp {
        background-color: #fbfbfd;
        color: #1d1d1f;
        font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* 2. SOL MENÜ */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #d2d2d7;
    }
    
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3 {
        color: #1d1d1f !important;
    }

    /* 3. ÜRÜN KARTLARI */
    div[data-testid="column"] {
        background-color: #ffffff;
        border-radius: 18px;
        padding: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        border: 1px solid #f0f0f0;
        transition: all 0.3s ease;
        text-align: center;
        height: 100%; /* Eşit yükseklik */
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    div[data-testid="column"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        border-color: #d4af37;
    }

    /* 4. RESİMLER */
    div[data-testid="stImage"] {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 220px;
        margin-bottom: 15px;
    }
    
    div[data-testid="stImage"] img {
        max-height: 210px !important;
        object-fit: contain !important;
        mix-blend-mode: multiply;
    }

    /* 5. METİNLER */
    .product-title {
        font-size: 15px;
        font-weight: 600;
        color: #1d1d1f;
        margin-bottom: 10px;
        min-height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        line-height: 1.3;
    }

    /* 6. ARAMA KUTUSU */
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
        border-color: #0071e3;
        box-shadow: 0 0 0 4px rgba(0,113,227,0.1);
    }

    /* 7. BUTONLAR */
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
        background-color: #1d1d1f;
        color: #ffffff;
    }

    /* 8. DETAY ALANLARI */
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
            # ID ataması
            for i, item in enumerate(data):
                item['id'] = i
            return data
    except FileNotFoundError:
        return []

products = load_data()

# --- STATE YÖNETİMİ (SORUNU ÇÖZEN KISIM) ---
# Rastgele ürünleri bir kez seçip hafızada tutmalıyız ki her tıklamada değişmesin.
if 'random_products' not in st.session_state:
    if products:
        sample_size = min(len(products), 8)
        st.session_state.random_products = random.sample(products, sample_size)
    else:
        st.session_state.random_products = []

if 'selected_product' not in st.session_state:
    st.session_state.selected_product = None

def select_product(product):
    st.session_state.selected_product = product

# --- 4. SOL MENÜ (BUTİK SİHİRBAZI) ---
with st.sidebar:
    # Logo / Başlık
    st.markdown("<h2 style='text-align: center; color: #1d1d1f;'>BUTİK SİHİRBAZI</h2>", unsafe_allow_html=True)
    st.caption("“Zarafet, detayda gizlidir.”") # Özlü söz
    st.markdown("---")
    
    # Navigasyon
    menu = st.radio("Menü", ["Koleksiyon Ara", "Duyurular", "İletişim"])
    
    st.markdown("---")
    
    # Menü İçerikleri
    if menu == "İletişim":
        st.info("**Sistem Sorunları ve Geri Bildirim:**\n\n**Palladium Paşabahçe Mağazası**\n\n📩 isdogan@sisecam.com\n📩 palladiummgz@sisecam.com")
    
    elif menu == "Duyurular":
        st.warning("""
        **📢 HAKKIMIZDA & DUYURULAR**
        
        Butik Sihirbazı, **Palladium ve Hilltown Paşabahçe Mağazaları** tarafından üretilmiş olup, tüm Paşabahçe mağazalarındaki çalışma arkadaşlarımızı desteklemek üzere tüm fonksiyonları ile kullanıma hazırdır.
        
        ---
        **⚠️ Dipnot:** Sistemi kendi imkanlarımız ile yaptığımızdan yoğunluk sebebi ile sistemde aksaklık yaşanabilir. Böyle bir durumda lütfen iletişime geçiniz. 
        
        Geri bildirimleriniz ve fikirleriniz bizim için önemlidir.
        """)
    
    # Emeği Geçenler (Footer)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size: 11px; color: #666;'>
    <b>Designed by Umut Doğan</b><br>
    (Tasarım & Kodlama)<br><br>
    <b>Emeği Geçenler:</b><br>
    Nuriye Kulaksız<br>
    Fatih Demir<br>
    Adem Keleş<br><br>
    <i>Palladium ve Hilltown Mağazaları ürünüdür.</i>
    </div>
    """, unsafe_allow_html=True)

# --- 5. ANA EKRAN MANTIĞI ---

# --- MOD 1: VİTRİN (GALLERY) ---
if st.session_state.selected_product is None:
    
    # Başlık ve Arama
    c1, c2, c3 = st.columns([1, 6, 1])
    with c2:
        st.markdown("<h1 style='text-align: center; font-size: 40px;'>Koleksiyonu Keşfet.</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #86868b; font-size: 18px;'>Her hikaye dinlemeye değerdir.</p>", unsafe_allow_html=True)
        # Unique key ekleyerek input karışıklığını önleyelim
        search_query = st.text_input("", placeholder="🔍 Ürün, hikaye veya duygu arayın...", label_visibility="collapsed", key="main_search")

    st.markdown("<br>", unsafe_allow_html=True)

    # İçerik Belirleme
    if search_query:
        # Arama varsa veritabanından filtrele
        display_items = [p for p in products if search_query.lower() in p['name'].lower() or search_query.lower() in p.get('short_story', '').lower()]
        st.markdown(f"### 📂 Arama Sonuçları ({len(display_items)})")
    else:
        # Arama yoksa sabitlenmiş rastgele listeyi kullan
        display_items = st.session_state.random_products
        st.markdown("### 🍀 Şanslı Öneriler")

    # Grid Sistemi (4 Sütun)
    cols = st.columns(4)
    
    for idx, p in enumerate(display_items):
        with cols[idx % 4]:
            # --- KART ---
            if p.get('image'):
                st.image(p['image'], use_container_width=True)
            else:
                st.markdown("<div style='height:200px; display:flex; align-items:center; justify-content:center; color:#ccc;'>Görsel Yok</div>", unsafe_allow_html=True)
            
            st.markdown(f"<div class='product-title'>{p['name']}</div>", unsafe_allow_html=True)
            
            if st.button("İncele", key=f"btn_{p['id']}"):
                select_product(p)
                st.rerun()
            # --- KART SONU ---

# --- MOD 2: DETAY SAYFASI ---
else:
    p = st.session_state.selected_product
    
    # Geri Dön Butonu
    if st.button("← Koleksiyona Dön", use_container_width=False):
        st.session_state.selected_product = None
        st.rerun()
        
    st.markdown("<br>", unsafe_allow_html=True)

    # İki Sütunlu Düzen
    col_left, col_right = st.columns([1, 1.2])

    with col_left:
        # Büyük Görsel
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
        
        # Fiyat güvenli gösterim
        fiyat = p.get('price', '')
        if fiyat:
            st.markdown(f"<h3 style='color: #86868b; margin-top: 0;'>{fiyat}</h3>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)

        # Hikaye Kutusu
        hikaye = p.get('short_story', p.get('raw_story', '...'))
        st.markdown(f"""
            <div class="story-box">
                <span style="font-size: 20px;">❝</span><br>
                {hikaye}
            </div>
        """, unsafe_allow_html=True)

        # Alegori Analizi
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
        
        # Tip verisi liste mi string mi kontrolü
        if isinstance(tips, str): tips = [tips]
        
        with c1:
            st.success(f"**Hedef Kitle:** {tips[0]}")
        with c2:
            if len(tips) > 1:
                st.info(f"**Strateji:** {tips[1]}")
            else:
                st.info("**Strateji:** Bağ kurun.")

    # Footer (Sadece detay sayfasında)
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; color: #86868b; font-size: 13px;'>Tutku ile yapıldı ❤️</div>", unsafe_allow_html=True)
