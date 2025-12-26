// ========== MOSTRAR TABS ==========
function mostrarTab(nombre) {
    // Ocultar todos los tabs
    document.querySelectorAll('.tab-main').forEach(tab => {
        tab.classList.add('hidden');
    });
    
    // Mostrar el seleccionado
    const tab = document.getElementById(nombre);
    if (tab) {
        tab.classList.remove('hidden');
        
        // Actualizar botones activos
        document.querySelectorAll('.nav-btn-main').forEach(btn => {
            btn.classList.remove('active');
        });
        
        // Marcar botón actual como activo
        const btns = document.querySelectorAll('.nav-btn-main');
        btns.forEach(btn => {
            if (btn.getAttribute('onclick').includes(`'${nombre}'`)) {
                btn.classList.add('active');
            }
        });
    }
}

// ========== ELEMENTOS ==========
let pdfCargado = false;
let pdfPath = "";
let epubCargado = false;
let epubData = null;

// Elementos del DOM
const elementos = {
    // General
    voz: document.getElementById('voz'),
    velocidad: document.getElementById('velocidad'),
    velocidadValor: document.getElementById('velocidadValor'),
    
    // Texto
    textoInput: document.getElementById('textoInput'),
    wordCount: document.getElementById('wordCount'),
    wordBar: document.getElementById('wordBar'),
    btnTexto: document.getElementById('btnTexto'),
    loadingTexto: document.getElementById('loadingTexto'),
    
    // PDF
    uploadArea: document.getElementById('uploadArea'),
    pdfFile: document.getElementById('pdfFile'),
    fileName: document.getElementById('fileName'),
    fileNameText: document.getElementById('fileNameText'),
    uploadProgress: document.getElementById('uploadProgress'),
    progressBar: document.getElementById('progressBar'),
    progressPercent: document.getElementById('progressPercent'),
    paginasDesde: document.getElementById('paginasDesde'),
    paginasHasta: document.getElementById('paginasHasta'),
    btnPDF: document.getElementById('btnPDF'),
    loadingPDF: document.getElementById('loadingPDF'),
    
    // EPUB
    uploadAreaEpub: document.getElementById('uploadAreaEpub'),
    epubFile: document.getElementById('epubFile'),
    fileNameEpub: document.getElementById('fileNameEpub'),
    fileNameTextEpub: document.getElementById('fileNameTextEpub'),
    uploadProgressEpub: document.getElementById('uploadProgressEpub'),
    progressBarEpub: document.getElementById('progressBarEpub'),
    progressPercentEpub: document.getElementById('progressPercentEpub'),
    epubChapter: document.getElementById('epubChapter'),
    btnEpub: document.getElementById('btnEpub'),
    loadingEpub: document.getElementById('loadingEpub'),
    paginasDesde: document.getElementById('paginasDesde'),
    paginasHasta: document.getElementById('paginasHasta'),
    btnPDF: document.getElementById('btnPDF'),
    loadingPDF: document.getElementById('loadingPDF'),
    
    // Mensajes
    msgSuccess: document.getElementById('msgSuccess'),
    msgError: document.getElementById('msgError'),
    msgInfo: document.getElementById('msgInfo'),
    msgSuccessText: document.getElementById('msgSuccessText'),
    msgErrorText: document.getElementById('msgErrorText'),
    msgInfoText: document.getElementById('msgInfoText'),
    
    // Reproductor
    playerBox: document.getElementById('playerBox'),
    audioPlayer: document.getElementById('audioPlayer'),
    downloadBtn: document.getElementById('downloadBtn'),
};

// ========== INICIALIZAR ==========
document.addEventListener('DOMContentLoaded', () => {
    // Mostrar tab inicial
    mostrarTab('inicio');
    
    // Inputs
    elementos.velocidad.addEventListener('change', actualizarVelocidad);
    elementos.velocidad.addEventListener('input', actualizarVelocidad);
    elementos.textoInput.addEventListener('input', contarPalabras);
    elementos.btnTexto.addEventListener('click', generarAudioTexto);
    elementos.btnPDF.addEventListener('click', generarAudioPDF);
    elementos.downloadBtn.addEventListener('click', descargarAudio);
    
    // PDF upload
    elementos.uploadArea.addEventListener('click', () => elementos.pdfFile.click());
    elementos.pdfFile.addEventListener('change', cargarPDF);
    elementos.uploadArea.addEventListener('dragover', handleDragOver);
    elementos.uploadArea.addEventListener('dragleave', handleDragLeave);
    elementos.uploadArea.addEventListener('drop', handleDrop);
    
    // Tabs de conversión
    document.querySelectorAll('.conv-btn').forEach(btn => {
        btn.addEventListener('click', cambiarConvTab);
    });
});

