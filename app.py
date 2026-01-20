import streamlit as st
from curl_cffi import requests # Standart requests yerine bunu kullanıyoruz
from bs4 import BeautifulSoup
import pandas as pd
import time

def bariyer_asan_kaziyici():
    # Chrome'un güncel imzasını taklit et (impersonate="chrome120")
    base_url = "https://www.pasabahcemagazalari.com/butik-koleksiyonlar/"
    butun_veriler = []
    
    # Klinik müdahale: İlk 5 sayfayı örnek olarak tarayalım
    for sayfa in range(1, 17): 
        url = f"{base_url}?pg={sayfa}"
        try:
            # impersonate parametresi burada kilit noktadır
            response = requests.get(url, impersonate="chrome120", timeout=30)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                items = soup.find_all('div', class_='product-item')
                
                for item in items:
                    name = item.find('h3').text.strip() if item.find('h3') else None
                    if name:
                        butun_veriler.append({"isim": name, "hikaye": "Butik Koleksiyon Eseri"})
                
                time.sleep(2) # Antropolojik bekleme: İnsan hızı simülasyonu
            else:
                st.error(f"Sayfa {sayfa} erişim reddedildi: Durum Kodu {response.status_code}")
                break
        except Exception as e:
            st.error(f"Teknik hata: {e}")
            break
            
    return pd.DataFrame(butun_veriler)

# Streamlit Arayüzü
if st.button("Sistem Engelini Aş ve 312 Ürünü Çek"):
    with st.spinner("Site koruması analiz ediliyor ve bypass ediliyor..."):
        df = bariyer_asan_kaziyici()
        if not df.empty:
            st.session_state['data'] = df
            st.success(f"Analiz Tamam! {len(df)} ürün başarıyla dijital hafızaya alındı.")
