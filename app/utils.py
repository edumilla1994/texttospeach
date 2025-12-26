"""
Utilidades para procesamiento de audio
"""
import asyncio
import edge_tts
from io import BytesIO
from pathlib import Path
import os
from typing import List
import tempfile
import uuid

try:
    import ebooklib
    from ebooklib import epub
    from bs4 import BeautifulSoup
    EPUB_AVAILABLE = True
except Exception:
    EPUB_AVAILABLE = False

def calcular_rate(velocidad: float) -> str:
    """
    Calcula el rate para edge-tts
    velocidad: float entre 0.5 y 2.0
    """
    # Normalizar dentro del rango esperado (evita signos extraños)
    min_vel, max_vel = 0.5, 2.0
    if velocidad < min_vel:
        velocidad = min_vel
    elif velocidad > max_vel:
        velocidad = max_vel

    rate_value = int((velocidad - 1) * 50)
    # Formatear con el signo correcto: positivo -> "+N%", negativo -> "-N%"
    if rate_value >= 0:
        return f"+{rate_value}%"
    else:
        return f"{rate_value}%"

async def generar_audio_desde_texto(
    texto: str,
    voz: str,
    velocidad: float,
    archivo_salida: Path
) -> bool:
    """
    Genera audio desde texto
    Soporta textos largos mediante fragmentación
    """
    # Para textos largos, dividir en fragmentos y generar por partes, luego concatenar
    try:
        from pydub import AudioSegment
        
        rate = calcular_rate(velocidad)
        print(f"[DEBUG] Rate calculado: {rate} para velocidad {velocidad}")

        # Tamaño máximo por fragmento (caracteres). Ajustable según pruebas.
        max_chars = 4500
        # Normalizar texto y dividir en trozos sin cortar palabras
        texto = texto.strip()
        if not texto:
            print("[ERROR] Texto vacío después de strip")
            return False
        
        print(f"[DEBUG] Texto original: {len(texto)} caracteres")

        # Crear fragmentos aproximados
        fragments = []
        if len(texto) <= max_chars:
            fragments = [texto]
        else:
            start = 0
            L = len(texto)
            while start < L:
                end = min(start + max_chars, L)
                # intentar cortar en el último salto de línea o espacio
                if end < L:
                    # buscar última '\n' o ' ' entre start y end
                    slice_ = texto[start:end]
                    idx = max(slice_.rfind('\n'), slice_.rfind(' '))
                    if idx > 100:  # evitar cortes muy cortos
                        end = start + idx
                fragments.append(texto[start:end].strip())
                start = end

        # Generar cada fragmento a archivo temporal
        temp_files = []
        print(f"[DEBUG] {len(fragments)} fragmentos a generar")
        for i, frag in enumerate(fragments):
            if not frag:
                print(f"[DEBUG] Fragmento {i} vacío, saltando")
                continue
            print(f"[DEBUG] Generando fragmento {i}: {len(frag)} caracteres")
            temp_name = Path(tempfile.gettempdir()) / f"{uuid.uuid4().hex}_{i}.mp3"
            try:
                print(f"[DEBUG] Llamando edge_tts para fragmento {i} con voz='{voz}', rate='{rate}'")
                communicate = edge_tts.Communicate(frag, voz, rate=rate)
                await communicate.save(str(temp_name))
                # Verificar que el archivo se creó y tiene contenido
                if temp_name.exists() and temp_name.stat().st_size > 0:
                    print(f"[DEBUG] Fragmento {i} OK ({temp_name.stat().st_size} bytes)")
                    temp_files.append(temp_name)
                else:
                    print(f"[ERROR] Fragmento {i} creado pero vacío o no existe")
                    if temp_name.exists():
                        temp_name.unlink()
            except Exception as e:
                print(f"[ERROR] Fragmento {i} falló: {type(e).__name__}: {e}")
                import traceback
                traceback.print_exc()
                # Limpiar temporales en caso de error
                for f in temp_files:
                    f.unlink(missing_ok=True)
                return False

        # Validar que se generaron fragmentos
        if not temp_files:
            print("[ERROR] No se generaron fragmentos de audio")
            return False

        # Si sólo hay un fragmento, renombrar/mover
        if len(temp_files) == 1:
            print(f"[DEBUG] 1 fragmento, moviendo a salida final")
            Path(temp_files[0]).replace(archivo_salida)
            print(f"[DEBUG] Audio final: {archivo_salida.stat().st_size} bytes")
            return True

        # Concatenar múltiples fragmentos con pydub
        print(f"[DEBUG] Concatenando {len(temp_files)} fragmentos de audio")
        combined = None
        try:
            for i, f in enumerate(temp_files):
                segment = AudioSegment.from_mp3(str(f))
                print(f"[DEBUG] Fragmento {i}: {len(segment)}ms de audio")
                if combined is None:
                    combined = segment
                else:
                    combined += segment
        except Exception as e:
            print(f"[ERROR] Error en concatenación: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            for f in temp_files:
                f.unlink(missing_ok=True)
            return False

        if combined is None or len(combined) == 0:
            print("[ERROR] Audio concatenado vacío")
            return False

        # Guardar audio final
        combined.export(str(archivo_salida), format="mp3")
        print(f"[DEBUG] Audio final guardado: {archivo_salida.stat().st_size} bytes, {len(combined)}ms")
        
        # Limpiar temporales
        for f in temp_files:
            f.unlink(missing_ok=True)
        
        return True

    except Exception as e:
        print(f"Error generando audio: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
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
    # Reutilizar la lógica de texto (manejo de fragmentos)
    return await generar_audio_desde_texto(texto, voz, velocidad, archivo_salida)

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


def obtener_capitulos_epub(epub_path: str) -> List[str]:
    """
    Retorna un dict con metadata del libro y la lista de capítulos en orden de spine.
    Devuelve: { 'title': str, 'author': str, 'chapters': [ { 'index': int, 'id': str, 'title': str } ] }
    """
    if not EPUB_AVAILABLE:
        return {'title': '', 'author': '', 'chapters': []}
    try:
        book = epub.read_epub(epub_path)
        # metadata
        title_meta = book.get_metadata('DC', 'title')
        author_meta = book.get_metadata('DC', 'creator')
        book_title = title_meta[0][0] if title_meta else ''
        book_author = author_meta[0][0] if author_meta else ''

        # map items by id
        docs = {item.get_id(): item for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT)}

        chapters = []
        # book.spine is a list of tuples (idref, ) or similar; iterate preserving order
        spine = getattr(book, 'spine', [])
        idx = 0
        for entry in spine:
            # entry may be ('nav',) or ('itemid', '...')
            if isinstance(entry, (list, tuple)) and len(entry) > 0:
                idref = entry[0]
            else:
                idref = entry
            if idref in docs:
                item = docs[idref]
                soup = BeautifulSoup(item.get_content(), 'html.parser')
                h = soup.find(['h1', 'h2', 'h3'])
                chap_title = h.get_text().strip() if (h and h.get_text().strip()) else item.get_id()
                chapters.append({'index': idx, 'id': idref, 'title': chap_title})
                idx += 1

        # Fallback: if no chapters found via spine, iterate docs
        if not chapters:
            for item in docs.values():
                soup = BeautifulSoup(item.get_content(), 'html.parser')
                h = soup.find(['h1', 'h2', 'h3'])
                chap_title = h.get_text().strip() if (h and h.get_text().strip()) else item.get_id()
                chapters.append({'index': idx, 'id': item.get_id(), 'title': chap_title})
                idx += 1

        return {'title': book_title, 'author': book_author, 'chapters': chapters}
    except Exception as e:
        print(f"Error leyendo EPUB: {e}")
        return {'title': '', 'author': '', 'chapters': []}


def extraer_texto_epub(epub_path: str, chapter_index: int) -> str:
    """
    Extrae el texto de un capítulo específico (index) de un EPUB.
    """
    if not EPUB_AVAILABLE:
        print("[ERROR] ebooklib no disponible")
        return ""
    try:
        book = epub.read_epub(epub_path)
        # Build ordered docs using spine if possible
        docs_map = {item.get_id(): item for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT)}
        print(f"[DEBUG] EPUB tiene {len(docs_map)} documentos")
        
        spine = getattr(book, 'spine', [])
        ordered = []
        for entry in spine:
            if isinstance(entry, (list, tuple)) and len(entry) > 0:
                idref = entry[0]
            else:
                idref = entry
            if idref in docs_map:
                ordered.append(docs_map[idref])

        if not ordered:
            print(f"[DEBUG] Spine vacío o inválido, usando todos los documentos")
            ordered = list(docs_map.values())

        print(f"[DEBUG] Extrayendo capítulo {chapter_index} de {len(ordered)} ordenados")
        if chapter_index < 0 or chapter_index >= len(ordered):
            print(f"[ERROR] Índice {chapter_index} fuera de rango [0, {len(ordered)-1}]")
            return ""
        
        item = ordered[chapter_index]
        print(f"[DEBUG] Item seleccionado: {item.get_id()}")
        
        soup = BeautifulSoup(item.get_content(), 'html.parser')
        # Extraer texto plano
        text = soup.get_text(separator='\n')
        print(f"[DEBUG] Texto extraído: {len(text)} caracteres")
        return text
    except Exception as e:
        print(f"Error extrayendo EPUB: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return ""