// ========== FUNCIONES BÁSICAS ==========
function actualizarVelocidad() {
    const valor = parseFloat(elementos.velocidad.value);
    elementos.velocidadValor.textContent = valor.toFixed(1) + 'x';
}

function contarPalabras() {
    const texto = elementos.textoInput.value;
    const palabras = texto.trim() ? texto.split(/\s+/).length : 0;
    const maximo = 1000;
    
    elementos.wordCount.textContent = palabras;
    const porcentaje = Math.min((palabras / maximo) * 100, 100);
    if (elementos.wordBar) elementos.wordBar.style.width = porcentaje + '%';
    
    if (palabras > maximo) {
        elementos.btnTexto.disabled = true;
        elementos.textoInput.style.borderColor = '#ef4444';
    } else {
        elementos.btnTexto.disabled = false;
        elementos.textoInput.style.borderColor = '';
    }
}

function mostrarMensaje(tipo, texto) {
    const elemento = elementos[`msg${tipo}`];
    if (!elemento) return;
    
    const elementoTexto = elementos[`msg${tipo}Text`];
    if (elementoTexto) {
        elementoTexto.textContent = texto;
    } else {
        elemento.textContent = texto;
    }
    
    elemento.classList.remove('hidden');
    setTimeout(() => elemento.classList.add('hidden'), 5000);
}

function mostrarPlayer(show, url = null) {
    if (show && url) {
        elementos.audioPlayer.src = url;
        elementos.playerBox.classList.remove('hidden');
    } else {
        elementos.playerBox.classList.add('hidden');
    }
}

function descargarAudio() {
    const url = elementos.audioPlayer.src;
    if (!url) return;
    
    const link = document.createElement('a');
    link.href = url;
    link.download = 'audio.mp3';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// ========== TABS DE CONVERSIÓN ==========
function cambiarConvTab(e) {
    const convName = e.currentTarget.dataset.conv;
    
    // Actualizar botones
    document.querySelectorAll('.conv-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    e.currentTarget.classList.add('active');
    
    // Actualizar contenido
    document.querySelectorAll('.conv-content').forEach(el => {
        el.style.display = 'none';
    });
    document.getElementById(`${convName}-conv`).style.display = 'block';
}

// ========== MANEJO DE PDF ==========
function cargarPDF(e) {
    const file = e.target.files[0];
    if (!file) return;
    
    const formData = new FormData();
    formData.append('file', file);
    
    // Mostrar barra de progreso
    const intervalo = simularProgresoDescarga();
    elementos.loadingPDF.classList.remove('hidden');
    mostrarPlayer(false);
    mostrarMensaje('Info', '📤 Cargando PDF...');
    
    fetch('/api/upload-pdf', {
        method: 'POST',
        body: formData
    })
    .then(r => r.json())
    .then(data => {
        clearInterval(intervalo);
        elementos.uploadProgress.classList.add('hidden');
        elementos.progressBar.style.width = '0%';
        elementos.progressPercent.textContent = '0%';
        elementos.loadingPDF.classList.add('hidden');
        
        if (data.success) {
            pdfCargado = true;
            pdfPath = data.path;
            elementos.fileNameText.textContent = `${data.filename} (${data.paginas} páginas)`;
            elementos.fileName.classList.remove('hidden');
            elementos.btnPDF.disabled = false;
            elementos.paginasDesde.max = data.paginas;
            elementos.paginasHasta.max = data.paginas;
            elementos.paginasHasta.value = Math.min(5, data.paginas);
            mostrarMensaje('Success', `✅ PDF cargado: ${data.paginas} páginas`);
        } else {
            mostrarMensaje('Error', `❌ ${data.error || 'Error al cargar PDF'}`);
        }
    })
    .catch(err => {
        elementos.loadingPDF.classList.add('hidden');
        mostrarMensaje('Error', `❌ Error: ${err}`);
    });
}

// ========== GENERACIÓN DE AUDIO ==========
function generarAudioTexto() {
    const texto = elementos.textoInput.value.trim();
    if (!texto) {
        mostrarMensaje('Error', '❌ El texto está vacío');
        return;
    }
    
    const palabras = texto.split(/\s+/).length;
    if (palabras > 1000) {
        mostrarMensaje('Error', '❌ Máximo 1000 palabras');
        return;
    }
    
    elementos.loadingTexto.classList.remove('hidden');
    elementos.btnTexto.disabled = true;
    mostrarPlayer(false);
    mostrarMensaje('Info', '🎙️ Generando audio...');
    
    fetch('/api/generar-texto', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            texto: texto,
            voz: elementos.voz.value,
            velocidad: parseFloat(elementos.velocidad.value)
        })
    })
    .then(r => r.json())
    .then(data => {
        elementos.loadingTexto.classList.add('hidden');
        elementos.btnTexto.disabled = false;
        
        if (data.success) {
            mostrarMensaje('Success', '✅ Audio generado');
            mostrarPlayer(true, data.url);
        } else {
            mostrarMensaje('Error', `❌ ${data.error || 'Error'}`);
        }
    })
    .catch(err => {
        elementos.loadingTexto.classList.add('hidden');
        elementos.btnTexto.disabled = false;
        mostrarMensaje('Error', `❌ Error: ${err}`);
    });
}

