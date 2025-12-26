"""
Test para simular exactamente la generación de audio desde EPUB
"""
import asyncio
import sys
sys.path.insert(0, r'c:\Users\edumi\Code\251225')

from app.utils import extraer_texto_epub, generar_audio_desde_texto
from pathlib import Path
import tempfile

async def test_epub_audio_generation():
    """Test la generación de audio para el capítulo 8"""
    
    epub_file = r"c:\Users\edumi\Code\251225\uploads\El acto de crear - Rick Rubin.epub"
    
    print("=" * 60)
    print("Test: Generación de audio desde EPUB capítulo 8")
    print("=" * 60)
    
    # Extraer el texto
    print("\n1. Extrayendo texto del capítulo 8...")
    texto = extraer_texto_epub(epub_file, 8)
    print(f"   ✓ Texto extraído: {len(texto)} caracteres")
    
    if not texto:
        print("   ✗ ERROR: Texto vacío")
        return
    
    # Generar audio
    print("\n2. Generando audio...")
    
    output_file = Path(tempfile.gettempdir()) / "test_epub_chapter8.mp3"
    
    resultado = await generar_audio_desde_texto(
        texto=texto,
        voz="es-ES-ElviraNeural",
        velocidad=1.0,
        archivo_salida=output_file
    )
    
    print(f"   Resultado: {resultado}")
    
    if output_file.exists():
        size = output_file.stat().st_size
        print(f"   ✓ Archivo generado: {size} bytes")
        output_file.unlink()
    else:
        print(f"   ✗ Archivo NO generado")

if __name__ == "__main__":
    asyncio.run(test_epub_audio_generation())
