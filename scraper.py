import asyncio
import json
from playwright.async_api import async_playwright
import random

# Mutedra Veri Toplama Protokolü
async def scrape_pasabahce():
    print("Mutedra Scraper Başlatılıyor... Hedef: Mutlak Veri.")
    products = []
    
    async with async_playwright() as p:
        # Tarayıcıyı görünür modda aç (headless=False) ki Cloudflare bizi robot sanmasın
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        )
        
        page = await context.new_page()
        
        # Paşabahçe Butik Sayfası
        base_url = "https://www.pasabahcemagazalari.com/butik-koleksiyonlar"
        print(f"Bağlanılıyor: {base_url}")
        
        try:
            await page.goto(base_url, timeout=60000)
            await page.wait_for_timeout(5000) # Sayfanın yüklenmesi için bekle
            
            # İlk 20 ürünü çek (Örneklem)
            items = await page.query_selector_all('.product-item')
            print(f"{len(items)} adet ham veri tespit edildi.")

            for i, item in enumerate(items[:10]): # Test için ilk 10 ürünle sınırlandırıldı
                try:
                    name_el = await item.query_selector('.product-name a')
                    price_el = await item.query_selector('.price')
                    img_el = await item.query_selector('.product-image-photo')
                    link_el = await item.query_selector('.product-item-link')

                    name = await name_el.inner_text() if name_el else "Bilinmeyen Obje"
                    price = await price_el.inner_text() if price_el else "Değer Biçilemedi"
                    img = await img_el.get_attribute('src') if img_el else ""
                    link = await link_el.get_attribute('href') if link_el else ""

                    products.append({
                        "id": i,
                        "name": name.strip(),
                        "price": price.strip(),
                        "image": img,
                        "link": link,
                        # Buraya yapay zeka analizi için ham metin eklenecek
                        "raw_story": f"{name} isimli Paşabahçe butik ürünü. Fiyat: {price}." 
                    })
                    print(f"✓ İşlendi: {name}")
                except Exception as e:
                    print(f"X Hata: {e}")

        except Exception as e:
            print(f"Kritik Hata: {e}")
        
        await browser.close()
    
    # Veriyi JSON olarak kaydet
    with open('urunler.json', 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=2)
    print("Veri kalıcılığı sağlandı: urunler.json oluşturuldu.")

if __name__ == "__main__":
    asyncio.run(scrape_pasabahce())
