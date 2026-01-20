import streamlit as st
import requests
from bs4 import BeautifulSoup
import time

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Mutedra Butik Rehberi", layout="centered")

# --- CSS: ŞIK VE MODERN GÖRÜNÜM ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .product-box { border: 1px solid #e0e0e0; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
    .title-text { color: #1a1a1a; font-family: 'Georgia', serif; }
    .sales-trick { background-color: #f9f9f9; border-left: 5px solid #2ecc71; padding: 10px; font-style: italic; }
    </style>
    """, unsafe_allow_html=True)

# --- VERİ KAZIMA FONKSİYONU ---
@st.cache_data # Veriyi bir kez çeker, hafızaya alır.
def verileri_getir():
    url = "https://www.pasabahcemagazalari.com/butik-koleksiyonlar/"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Paşabahçe'nin butik ürünlerini bulmaya yönelik genel mantık
        urunler = []
        items = soup.find_all('div', class_='product-item') # Sitenin yapısına göre güncellenir
        
        # Eğer site yapısı değişmişse boş dönmemesi için örnek veri seti
        if not items:
            return [
                {"isim": "Amazon Vazo", "ozet": "Anadolu'nun savaşçı kadınlarından ilham alan koleksiyon."},
                {"isim": "Zeugma Mozaik Tabak", "ozet": "Antik kentin tarihsel dokusunu yansıtan eser."},
                {"isim": "Selçuklu Kandil", "ozet": "Geometrik desenlerin ruhani ışığı."}
            ]
            
        for item in items:
            name = item.find('h3').text.strip() if item.find('h3') else "İsimsiz Eser"
            urunler.append({"isim": name, "ozet": "Butik Koleksiyonun Seçkin Parçası"})
        return urunler
    except:
        return [{"isim": "Bağlantı Hatası", "ozet": "Siteye erişilemedi, lütfen internetinizi kontrol edin."}]

# --- ALEGORİK ANALİZ MOTORU (API'SIZ SİMÜLASYON) ---
def analiz_uret(urun_adi):
    # Bu kısım, API'n yoksa "Klinik ve Alegorik" bir taslak oluşturur.
    # Eğer Gemini API alırsan buraya o mantığı bağlayabiliriz.
    return {
        "alegori": f"{urun_adi}, insan ruhunun zaman karşısındaki direncinin bir metaforudur. Tıpkı camın ateşte pişmesi gibi, bu eser de tarihsel hafızanın estetik bir tezahürüdür.",
        "mnemoni": [
            "Zamansız tasarım: Geçmişin izini geleceğe taşır.",
            "Ustalık: El işçiliğinin teknik mükemmeliyeti.",
            "Sembolizm: Her desende kadim bir hikaye gizli."
        ],
        "satis_tiyosu": f"Müşteriye bu ürünün sadece bir nesne değil, bir 'miras' olduğu vurgulanmalı. '{urun_adi}' sahibi olmanın, kültürel bir sermaye edinmek olduğu klinik bir dille anlatılmalıdır."
    }

# --- ARAYÜZ ---
st.markdown("<h1 class='title-text'>🏛️ Mutedra Butik Rehberi</h1>", unsafe_allow_html=True)

# Karşılama
st.subheader("Hangi butik ürününü arıyordun kıymetli dostum?")

# Veriyi Yükle
veriler = verileri_getir()

# Arama Kutusu
search_query = st.text_input("", placeholder="Ürün adını yazın... (Örn: Amazon)", label_visibility="collapsed")

if search_query:
    # Arama sonuçlarını filtrele
    sonuclar = [u for u in veriler if search_query.lower() in u['isim'].lower()]
    
    if sonuclar:
        for urun in sonuclar:
            analiz = analiz_uret(urun['isim'])
            
            with st.container():
                st.markdown(f"### 🏺 {urun['isim']}")
                st.write(f"**Kısa Bilgi:** {urun['ozet']}")
                
                # Alegori
                st.markdown("#### 📖 Derin Alegori ve Ruhsal İzlem")
                st.write(analiz['alegori'])
                
                # Maddeler
                st.markdown("#### 🧠 Hafıza Çivileri (Mnemoni)")
                for m in analiz['mnemoni']:
                    st.write(f"* {m}")
                
                # Satış Tiyosu
                st.markdown("<div class='sales-trick'>", unsafe_allow_html=True)
                st.markdown("#### 💰 Satış Tiyosu")
                st.write(analiz['satis_tiyosu'])
                st.markdown("</div>", unsafe_allow_html=True)
                
                st.divider()
    else:
        st.warning("Aradığınız kriterde bir ürün bulunamadı.")
else:
    st.info(f"Şu anda butik koleksiyondaki ürünler taranmaya hazır. (Toplam: {len(veriler)} potansiyel ürün)")
