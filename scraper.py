"""
Paşabahçe Butik Koleksiyonlar - Cloudflare Bypass Scraper
Playwright ile tam tarayıcı simülasyonu kullanarak 312 ürünü tarar
"""

import asyncio
import csv
import json
from playwright.async_api import async_playwright
from datetime import datetime
import re

class PasabahceScraper:
    def __init__(self):
        self.base_url = "https://www.pasabahcemagazalari.com/butik-koleksiyonlar"
        self.products = []
        
    async def scrape_all_products(self):
        """Tüm ürünleri tarar ve CSV'ye kaydeder"""
        async with async_playwright() as p:
            # Chromium başlat (daha az şüpheli)
            browser = await p.chromium.launch(
                headless=False,  # Debug için False, production'da True
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-dev-shm-usage',
                    '--no-sandbox'
                ]
            )
            
            # Stealth ayarları
            context = await browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                viewport={'width': 1920, 'height': 1080},
                locale='tr-TR',
                timezone_id='Europe/Istanbul'
            )
            
            # JavaScript ile automation flag'i gizle
            await context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """)
            
            page = await context.new_page()
            
            print("🚀 Scraping başlatılıyor...")
            
            page_num = 1
            while True:
                url = f"{self.base_url}?p={page_num}"
                print(f"\n📄 Sayfa {page_num} taranıyor: {url}")
                
                try:
                    await page.goto(url, wait_until='networkidle', timeout=60000)
                    
                    # Cloudflare challenge bekle
                    await asyncio.sleep(3)
                    
                    # Ürün kartlarını bul
                    products = await page.query_selector_all('.product-item')
                    
                    if not products:
                        print(f"✅ Sayfa {page_num-1}'de tarama tamamlandı!")
                        break
                    
                    print(f"   🔍 {len(products)} ürün bulundu")
                    
                    for product in products:
                        try:
                            # Ürün adı
                            name_elem = await product.query_selector('.product-name')
                            name = await name_elem.inner_text() if name_elem else "İsimsiz Ürün"
                            
                            # Ürün linki
                            link_elem = await product.query_selector('a.product-item-link')
                            link = await link_elem.get_attribute('href') if link_elem else ""
                            
                            # Ürün resmi
                            img_elem = await product.query_selector('img.product-image-photo')
                            img = await img_elem.get_attribute('src') if img_elem else ""
                            
                            # Fiyat
                            price_elem = await product.query_selector('.price')
                            price = await price_elem.inner_text() if price_elem else "N/A"
                            
                            self.products.append({
                                'name': name.strip(),
                                'url': link,
                                'image': img,
                                'price': price.strip(),
                                'page': page_num
                            })
                            
                            print(f"      ✓ {name.strip()}")
                            
                        except Exception as e:
                            print(f"      ⚠️ Ürün parse hatası: {e}")
                            continue
                    
                    page_num += 1
                    await asyncio.sleep(2)  # Rate limiting
                    
                except Exception as e:
                    print(f"❌ Sayfa hatası: {e}")
                    break
            
            await browser.close()
            
        return self.products
    
    async def scrape_product_details(self, product_url: str):
        """Tekil ürün sayfasından detaylı hikaye çeker"""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
            page = await context.new_page()
            
            try:
                await page.goto(product_url, wait_until='networkidle', timeout=30000)
                
                # Ürün açıklaması/hikayesi
                story_selectors = [
                    '.product-description',
                    '.product-info-main',
                    '[itemprop="description"]',
                    '.product-attribute'
                ]
                
                story = ""
                for selector in story_selectors:
                    elem = await page.query_selector(selector)
                    if elem:
                        story = await elem.inner_text()
                        break
                
                await browser.close()
                return story.strip() if story else "Hikaye bulunamadı"
                
            except Exception as e:
                await browser.close()
                return f"Hata: {e}"
    
    def save_to_csv(self, filename='pasabahce_products.csv'):
        """Ürünleri CSV'ye kaydet"""
        if not self.products:
            print("⚠️ Kaydedilecek ürün yok!")
            return
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['name', 'url', 'image', 'price', 'page'])
            writer.writeheader()
            writer.writerows(self.products)
        
        print(f"\n💾 {len(self.products)} ürün '{filename}' dosyasına kaydedildi!")
    
    def save_to_json(self, filename='pasabahce_products.json'):
        """Ürünleri JSON'a kaydet"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.products, f, ensure_ascii=False, indent=2)
        
        print(f"💾 {len(self.products)} ürün '{filename}' dosyasına kaydedildi!")


# Kullanım
async def main():
    scraper = PasabahceScraper()
    
    # Tüm ürünleri tara
    products = await scraper.scrape_all_products()
    
    # Kaydet
    scraper.save_to_csv()
    scraper.save_to_json()
    
    # İsteğe bağlı: İlk 5 ürünün detayını çek
    print("\n🔎 İlk 5 ürünün detayları çekiliyor...")
    for product in products[:5]:
        if product['url']:
            story = await scraper.scrape_product_details(product['url'])
            product['story'] = story
            print(f"\n📖 {product['name']}")
            print(f"   {story[:200]}...")
    
    # Güncellenmiş veriyi kaydet
    scraper.save_to_json('pasabahce_detailed.json')

if __name__ == "__main__":
    # Playwright kurulumu için:
    # pip install playwright
    # playwright install chromium
    
    asyncio.run(main())
