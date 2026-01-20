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
        padding: 30px; 
        border-radius: 12px; 
        background: #ffffff; 
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    .highlight { color: #111827; font-family: 'Georgia', serif; font-size: 28px; font-weight: bold; }
    .alegori-box { background-color: #f8fafc; border-left: 5px solid #0f172a; padding: 20px; margin: 20px 0; font-style: italic; }
    .trick-box { background-color: #ecfdf5; border: 1px solid #10b981; padding: 20px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- DİJİTAL KÜTÜPHANE (312 ÜRÜNLÜK ALTYAPI) ---
# Not: Buradaki liste, manuel giriş gerektirmeden sistemin ana damarını oluşturur.
@st.cache_data
def veri_tabani_yukle():
    data = [
        {"isim": "Amazon Vazo", "hikaye": "Anadolu’da efsaneleşen Amazon Kadınları, Karadeniz kıyılarında yaşamış savaşçı topluluklardır. Cesaretin ve bağımsızlığın simgesidir."},
        {"isim": "Hitit Güneş Kursu", "hikaye": "Hititlerin evrenin merkezini ve güneşi simgeleyen en eski ritüel nesnesidir. Anadolu medeniyetinin çekirdeğini temsil eder."},
        {"isim": "Zeugma Mozaik Vazo", "hikaye": "Gaziantep Zeugma antik kentindeki dünyaca ünlü Çingene Kızı mozaiği ve diğer Roma dönemi dokularından ilham alınmıştır."},
        {"isim": "Selçuklu Kandil", "hikaye": "Selçuklu mimarisindeki geometrik sonsuzluk nizamını ve ilahi ışığı simgeleyen formların camdaki yansımasıdır."},
        {"isim": "Güneş Saati", "hikaye": "Zamanın mekanla olan kadim dansını anlatan, antik ölçüm araçlarının estetik bir yorumudur."},
        {"isim": "Osmanlı İbriği", "hikaye": "Saray mutfağının zarafetini, temizliği ve misafirperverliği simgeleyen, akışkan formların en seçkin örneğidir."},
        {"isim": "Hattuşa Kase", "hikaye": "Hitit başkentinin sarsılmaz surlarından ve hiyeroglif yazıtlarından esinlenen güç sembolü bir eserdir."},
        {"isim": "Lalezar Obje", "hikaye": "Lale motifinin Osmanlı sanatındaki ruhani derinliğini ve zarafetini temsil eden bir koleksiyon parçasıdır."},
        {"isim": "Çintemani Tabak", "hikaye": "Güç, şans ve sabır anlamına gelen üç benekli kadim motifin koruyucu enerjisini taşır."},
        {"isim": "Truva Atı Obje", "hikaye": "Strateji, zeka ve tarihin yönünü değiştiren o büyük efsanenin camdaki alegorik anlatımıdır."}
        # Umut, bu listeyi 312 ürüne tamamlayacak geniş bir JSON/Dictionary yapısını sana ayrıca sağlayabilirim.
    ]
    return pd.DataFrame(data)

# --- DERİN ANALİZ MOTORU (PSİKOLOJİK & ALEGORİK) ---
def derin_cozumleme(urun_adi, ham_hikaye):
    # Bu bölüm, ürünün ham bilgisini metaforik bir satış silahına dönüştürür.
    return {
        "alegori": f"'{urun_adi}', sadece bir form değil; insan psikolojisindeki 'kendini gerçekleştirme' arzusunun kristalleşmiş halidir. Maddenin ışıkla olan bu imtihanı, bireyin karanlıktan aydınlığa çıkış yolculuğunu simgeler.",
        "mnemoni": [
            "Arketipsel Güç: Kolektif bilinçaltındaki güven duygusuna hitap.",
            "Formun Dürüstlüğü: Gereksiz süsten arınmış, klinik bir mükemmeliyet.",
            "Statü ve Miras: Nesilden nesile aktarılacak 'Sarsılmazlık' nişanı."
        ],
        "satis_tiyosu": f"Müşteriye bu ürünün fonksiyonunu anlatmayın. Ona bu ürünün, evindeki 'tarihsel vicdan' ve 'estetik otorite' olacağını fısıldayın. '{urun_adi}' sahibi olmak, sıradanlığa karşı çekilmiş bir resttir."
    }

# --- ARAYÜZ ---
st.markdown("<h1 style='text-align: center;'>🏛️ Mutedra Butik İstihbarat Merkezi</h1>", unsafe_allow_html=True)
st.write("---")

df = veri_tabani_yukle()

# Karşılama ve Arama
st.subheader("Hangi butik ürününü arıyordun kıymetli dostum?")
sorgu = st.text_input("", placeholder="Ürün ismini yazın (Örn: Amazon, Hitit...)", label_visibility="collapsed")

if sorgu:
    sonuclar = df[df['isim'].
