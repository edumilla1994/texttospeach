"""
Test del API del servidor Flask
"""
import requests
import json
import time

# Probar la generación de audio desde EPUB
url = "http://127.0.0.1:5000/api/generar-epub"

payload = {
    "archivo": "El acto de crear - Rick Rubin.epub",
    "capitulo": 8,
    "voz": "es-ES-ElviraNeural",
    "velocidad": 1.0
}

print("=" * 60)
print("Test: Generación de audio desde EPUB vía API")
print("=" * 60)
print(f"\nURL: {url}")
print(f"Payload: {json.dumps(payload, indent=2)}")
print("\nEnviando request...")

try:
    response = requests.post(url, json=payload, timeout=60)
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2))
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print(f"\n✓ Éxito!")
            print(f"  Archivo: {data.get('filename')}")
            print(f"  Audio URL: {data.get('audio')}")
            print(f"  Nombre descarga: {data.get('download_name')}")
        else:
            print(f"\n✗ Error: {data.get('error')}")
    else:
        print(f"\n✗ HTTP Error: {response.status_code}")
except Exception as e:
    print(f"\n✗ Excepción: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
