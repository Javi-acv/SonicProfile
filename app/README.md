# SonicProfile

Prototipo de interfaz en Python + PySide6 con captura automática del audio de salida de Windows mediante loopback.

## Ejecutar desde la carpeta `app`
```powershell
python -m venv .venv
.venv\\Scripts\\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

La captura se inicia automáticamente al abrir la aplicación. Reproduce audio en Spotify, YouTube u otra aplicación y abre la sección **Audio en tiempo real** para ver los niveles y las 24 bandas Bark. No es necesario importar archivos de música.

El procesamiento de audio corre en un hilo independiente. El extractor calcula características acústicas básicas (RMS, centroide, rolloff y energía relativa en bandas Bark); todavía no identifica canciones, artistas ni géneros.

El diseño utiliza una paleta azul marino tenue con acentos azul claro, distinta del tema morado de IntelliEQ.

## Refinamiento visual
- Jerarquía tipográfica con Segoe UI Variable (con Segoe UI como alternativa).
- Pesos de letra normal, medio y seminegrita definidos de forma consistente.
- Contraste y colores alineados con la paleta azul marino.
- Tarjetas y navegación con bordes y estados discretos.
- La página de inicio explica el propósito del mapa sin aparentar que el análisis ya está implementado.

## Reproduciendo ahora
La pantalla de inicio consulta cada dos segundos los metadatos que Windows expone mediante Global System Media Transport Controls: título, artista, álbum, aplicación y miniatura. Esto funciona con Spotify y con reproductores/navegadores compatibles, pero la disponibilidad depende de que la aplicación publique esos metadatos a Windows. No se descarga ni se guarda la canción. Si la portada o los metadatos no están disponibles, se muestra un estado alternativo.
