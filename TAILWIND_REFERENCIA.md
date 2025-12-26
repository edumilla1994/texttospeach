═══════════════════════════════════════════════════════════════════════════
   🎨 REFERENCIA DE DISEÑO - TAILWIND CSS
═══════════════════════════════════════════════════════════════════════════

🏗️ ESTRUCTURA HTML
────────────────────────────────────────────────────────────────────────────

HTML5 Semántico
  ├── <header>           Header principal con gradiente
  ├── <nav>              Navegación sticky con 4 tabs
  └── <main>
      ├── #inicio-tab    Página de inicio
      ├── #convertidor-tab  Convertidor (con subtabs)
      ├── #instrucciones-tab  Cómo usar
      └── #info-tab      Información

🎨 TAILWIND CSS UTILITIES USADOS
────────────────────────────────────────────────────────────────────────────

LAYOUT
  • container mx-auto px-4        - Contenedor responsivo
  • grid grid-cols-1 md:grid-cols-3 - Grid responsivo
  • flex justify-between items-center - Flexbox
  • gap-6 space-y-4              - Espaciado

COLORES
  • bg-gradient-to-r from-purple-600 to-purple-800 - Gradiente
  • text-white text-gray-600     - Colores de texto
  • border-gray-200 border-purple-200 - Bordes
  • hover:shadow-lg hover:scale-105 - Estados hover

TIPOGRAFÍA
  • text-4xl font-bold           - Títulos grandes
  • text-xl font-semibold        - Subtítulos
  • text-sm text-gray-600        - Textos pequeños
  • font-family: Poppins         - Fuente principal

ESPACIADO
  • p-6 px-4 py-3               - Padding
  • m-4 mb-6 mt-2               - Margen
  • gap-3 gap-6                 - Gap en flex/grid
  • rounded-lg rounded-full      - Border radius

EFECTOS
  • shadow shadow-lg shadow-xl   - Sombras
  • transition transform         - Animaciones
  • opacity-50 opacity-0         - Transparencia
  • hover:scale-105             - Escala hover

RESPONSIVE
  • hidden md:flex              - Mostrar solo en desktop
  • md:grid-cols-3 lg:col-span-2 - Responsive grid
  • w-full flex-1 max-w-xs      - Ancho responsivo

🎯 ESTRUCTURA DE TABS
────────────────────────────────────────────────────────────────────────────

NAVEGACIÓN PRINCIPAL (sticky)
  ├── nav-tab (data-tab="inicio")      [🏠 Inicio]
  ├── nav-tab (data-tab="convertidor") [✨ Convertidor]
  ├── nav-tab (data-tab="instrucciones") [📚 Cómo usar]
  └── nav-tab (data-tab="info")        [ℹ️ Información]

ESTADOS
  • active: text-purple-600 border-b-2 border-purple-600
  • inactive: text-gray-600 hover:text-gray-900

CONTENIDO
  • Cada tab tiene un div con id="{tabname}-tab"
  • Al hacer click en nav-tab: se activa el tab correspondiente
  • Clases hidden/visible para mostrar/ocultar

📦 COMPONENTES REUTILIZABLES
────────────────────────────────────────────────────────────────────────────

CARD (Tarjeta)
  <div class="bg-white p-6 rounded-lg shadow card-hover">
    • bg-white: Fondo blanco
    • p-6: Padding interno
    • rounded-lg: Bordes redondeados
    • shadow: Sombra
    • card-hover: Efecto hover personalizado

BOTÓN PRIMARIO
  <button class="gradient-bg text-white px-8 py-4 rounded-lg 
                  font-semibold hover:shadow-lg transform hover:scale-105">
    • gradient-bg: Gradiente personalizado
    • px-8 py-4: Padding horizontal y vertical
    • hover:shadow-lg: Sombra al pasar mouse
    • transform hover:scale-105: Escala 105% en hover

INPUT/TEXTAREA
  <input class="input-field w-full px-4 py-2 border border-gray-300 
                 rounded-lg focus:ring-2 focus:ring-purple-500">
    • w-full: Ancho completo
    • border: Borde visible
    • focus:ring-2: Anillo en focus
    • input-field: Transiciones personalizadas

MENSAJE
  <div class="bg-green-50 border border-green-200 text-green-700 
              px-4 py-3 rounded-lg flex items-center gap-2">
    <i class="fas fa-check-circle"></i>
    <span>Mensaje de éxito</span>
  </div>
    • bg-{color}-50: Fondo pastel
    • border-{color}-200: Borde
    • text-{color}-700: Texto oscuro
    • flex items-center: Alineación

🎬 ANIMACIONES PERSONALIZADAS
────────────────────────────────────────────────────────────────────────────

SPINNER (Carga)
  <div class="spinner"></div>
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

FADE-IN (Entrada suave)
  @keyframes fadeIn {
      from { opacity: 0; }
      to { opacity: 1; }
  }
  .fadeIn { animation: fadeIn 0.3s ease-in; }

