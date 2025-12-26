# 🎵 AudioVerse

Convierte texto, PDFs y EPUBs a audio con voces neurales en tiempo real. Una herramienta minimalista y profesional para crear audiolibros y contenido de audio.

## ✨ Características

- ✅ **Texto a Audio**: Convierte hasta 1000 palabras a voz natural
- ✅ **PDF a Audio**: Lee PDFs con barra de progreso y selección de páginas
- ✅ **EPUB a Audio**: Carga libros electrónicos y escucha mientras lees
- ✅ **Voces Neurales**: 4 voces diferentes en español (Microsoft Edge)
- ✅ **Control de Velocidad**: Desde 0.5x hasta 2.0x
- ✅ **Barra de Progreso**: Visualiza el estado de carga en tiempo real
- ✅ **Reproducción Integrada**: Escucha en la plataforma
- ✅ **Descarga MP3**: Guarda tu audio localmente
- ✅ **100% Gratis**: Sin registro ni publicidad
- ✅ **Privado**: Tus datos no se guardan

## 🚀 Inicio Rápido

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar
python main.py

# 3. Abrir en navegador
http://localhost:5000
```

## 📋 Requisitos

Python 3.8+ con las siguientes librerías:
- Flask 3.0.0
- edge-tts 6.1.12
- pdfplumber 0.10.3
- python-multipart 0.0.6

## 🎯 Cómo Usar

### Texto a Audio
1. Selecciona "Convertidor" → "Texto"
2. Elige voz y velocidad
3. Escribe tu texto (máx 1000 palabras)
4. Haz clic en "Generar Audio"
5. Descarga el MP3

### PDF a Audio
1. Ve a "Convertidor" → "PDF"
2. Carga tu PDF (verás el % de progreso)
3. Selecciona el rango de páginas
4. Genera el audio
5. Descarga tu audiolibro

### EPUB a Audio  
1. Abre "Convertidor" → "EPUB"
2. Carga tu archivo EPUB
3. Selecciona el capítulo
4. Escucha mientras lees
5. Descarga el audio

## 📁 Estructura

```
audioverse/
├── app/
│   ├── __init__.py
│   ├── utils.py
│   ├── static/
│   │   ├── css/style.css       (Estilos minimalistas)
│   │   └── js/script.js        (Lógica + progreso + EPUB)
│   └── templates/
│       └── index.html          (4 tabs + 3 conversores)
├── main.py                      (Servidor Flask)
├── config.py                    (Configuración)
├── requirements.txt             (Dependencias)
└── README.md
```
├── config.py                ← Configuración centralizada
├── requirements.txt         ← Dependencias Python
├── verificar.py             ← Verificar instalación
│
├── app/                     ← Paquete principal
│   ├── __init__.py
│   ├── utils.py             ← Funciones de procesamiento
│   ├── static/
│   │   ├── css/style.css    ← Estilos
│   │   └── js/script.js     ← JavaScript interactivo
│   └── templates/
│       └── index.html       ← HTML template
│
├── media/                   ← Audios generados (automático)
│   ├── text_audio/          ← Audios desde texto
│   └── pdf_audio/           ← Audios desde PDF
│
├── uploads/                 ← PDFs subidos (automático)
└── logs/                    ← Logs de la app (automático)
```

## ✨ Características

### 📝 Convertir Texto a Audio
- Límite: 1000 palabras
- Entrada: Escribe o pega directamente
- Salida: MP3 descargable

### 📄 Convertir PDF a Audio  
- Carga: Drag & drop o selector
- Selecciona: 1-50 páginas específicas (ideal capítulos)
- Salida: MP3 descargable

### ⚡ Control de Velocidad (0.5x a 2.0x)
- Como un control de volumen
- 0.5x: Más lento y claro
- 1.0x: Velocidad normal
- 2.0x: Más rápido

### 🎤 4 Voces Naturales en Español
1. **es-ES-ElviraNeural** - Mujer española (natural, cálida)
2. **es-ES-AlvaroNeural** - Hombre español (profundo)
3. **es-MX-DaliaNeural** - Mujer mexicana (clara)
4. **es-AR-EloiseNeural** - Mujer argentina (expresiva)

### ▶️ Reproductor Integrado
- Escucha antes de descargar
- Controles estándar de audio
- Descarga cuando esté listo

## 📋 Instalación

### Requisitos
- Python 3.8+
- pip (gestor de paquetes)

### Pasos

1. **Clonar o descargar el proyecto**
   ```bash
   cd tu_carpeta
   ```

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar la aplicación**
   ```bash
   python main.py
   ```

