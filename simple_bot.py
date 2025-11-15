#!/usr/bin/env python3
"""
Basit Domain Checker - Render.com için
Tek dosya, sade çalışma
"""

from flask import Flask
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import threading
import time
import os

app = Flask(__name__)

# ============================================================================
# BURADAN AYARLARI DEĞİŞTİR
# ============================================================================

DOMAINS = [
    "matadorbet937.com",
    # Buraya diğer domain'leri ekle
]

CHECK_INTERVAL = 1800  # 30 dakika (saniye)

# ============================================================================

def check_domain(domain):
    try:
        url = "https://www.guvenlinet.org.tr/sorgula"
        data = {'domain': domain}
        
        response = requests.post(url, data=data, timeout=30, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Çocuk Profili kontrol et
            cocuk_kirmizi = False
            if soup.find(class_='text-warning') or '!' in soup.get_text():
                cocuk_kirmizi = True
            
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            if cocuk_kirmizi:
                msg = f"⚠️ UYARI [{timestamp}] {domain} - ÇOCUK PROFİLİ KIRMIZI!"
                print(msg)
                return {'domain': domain, 'status': 'kırmızı', 'time': timestamp}
            else:
                print(f"✓ [{timestamp}] {domain} - Güvenli")
                return {'domain': domain, 'status': 'yeşil', 'time': timestamp}
        else:
            print(f"✗ {domain} - Hata: HTTP {response.status_code}")
            return {'domain': domain, 'status': 'hata'}
            
    except Exception as e:
        print(f"✗ {domain} - Hata: {str(e)}")
        return {'domain': domain, 'status': 'hata'}

def background_check():
    print(f"🤖 Bot başlatıldı - Her {CHECK_INTERVAL//60} dakikada kontrol")
    print(f"📍 İzlenen domain'ler: {', '.join(DOMAINS)}\n")
    
    while True:
        print(f"\n{'='*60}")
        print(f"🔍 Kontrol başladı: {datetime.now().strftime('%H:%M:%S')}")
        print(f"{'='*60}")
        
        for domain in DOMAINS:
            check_domain(domain)
            time.sleep(2)
        
        next_time = datetime.now().timestamp() + CHECK_INTERVAL
        next_str = datetime.fromtimestamp(next_time).strftime('%H:%M:%S')
        print(f"\n⏰ Sonraki kontrol: {next_str}")
        print(f"{'='*60}\n")
        
        time.sleep(CHECK_INTERVAL)

@app.route('/')
def home():
    return "Domain Checker Bot - Çalışıyor ✓"

@app.route('/health')
def health():
    return {'status': 'ok'}

if __name__ == '__main__':
    # Arka plan kontrolü başlat
    thread = threading.Thread(target=background_check, daemon=True)
    thread.start()
    
    # Flask başlat
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
