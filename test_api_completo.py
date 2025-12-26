"""
Test completo del API EPUB: cargar y generar audio
"""
import requests
import json
import time

# Paso 1: Cargar el EPUB
print("=" * 60)
print("PASO 1: Cargar el EPUB")
print("=" * 60)

with open(r'c:\Users\edumi\Code\251225\uploads\El acto de crear - Rick Rubin.epub', 'rb') as f:
    files = {'file': f}
    response = requests.post(
        "http://127.0.0.1:5000/api/upload-epub",
        files=files,
        timeout=30
    )

print(f"Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"Título: {data.get('title')}")
    print(f"Autor: {data.get('author')}")
    print(f"Capítulos: {data.get('chapters_count')}")
    print("\nCapítulos disponibles:")
    for ch in data.get('chapters', [])[:10]:
        print(f"  [{ch['index']}] {ch['title']}")
else:
    print(f"Error: {response.text}")
    exit(1)

# Paso 2: Generar audio
print("\n" + "=" * 60)
print("PASO 2: Generar audio del capítulo 8 (Sintonización)")
print("=" * 60)

time.sleep(1)  # Pequeña pausa

payload = {
    "archivo": "El acto de crear - Rick Rubin.epub",
    "capitulo": 8,
    "voz": "es-ES-ElviraNeural",
    "velocidad": 1.0
}

print(f"Enviando request...")
response = requests.post(
    "http://127.0.0.1:5000/api/generar-epub",
    json=payload,
    timeout=120
)

print(f"Status: {response.status_code}")
data = response.json()

if response.status_code == 200 and data.get('success'):
    print(f"✓ Éxito!")
    print(f"  Archivo: {data.get('filename')}")
    print(f"  URL: {data.get('audio')}")
    print(f"  Nombre descarga: {data.get('download_name')}")
else:
    print(f"✗ Error: {data.get('error')}")
