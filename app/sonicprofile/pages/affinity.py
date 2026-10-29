from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QHBoxLayout, QPushButton, QComboBox
from .common import BasePage
from sonicprofile.widgets.panels import Panel

class AffinityPage(BasePage):
    def __init__(self):
        super().__init__("Mapa de afinidad", "Explora las relaciones entre canciones según sus características acústicas.")
        controls = QHBoxLayout()
        genre = QComboBox()
        genre.addItems(["Todos los géneros", "Rock", "Electrónica", "Hip-hop", "Jazz", "Pop"])
        controls.addWidget(genre)
        controls.addStretch()
        controls.addWidget(QPushButton("Restablecer vista"))
        self.layout.addLayout(controls)
        panel = Panel("Explorador musical")
        placeholder = QLabel("El mapa interactivo se implementará tras validar el motor de similitud.\n\nCada punto representará una canción; la cercanía indicará similitud aproximada.")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setMinimumHeight(390)
        placeholder.setStyleSheet("color: #A8A0B8; background: #211E2B; border-radius: 12px; padding: 24px;")
        panel.layout.addWidget(placeholder)
        self.layout.addWidget(panel)
        self.layout.addStretch()
