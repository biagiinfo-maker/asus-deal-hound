# ASUS Deal Hound - Scraper

Script en Python para extraer productos y precios de ASUS Shop.

## 📋 Requisitos

- Python 3.8+
- pip

## 🚀 Instalación

```bash
# Instalar dependencias
pip install playwright requests

# Instalar navegador Chromium
playwright install chromium
```

## 💻 Uso

### 1. Ejecutar el scraper

```bash
python asus_scraper.py
```

Esto generará un archivo `products.json` con todos los productos encontrados.

### 2. Importar al dashboard

1. Abre el dashboard de ASUS Deal Hound en tu navegador
2. Haz clic en "Importar/Exportar"
3. Pega el contenido del archivo `products.json`
4. Haz clic en "Importar Datos"

## 🔔 Configurar notificaciones de Telegram (Opcional)

### Obtener credenciales

1. Crea un bot con [@BotFather](https://t.me/BotFather)
   - Envía `/newbot`
   - Sigue las instrucciones
   - Guarda el **Bot Token**

2. Obtén tu Chat ID
   - Envía un mensaje a tu bot
   - Visita: `https://api.telegram.org/bot<TU_BOT_TOKEN>/getUpdates`
   - Copia el valor de `chat.id`

### Configurar en el script

Edita `asus_scraper.py` y añade tus credenciales:

```python
TELEGRAM_BOT_TOKEN = "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
TELEGRAM_CHAT_ID = "-1001234567890"
```

Ahora recibirás notificaciones automáticas cuando se detecten ofertas con más del 60% de descuento.

## ⏰ Automatización (Opcional)

### Linux/macOS con cron

```bash
# Editar crontab
crontab -e

# Ejecutar cada 4 horas
0 */4 * * * cd /ruta/al/scraper && python asus_scraper.py
```

### Windows con Task Scheduler

1. Abre "Programador de tareas"
2. Crear tarea básica
3. Acción: Iniciar programa
   - Programa: `python`
   - Argumentos: `asus_scraper.py`
   - Carpeta: ruta al directorio del script
4. Configurar desencadenador (cada 4 horas)

## 🔧 Personalización

### Cambiar URL de scraping

Edita la variable `ASUS_URL` en el script:

```python
ASUS_URL = "https://shop.asus.com/us/laptops"
```

### Ajustar selectores CSS

Si los selectores no funcionan, inspecciona la página y actualiza:

```python
# Línea ~70 del script
product_cards = page.query_selector_all('.tu-selector-aqui')
```

## 📊 Formato de salida

El script genera un JSON con esta estructura:

```json
[
  {
    "id": "uuid-único",
    "name": "ASUS Zen AiO 24",
    "url": "https://shop.asus.com/...",
    "currentPrice": 899.99,
    "originalPrice": 1299.99,
    "discount": 30.77,
    "isSpectacularDeal": false,
    "lastUpdated": "2025-01-15T10:30:00",
    "priceHistory": [
      {
        "price": 899.99,
        "date": "2025-01-15T10:30:00"
      }
    ]
  }
]
```

## 🐛 Troubleshooting

### "No se encontraron productos"

- Los selectores CSS pueden haber cambiado
- Inspecciona la página web y actualiza los selectores
- Aumenta el tiempo de espera en `time.sleep()`

### Errores de Playwright

```bash
# Reinstalar navegador
playwright install chromium --force
```

### Notificaciones de Telegram no funcionan

- Verifica que el bot esté en el chat/grupo
- Confirma que las credenciales sean correctas
- Revisa los logs de error en la consola

## 📝 Notas

- Respeta el rate limiting (el script incluye delays)
- No abuses del scraping
- Los selectores pueden cambiar si ASUS actualiza su web
