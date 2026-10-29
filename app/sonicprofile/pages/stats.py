from PySide6.QtWidgets import QLabel, QGridLayout
from .common import BasePage
from sonicprofile.widgets.panels import Panel, MetricCard

class StatsPage(BasePage):
    def __init__(self):
        super().__init__("Estadísticas", "Comprende la composición de tu biblioteca y sus tendencias musicales.")
        grid = QGridLayout()
        grid.setSpacing(12)
        for i, (value, caption) in enumerate([("—", "Canciones por género"), ("—", "Artistas en la biblioteca"), ("—", "Duración total"), ("—", "Grupos acústicos")]):
            grid.addWidget(MetricCard(value, caption), i // 2, i % 2)
        self.layout.addLayout(grid)
        panel = Panel("Visualizaciones")
        label = QLabel("Aquí se integrarán gráficos de distribución y comparaciones del perfil musical.")
        label.setWordWrap(True)
        label.setStyleSheet("color: #BDB5CC;")
        panel.layout.addWidget(label)
        self.layout.addWidget(panel)
        self.layout.addStretch()
