import streamlit as st
import pandas as pd

# --- KONFİGÜRASYON ---
st.set_page_config(page_title="Mutedra Butik İstihbarat Merkezi", layout="wide")

# Klinik ve Seçkin Görünüm
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .product-card { 
        border: 1px solid #e5e7eb; 
        padding: 25px; 
        border-radius: 15px; 
        background: #ffffff; 
        margin-bottom: 25px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .highlight { color: #111827; font-family: 'Georgia', serif; font-size: 26px; }
    .alegori-box { background-color: #f8fafc; border-left: 4px solid #1e293b; padding: 15px; margin: 15px 0; }
    .trick-box { background-color: #f0fdf4; border: 1px solid #dcfce7; padding: 15px; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# --- VERİ MERKEZİ (312 ÜRÜN KAPASİTELİ) ---
@st.cache_data
def veri_yukle():
    """
    Mutlak Doğru: Veriyi bir kez dışarıdan (CSV) al veya dahili listeyi kullan.
    """
    try:
        # Eğer 'butik_urunler.csv' dosyan varsa onu okur
        df = pd.read_csv("butik_urunler.csv")
    except FileNotFoundError:
        # CSV yoksa, sistemi test etmek için genişletilmiş liste
        # Burayı 312 ürüne kadar manuel veya bir script ile doldurabilirsin.
        data = {
            "isim": [
                "Amazon Vazo", "Hitit Güneş Kursu", "Zeugma Mozaik", 
                "Selçuklu Kandil", "Osmanlı İbriği", "Güneş Saati", 
                "Anadolu Medeniyetleri Serisi", "Lalezar Kase"
            ],
            "hikaye": [
                "Anadolu'nun savaşçı kadınları Amazonlar...",
                "Hitit evren tasarımı ve dinsel ritüel nesnesi...",
                "Antik kentin ruhunu taşıyan mozaik dokusu...",
                "Geometrik mükemmeliyetin Selçuklu yorumu...",
                "Saray estetiğinin su ile buluştuğu form...",
                "Zamanın mekanla dansı...",
                "Binlerce yıllık kültürel mirasın sentezi...",
                "Lale motifinin camdaki zarafeti..."
            ]
        }
        df = pd.DataFrame(data)
    return df

# --- ANALİZ MOTORU ---
def derin_analiz(urun_adi):
    # Bu fonksiyon, ürün ismini metaforik ve psikolojik bir süzgeçten geçirir.
    return {
        "alegori": f"'{urun_adi}', zamansızlığın bir tezahürüdür. İnsan zihnindeki 'kalıcılık' arzusunun, camın kırılganlığıyla kurduğu paradoksal bir dengedir.",
        "mnemoni": [
            "Arketipsel Bağ: İnsanlık tarihinin ortak hafızasına hitap.",
            "Formun Dürüstlüğü: Gereksiz süsten arınmış bir estetik.",
            "Kolektif Miras: Bireysel mülkiyetin ötesinde bir değer."
        ],
        "satis_tiyosu": "Müşteriye bu ürünün bir 'eşya' değil, bir 'felsefi duruş' olduğunu anlatın. Sahip olmak değil, bu hikayenin bir parçası olmak vurgulanmalıdır."
    }

# --- ARAYÜZ ---
st.markdown("<h1 style='text-align: center;'>🏛️ Mutedra Butik İstihbarat Merkezi</h1>", unsafe_allow_html=True)
st.write("---")

df = veri_yukle()

# Kullanıcı Etkileşimi
st.subheader("Hangi butik ürününü arıyordun Umut dostum?")
sorgu = st.text_input("", placeholder="Örn: Amazon, Zeugma...", label_visibility="collapsed")

if sorgu:
    sonuclar = df[df['isim'].str.contains(sorgu, case=False, na=False)]
    
    if not sonuclar.empty:
        for _, row in sonuclar.iterrows():
            analiz = derin_analiz(row['isim'])
            with st.container():
                st.markdown(f"""
                <div class="product-card">
                    <div class="highlight">🏺 {row['isim']}</div>
                    <p><strong>Arka Plan:</strong> {row['hikaye']}</p>
                    <div class="alegori-box">
                        <strong>📖 Derin Alegori:</strong><br>{analiz['alegori']}
                    </div>
                    <strong>🧠 Hafıza Çivileri (Mnemoni):</strong>
                    <ul>{''.join([f'<li>{m}</li>' for m in analiz['mnemoni']])}</ul>
                    <div class="trick-box">
                        <strong>💰 Satış Tiyosu (Klinik Yaklaşım):</strong><br>{analiz['satis_tiyosu']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("Eşleşen ürün bulunamadı. Lütfen veri tabanını güncelleyin.")
else:
    st.info(f"Sistemde şu an analiz edilmeye hazır {len(df)} ürün bulunuyor.")
