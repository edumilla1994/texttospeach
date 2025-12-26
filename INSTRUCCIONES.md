# 🎵 Edge-TTS Web - Documentación Técnica Completa

## ✅ Instalación completada

Todos los componentes están listos para usar.

## 🚀 Iniciar la aplicación web

```bash
python main.py
```

Luego abre en tu navegador:
```
http://localhost:5000
```

## 📁 Estructura del proyecto

```
251225/
├── main.py                         ← EJECUTAR ESTO - Aplicación Flask
├── config.py                       ← Configuración centralizada
├── verificar.py                    ← Verificar dependencias
├── requirements.txt                ← Dependencias del proyecto
├── QUICK_START.txt                 ← Guía rápida
├── README.md                       ← Documentación para usuarios
│
├── app/                            ← Paquete principal
│   ├── __init__.py
│   ├── utils.py                    ← Funciones: generar audio, procesar PDF
│   ├── templates/
│   │   └── index.html              ← Template HTML con 2 tabs
│   └── static/
│       ├── css/
│       │   └── style.css           ← Estilos responsivos
│       └── js/
│           └── script.js           ← Interactividad frontend
│
├── media/                          ← Audios generados (automático)
│   ├── text_audio/                 ← Audios desde texto
│   └── pdf_audio/                  ← Audios desde PDF
│
├── uploads/                        ← PDFs subidos (automático)
└── logs/                           ← Logs de aplicación (automático)
```

## 🎯 Características principales

### ✍️ Convertir Texto a Audio
- **Límite**: 1000 palabras
- **Entrada**: Escribe o pega en textarea
- **Contador**: Palabra count en tiempo real
- **Salida**: MP3 descargable y reproducible

### 📄 Convertir PDF a Audio  
- **Subir**: Drag & drop o selector de archivos
- **Detección**: Número de páginas automático
- **Rango**: Selecciona 1-50 páginas específicas
- **Extracción**: Usar pdfplumber
- **Salida**: Audiolibro MP3

### ⚡ Control de Velocidad (0.5x a 2.0x)
- **Interfaz**: Slider (como control de volumen)
- **Rango**: 0.5x (lento) a 2.0x (rápido)
- **Conversión**: Transforma a formato Edge-TTS (+X%, -X%)
- **Efecto**: Cambia velocidad y duración del audio

### 🎤 Voces en español
1. **es-ES-ElviraNeural** - Mujer española (natural, cálida)
2. **es-ES-AlvaroNeural** - Hombre español (profundo, grave)
3. **es-MX-DaliaNeural** - Mujer mexicana (clara, moderna)
4. **es-AR-EloiseNeural** - Mujer argentina (expresiva, alegre)

### ▶️ Reproductor Integrado
- **HTML5 Audio**: Controls nativas del navegador
- **Preview**: Escucha antes de descargar
- **Descargar**: Botón para guardar MP3

## 💾 Gestión de archivos

### Audios generados
```
media/text_audio/      → Archivos desde texto
media/pdf_audio/       → Archivos desde PDF
```

### PDFs subidos
```
uploads/               → Almacenamiento temporal
```

### Logs
```
logs/                  → application.log
```

## 🔧 Arquitectura técnica

### Backend (main.py)

**Rutas API:**

```python
POST /api/generar-texto
  Parámetros: texto, voz, velocidad
  Retorna: { filename, url, message }

POST /api/generar-pdf
  Parámetros: paginas, voz, velocidad  
  Retorna: { filename, url, message }

POST /api/upload-pdf
  Parámetros: file (PDF)
  Retorna: { filepath, pages, message }

GET /media/<tipo>/<filename>
  Tipo: text_audio o pdf_audio
  Retorna: Stream MP3 (descargable)
```

### Utils (app/utils.py)

```python
calcular_rate(velocidad: float) → str
  Convierte 0.5-2.0 a formato Edge-TTS

generar_audio_desde_texto(texto, voz, velocidad) → str
  Async, retorna nombre del archivo

generar_audio_desde_pdf(paginas, voz, velocidad) → str
  Async, procesa PDF y genera audio

extraer_texto_pdf(ruta, paginas) → str
  Extrae texto con pdfplumber

obtener_info_pdf(ruta) → dict
  Retorna { "pages": N }
```

### Frontend (HTML/JS/CSS)

**JavaScript (script.js):**
- `generarAudioTexto()` - Valida, envía POST, reproduce audio
- `generarAudioPDF()` - Maneja PDF, extrae páginas, genera
- `cargarPDF()` - Upload con FormData
- `mostrarPlayer()` - Carga audio en reproductor
- `descargarAudio()` - Crea link descarga temporal

**HTML (index.html):**
- 2 tabs con data-tab: "texto" y "pdf"
- Textarea con contador de palabras
- Slider velocidad (0.5 a 2.0)
- Selector de voces
- Área drop PDF
- Audio player HTML5

