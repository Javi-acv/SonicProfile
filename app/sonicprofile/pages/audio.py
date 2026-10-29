from PySide6.QtWidgets import QLabel
from .common import BasePage
from sonicprofile.audio.loopback import SystemAudioWidget


class AudioPage(BasePage):
    def __init__(self):
        super().__init__(
            "Audio en tiempo real",
            "Captura la salida de audio de Windows, incluida la música que reproduces en Spotify o en tu navegador."
        )
        self.capture = SystemAudioWidget()
        self.layout.addWidget(self.capture)
        self.layout.addStretch()
