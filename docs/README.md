## Documentación del proyecto

Este directorio agrupa la documentación del proyecto y sirve como índice rápido para encontrar guías, diseños y referencias.

Estructura

- docs/design/
  - DISEÑO.md — Documentación de diseño y decisiones arquitectónicas.
- docs/guides/
  - GUIA_VISUAL.md — Guía visual (estilos, UI/UX).
  - INSTRUCCIONES.md — Instrucciones operativas y flujo de trabajo.
  - QUICK_START.txt — Inicio rápido para desarrollar y ejecutar la aplicación.
- docs/references/
  - TAILWIND_REFERENCIA.md — Referencias relacionadas con Tailwind y utilidades.
- docs/changelog/
  - RESUMEN_ACTUALIZACION.txt — Resumen de cambios y actualizaciones del proyecto.

Otros recursos

- `scripts/` — Scripts y utilidades de desarrollo (depuración, herramientas de soporte).
- `tests/` — Tests automatizados y scripts de comprobación.

Cómo usar esta documentación

- Leer `docs/guides/QUICK_START.txt` para ejecutar rápidamente el servicio en local.
- Consultar `docs/design/DISEÑO.md` para entender las decisiones técnicas (TTS, EPUB, pydub/ffmpeg).
- Ver `docs/changelog/RESUMEN_ACTUALIZACION.txt` para historial de cambios.

Contribuir

- Para cambios en la documentación, crea una rama feature/ o usa un PR hacia `main` con tus modificaciones.
- Los archivos generados (audio, logs, uploads) están ignorados via `.gitignore`.

Contacto

- Repo: https://github.com/edumilla1994/texttospeach

----

Si quieres, puedo crear un script que genere automáticamente este índice extrayendo encabezados Markdown de cada archivo y listándolos con títulos más descriptivos.
