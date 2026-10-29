from PySide6.QtCore import QThread, Signal, Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel
from sonicprofile.widgets.panels import Panel
from sonicprofile.audio.now_playing import run_polling


class NowPlayingWorker(QThread):
    updated = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._running = True

    def stop(self):
        self._running = False

    def run(self):
        try:
            run_polling(self.updated.emit, lambda: not self._running, 2.0)
        except Exception:
            self.updated.emit(None)


class NowPlayingWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.worker = None
        self._last_artwork = None
        self.panel = Panel("Reproduciendo ahora")
        outer = QHBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(self.panel)

        content = QHBoxLayout()
        content.setSpacing(20)
        self.cover = QLabel()
        self.cover.setFixedSize(140, 140)
        self.cover.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cover.setStyleSheet(
            "background: #101B2A; border: 1px solid #2B405A; border-radius: 12px; "
            "color: #8FA5C2; font-size: 34pt;"
        )
        self.cover.setText("♫")
        content.addWidget(self.cover, 0, Qt.AlignmentFlag.AlignTop)

        text_col = QVBoxLayout()
        text_col.setContentsMargins(0, 2, 0, 2)
        text_col.setSpacing(7)
        self.title = QLabel("Esperando reproducción")
        self.title.setStyleSheet(
            "background: transparent; font-size: 17pt; font-weight: 700; color: #F2F6FC;"
        )
        self.title.setWordWrap(True)
        self.artist = QLabel("Reproduce algo en Spotify, YouTube u otra aplicación.")
        self.artist.setStyleSheet(
            "background: transparent; color: #C5D4E7; font-size: 11pt; font-weight: 600;"
        )
        self.artist.setWordWrap(True)
        self.album = QLabel("")
        self.album.setStyleSheet(
            "background: transparent; color: #8FA5C2; font-size: 10pt;"
        )
        self.album.setWordWrap(True)
        self.source = QLabel("ESPERANDO REPRODUCCIÓN")
        self.source.setStyleSheet(
            "background: #1A2A40; border: 1px solid #2B405A; border-radius: 9px; "
            "padding: 5px 9px; font-size: 8pt; font-weight: 650; color: #8CC8FF;"
        )
        self.source.setMaximumWidth(300)
        text_col.addWidget(self.title)
        text_col.addWidget(self.artist)
        text_col.addWidget(self.album)
        text_col.addStretch()
        text_col.addWidget(self.source)
        content.addLayout(text_col, 1)
        self.panel.layout.addLayout(content)

        self.worker = NowPlayingWorker(self)
        self.worker.updated.connect(self.update_track)
        self.worker.start()

    def update_track(self, item):
        if item is None or not (item.title or item.artist):
            self.title.setText("No se detecta ninguna reproducción")
            self.artist.setText("Abre Spotify o un reproductor compatible con los controles multimedia de Windows.")
            self.album.setText("")
            self.source.setText("ESPERANDO METADATOS")
            self.cover.setPixmap(QPixmap())
            self.cover.setText("♫")
            self._last_artwork = None
            return

        self.title.setText(item.title or "Título desconocido")
        self.artist.setText(item.artist or "Artista desconocido")
        self.album.setText(item.album or "")
        source_id = (item.source or "").lower()
        if "spotify" in source_id:
            app_name = "SPOTIFY"
        elif "chrome" in source_id or "msedge" in source_id or "firefox" in source_id:
            app_name = "NAVEGADOR"
        elif item.source:
            app_name = item.source.split("!")[-1].split("\\")[-1].replace(".exe", "").upper()
        else:
            app_name = "REPRODUCTOR"
        status = "REPRODUCIENDO" if "playing" in item.playback_status.lower() else "EN SESIÓN"
        self.source.setText(f"♫  {app_name}  ·  {status}")

        if item.artwork and item.artwork != self._last_artwork:
            pixmap = QPixmap()
            if pixmap.loadFromData(item.artwork):
                # Spotify's Windows thumbnail may include its own logo beneath
                # the album cover. Crop only that source's lower branding strip.
                if "spotify" in source_id and pixmap.height() > pixmap.width():
                    crop_height = max(1, int(pixmap.height() * 0.78))
                    pixmap = pixmap.copy(0, 0, pixmap.width(), crop_height)
                pixmap = pixmap.scaled(
                    self.cover.size(),
                    Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                    Qt.TransformationMode.SmoothTransformation,
                )
                x = max(0, (pixmap.width() - self.cover.width()) // 2)
                y = max(0, (pixmap.height() - self.cover.height()) // 2)
                self.cover.setPixmap(pixmap.copy(x, y, self.cover.width(), self.cover.height()))
                self.cover.setText("")
                self._last_artwork = item.artwork
        elif not item.artwork:
            self.cover.setPixmap(QPixmap())
            self.cover.setText("♫")

    def closeEvent(self, event):
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.worker.wait(3000)
        super().closeEvent(event)
