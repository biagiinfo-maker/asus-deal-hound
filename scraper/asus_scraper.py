"""
ASUS Shop Deal Scraper (Versión Robusta)
========================================
Extrae productos y precios de la página de ofertas de ASUS US.
Maneja banners de cookies y esperas dinámicas.

Instalación:
pip install playwright requests
playwright install chromium

Uso:
python scraper/asus_scraper.py
"""
import json
import time
import uuid
import re
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError

# --- CONFIGURACIÓN ---
ASUS_URL = "https://www.asus.com/us/deals/displays-desktops/"
OUTPUT_FILE = "products.json"
HEADLESS_MODE = True  # Cambia a False para ver el navegador en acción

# --- NOTIFICACIONES (Opcional) ---
TELEGRAM_BOT_TOKEN = ""
TELEGRAM_CHAT_ID = ""

def calculate_discount(current, original):
    if not original or original <= current:
        return 0
    return round(((original - current) / original) * 100, 2)

def scrape_asus_products():
    products = []
    print("=" * 50)
    print("🐕 ASUS Deal Hound - Scraper v2.0")
    print("=" * 50)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS_MODE, slow_mo=50)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        page = context.new_page()

        try:
            print(f"📡 Navegando a: {ASUS_URL}")
            page.goto(ASUS_URL, wait_until='domcontentloaded', timeout=90000)

            # --- MANEJO DE COOKIES ---
            print("🔎 Buscando banner de cookies...")
            try:
                # Espera hasta 10 segundos por el botón y haz clic
                cookie_button = page.locator('button:has-text("Accept")')
                cookie_button.wait_for(timeout=10000)
                cookie_button.click()
                print("✓ Banner de cookies aceptado.")
            except TimeoutError:
                print("ℹ️ No se encontró el banner de cookies o ya estaba aceptado.")

            # --- ESPERA Y SCROLL ---
            print("⏳ Esperando a que la red se estabilice...")
            page.wait_for_load_state('networkidle', timeout=30000)
            
            print("📜 Haciendo scroll para cargar todos los productos...")
            for i in range(5): # Hacemos scroll varias veces para asegurar la carga
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(1)

            # --- EXTRACCIÓN DE PRODUCTOS ---
            print("🔎 Buscando tarjetas de productos...")
            product_selector = '[class*="ProductCardNormalGrid__productCardContainer__"]'
            
            try:
                # Espera a que al menos una tarjeta de producto sea visible
                page.wait_for_selector(product_selector, timeout=20000)
                print("✓ Contenedor de productos encontrado.")
            except TimeoutError:
                print("❌ No se encontraron productos. La estructura de la web puede haber cambiado.")
                browser.close()
                return []

            product_cards = page.query_selector_all(product_selector)
            print(f"📦 Encontrados {len(product_cards)} productos para procesar.")

            for card in product_cards:
                try:
                    name_elem = card.query_selector('a[class*="ProductCardNormalGrid__headingRow__"] h2')
                    if not name_elem: continue
                    name = name_elem.inner_html().replace('<br>', ' ').strip()

                    link_elem = card.query_selector('a[class*="ProductCardNormalGrid__headingRow__"]')
                    url = link_elem.get_attribute('href') if link_elem else ASUS_URL
                    if url and not url.startswith('http'):
                        url = f"https://www.asus.com{url}"

                    current_price_elem = card.query_selector('[class*="ProductCardNormalGrid__priceDiscount__"]')
                    original_price_elem = card.query_selector('.regularPrice')

                    current_price_text = current_price_elem.inner_text().strip() if current_price_elem else None
                    if not current_price_text: continue

                    current_price = float(re.sub(r'[^\d.]', '', current_price_text))
                    original_price = None

                    if original_price_elem:
                        original_price_text = original_price_elem.inner_text().strip()
                        original_price = float(re.sub(r'[^\d.]', '', original_price_text))

                    if not original_price or original_price < current_price:
                        original_price = current_price

                    discount = calculate_discount(current_price, original_price)

                    product = {
                        'id': str(uuid.uuid4()),
                        'name': name,
                        'url': url,
                        'currentPrice': current_price,
                        'originalPrice': original_price if original_price != current_price else None,
                        'discount': discount,
                        'isSpectacularDeal': discount >= 60,
                        'lastUpdated': datetime.now().isoformat(),
                        'priceHistory': [{'price': current_price, 'date': datetime.now().isoformat()}]
                    }
                    
                    products.append(product)
                    print(f"  -> {name} - ${current_price}")

                except Exception as e:
                    print(f"  ✗ Error procesando una tarjeta: {e}")
                    continue
            
        except Exception as e:
            print(f"❌ Error fatal durante el scraping: {e}")
        finally:
            print("🚪 Cerrando navegador.")
            browser.close()
    
    return products

def save_products(products):
    """Guarda los productos en el archivo JSON de salida."""
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(products, f, indent=2, ensure_ascii=False)
        print(f"\n✅ ¡Éxito! Se guardaron {len(products)} productos en '{OUTPUT_FILE}'.")
        print(f"   Ahora puedes copiar el contenido de este archivo e importarlo en el dashboard.")
    except Exception as e:
        print(f"❌ Error al guardar el archivo: {e}")

if __name__ == "__main__":
    found_products = scrape_asus_products()
    if found_products:
        save_products(found_products)
    else:
        print("\n⚠️ No se extrajo ningún producto. Revisa los logs para más detalles.")