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
import re

# --- 1. URL ACTUALIZADA ---
ASUS_URL = "https://www.asus.com/us/deals/displays-desktops/"
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
            time.sleep(5) # Aumentamos un poco la espera por si acaso
            
            # Scroll para cargar lazy-loaded content
            print("📜 Haciendo scroll para cargar todos los productos...")
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(3)
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(2)
            
            print("🔎 Extrayendo productos...")
            
            # --- 2. NUEVOS SELECTORES ---
            # Selector principal para cada tarjeta de producto
            product_cards = page.query_selector_all('[class*="ProductCardNormalGrid__productCardContainer__"]')
            
            if not product_cards:
                print("⚠️ No se encontraron productos. La estructura de la web puede haber cambiado.")
            
            print(f"📦 Encontrados {len(product_cards)} elementos")
            
            for card in product_cards:
                try:
                    # Selector para el nombre
                    name_elem = card.query_selector('h2')
                    if not name_elem:
                        continue
                    
                    name = name_elem.inner_html().replace('<br>', ' ').strip()
                    
                    # Selector para la URL (el primer enlace dentro de la tarjeta)
                    link_elem = card.query_selector('a')
                    url = link_elem.get_attribute('href') if link_elem else ASUS_URL
                    if url and not url.startswith('http'):
                        base_url = "https://www.asus.com" if "asus.com" in ASUS_URL else "https://shop.asus.com"
                        url = f"{base_url}{url}"

                    # Selectores para los precios
                    current_price_elem = card.query_selector('[class*="ProductCardNormalGrid__priceDiscount__"]')
                    original_price_elem = card.query_selector('.regularPrice')

                    current_price_text = current_price_elem.inner_text().strip() if current_price_elem else None
                    original_price_text = original_price_elem.inner_text().strip() if original_price_elem else None

                    if not current_price_text:
                        continue

                    # Extraer números de los precios
                    current_price = float(re.sub(r'[^\d.]', '', current_price_text))
                    original_price = None
                    if original_price_text:
                        original_price = float(re.sub(r'[^\d.]', '', original_price_text))

                    # Si no hay precio original explícito, el actual es el único
                    if not original_price:
                        original_price = current_price
                    
                    if original_price < current_price:
                        original_price = current_price

                    discount = calculate_discount(current_price, original_price)
                    is_spectacular = discount >= 60
                    
                    product = {
                        'id': str(uuid.uuid4()),
                        'name': name,
                        'url': url,
                        'currentPrice': current_price,
                        'originalPrice': original_price if original_price != current_price else None,
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
                    
                    if is_spectacular:
                        send_telegram_notification(product)
                    
                except Exception as e:
                    print(f"✗ Error procesando un producto: {e}")
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
    
    if not TELEGRAM_BOT_TOKEN:
        print("\n⚠️ Telegram no configurado. Edita el script para añadir tus credenciales.")
    
    products = scrape_asus_products()
    
    if products:
        save_products(products)
        
        spectacular = sum(1 for p in products if p['isSpectacularDeal'])
        avg_discount = sum(p['discount'] for p in products) / len(products) if products else 0
        
        print(f"\n📊 Estadísticas:")
        print(f"   Total de productos: {len(products)}")
        print(f"   Ofertas espectaculares (>60%): {spectacular}")
        print(f"   Descuento promedio: {avg_discount:.2f}%")
    else:
        print("\n⚠️ No se encontraron productos. Revisa los selectores CSS si la web cambió.")

if __name__ == "__main__":
    main()
