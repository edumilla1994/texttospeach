"""
🎵 Edge-TTS Web - Aplicación Principal
"""
from flask import Flask, render_template, request, send_file, jsonify
import asyncio
from pathlib import Path
import time
import os

from config import (
    Config, DevelopmentConfig,
    UPLOAD_FOLDER, TEXT_AUDIO_FOLDER, PDF_AUDIO_FOLDER,
    MAX_PALABRAS_TEXTO, MAX_PAGINAS_PDF, VOCES_ESPANOL
)
from app.utils import (
    generar_audio_desde_texto,
    generar_audio_desde_pdf,
    extraer_texto_pdf,
    obtener_info_pdf
)

# Crear aplicación Flask
app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.config.from_object(DevelopmentConfig)
# Flask config expects path strings; asegurar consistencia usando str()
app.config['UPLOAD_FOLDER'] = str(UPLOAD_FOLDER)

# Variables globales
pdf_cargado = {
    'path': None,
    'nombre': None
}

epub_cargado = {
    'path': None,
    'nombre': None
}

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html', voces=VOCES_ESPANOL)

@app.route('/api/upload-pdf', methods=['POST'])
def upload_pdf():
    """Carga un archivo PDF"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file'}), 400
        
        file = request.files['file']
        if not file.filename.endswith('.pdf'):
            return jsonify({'success': False, 'error': 'Solo PDFs'}), 400
        
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        
        # Obtener info del PDF
        paginas = obtener_info_pdf(filepath)
        
        # Guardar info en sesión
        pdf_cargado['path'] = filepath
        pdf_cargado['nombre'] = file.filename
        
        return jsonify({
            'success': True,
            'path': filepath,
            'filename': file.filename,
            'paginas': paginas
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/generar-texto', methods=['POST'])
def generar_texto():
    """Genera audio desde texto"""
    try:
        data = request.get_json()
        texto = data.get('texto', '').strip()
        voz = data.get('voz', 'es-ES-ElviraNeural')
        velocidad = float(data.get('velocidad', 1.0))
        
        if not texto:
            return jsonify({'success': False, 'error': 'Texto vacío'}), 400
        
        palabras = len(texto.split())
        if palabras > MAX_PALABRAS_TEXTO:
            return jsonify({'success': False, 'error': f'Máximo {MAX_PALABRAS_TEXTO} palabras'}), 400
        
        # Generar archivo
        timestamp = int(time.time())
        filename = f"text_{timestamp}.mp3"
        filepath = TEXT_AUDIO_FOLDER / filename
        
        # Generar audio (async)
        async def generar():
            return await generar_audio_desde_texto(
                texto, voz, velocidad, filepath
            )
        
        resultado = asyncio.run(generar())
        
        if not resultado:
            return jsonify({'success': False, 'error': 'Error generando audio'}), 500
        
        return jsonify({
            'success': True,
            'filename': filename,
            'url': f'/media/text_audio/{filename}'
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/generar-pdf', methods=['POST'])
def generar_pdf():
    """Genera audio desde PDF"""
    try:
        if not pdf_cargado['path']:
            return jsonify({'success': False, 'error': 'No hay PDF cargado'}), 400
        
        data = request.get_json()
        paginas_str = data.get('paginas', '1-1')  # Formato: "desde-hasta"
        voz = data.get('voz', 'es-ES-ElviraNeural')
        velocidad = float(data.get('velocidad', 1.0))
        
        # Parsear rango de páginas
        try:
            desde, hasta = map(int, paginas_str.split('-'))
        except:
            desde, hasta = 1, 1
        
        # Validar rango
        num_paginas = hasta - desde + 1
        if num_paginas > MAX_PAGINAS_PDF:
            return jsonify({'success': False, 'error': f'Máximo {MAX_PAGINAS_PDF} páginas'}), 400
        
        # Extraer texto del PDF (rango desde-hasta)
        texto = extraer_texto_pdf(pdf_cargado['path'], list(range(desde, hasta + 1)))
        
        if not texto.strip():
            return jsonify({'success': False, 'error': 'PDF sin texto extraíble'}), 400
        
        # Generar archivo
        timestamp = int(time.time())
        filename = f"pdf_{timestamp}.mp3"
        filepath = PDF_AUDIO_FOLDER / filename
        
        # Generar audio (async)
        async def generar():
            return await generar_audio_desde_pdf(
                texto, voz, velocidad, filepath
            )
        
        resultado = asyncio.run(generar())
        
        if not resultado:
            return jsonify({'success': False, 'error': 'Error generando audio'}), 500
        
        return jsonify({
            'success': True,
            'filename': filename,
            'url': f'/media/pdf_audio/{filename}'
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/upload-epub', methods=['POST'])
def upload_epub():
    """Recibe un EPUB y devuelve la lista de capítulos disponibles"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file'}), 400
        file = request.files['file']
        if not file.filename.endswith('.epub'):
            return jsonify({'success': False, 'error': 'Solo EPUBs'}), 400

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Obtener lista de capítulos y metadata
        from app.utils import obtener_capitulos_epub
        cap_info = obtener_capitulos_epub(filepath)

        epub_cargado['path'] = filepath
        epub_cargado['nombre'] = file.filename
        epub_cargado['chapters'] = cap_info.get('chapters', [])
        epub_cargado['title'] = cap_info.get('title', '')
        epub_cargado['author'] = cap_info.get('author', '')

        return jsonify({
            'success': True,
            'filename': file.filename,
            'chapters': epub_cargado['chapters'],
            'title': epub_cargado['title'],
            'author': epub_cargado['author']
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/generar-epub', methods=['POST'])
def generar_epub():
    """Genera audio desde un capítulo de EPUB previamente cargado"""
    try:
        data = request.get_json()
        archivo = data.get('archivo')
        capitulo = int(data.get('capitulo', 0))
        voz = data.get('voz', 'es-ES-ElviraNeural')
        velocidad = float(data.get('velocidad', 1.0))

        if not archivo:
            return jsonify({'success': False, 'error': 'Archivo no especificado'}), 400

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], archivo)
        if not os.path.exists(filepath):
            return jsonify({'success': False, 'error': 'Archivo no encontrado'}), 404

        from app.utils import extraer_texto_epub, generar_audio_desde_texto

        print(f"[DEBUG] Extrayendo capítulo {capitulo} de {filepath}")
        texto = extraer_texto_epub(filepath, capitulo)
        print(f"[DEBUG] Texto extraído: {len(texto)} caracteres")
        
        if not texto.strip():
            return jsonify({'success': False, 'error': 'Capítulo sin texto'}), 400

        timestamp = int(time.time())
        filename = f"epub_{timestamp}.mp3"
        outpath = PDF_AUDIO_FOLDER / filename

        print(f"[DEBUG] Iniciando generación de audio -> {outpath}")
        
        # Ejecutar la función async
        try:
            result = asyncio.run(generar_audio_desde_texto(texto, voz, velocidad, outpath))
        except Exception as e:
            print(f"[ERROR] Error en asyncio.run: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            raise
        
        print(f"[DEBUG] Resultado de generación: {result}")
        
        if not result:
            print(f"[ERROR] Generación falló para {archivo} capítulo {capitulo}")
            return jsonify({'success': False, 'error': 'Error generando audio'}), 500

        # Verificar que el archivo existe
        if not outpath.exists():
            print(f"[ERROR] Archivo de salida no existe: {outpath}")
            return jsonify({'success': False, 'error': 'Archivo no generado'}), 500
        
        size = outpath.stat().st_size
        print(f"[DEBUG] Audio generado: {size} bytes")

        # Construir nombre de descarga bonito: "Capítulo - Libro - Autor.mp3"
        chap_title = ''
        try:
            chaps = epub_cargado.get('chapters', [])
            if chaps and int(capitulo) < len(chaps):
                chap_title = chaps[int(capitulo)].get('title', '')
        except Exception as e:
            print(f"[DEBUG] No se pudo obtener título del capítulo: {e}")
        
        book_title = epub_cargado.get('title', '')
        book_author = epub_cargado.get('author', '')

        def sanitize(name: str) -> str:
            if not name:
                return ''
            return ''.join(c for c in name if c.isalnum() or c in (' ', '-', '_')).strip()

        parts = [sanitize(chap_title), sanitize(book_title), sanitize(book_author)]
        parts = [p for p in parts if p]  # Filtrar vacíos
        download_name = ' - '.join(parts) + '.mp3' if parts else filename

        return jsonify({'success': True, 'filename': filename, 'audio': f'/media/pdf_audio/{filename}', 'download_name': download_name} )
    except Exception as e:
        print(f"[ERROR] Excepción en generar_epub: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/debug-epub', methods=['GET'])
def debug_epub():
    """Endpoint de depuración: muestra info del EPUB cargado y una muestra de texto del capítulo 0."""
    try:
        if not epub_cargado['path']:
            return jsonify({'exists': False, 'error': 'No hay EPUB cargado'}), 400
        path = epub_cargado['path']
        from app.utils import obtener_capitulos_epub, extraer_texto_epub
        exists = os.path.exists(path)
        # preferir datos almacenados en memoria
        if epub_cargado.get('chapters'):
            chapters = epub_cargado.get('chapters')
            book_title = epub_cargado.get('title', '')
            book_author = epub_cargado.get('author', '')
        else:
            cap_info = obtener_capitulos_epub(path)
            chapters = cap_info.get('chapters', [])
            book_title = cap_info.get('title', '')
            book_author = cap_info.get('author', '')
        sample = extraer_texto_epub(path, 0)[:500]
        return jsonify({'exists': exists, 'path': path, 'chapters_count': len(chapters), 'chapters': chapters, 'title': book_title, 'author': book_author, 'sample_text_start': sample})
    except Exception as e:
        return jsonify({'exists': False, 'error': str(e)}), 500

@app.route('/media/<tipo>/<filename>')
def descargar_audio(tipo, filename):
    """Descarga un archivo de audio"""
    try:
        if tipo == 'text_audio':
            filepath = TEXT_AUDIO_FOLDER / filename
        elif tipo == 'pdf_audio':
            filepath = PDF_AUDIO_FOLDER / filename
        else:
            return jsonify({'error': 'Tipo inválido'}), 400
        
        if not filepath.exists():
            return jsonify({'error': 'Archivo no encontrado'}), 404
        
        return send_file(str(filepath), as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    """Error 404"""
    return jsonify({'error': 'Página no encontrada'}), 404

@app.errorhandler(500)
def server_error(error):
    """Error 500"""
    return jsonify({'error': 'Error del servidor'}), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("[AUDIO] Edge-TTS Web - Aplicacion Principal")
    print("="*60)
    print("\nWeb: http://localhost:5000")
    print("Presiona Ctrl+C para detener\n")
    
    app.run(debug=True, host='127.0.0.1', port=5000)
