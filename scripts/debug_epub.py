"""
Script para debuggear la extracción de texto del EPUB
"""
import sys
sys.path.insert(0, r'c:\Users\edumi\Code\251225')

from app.utils import obtener_capitulos_epub, extraer_texto_epub
from pathlib import Path

epub_file = r"c:\Users\edumi\Code\251225\uploads\El acto de crear - Rick Rubin.epub"

if not Path(epub_file).exists():
    print(f"Error: {epub_file} no encontrado")
    sys.exit(1)

print("=" * 60)
print("Obteniendo información del EPUB...")
print("=" * 60)

info = obtener_capitulos_epub(epub_file)
print(f"Título: {info['title']}")
print(f"Autor: {info['author']}")
print(f"Capítulos: {len(info['chapters'])}")

for ch in info['chapters']:
    print(f"  [{ch['index']}] {ch['title']}")

print("\n" + "=" * 60)
print("Extrayendo texto del capítulo 8...")
print("=" * 60)

if len(info['chapters']) > 8:
    ch8 = info['chapters'][8]
    print(f"Capítulo seleccionado: {ch8['title']}")
    
    texto = extraer_texto_epub(epub_file, 8)
    print(f"Longitud del texto: {len(texto)} caracteres")
    
    if texto:
        print("\nPrimeros 500 caracteres:")
        print("-" * 40)
        print(texto[:500])
        print("-" * 40)
        
        print("\nÚltimos 500 caracteres:")
        print("-" * 40)
        print(texto[-500:])
        print("-" * 40)
        
        # Verificar caracteres especiales
        problematic = False
        for i, c in enumerate(texto):
            if ord(c) > 127 and ord(c) < 160:
                print(f"Carácter problemático encontrado en posición {i}: ord={ord(c)}")
                problematic = True
        
        if not problematic:
            print("\n✓ No hay caracteres problemáticos")
    else:
        print("✗ Error: texto extraído está vacío")
else:
    print(f"✗ El EPUB solo tiene {len(info['chapters'])} capítulos")

print("\nProbando todos los capítulos:")
print("-" * 40)
for i, ch in enumerate(info['chapters']):
    texto = extraer_texto_epub(epub_file, i)
    chars = len(texto) if texto else 0
    print(f"  [{i}] {ch['title']:<30} -> {chars:>5} caracteres")
