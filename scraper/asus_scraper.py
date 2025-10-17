"""
ASUS Shop Deal Scraper
======================
Script para extraer productos y precios de ASUS Shop US

Instalación:
pip install playwright requests
playwright install chromium

Uso:
python asus_scraper.py

El script generará un archivo 'products.json' que puedes importar en el dashboard.
"""

import json
import time
from datetime import datetime
from playwright.sync_api import sync_playwright
import uuid

# Configuración
ASUS_URL = "https://shop.asus.com/us/all-in-one-pcs"
OUTPUT_FILE = "products.json"
TELEGRAM_BOT_TOKEN = ""  # Opcional: tu bot token de Telegram
TELEGRAM_CHAT_ID = ""     # Opcional: tu chat ID

def send_telegram_notification(product):
    """Envía notificación a Telegram para ofertas espectaculares"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID or not product.get('isSpectacularDeal'):
        return
    
    try:
        import requests
        message = f"""
🔥 ¡OFERTA ESPECTACULAR DETECTADA! 🔥

📦 {product['name']}
💰 Precio: ${product['currentPrice']}
{'🏷️ Antes: $' + str(product['originalPrice']) if product['originalPrice'] else ''}
📉 Descuento: {product['discount']}%
🔗 {product['url']}
        """.strip()
        
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        requests.post(url, json={
            'chat_id': TELEGRAM_CHAT_ID,
            'text': message,
            'parse_mode': 'HTML'
        })
        print(f"✓ Notificación enviada para: {product['name']}")
    except Exception as e:
        print(f"✗ Error enviando notificación: {e}")

def calculate_discount(current, original):
    """Calcula el porcentaje de descuento"""
    if not original or original <= current:
        return 0
    return round(((original - current) / original) * 100, 2)

def scrape_asus_products():
    """Extrae productos de ASUS Shop"""
    products = []
    
    print(f"🔍 Iniciando scraping de {ASUS_URL}")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            print("📡 Cargando página...")
            page.goto(ASUS_URL, wait_until='networkidle', timeout=60000)
            
            # Esperar a que los productos se carguen
            time.sleep(3)
            
            # Scroll para cargar lazy-loaded content
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(2)
            
            print("🔎 Extrayendo productos...")
            
            # Selector de productos (ajustar según la estructura real)
            product_cards = page.query_selector_all('.product-item, [data-testid="product-card"], .product-card')
            
            if not product_cards:
                print("⚠️ No se encontraron productos. Ajusta los selectores.")
                # Fallback: intentar con otros selectores comunes
                product_cards = page.query_selector_all('article, .card, .item')
            
            print(f"📦 Encontrados {len(product_cards)} elementos")
            
            for card in product_cards:
                try:
                    # Extraer nombre
                    name_elem = card.query_selector('h2, h3, .product-name, [class*="title"], a[class*="name"]')
                    if not name_elem:
                        continue
                    
                    name = name_elem.inner_text().strip()
                    
                    # Extraer URL
                    link_elem = card.query_selector('a')
                    url = link_elem.get_attribute('href') if link_elem else ASUS_URL
                    if url and not url.startswith('http'):
                        url = f"https://shop.asus.com{url}"
                    
                    # Extraer precios
                    price_text = card.query_selector('[class*="price"], .price, [class*="cost"]')
                    if not price_text:
                        continue
                    
                    price_html = card.inner_html()
                    
                    # Buscar precio actual
                    current_price = None
                    original_price = None
                    
                    # Extraer números de precios
                    import re
                    prices = re.findall(r'\$\s*(\d+(?:,\d{3})*(?:\.\d{2})?)', price_html)
                    prices = [float(p.replace(',', '')) for p in prices]
                    
                    if len(prices) >= 2:
                        # Hay descuento: precio actual (menor) y original (mayor)
                        current_price = min(prices)
                        original_price = max(prices)
                    elif len(prices) == 1:
                        current_price = prices[0]
                    
                    if not current_price:
                        continue
                    
                    discount = calculate_discount(current_price, original_price)
                    is_spectacular = discount >= 60
                    
                    product = {
                        'id': str(uuid.uuid4()),
                        'name': name,
                        'url': url,
                        'currentPrice': current_price,
                        'originalPrice': original_price,
                        'discount': discount,
                        'isSpectacularDeal': is_spectacular,
                        'lastUpdated': datetime.now().isoformat(),
                        'priceHistory': [
                            {
                                'price': current_price,
                                'date': datetime.now().isoformat()
                            }
                        ]
                    }
                    
                    products.append(product)
                    print(f"✓ {name} - ${current_price}" + (f" ({discount}% OFF)" if discount > 0 else ""))
                    
                    # Enviar notificación si es oferta espectacular
                    if is_spectacular:
                        send_telegram_notification(product)
                    
                except Exception as e:
                    print(f"✗ Error procesando producto: {e}")
                    continue
            
        except Exception as e:
            print(f"❌ Error durante el scraping: {e}")
        finally:
            browser.close()
    
    return products

def save_products(products):
    """Guarda productos en JSON"""
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(products, f, indent=2, ensure_ascii=False)
        print(f"\n✅ Guardados {len(products)} productos en {OUTPUT_FILE}")
        print(f"📁 Importa este archivo en el dashboard de ASUS Deal Hound")
    except Exception as e:
        print(f"❌ Error guardando archivo: {e}")

def main():
    print("=" * 50)
    print("🐕 ASUS Deal Hound - Scraper")
    print("=" * 50)
    
    # Configurar Telegram (opcional)
    if not TELEGRAM_BOT_TOKEN:
        print("\n⚠️ Telegram no configurado. Edita el script para añadir:")
        print("   TELEGRAM_BOT_TOKEN = 'tu_token'")
        print("   TELEGRAM_CHAT_ID = 'tu_chat_id'")
    
    products = scrape_asus_products()
    
    if products:
        save_products(products)
        
        # Estadísticas
        spectacular = sum(1 for p in products if p['isSpectacularDeal'])
        avg_discount = sum(p['discount'] for p in products) / len(products) if products else 0
        
        print(f"\n📊 Estadísticas:")
        print(f"   Total de productos: {len(products)}")
        print(f"   Ofertas espectaculares (>60%): {spectacular}")
        print(f"   Descuento promedio: {avg_discount:.2f}%")
    else:
        print("\n⚠️ No se encontraron productos.")
        print("💡 Consejo: Revisa los selectores CSS en el código")

if __name__ == "__main__":
    main()