CARD HOVER (Efecto levantamiento)
  .card-hover:hover {
      transform: translateY(-4px);
      box-shadow: 0 20px 25px rgba(0,0,0,0.1);
  }

🎤 VOCES - GALERÍA CON GRADIENTES
────────────────────────────────────────────────────────────────────────────

Estructura por voz:
  <div class="p-4 bg-gradient-to-br from-{color}-50 to-{color}-100 
              rounded-lg border border-{color}-200">
    • from-{color}-50: Gradiente claro arriba
    • to-{color}-100: Gradiente oscuro abajo
    • border-{color}-200: Borde con color

Colores asignados:
  • Elvira: Red gradient (from-red-50 to-red-100)
  • Álvaro: Blue gradient (from-blue-50 to-blue-100)
  • Dalia: Green gradient (from-green-50 to-green-100)
  • Eloise: Purple gradient (from-purple-50 to-purple-100)

📱 RESPONSIVE BREAKPOINTS
────────────────────────────────────────────────────────────────────────────

Mobile (default)
  • Ancho completo (w-full)
  • 1 columna (grid-cols-1)
  • Elementos apilados

Tablet (md: 768px)
  • md:grid-cols-2 o md:grid-cols-3
  • md:flex / md:block
  • Layouts adaptados

Desktop (lg: 1024px)
  • Diseño completo
  • Múltiples columnas
  • Elementos lado a lado

🔍 SELECTORES IMPORTANTES
────────────────────────────────────────────────────────────────────────────

Elementos del DOM
  • .tab-content: Contenedor de tab (puede estar hidden)
  • .nav-tab: Botón de navegación principal
  • .conv-tab: Botón de conversión (Texto/PDF)
  • .conv-content: Contenedor de conversión
  • .card-hover: Card con efecto hover
  • .upload-drag: Área de upload con drag-drop
  • .spinner: Indicador de carga

Estados
  • .active: Tab activo
  • .hidden: Elemento oculto (display: none)
  • .drag-over: Drag-drop activo
  • :focus: Input enfocado
  • :hover: Hover en elemento

⚡ VENTAJAS DE TAILWIND VS CUSTOM CSS
────────────────────────────────────────────────────────────────────────────

Tailwind CSS
  ✅ Clases reutilizables
  ✅ Consistencia visual
  ✅ Responsive out-of-the-box
  ✅ Cambios rápidos sin tocar CSS
  ✅ CDN (sin instalación)
  ✅ Purge automático en producción
  ✅ Documentación excelente

Custom CSS
  ❌ Más código CSS
  ❌ Difícil mantener consistencia
  ❌ Duplicación de estilos
  ❌ Más propenso a errores

🎨 PALETA DE COLORES COMPLETA
────────────────────────────────────────────────────────────────────────────

Grays
  • gray-50: #f9fafb (Fondo muy claro)
  • gray-100: #f3f4f6 (Fondo claro)
  • gray-200: #e5e7eb (Bordes)
  • gray-600: #4b5563 (Texto secundario)
  • gray-900: #111827 (Texto principal)

Purples (Primario)
  • purple-100: #f3e8ff
  • purple-200: #e9d5ff
  • purple-600: #9333ea (Primario)
  • purple-800: #6b21a8

Colors (Estados)
  • green-50: #f0fdf4 (Éxito bg)
  • green-500: #22c55e (Éxito texto)
  • red-50: #fef2f2 (Error bg)
  • red-500: #ef4444 (Error texto)
  • blue-50: #eff6ff (Info bg)
  • blue-500: #3b82f6 (Info texto)

🚀 TIPS DE DESARROLLO
────────────────────────────────────────────────────────────────────────────

1. Cambiar colores primarios
   Búsqueda y reemplazo:
   • purple-600 → tu-color-600
   • purple-100 → tu-color-100
   
2. Agregar nuevas secciones
   • Crear nuevo div con id="{nombre}-tab"
   • Crear nuevo botón nav-tab con data-tab="{nombre}"
   • JavaScript lo detectará automáticamente

3. Modificar tamaño de fuentes
   • text-4xl: Títulos principales
   • text-2xl: Subtítulos
   • text-xl: Encabezados
   • text-base: Texto normal
   • text-sm: Texto pequeño
   • text-xs: Texto muy pequeño

4. Agregar efectos adicionales
   • hover:bg-gray-100: Background en hover
   • focus:outline-none focus:ring: Focus styling
   • transition duration-300: Transiciones suaves

5. Responsive best practices
   • Mobile-first (base styles)
   • md: para tablet
   • lg: para desktop
   • hidden md:flex: Mostrar solo en desktop

═══════════════════════════════════════════════════════════════════════════

Última actualización: 25 de diciembre, 2025
Versión: 2.0 (Tailwind CSS)

Para más info: Revisa app/templates/index.html y app/static/css/style.css

═══════════════════════════════════════════════════════════════════════════
