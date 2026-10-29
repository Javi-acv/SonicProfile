from PySide6.QtWidgets import QLabel
from .common import BasePage
from sonicprofile.widgets.panels import Panel

class FindingsPage(BasePage):
    def __init__(self):
        super().__init__("Hallazgos musicales", "Patrones y conexiones relevantes identificados dentro de tu biblioteca.")
        for title, desc in [
            ("Afinidades inesperadas", "Relaciones entre canciones de géneros distintos que comparten características acústicas."),
            ("Agrupaciones detectadas", "Conjuntos de canciones que presentan patrones musicales similares."),
            ("Canciones distintivas", "Elementos que se apartan de las tendencias predominantes de la colección.")
        ]:
            panel = Panel(title)
            label = QLabel(desc + "\n\nLos hallazgos reales aparecerán cuando el análisis esté conectado.")
            label.setWordWrap(True)
            label.setStyleSheet("color: #BDB5CC;")
            panel.layout.addWidget(label)
            self.layout.addWidget(panel)
        self.layout.addStretch()
