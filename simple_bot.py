from flask import Flask
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import threading
import time
import os

app = Flask(__name__)

# BURAYA DOMAIN'LERİNİ EKLE
DOMAINS = [
    "matadorbet937.com",
    # "ornekdomain.com",  # Buraya ekle
]

CHECK_INTERVAL = 1800  # 30 dakika

def check_domain(domain):
    try:
        url = "https://www.guvenlinet.org.tr/sorgula"
        response = requests.post(url, data={'domain': domain}, timeout=30, 
                               headers={'User-Agent': 'Mozilla/5.0'})
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            cocuk_kirmizi = bool(soup.find(class_='text-warning'))
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            if cocuk_kirmizi:
                print(f"⚠️ UYARI [{timestamp}] {domain} - ÇOCUK PROFİLİ KIRMIZI!")
            else:
                print(f"✓ [{timestamp}] {domain} - Güvenli")
    except Exception as e:
        print(f"✗ {domain} - Hata: {e}")

def background_check():
    print(f"🤖 Bot başladı - {len(DOMAINS)} domain izleniyor")
    while True:
        print(f"\n🔍 Kontrol: {datetime.now().strftime('%H:%M:%S')}")
        for domain in DOMAINS:
            check_domain(domain)
            time.sleep(2)
        print(f"⏰ Sonraki kontrol: {(datetime.now().timestamp() + CHECK_INTERVAL)}")
        time.sleep(CHECK_INTERVAL)

@app.route('/')
def home():
    return "Bot çalışıyor ✓"

@app.route('/health')
def health():
    return {'status': 'ok'}

if __name__ == '__main__':
    thread = threading.Thread(target=background_check, daemon=True)
    thread.start()
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 10000)))
```

4. **"Commit changes"** bas

**İkinci dosya - requirements.txt:**
1. **"Add file"** → **"Create new file"**
2. İsim: `requirements.txt`
3. Şunu yapıştır:
```
flask==3.0.0
requests==2.31.0
beautifulsoup4==4.12.2
lxml==5.1.0
gunicorn==21.2.0
```

4. **"Commit changes"** bas

### ADIM 4: Render'a Deploy

1. https://render.com → Giriş yap
2. **"New +" → "Web Service"**
3. **Repository'ni seç** (domain-bot)
4. Ayarlar:
```
   Name: domain-bot
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn simple_bot:app
   Plan: FREE
