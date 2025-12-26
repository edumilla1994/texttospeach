"""
Script para probar edge-tts de forma aislada
"""
import asyncio
import edge_tts
import tempfile
from pathlib import Path

async def test_edge_tts():
    """Test edge-tts con un texto simple"""
    print("=" * 60)
    print("Test 1: Texto simple corto")
    print("=" * 60)
    
    texto_corto = "Hola, esto es una prueba de edge-tts."
    voz = "es-ES-ElviraNeural"
    rate = "+0%"
    
    output = Path(tempfile.gettempdir()) / "test_edgetts_1.mp3"
    
    try:
        print(f"Parámetros:")
        print(f"  Texto: {texto_corto[:50]}...")
        print(f"  Voz: {voz}")
        print(f"  Rate: {rate}")
        print(f"  Salida: {output}")
        
        communicate = edge_tts.Communicate(texto_corto, voz, rate=rate)
        await communicate.save(str(output))
        
        if output.exists():
            size = output.stat().st_size
            print(f"✓ Éxito: {size} bytes generados")
            output.unlink()
        else:
            print("✗ Error: archivo no creado")
    except Exception as e:
        print(f"✗ Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 60)
    print("Test 2: Texto más largo (como capítulo)")
    print("=" * 60)
    
    texto_largo = """
    La vida es un viaje fascinante lleno de oportunidades y desafíos.
    Cada día nos presenta nuevas experiencias que nos ayudan a crecer 
    como personas. Es importante mantener una actitud positiva y seguir 
    adelante sin importar los obstáculos que encontremos en el camino.
    La perseverancia y la dedicación son clave para lograr nuestros objetivos.
    """ * 3  # Repetir para hacerlo más largo
    
    output2 = Path(tempfile.gettempdir()) / "test_edgetts_2.mp3"
    
    try:
        print(f"Parámetros:")
        print(f"  Texto: {len(texto_largo)} caracteres")
        print(f"  Voz: {voz}")
        print(f"  Rate: {rate}")
        print(f"  Salida: {output2}")
        
        communicate = edge_tts.Communicate(texto_largo, voz, rate=rate)
        await communicate.save(str(output2))
        
        if output2.exists():
            size = output2.stat().st_size
            print(f"✓ Éxito: {size} bytes generados")
            output2.unlink()
        else:
            print("✗ Error: archivo no creado")
    except Exception as e:
        print(f"✗ Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 60)
    print("Test 3: Diferentes voces en español")
    print("=" * 60)
    
    voces = [
        "es-ES-AlvaroNeural",
        "es-ES-ElviraNeural",
        "es-MX-JorgeNeural",
        "es-AR-ElenaNeural"
    ]
    
    texto = "Hola, esto es una prueba."
    
    for v in voces:
        output = Path(tempfile.gettempdir()) / f"test_edgetts_{v.replace('-', '_')}.mp3"
        try:
            print(f"Probando voz: {v}... ", end="", flush=True)
            communicate = edge_tts.Communicate(texto, v, rate=rate)
            await communicate.save(str(output))
            
            if output.exists():
                size = output.stat().st_size
                print(f"✓ ({size} bytes)")
                output.unlink()
            else:
                print(f"✗ (archivo vacío)")
        except Exception as e:
            print(f"✗ ({type(e).__name__})")

if __name__ == "__main__":
    asyncio.run(test_edge_tts())
