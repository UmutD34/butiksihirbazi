import streamlit as st
import json
import time
import random

# --- Yapılandırma ---
st.set_page_config(
    page_title="Mutedra Alegorik Analizör",
    page_icon="⚱️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS Stil Manipülasyonu (Estetik Otorite) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    .block-container {
        padding-top: 2rem;
    }
    h1, h2, h3 {
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 300;
        letter-spacing: 0.1em;
    }
    .allegory-box {
        background-color: #1e2130;
        border-left: 4px solid #d4af37;
        padding: 20px;
        margin: 10px 0;
        border-radius: 5px;
    }
    .highlight {
        color: #d4af37; /* Altın sarısı */
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- Veri Yükleme ---
def load_data():
    try:
        with open('urunler.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# --- AI Simülasyon Motoru (API Yerine Geçici Mantık) ---
def generate_analysis(product_name):
    """
    Claude API entegrasyonu yapılana kadar, beklenen çıktı formatını
    simüle eden deterministik fonksiyon.
    """
    
    # Gerçek API buraya bağlanacak. Şimdilik Mutedra felsefesini simüle ediyoruz.
    allegories = [
        f"{product_name}, maddenin kristalleşmiş iradesidir. Camın şeffaflığı, hakikatin gizlenemez doğasına bir atıftır.",
        f"{product_name}, boşluğun (void) madde ile çevrelenmiş halidir. Kullanıcısına sahip olmayı değil, muhafaza etmeyi öğretir.",
        f"Zamanın akışına direnen bir form: {product_name}. Kırılganlığı, insan ruhunun hassasiyetiyle analojik bir bağ kurar."
    ]
    
    sales_tactics = [
        "Müşteride 'seçkinlik' algısını tetikleyin (Veblen Etkisi).",
        "Ürünü bir 'ihtiyaç' değil, bir 'kimlik uzantısı' olarak konumlandırın.",
        "Kıtlık prensibini vurgulayın: Bu bir üretim değil, bir yaratımdır."
    ]
    
    return {
        "allegory": random.choice(allegories),
        "mnemonics": [f"{product_name} = Statü", "Şeffaflık = Dürüstlük", "Ağırlık = Gerçeklik"],
        "sales_tip": random.choice(sales_tactics)
    }

# --- Arayüz Mimarisi ---

# Başlık
st.title("⚱️ Mutedra: Alegorik Ürün İstihbaratı")
st.markdown("*\"Mutlak Doğru, nesnenin görünen yüzeyinin ötesindedir.\"*")
st.divider()

# Veri Kontrolü
products = load_data()

if not products:
    st.error("Veri bulunamadı! Önce 'scraper.py' dosyasını çalıştırarak veritabanını oluşturun.")
    st.info("Terminal Komutu: python scraper.py")
else:
    # Arama Çubuğu
    search_term = st.text_input("Ürün Veritabanında Ara:", placeholder="Örn: Vazo, Kase, Gondol...")

    # Filtreleme
    filtered_products = [p for p in products if search_term.lower() in p['name'].lower()]

    if search_term:
        st.write(f"Tespit edilen varlık sayısı: {len(filtered_products)}")
        
        for p in filtered_products:
            with st.container():
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    if p['image']:
                        st.image(p['image'], use_column_width=True)
                    else:
                        st.markdown("👻 *Görsel veri yok*")
                    
                    st.caption(f"Fiyat Endeksi: {p['price']}")
                    st.link_button("Kaynağa Git", p['link'])

                with col2:
                    st.subheader(p['name'])
                    
                    if st.button(f"Analiz Et: {p['name']}", key=p['id']):
                        with st.spinner('Mutedra Nöral Ağları çalışıyor...'):
                            time.sleep(1.5) # İşlem ağırlığı hissi
                            analysis = generate_analysis(p['name'])
                            
                            st.markdown("### 👁️ Derin Alegori")
                            st.markdown(f"""
                            <div class="allegory-box">
                                {analysis['allegory']}
                            </div>
                            """, unsafe_allow_html=True)
                            
                            c1, c2 = st.columns(2)
                            with c1:
                                st.markdown("#### 🧠 Hafıza Çivileri (Mnemoni)")
                                for m in analysis['mnemonics']:
                                    st.markdown(f"- {m}")
                            
                            with c2:
                                st.markdown("#### 📈 Klinik Satış Stratejisi")
                                st.info(analysis['sales_tip'])
                
                st.divider()

# Footer
st.markdown("---")
st.caption("Mutedra © 2026 | Sarsılmazlık İlkesi ile kodlanmıştır. | Developer: Umut")
