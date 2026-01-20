import streamlit as st
import pandas as pd

# --- KONFİGÜRASYON ---
st.set_page_config(page_title="Mutedra: Butik İstihbarat Merkezi", layout="wide")

# Klinik ve Seçkin Görünüm Ayarları
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .product-card { 
        border: 1px solid #e0e0e0; 
        padding: 25px; 
        border-radius: 12px; 
        background: #ffffff; 
        margin-bottom: 20px;
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
    }
    .highlight { color: #111827; font-size: 24px; font-weight: 800; }
    .alegori-section { color: #374151; font-style: italic; border-left: 4px solid #111827; padding-left: 15px; margin: 15px 0; }
    .trick-box { background-color: #f9fafb; border: 1px dashed #d1d5db; padding: 15px; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# --- VERİ YÜKLEME (GÜVENLİ LİMAN) ---
@st.cache_data
def veri_hazirla():
    # Burası senin 312 ürünlük veri tabanın. 
    # Gerçek kullanımda 'pasabahce_urunler.csv' dosyasından okunacaktır.
    try:
        df = pd.read_csv("butik_urunler.csv")
    except FileNotFoundError:
        # Eğer CSV yoksa, test için manuel bir veri seti (Örnek)
        data = {
            "isim": ["Amazon Vazo", "Hitit Güneş Kursu", "Zeugma Mozaik", "Selçuklu Kandil", "Osmanlı İbriği"],
            "hikaye": [
                "Anadolu’da efsaneleşen Amazon Kadınları, savaşçı kadın topluluklarıdır.",
                "Hititlerin evreni simgeleyen en önemli dinsel objesidir.",
                "Gaziantep Zeugma antik kentinden çıkan dünya mirası mozaikler.",
                "Selçuklu mimarisinin geometrik nizamını yansıtan aydınlatma.",
                "Saray mutfağının ve zarafetinin simgesi olan form."
            ]
        }
        df = pd.DataFrame(data)
    return df

# --- DERİN ANALİZ MOTORU ---
def derin_cozumleme(urun_adi, ham_hikaye):
    # Bu fonksiyon, ürün isminden yola çıkarak alegorik ve satış odaklı veriyi kurgular.
    # Klinik ve rasyonel bir derinlik katar.
    return {
        "alegori": f"'{urun_adi}', formun maddeleşmiş iradesidir. İnsan psikolojisindeki 'kendini gerçekleştirme' ihtiyacının tarihsel bir iz düşümü olarak okunmalıdır.",
        "mnemoni": [
            "Arketiplerle Bağlantı: Kolektif bilinçaltına hitap eden form.",
            "Malzeme Dürüstlüğü: Camın en saf, en dürüst hali.",
            "Tarihsel Süreklilik: Geçmişle kurulan kopmaz bir bağ."
        ],
        "satis_tiyosu": f"Müşteriye bu ürünün bir 'satın alma' değil, bir 'aktarım' (transfer of legacy) olduğunu hissettirin. '{urun_adi}' sahibi olmak, zamanın ötesinde bir duruş sergilemektir."
    }

# --- ARAYÜZ TASARIMI ---
st.markdown("<h1 style='text-align: center; color: #111827;'>🏛️ Mutedra Butik İstihbarat Merkezi</h1>", unsafe_allow_html=True)
st.write("---")

df = veri_hazirla()

# Karşılama ve Arama
st.subheader("Hangi butik ürününü arıyordun Umut dostum?")
sorgu = st.text_input("", placeholder="Ürün ismini yazın...", label_visibility="collapsed")

if sorgu:
    sonuclar = df[df['isim'].str.contains(sorgu, case=False, na=False)]
    
    if not sonuclar.empty:
        for _, row in sonuclar.iterrows():
            analiz = derin_cozumleme(row['isim'], row['hikaye'])
            with st.container():
                st.markdown(f"""
                <div class="product-card">
                    <div class="highlight">🏺 {row['isim']}</div>
                    <p style="margin-top:10px;"><strong>Orijinal Arka Plan:</strong> {row['hikaye']}</p>
                    <div class="alegori-section">
                        <strong>📖 Derin Alegori:</strong><br>
                        {analiz['alegori']}
                    </div>
                    <div style="margin: 15px 0;">
                        <strong>🧠 Hafıza Çivileri:</strong>
                        <ul>{''.join([f'<li>{m}</li>' for m in analiz['mnemoni']])}</ul>
                    </div>
                    <div class="trick-box">
                        <strong>💰 Satış Tiyosu (Klinik Yaklaşım):</strong><br>
                        {analiz['satis_tiyosu']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("Eşleşen ürün bulunamadı. Lütfen veri tabanını kontrol edin.")
else:
    st.info(f"Sistemde şu an {len(df)} ürün analiz edilmeye hazır bekliyor.")