**CSS (style.css):**
- Gradient fondo (morado/azul)
- Cards con shadow
- Responsive max-width 700px
- Tabs dinámicas
- Spinner animado
- Player box con gradiente

## ⚙️ Configuración (config.py)

```python
# Límites
MAX_PALABRAS_TEXTO = 1000
MAX_PAGINAS_PDF = 50
MAX_ARCHIVO_PDF = 50 * 1024 * 1024  # 50MB

# Voces
VOCES_ESPANOL = {
    'elvira': 'es-ES-ElviraNeural',
    'alvaro': 'es-ES-AlvaroNeural',
    'dalia': 'es-MX-DaliaNeural',
    'eloise': 'es-AR-EloiseNeural'
}

# Carpetas
UPLOAD_FOLDER = BASE_DIR / 'uploads'
MEDIA_FOLDER = BASE_DIR / 'media'
```

## 🔄 Flujo de generación

### Texto → Audio
```
1. Usuario escribe texto
2. JavaScript valida (max 1000 palabras)
3. POST a /api/generar-texto
4. Backend:
   - Valida entrada
   - Llama edge_tts.Communicate()
   - Guarda en media/text_audio/
   - Retorna URL
5. Frontend reproduce en player
6. Usuario descarga
```

### PDF → Audio
```
1. Usuario carga PDF
2. POST a /api/upload-pdf
3. Backend detecta páginas
4. Usuario selecciona rango (1-50)
5. POST a /api/generar-pdf
6. Backend:
   - Extrae texto con pdfplumber
   - Concatena páginas
   - Genera audio con edge_tts
   - Guarda en media/pdf_audio/
7. Frontend reproduce
8. Usuario descarga
```

## 📊 Casos de uso

| Caso | Entrada | Velocidad | Uso |
|------|---------|-----------|-----|
| Artículo corto | Texto <500 pabs | Normal | Lectura diaria |
| 1-2 capítulos | PDF 2-10 págs | Normal | Audiolibro parcial |
| Capítulo completo | PDF 10-30 págs | Normal | Sesión completa |
| Libro entero | PDF 30-50 págs | Normal | Audiolibro full |
| Escuchar rápido | Cualquiera | 1.5x-2.0x | Repaso rápido |
| Accesibilidad | Cualquiera | 0.5x-0.75x | Mejor comprensión |

## 🛠️ Extensiones posibles

### Agregar nueva voz
1. Editar `config.py`: `VOCES_ESPANOL`
2. Editar `app/templates/index.html`: agregar `<option>`

### Cambiar límite de palabras
1. `config.py`: `MAX_PALABRAS_TEXTO`
2. `app/static/js/script.js`: validar localmente

### Soportar otros idiomas
1. Agregar diccionario `VOCES_INGLES`, etc en `config.py`
2. Agregar tabs en HTML
3. Crear rutas nuevas en `main.py`

## ❓ Troubleshooting

### Error 500 en generar audio
- Verifica conexión a Internet
- Comprueba que Edge-TTS esté instalado: `pip install edge-tts==6.1.12`

### PDF no se carga
- Verifica que sea PDF válido (no cifrado)
- Máximo 50MB recomendado

### Texto no se genera
- Máximo 1000 palabras (checar contador)
- Verifica sintaxis en consola del navegador (F12)

### Audio suena mal
- Prueba otra velocidad
- Prueba otra voz
- Comprueba calidad del micrófono original

## 📚 Dependencias

```
flask==3.0.0          - Framework web
edge-tts==6.1.12      - TTS neural Microsoft
pdfplumber==0.10.3    - Extracción PDF
pydub==0.25.1         - Manipulación audio
```

## 📝 Código importante

### Cálculo de velocidad
```python
def calcular_rate(velocidad):
    rate_value = round((velocidad - 1.0) * 100)
    return f"+{rate_value}%"  # Siempre con +
```

### Generar audio
```python
async def generar_audio_desde_texto(texto, voz, velocidad):
    rate = calcular_rate(velocidad)
    communicate = edge_tts.Communicate(text=texto, voice=voz, rate=rate)
    await communicate.save(ruta_archivo)
```

### Extraer PDF
```python
def extraer_texto_pdf(ruta, paginas):
    with pdfplumber.open(ruta) as pdf:
        texto = ""
        for i in paginas:
            texto += pdf.pages[i-1].extract_text()
    return texto
```

## 🎨 Diseño responsivo

- **Desktop**: Ancho máximo 700px, centrado
- **Tablet**: Full width con padding
- **Mobile**: Touch-friendly, botones grandes
- **Dark/Light**: Compatible ambos modos navegador

---

**Última actualización**: 25 de diciembre de 2025  
**Versión**: 1.0 - Production Ready  
**Framework**: Flask 3.0.0  
**Python**: 3.8+

Para más info: Ver README.md o QUICK_START.txt
