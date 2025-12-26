#!/usr/bin/env python3
"""
Verificar que todas las dependencias están instaladas correctamente
"""

import sys
import subprocess

print("=" * 60)
print("✅ VERIFICADOR DE DEPENDENCIAS - Edge-TTS Web")
print("=" * 60)

dependencias = {
    "edge_tts": "edge-tts",
    "pydub": "pydub",
    "pdfplumber": "pdfplumber",
    "reflex": "reflex",
}

todas_ok = True

for modulo, nombre in dependencias.items():
    try:
        __import__(modulo)
        print(f"✓ {nombre:<20} ✅ Instalado")
    except ImportError:
        print(f"✗ {nombre:<20} ❌ NO INSTALADO")
        todas_ok = False

print("\n" + "=" * 60)

if todas_ok:
    print("\n🎉 ¡TODO LISTO! Puedes ejecutar:\n")
    print("   python app.py")
    print("\nLuego abre: http://localhost:3000\n")
else:
    print("\n⚠️  Faltan algunas dependencias. Instalando...\n")
    subprocess.run([
        sys.executable, "-m", "pip", "install", 
        "edge-tts", "pydub", "pdfplumber", "reflex"
    ])
    print("\n✅ Dependencias instaladas. Intenta de nuevo.\n")

print("=" * 60)
