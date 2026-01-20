import streamlit as st
import json
import time
import random
import os

# --- 1. YAPILANDIRMA ---
st.set_page_config(
    page_title="Butik Sihirbazı | Alegorik Ürün İstihbaratı",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ESTETİK OTORİTE (PREMIUM CSS) ---
st.markdown("""
    <style>
    /* GENEL ZEMİN */
    .stApp { background-color: #fbfbfd; color: #1d1d1f; font-family: -apple-system, BlinkMacSystemFont, sans-serif; }
    
    /* SOL MENÜ */
    section[data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #d2d2d7; }
    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 { color: #1d1d1f !important; }

    /* ÜRÜN KARTLARI */
    div[data-testid="column"] {
        background-color: #ffffff; border-radius: 18px; padding: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05); border: 1px solid #f0f0f0;
        transition: all 0.3s ease; text-align: center; height: 100%;
        display: flex; flex-direction: column; justify-content: space-between;
    }
    div[data-testid="column"]:hover { transform: translateY(-5px); box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1); border-color: #d4af37; }

    /* RESİMLER */
    div[data-testid="stImage"] { display: flex; justify-content: center; align-items: center; height: 220px; margin-bottom: 15px; }
    div[data-testid="stImage"] img { max-height: 210px !important; object-fit: contain !important; mix-blend-mode: multiply; }

    /* METİNLER */
    .product-title { font-size: 15px; font-weight: 600; color: #1d1d1f; margin-bottom: 10px; min-height: 40px; display: flex; align-items: center; justify-content: center; line-height: 1.3; }

    /* ARAMA KUTUSU */
    .stTextInput > div > div > input { background-color: #ffffff; color: #1d1d1f; border: 1px solid #d2d2d7; border-radius: 12px; padding: 12px 15px; font-size: 16px; box-shadow: 0 2px 5px rgba(0,0,0,0.02); }
    .stTextInput > div > div > input:focus { border-color: #0071e3; box-shadow: 0 0 0 4px rgba(0,113,227,0.1); }

    /* BUTONLAR */
    .stButton > button { background-color: #f5f5f7; color: #1d1d1f; border: none; border-radius: 20px; padding: 8px 20px; font-weight: 500; width: 100%; transition: all 0.2s; }
    .stButton > button:hover { background-color: #1d1d1f; color: #ffffff; }

    /* DETAY ALANLARI */
    .story-box { background-color: #ffffff; border-left: 4px solid #d4af37; padding: 20px; border-radius: 0 12px 12px 0; box-shadow: 0 4px 12px rgba(0,0,0,0.05); color: #424245; font-style: italic; }
    .allegory-section { background-color: #f5f5f7; padding: 25px; border-radius: 18px; margin-top: 20px; }
    .tag-badge { background-color: #e5e5ea; color: #1d1d1f; padding: 4px 8px; border-radius: 6px; font-size: 11px; margin-right: 5px; display: inline-block; margin-bottom: 5px; }
    
    /* MOBİL MENÜ BUTONU */
    [data-testid="stSidebarCollapsedControl"] {
        background-color: #ffffff; color: #d4af37 !important; border: 2px solid #d4af37;
        border-radius: 50%; width: 50px; height: 50px; transform: scale(1.2);
        margin-top: 10px; margin-left: 10px; box-shadow: 0 4px 10px rgba(212, 175, 55, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. VERİ MOTORU (ZIRHLI MOD: HATA VERMEZ) ---
@st.cache_data
def load_data():
    # Öncelik urunler2.json (Temiz), yoksa urunler.json (Eski)
    files = ['urunler2.json', 'urunler.json']
    
    for file in files:
        if os.path.exists(file):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Boş veya hatalı kayıtları temizle
                    valid_data = []
                    for i, item in enumerate(data):
                        # İsmi olmayan ürünü listeye alma (Çökme sebebi buydu!)
                        if not item.get('name'): 
                            continue
                        item['id'] = i
                        valid_data.append(item)
                    return valid_data
            except:
                continue
    return []

products = load_data()

# --- STATE YÖNETİMİ ---
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

# --- 4. SOL MENÜ ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #1d1d1f; margin-bottom: 5px;'>BUTİK SİHİRBAZI</h2>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; font-style: italic; color: #86868b; font-size: 14px; margin-bottom: 20px;'>“Zarafet göze batmak değil,<br>akılda kalmaktır.”</div>", unsafe_allow_html=True)
    st.markdown("---")
    
    menu = st.radio("Menü", ["🔍 Koleksiyon Ara", "📢 Duyurular", "📞 İletişim"])
    st.markdown("---")
    
    if menu == "📞 İletişim":
        st.info("**Sistem Sorunları ve Geri Bildirim:**\n\n**Palladium Paşabahçe Mağazası**\n\n📩 isdogan@sisecam.com\n📩 palladiummgz@sisecam.com")
    elif menu == "📢 Duyurular":
        st.warning("**BUTİK SİHİRBAZI HAKKINDA**\n\nBu sistem, **Palladium ve Hilltown Paşabahçe Mağazaları** tarafından geliştirilmiştir.\n\n**⚠️ Dipnot:** Yoğunluk sebebiyle aksaklıklar yaşanabilir.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # EMEĞİ GEÇENLER KARTI
    st.markdown("""<div style='background-color: #ffffff; padding: 20px; border-radius: 12px; border: 1px solid #d2d2d7; text-align: center; color: #1d1d1f; box-shadow: 0 4px 6px rgba(0,0,0,0.05);'><div style='font-size: 15px; font-weight: bold; margin-bottom: 5px; color: #000;'>Designed by Umut Doğan</div><div style='font-size: 12px; color: #555; margin-bottom: 15px;'>(Tasarım & Kodlama)</div><div style='border-top: 1px solid #e5e5e5; margin: 10px 20px;'></div><div style='font-size: 13px; font-weight: 700; color: #555; margin-bottom: 8px; letter-spacing: 1px;'>EMEĞİ GEÇENLER</div><div style='font-size: 14px; font-weight: 500; line-height: 1.8; color: #333;'>Adem Keleş<br>Fatih Demir<br>Nuriye Kulaksız</div><div style='border-top: 1px solid #e5e5e5; margin: 15px 20px;'></div><div style='font-size: 12px; font-weight: 700; color: #d4af37;'>Palladium ve Hilltown<br>Mağazaları Ürünüdür.</div></div>""", unsafe_allow_html=True)

# --- 5. ANA EKRAN MANTIĞI ---

def smart_search(query, products):
    if not query: return []
    query = query.lower()
    results = []
    for p in products:
        # HATA KORUMASI: .get() kullanarak veri yoksa boş string alıyoruz
        name = p.get('name', '')
        story = p.get('short_story', '')
        raw = p.get('raw_story', '')
        tags = " ".join(p.get('tags', []))
        allegory = p.get('allegory', '')
        tips = " ".join(p.get('sales_tips', []))
        
        # Tüm metni birleştirip arama yap
        full_text = f"{name} {story} {raw} {tags} {allegory} {tips}".lower()
        
        if query in full_text:
            results.append(p)
    return results

# MOD 1: VİTRİN
if st.session_state.selected_product is None:
    c1, c2, c3 = st.columns([1, 6, 1])
    with c2:
        st.markdown("<h1 style='text-align: center; font-size: 40px;'>Koleksiyonu Keşfet.</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #86868b; font-size: 18px;'>Her hikaye dinlemeye değerdir.</p>", unsafe_allow_html=True)
        search_query = st.text_input("", placeholder="🔍 Duygu, Meslek, Kişi veya Ürün Ara (Örn: Doktor, Aşk, Güç)", label_visibility="collapsed", key="main_search")

    st.markdown("<br>", unsafe_allow_html=True)

    if search_query:
        display_items = smart_search(search_query, products)
        st.markdown(f"### 📂 '{search_query}' için Sonuçlar ({len(display_items)})")
        if len(display_items) == 0: st.warning("😔 Sonuç bulunamadı.")
    else:
        display_items = st.session_state.random_products
        st.markdown("### 🍀 Şanslı Öneriler")

    cols = st.columns(4)
    for idx, p in enumerate(display_items):
        with cols[idx % 4]:
            # Görsel Koruması
            img_url = p.get('image')
            if img_url: 
                st.image(img_url, use_container_width=True)
            else: 
                st.markdown("<div style='height:200px; display:flex; align-items:center; justify-content:center; color:#ccc;'>Görsel Yok</div>", unsafe_allow_html=True)
            
            # İsim Koruması
            prod_name = p.get('name', 'İsimsiz Ürün')
            st.markdown(f"<div class='product-title'>{prod_name}</div>", unsafe_allow_html=True)
            
            tags = p.get('tags', [])[:2]
            tag_html = "".join([f"<span class='tag-badge'>{t}</span>" for t in tags])
            if tag_html: st.markdown(f"<div style='text-align:center; margin-bottom:10px;'>{tag_html}</div>", unsafe_allow_html=True)

            if st.button("İncele", key=f"btn_{p.get('id', idx)}"):
                select_product(p)
                st.rerun()

# MOD 2: DETAY SAYFASI
else:
    p = st.session_state.selected_product
    if st.button("← Koleksiyona Dön", use_container_width=False):
        st.session_state.selected_product = None
        st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    col_left, col_right = st.columns([1, 1.2])

    with col_left:
        st.markdown("""<div style="background: white; padding: 20px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.08);">""", unsafe_allow_html=True)
        img_url = p.get('image')
        if img_url: st.image(img_url, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("### 🏷️ Etiketler")
        tags = p.get('tags', ["Genel"])
        for t in tags: st.markdown(f"<span class='tag-badge' style='font-size:14px; padding:6px 12px;'>#{t}</span>", unsafe_allow_html=True)
        
        if p.get('link'):
            st.markdown("<br>", unsafe_allow_html=True)
            st.link_button("🌐 Resmi Sitede Görüntüle", p['link'], use_container_width=True)

    with col_right:
        st.markdown(f"<h1 style='margin-bottom: 0;'>{p.get('name', 'Ürün')}</h1>", unsafe_allow_html=True)
        if p.get('price'): st.markdown(f"<h3 style='color: #86868b; margin-top: 0;'>{p.get('price')}</h3>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        hikaye = p.get('short_story', p.get('raw_story', '...'))
        st.markdown(f"""<div class="story-box"><span style="font-size: 20px;">❝</span><br>{hikaye}</div>""", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        alegori = p.get('allegory', "Derin anlam yükleniyor...")
        st.markdown(f"""<div class="allegory-section"><h4 style="color: #d4af37; margin-top:0;">👁️ DERİN ANLAM (ALEGORİ)</h4><p style="color: #1d1d1f; font-size: 15px; line-height: 1.6;">{alegori}</p></div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        tips = p.get('sales_tips', ["Özel bir parça.", "Hikayesini anlatın."])
        if isinstance(tips, str): tips = [tips]
        
        with c1: st.success(f"**Hedef Kitle:** {tips[0]}")
        with c2: 
            if len(tips) > 1: st.info(f"**Strateji:** {tips[1]}")
            else: st.info("**Strateji:** Bağ kurun.")

    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; color: #86868b; font-size: 13px;'>Tutku ile yapıldı ❤️</div>", unsafe_allow_html=True)
