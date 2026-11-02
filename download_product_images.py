"""
Download high-resolution realistic commercial product photography for all 13 KARTMART categories.
"""
import os
import urllib.request
import time

TARGET_DIR = os.path.join(os.path.dirname(__file__), 'app', 'static', 'img', 'products')
os.makedirs(TARGET_DIR, exist_ok=True)

# Curated high-resolution Unsplash commercial product photography IDs
PRODUCT_IMAGES = {
    'leather_jacket.jpg': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=600&h=600&fit=crop&q=85',
    'oxford_shirt.jpg': 'https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=600&h=600&fit=crop&q=85',
    'womens_trench.jpg': 'https://images.unsplash.com/photo-1544441893-675973e31985?w=600&h=600&fit=crop&q=85',
    'activewear_set.jpg': 'https://images.unsplash.com/photo-1518611012118-696072aa579a?w=600&h=600&fit=crop&q=85',
    'kids_hoodie.jpg': 'https://images.unsplash.com/photo-1519238263530-99bdd11df2ea?w=600&h=600&fit=crop&q=85',
    'leather_shoes.jpg': 'https://images.unsplash.com/photo-1533867617858-e7b97e060509?w=600&h=600&fit=crop&q=85',
    'sneakers.jpg': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600&h=600&fit=crop&q=85',
    'drone.jpg': 'https://images.unsplash.com/photo-1508614589041-895b88991e3e?w=600&h=600&fit=crop&q=85',
    'robot_toy.jpg': 'https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=600&h=600&fit=crop&q=85',
    'espresso_machine.jpg': 'https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?w=600&h=600&fit=crop&q=85',
    'air_fryer.jpg': 'https://images.unsplash.com/photo-1584269600464-37b1b58a9fe7?w=600&h=600&fit=crop&q=85',
    'cookware.jpg': 'https://images.unsplash.com/photo-1584990347449-39943260c6d2?w=600&h=600&fit=crop&q=85',
    'office_chair.jpg': 'https://images.unsplash.com/photo-1580481077195-c3a821a58875?w=600&h=600&fit=crop&q=85',
    'oak_desk.jpg': 'https://images.unsplash.com/photo-1518455027359-f3f8164ba6bd?w=600&h=600&fit=crop&q=85',
    'floor_lamp.jpg': 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=600&h=600&fit=crop&q=85',
    'serum.jpg': 'https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=600&h=600&fit=crop&q=85',
    'perfume.jpg': 'https://images.unsplash.com/photo-1592945403244-b3fbafd7f539?w=600&h=600&fit=crop&q=85',
    'dumbbells.jpg': 'https://images.unsplash.com/photo-1583454110551-21f2fa2afe61?w=600&h=600&fit=crop&q=85',
    'yoga_mat.jpg': 'https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=600&h=600&fit=crop&q=85',
    'cycling_helmet.jpg': 'https://images.unsplash.com/photo-1558981806-ec527fa84c39?w=600&h=600&fit=crop&q=85',
    'leather_journal.jpg': 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=600&h=600&fit=crop&q=85',
    'fountain_pen.jpg': 'https://images.unsplash.com/photo-1583485088034-697b5bc54ccd?w=600&h=600&fit=crop&q=85',
    'leather_bag.jpg': 'https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=600&h=600&fit=crop&q=85',
    'sunglasses.jpg': 'https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=600&h=600&fit=crop&q=85',
    'coffee_beans.jpg': 'https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=600&h=600&fit=crop&q=85',
    'olive_oil.jpg': 'https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=600&h=600&fit=crop&q=85',
    'diwali_hamper.jpg': 'https://images.unsplash.com/photo-1513151233558-d860c5398176?w=600&h=600&fit=crop&q=85',
    'gaming_laptop.jpg': 'https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=600&h=600&fit=crop&q=85',
    'diwali_banner.jpg': 'https://images.unsplash.com/photo-1605371924599-2d0365da1ae0?w=1200&h=450&fit=crop&q=85'
}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

print("[*] Downloading realistic commercial product images...")
for filename, url in PRODUCT_IMAGES.items():
    filepath = os.path.join(TARGET_DIR, filename)
    if os.path.exists(filepath) and os.path.getsize(filepath) > 1000:
        print(f" -> Already exists: {filename}")
        continue
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response, open(filepath, 'wb') as out_file:
            out_file.write(response.read())
        print(f" [+] Downloaded: {filename}")
        time.sleep(0.1)
    except Exception as e:
        print(f" [!] Failed {filename}: {e}")

print("[+] Product images download completed!")