function generarAudioPDF() {
    if (!pdfCargado) {
        mostrarMensaje('Error', '❌ Carga un PDF primero');
        return;
    }
    
    const desde = parseInt(elementos.paginasDesde.value) || 1;
    const hasta = parseInt(elementos.paginasHasta.value) || 1;
    
    if (desde > hasta) {
        mostrarMensaje('Error', '❌ Página inicial < final');
        return;
    }
    
    elementos.loadingPDF.classList.remove('hidden');
    elementos.btnPDF.disabled = true;
    mostrarPlayer(false);
    mostrarMensaje('Info', '📖 Procesando...');
    
    fetch('/api/generar-pdf', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            paginas: `${desde}-${hasta}`,
            voz: elementos.voz.value,
            velocidad: parseFloat(elementos.velocidad.value),
            pdf_path: pdfPath
        })
    })
    .then(r => r.json())
    .then(data => {
        elementos.loadingPDF.classList.add('hidden');
        elementos.btnPDF.disabled = false;
        
        if (data.success) {
            mostrarMensaje('Success', '✅ Audio generado');
            mostrarPlayer(true, data.url);
        } else {
            mostrarMensaje('Error', `❌ ${data.error || 'Error'}`);
        }
    })
    .catch(err => {
        elementos.loadingPDF.classList.add('hidden');
        elementos.btnPDF.disabled = false;
        mostrarMensaje('Error', `❌ Error: ${err}`);
    });
}

// ========== DRAG & DROP ==========
function handleDragOver(e) {
    e.preventDefault();
    elementos.uploadArea.classList.add('drag-over');
}

function handleDragLeave(e) {
    e.preventDefault();
    elementos.uploadArea.classList.remove('drag-over');
}

function handleDrop(e) {
    e.preventDefault();
    elementos.uploadArea.classList.remove('drag-over');
    
    const files = e.dataTransfer.files;
    if (files.length && files[0].type === 'application/pdf') {
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(files[0]);
        elementos.pdfFile.files = dataTransfer.files;
        cargarPDF({target: {files: dataTransfer.files}});
    } else {
        mostrarMensaje('Error', '❌ Solo PDFs');
    }
}

// ========== FUNCIÓN PARA SIMULAR PROGRESO PDF ==========
function simularProgresoDescarga() {
    elementos.uploadProgress.classList.remove('hidden');
    let progreso = 0;
    
    const intervalo = setInterval(() => {
        progreso += Math.random() * 30;
        if (progreso > 95) progreso = 95;
        
        elementos.progressBar.style.width = progreso + '%';
        elementos.progressPercent.textContent = Math.floor(progreso) + '%';
        
        if (progreso >= 95) {
            clearInterval(intervalo);
        }
    }, 300);
    
    return intervalo;
}

