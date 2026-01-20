import streamlit as st
import json
import os
import random

# --- 1. YAPILANDIRMA ---
st.set_page_config(
    page_title="Butik Sihirbazı",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS (Tasarım) ---
st.markdown("""
<style>
    .stApp { background-color: #fbfbfd; color: #1d1d1f; }
    div[data-testid="column"] { background-color: #fff; border-radius: 15px; padding: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); border: 1px solid #eee; text-align: center; height: 100%; display: flex; flex-direction: column; justify-content: space-between; }
    div[data-testid="stImage"] img { max-height: 200px !important; object-fit: contain !important; mix-blend-mode: multiply; }
    .product-title { font-weight: 600; margin: 10px 0; min-height: 40px; display: flex; align-items: center; justify-content: center; }
    .tag-badge { background-color: #eee; padding: 4px 8px; border-radius: 6px; font-size: 11px; margin: 2px; display: inline-block; }
</style>
""", unsafe_allow_html=True)

# --- 2. VERİ YÜKLEME (DEBUG MODU) ---
@st.cache_data
def load_data():
    file_path = 'urunler2.json'
    
    # KONTROL 1: Dosya var mı?
    if not os.path.exists(file_path):
        return None, f"❌ HATA: '{file_path}' dosyası bulunamadı! Lütfen önce 'hazirlik.py' dosyasını çalıştırın."
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if not data:
                return None, "⚠️ UYARI: Dosya bulundu ama içi boş!"
            return data, None
    except Exception as e:
        return None, f"❌ OKUMA HATASI: {str(e)}"

# Veriyi Yükle
products, error_message = load_data()

# --- 3. HATA YÖNETİMİ ---
if error_message:
    st.error(error_message)
    st.info("💡 İpucu: Terminale gidip `python hazirlik.py` yazarak veritabanını oluşturun.")
    st.stop() # Uygulamayı burada durdur

# --- 4. ANA UYGULAMA (Sadece Veri Varsa Çalışır) ---

# State Yönetimi
if 'selected_product' not in st.session_state:
    st.session_state.selected_product = None

if 'random_products' not in st.session_state:
    sample_size = min(len(products), 8)
    st.session_state.random_products = random.sample(products, sample_size)

def select_product(p):
    st.session_state.selected_product = p

# Arama Fonksiyonu
def smart_search(query):
    query = query.lower()
    return [p for p in products if query in (p.get('name','')+str(p.get('tags',''))+p.get('short_story','')).lower()]

# --- ARAYÜZ ---
with st.sidebar:
    st.header("BUTİK SİHİRBAZI")
    st.caption("“Zarafet akılda kalmaktır.”")
    menu = st.radio("Menü", ["🔍 Koleksiyon", "ℹ️ Hakkında"])
    
    if menu == "ℹ️ Hakkında":
        st.info(f"📚 Veritabanı: urunler2.json\n📦 Toplam Ürün: {len(products)}")

# SAYFA 1: LİSTE
if st.session_state.selected_product is None:
    st.title("Koleksiyonu Keşfet")
    search = st.text_input("🔍 Ara...", placeholder="Örn: Vazo, Atatürk, Aşk...")
    
    if search:
        items = smart_search(search)
        st.subheader(f"Sonuçlar ({len(items)})")
    else:
        items = st.session_state.random_products
        st.subheader("🍀 Öne Çıkanlar")
        
    cols = st.columns(4)
    for i, p in enumerate(items):
        with cols[i % 4]:
            if p.get('image'): st.image(p['image'])
            st.markdown(f"<div class='product-title'>{p['name']}</div>", unsafe_allow_html=True)
            # Etiketler
            tags = p.get('tags', [])[:2]
            st.markdown(" ".join([f"<span class='tag-badge'>{t}</span>" for t in tags]), unsafe_allow_html=True)
            
            if st.button("İncele", key=f"btn_{p.get('id', i)}"):
                select_product(p)
                st.rerun()

# SAYFA 2: DETAY
else:
    p = st.session_state.selected_product
    if st.button("← Geri Dön"):
        st.session_state.selected_product = None
        st.rerun()
        
    c1, c2 = st.columns([1, 1])
    with c1:
        if p.get('image'): st.image(p['image'])
    with c2:
        st.title(p['name'])
        st.caption(" ".join([f"#{t}" for t in p.get('tags', [])]))
        st.markdown(f"### {p.get('price', 'Fiyat Mağazada')}")
        st.info(f"**Hikaye:** {p.get('short_story', p.get('raw_story', '...'))}")
        st.success(f"**Satış İpucu:** {p.get('sales_tips', ['Hikayesini anlatın'])[0]}")
        st.warning(f"**Alegori:** {p.get('allegory', 'Estetik form.')}")
