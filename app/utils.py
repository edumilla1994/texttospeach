"""
Utilidades para procesamiento de audio
"""
import asyncio
import edge_tts
from io import BytesIO
from pathlib import Path
import os

def calcular_rate(velocidad: float) -> str:
    """
    Calcula el rate para edge-tts
    velocidad: float entre 0.5 y 2.0
    """
    rate_value = int((velocidad - 1) * 50)
    return f"+{rate_value}%"

async def generar_audio_desde_texto(
    texto: str,
    voz: str,
    velocidad: float,
    archivo_salida: Path
) -> bool:
    """
    Genera audio desde texto
    """
    try:
        rate = calcular_rate(velocidad)
        communicate = edge_tts.Communicate(texto, voz, rate=rate)
        await communicate.save(str(archivo_salida))
        return True
    except Exception as e:
        print(f"Error generando audio: {e}")
        return False

async def generar_audio_desde_pdf(
    texto: str,
    voz: str,
    velocidad: float,
    archivo_salida: Path
) -> bool:
    """
    Genera audio desde texto extraído de PDF
    """
    try:
        rate = calcular_rate(velocidad)
        communicate = edge_tts.Communicate(texto, voz, rate=rate)
        await communicate.save(str(archivo_salida))
        return True
    except Exception as e:
        print(f"Error generando audio PDF: {e}")
        return False

def extraer_texto_pdf(pdf_path: str, paginas) -> str:
    """
    Extrae texto de un PDF
    paginas: int (número de páginas) o list (rango de páginas como [1,2,3])
    """
    try:
        import pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            # Convertir a lista si es int
            if isinstance(paginas, int):
                paginas_list = list(range(paginas))
            else:
                # Restar 1 porque pdfplumber usa índice 0
                paginas_list = [p - 1 for p in paginas if p <= len(pdf.pages)]
            
            texto = "\n".join(
                pdf.pages[i].extract_text() or ""
                for i in paginas_list if i < len(pdf.pages)
            )
        return texto
    except Exception as e:
        print(f"Error extrayendo PDF: {e}")
        return ""

def obtener_info_pdf(pdf_path: str) -> int:
    """
    Obtiene el número de páginas de un PDF
    """
    try:
        import pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            return len(pdf.pages)
    except:
        return 0