// ========== EPUB HANDLERS ==========
document.addEventListener('DOMContentLoaded', () => {
    // EPUB upload
    if (elementos.uploadAreaEpub) {
        elementos.uploadAreaEpub.addEventListener('click', () => elementos.epubFile.click());
        elementos.epubFile.addEventListener('change', cargarEPUB);
        elementos.uploadAreaEpub.addEventListener('dragover', (e) => {
            e.preventDefault();
            elementos.uploadAreaEpub.classList.add('drag-over');
        });
        elementos.uploadAreaEpub.addEventListener('dragleave', (e) => {
            e.preventDefault();
            elementos.uploadAreaEpub.classList.remove('drag-over');
        });
        elementos.uploadAreaEpub.addEventListener('drop', (e) => {
            e.preventDefault();
            elementos.uploadAreaEpub.classList.remove('drag-over');
            const files = e.dataTransfer.files;
            if (files.length && files[0].name.endsWith('.epub')) {
                const dataTransfer = new DataTransfer();
                dataTransfer.items.add(files[0]);
                elementos.epubFile.files = dataTransfer.files;
                cargarEPUB({target: {files: dataTransfer.files}});
            } else {
                mostrarMensaje('Error', '❌ Solo archivos EPUB');
            }
        });
    }
    
    if (elementos.btnEpub) {
        elementos.btnEpub.addEventListener('click', generarAudioEPUB);
    }
});

function cargarEPUB(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    simularProgresoDescargaEpub();
    
    setTimeout(() => {
        elementos.uploadProgressEpub.classList.add('hidden');
        elementos.progressBarEpub.style.width = '0%';
        elementos.progressPercentEpub.textContent = '0%';
        
        elementos.fileNameEpub.classList.remove('hidden');
        elementos.fileNameTextEpub.textContent = file.name;
        elementos.btnEpub.disabled = false;
        elementos.epubChapter.disabled = false;
        
        epubCargado = true;
        epubData = {
            nombre: file.name,
            tamaño: file.size
        };
        
        // Simular capítulos disponibles
        const capitulos = ['Introducción', 'Capítulo 1', 'Capítulo 2', 'Capítulo 3', 'Conclusión'];
        elementos.epubChapter.innerHTML = capitulos.map((cap, idx) => 
            `<option value="${idx}">${cap}</option>`
        ).join('');
        
        mostrarMensaje('Success', '✓ EPUB cargado correctamente');
    }, 2000);
}

function simularProgresoDescargaEpub() {
    elementos.uploadProgressEpub.classList.remove('hidden');
    let progreso = 0;
    
    const intervalo = setInterval(() => {
        progreso += Math.random() * 25;
        if (progreso > 95) progreso = 95;
        
        elementos.progressBarEpub.style.width = progreso + '%';
        elementos.progressPercentEpub.textContent = Math.floor(progreso) + '%';
        
        if (progreso >= 95) {
            clearInterval(intervalo);
        }
    }, 400);
    
    return intervalo;
}

async function generarAudioEPUB() {
    if (!epubCargado) {
        mostrarMensaje('Error', '❌ Carga un EPUB primero');
        return;
    }
    
    const capitulo = elementos.epubChapter.value;
    elementos.loadingEpub.classList.remove('hidden');
    elementos.btnEpub.disabled = true;
    
    try {
        const response = await fetch('/api/generar-epub', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                capitulo: capitulo,
                voz: elementos.voz.value,
                velocidad: parseFloat(elementos.velocidad.value),
                archivo: epubData.nombre
            })
        });
        
        if (response.ok) {
            const data = await response.json();
            mostrarAudio(data.audio);
            mostrarMensaje('Success', '✓ Audio generado. Escuchando y leyendo...');
        } else {
            mostrarMensaje('Error', '❌ Error al generar audio');
        }
    } catch (error) {
        mostrarMensaje('Error', '❌ Error: ' + error.message);
    } finally {
        elementos.loadingEpub.classList.add('hidden');
        elementos.btnEpub.disabled = false;
    }
}
