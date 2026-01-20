import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# --- KONFİGÜRASYON ---
st.set_page_config(page_title="Mutedra: Butik Veri Merkezi", layout="wide")

# Klinik ve Seçkin Görünüm Ayarları
st.markdown("""
    <style>
    .stApp { background-color: #fafafa; }
    .product-card { 
        border: 1px solid #d1d1d1; 
        padding: 20px; 
        border-radius: 10px; 
        background: white; 
        margin-bottom: 15px;
        box-shadow: 3px 3px 10px rgba(0,0,0,0.05);
    }
    .highlight { color: #1a1a1a; font-weight: bold; font-family: 'Georgia', serif; }
    .trick-box { background-color: #f0fdf4; border-left: 5px solid #22c55e; padding: 15px; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- VERİ KAZIMA MOTORU ---
def urunleri_getir():
    """
    Hedef sitedeki ürünleri tarar. Kurumsal engelleri aşmak için 
    User-Agent ve bekleme süreleri optimize edilmiştir.
    """
    base_url = "https://www.pasabahcemagazalari.com/butik-koleksiyonlar/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    urun_listesi = []
    
    try:
        #
