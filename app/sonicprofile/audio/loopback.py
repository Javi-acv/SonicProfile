import numpy as np
import soundcard as sc
from PySide6.QtCore import QThread, Signal, Qt, QTimer
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QProgressBar
from sonicprofile.widgets.panels import Panel
from sonicprofile.audio.feature_extractor import RealtimeFeatureExtractor


class LoopbackWorker(QThread):
    # rms, peak, 24 normalized Bark-band levels, centroid Hz, rolloff Hz
    levels = Signal(float, float, object, float, float)
    status = Signal(str)

    def __init__(self, block_frames=2048, parent=None):
        super().__init__(parent)
        self.block_frames = block_frames
        self._running = True

    def stop(self):
        self._running = False

    def run(self):
        try:
            speaker = sc.default_speaker()
            if speaker is None:
                self.status.emit("No se encontró una salida de audio predeterminada.")
                return
            loopback = sc.get_microphone(id=str(speaker.name), include_loopback=True)
            sample_rate = 44100
            extractor = RealtimeFeatureExtractor(
                sample_rate=sample_rate,
                frame_ms=25,
                hop_ms=10,
                num_bands=24,
            )
            self.status.emit(f"Capturando audio de Windows · {speaker.name}")
            with loopback.recorder(
                samplerate=sample_rate,
                channels=2,
                blocksize=self.block_frames,
            ) as recorder:
                while self._running:
                    data = recorder.record(numframes=self.block_frames)
                    if data is None or not len(data):
                        continue
                    mono = np.mean(data, axis=1) if data.ndim > 1 else data
                    rms = float(np.sqrt(np.mean(np.square(mono, dtype=np.float64))))
                    peak = float(np.max(np.abs(mono)))
                    features = extractor.process(mono)
                    self.levels.emit(
                        rms,
                        peak,
                        features["bark_bands"],
                        features["centroid_hz"],
                        features["rolloff_hz"],
                    )
        except Exception as exc:
            self.status.emit(f"Error de captura: {exc}")