4. **Abre en navegador**
   ```
   http://localhost:5000
   ```

## 🔧 Configuración

Edita [config.py](config.py) para cambiar:

```python
MAX_PALABRAS_TEXTO = 1000        # Límite de palabras
MAX_PAGINAS_PDF = 50              # Páginas máximo PDF
DEBUG = True                      # Modo desarrollo
```

## 📦 Dependencias

```
flask==3.0.0
edge-tts==6.1.12
pdfplumber==0.10.3
pydub==0.25.1
```

Ver más: [requirements.txt](requirements.txt)

## 🎯 Casos de uso

| Caso | Tipo | Velocidad |
|------|------|-----------|
| Artículo a audio | Texto | Normal |
| Solo 2-3 capítulos | PDF (2-3 págs) | Normal |
| Audiolibro completo | PDF (50 págs) | Normal |
| Escuchar rápido | Cualquiera | 1.5x - 2.0x |
| Comprender mejor | Cualquiera | 0.5x - 0.75x |

## 🌐 Ventajas

✅ **Gratuito** - Sin costos, sin API key  
✅ **Offline** - Funciona después de instalar  
✅ **Voces naturales** - Redes neurales de Microsoft  
✅ **Multiidioma** - Excelente español  
✅ **Sin GPU** - Corre en cualquier PC  
✅ **Reproductor integrado** - Escucha antes de descargar  
✅ **Estructura profesional** - Código limpio y mantenible

## 🛠️ Desarrollo

### Estructura de carpetas
```
app/utils.py          - Lógica de TTS (generar audios)
app/static/           - CSS y JavaScript
app/templates/        - HTML templates
config.py             - Configuración centralizada
main.py               - Rutas Flask y servidor
```

### Agregar funcionalidad
1. Rutas → modificar [main.py](main.py)
2. Lógica → modificar [app/utils.py](app/utils.py)
3. Frontend → modificar [app/templates/index.html](app/templates/index.html)

## 📚 Recursos

- [Edge-TTS GitHub](https://github.com/rany2/edge-tts)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [pdfplumber Documentation](https://github.com/jsvine/pdfplumber)

## 💡 Troubleshooting

### La web no carga
```bash
python verificar.py  # Verifica dependencias
```

### Error de Internet
Edge-TTS necesita conexión para descargar voces. Verifica tu conexión.

### Audio muy lento/rápido
Ajusta el slider ⚡ **Velocidad** en la aplicación.

## 📝 Licencia

MIT License - Libre para usar y modificar

---

**Creado con ❤️ usando Edge-TTS y Flask**

Última actualización: 25 de diciembre de 2025

## 📁 Archivos disponibles

### 1. **prueba_tts.py** - Script simple de prueba
```bash
python prueba_tts.py
```
✅ Genera un audio simple de prueba (`prueba.mp3`)

### 2. **tts_avanzado.py** - Script con funciones avanzadas
```bash
python tts_avanzado.py
```
- Función para convertir texto a audio
- Función para convertir PDF a audio
- Ejemplos de uso

### 3. **tts_interactivo.py** - Menú interactivo (RECOMENDADO)
```bash
python tts_interactivo.py
```
Interfaz completa con menú para:
- Convertir texto a audio
- Convertir PDF a audio
- Elegir voces
- Nombrar archivos de salida

## 🎤 Voces disponibles en español

| Código | Nombre | Tipo |
|--------|--------|------|
| `es-ES-ElviraNeural` | Mujer española | Natural, cálida |
| `es-ES-AlvaroNeural` | Hombre español | Natural, profundo |
| `es-MX-DaliaNeural` | Mujer mexicana | Natural, clara |
| `es-AR-EloiseNeural` | Mujer argentina | Natural, expresiva |

## 💡 Ejemplo rápido

```python
import asyncio
import edge_tts

async def main():
    texto = "Hola, esto es una prueba"
    communicate = edge_tts.Communicate(texto, "es-ES-ElviraNeural")
    await communicate.save("salida.mp3")

asyncio.run(main())
```

## 🎯 Ventajas

✅ **Gratuito** - Sin costos ni API key  
✅ **Offline** - Funciona después de instalar la lib  
✅ **Voces naturales** - Redes neurales de Microsoft Edge  
✅ **Multiidioma** - Excelente español incluido  
✅ **Sin GPU** - Funciona en cualquier máquina  

## 📚 Recursos

- [Documentación Edge-TTS](https://github.com/rany2/edge-tts)
- [Proyecto Audiolibros: epub2tts-edge](https://github.com/search?q=epub2tts-edge)

---

**¡Disfruta creando audiolibros y contenido de audio!** 🎉
