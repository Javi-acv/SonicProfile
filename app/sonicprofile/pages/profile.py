from PySide6.QtWidgets import QLabel, QGridLayout
from .common import BasePage
from sonicprofile.widgets.panels import Panel, MetricCard

class ProfilePage(BasePage):
    def __init__(self):
        super().__init__("Perfil acústico", "Una vista de las características sonoras predominantes de tu colección.")
        grid = QGridLayout()
        grid.setSpacing(12)
        for i, (value, caption) in enumerate([("—", "Tempo predominante"), ("—", "Energía media"), ("—", "Brillo espectral"), ("—", "Género principal")]):
            grid.addWidget(MetricCard(value, caption), i // 2, i % 2)
        self.layout.addLayout(grid)
        panel = Panel("Resumen del perfil")
        label = QLabel("Los indicadores se calcularán a partir de las características acústicas extraídas de las canciones.")
        label.setWordWrap(True)
        label.setStyleSheet("color: #BDB5CC;")
        panel.layout.addWidget(label)
        self.layout.addWidget(panel)
        self.layout.addStretch()