class SystemAudioWidget(QWidget):
    """Automatic WASAPI loopback capture plus real-time acoustic feature display."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.worker = None
        self._user_stopped = False

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(14)

        self.panel = Panel("Audio del sistema")
        root.addWidget(self.panel)

        intro = QLabel(
            "SonicProfile escucha la salida de audio de Windows automáticamente. "
            "Reproduce música en Spotify, YouTube o cualquier aplicación; no necesitas importar canciones."
        )
        intro.setObjectName("Subtitle")
        intro.setWordWrap(True)
        self.panel.layout.addWidget(intro)

        header = QHBoxLayout()
        header.setSpacing(10)
        self.status_dot = QLabel("●")
        self.status_dot.setStyleSheet("color: #6F91B5; font-size: 14pt;")
        self.status = QLabel("Preparando captura automática…")
        self.status.setObjectName("Subtitle")
        self.status.setWordWrap(True)
        header.addWidget(self.status_dot)
        header.addWidget(self.status, 1)
        self.panel.layout.addLayout(header)

        self.toggle_btn = QPushButton("Detener captura")
        self.toggle_btn.setObjectName("PrimaryButton")
        self.toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.toggle_btn.clicked.connect(self.toggle_capture)
        self.panel.layout.addWidget(self.toggle_btn, alignment=Qt.AlignmentFlag.AlignLeft)

        metrics = QHBoxLayout()
        metrics.setSpacing(12)
        self.rms_label = QLabel("RMS\n—")
        self.peak_label = QLabel("Pico\n—")
        self.centroid_label = QLabel("Centroide espectral\n—")
        self.rolloff_label = QLabel("Rolloff 85 %\n—")
        for label in (self.rms_label, self.peak_label, self.centroid_label, self.rolloff_label):
            label.setStyleSheet(
                "QLabel { background: #101B2A; border: 1px solid #263A52; "
                "border-radius: 9px; padding: 10px; color: #D9E6F5; }"
            )
            label.setMinimumHeight(54)
            label.setWordWrap(True)
            metrics.addWidget(label)
        self.panel.layout.addLayout(metrics)

        self.panel.layout.addSpacing(4)
        bands_title = QLabel("Perfil de frecuencias · 24 bandas Bark")
        bands_title.setStyleSheet("font-weight: 650; color: #DCE9F8;")
        self.panel.layout.addWidget(bands_title)

        self.bars = []
        bars_layout = QHBoxLayout()
        bars_layout.setSpacing(4)
        for index in range(24):
            bar = QProgressBar()
            bar.setOrientation(Qt.Orientation.Vertical)
            bar.setRange(0, 100)
            bar.setValue(0)
            bar.setTextVisible(False)
            bar.setFixedWidth(13)
            bar.setFixedHeight(138)
            bar.setToolTip(f"Banda Bark {index + 1}")
            self.bars.append(bar)
            bars_layout.addWidget(bar)
        self.panel.layout.addLayout(bars_layout)

        note = QLabel(
            "Las bandas muestran energía relativa, no géneros ni identidad de la canción. "
            "El procesamiento se ejecuta en un hilo separado para mantener la interfaz fluida."
        )
        note.setObjectName("Subtitle")
        note.setWordWrap(True)
        self.panel.layout.addWidget(note)

        # Start only after the UI event loop is running.
        QTimer.singleShot(250, self.start_capture)

    def start_capture(self):
        if self.worker and self.worker.isRunning():
            return
        self._user_stopped = False
        self.worker = LoopbackWorker(parent=self)
        self.worker.levels.connect(self.update_levels)
        self.worker.status.connect(self.update_status)
        self.worker.finished.connect(self.capture_finished)
        self.toggle_btn.setText("Detener captura")
        self.toggle_btn.setEnabled(True)
        self.status.setText("Conectando con la salida de audio de Windows…")
        self.status_dot.setStyleSheet("color: #E5B85C; font-size: 14pt;")
        self.worker.start()

    def stop_capture(self):
        if self.worker and self.worker.isRunning():
            self._user_stopped = True
            self.worker.stop()
            self.worker.wait(3000)
        self.capture_finished()

    def toggle_capture(self):
        if self.worker and self.worker.isRunning():
            self.stop_capture()
        else:
            self.start_capture()

    def update_status(self, message):
        self.status.setText(message)
        if message.startswith("Error") or "No se encontró" in message:
            self.status_dot.setStyleSheet("color: #E57C7C; font-size: 14pt;")
        elif "Capturando audio" in message:
            self.status_dot.setStyleSheet("color: #73D6B0; font-size: 14pt;")
        else:
            self.status_dot.setStyleSheet("color: #E5B85C; font-size: 14pt;")

    def capture_finished(self):
        running = self.worker is not None and self.worker.isRunning()
        if running:
            return
        if self._user_stopped:
            self.status.setText("Captura detenida manualmente.")
            self.status_dot.setStyleSheet("color: #6F91B5; font-size: 14pt;")
            self.toggle_btn.setText("Reanudar captura")
        elif self.worker is not None:
            if not self.status.text().startswith("Error") and "No se encontró" not in self.status.text():
                self.status.setText("La captura se detuvo. Puedes intentar reanudarla.")
            self.toggle_btn.setText("Reintentar captura")
        self.toggle_btn.setEnabled(True)

    def update_levels(self, rms, peak, levels, centroid_hz, rolloff_hz):
        self.rms_label.setText(f"RMS\n{rms:.4f}")
        self.peak_label.setText(f"Pico\n{peak:.4f}")
        self.centroid_label.setText(f"Centroide espectral\n{centroid_hz:.0f} Hz")
        self.rolloff_label.setText(f"Rolloff 85 %\n{rolloff_hz:.0f} Hz")
        for bar, value in zip(self.bars, levels):
            bar.setValue(int(max(0.0, min(1.0, value)) * 100))

    def closeEvent(self, event):
        self.stop_capture()
        super().closeEvent(event)
