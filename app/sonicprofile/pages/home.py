from PySide6.QtWidgets import QLabel, QHBoxLayout, QPushButton
from .common import BasePage
from sonicprofile.widgets.panels import Panel, MetricCard
from sonicprofile.widgets.now_playing import NowPlayingWidget


class HomePage(BasePage):
    def __init__(self):
        super().__init__(
            "Tu universo musical",
            "Explora tu biblioteca, encuentra conexiones y descubre patrones en tu música."
        )

        metrics = QHBoxLayout()
        metrics.setSpacing(12)
        for value, caption in [
            ("—", "Canciones analizadas"),
            ("—", "Afinidades detectadas"),
            ("—", "Hallazgos"),
            ("—", "Géneros identificados"),
        ]:
            metrics.addWidget(MetricCard(value, caption))
        self.layout.addLayout(metrics)
        self.now_playing = NowPlayingWidget()
        self.layout.addWidget(self.now_playing)

        lower = QHBoxLayout()
        lower.setSpacing(14)

        map_panel = Panel("Mapa de afinidad")
        placeholder = QLabel(
            "Tu mapa aparecerá aquí cuando SonicProfile haya analizado tu biblioteca. "
            "Cada punto representará una canción y las distancias mostrarán similitudes acústicas."
        )
        placeholder.setWordWrap(True)
        placeholder.setMinimumHeight(125)
        placeholder.setAlignment(__import__("PySide6.QtCore", fromlist=["Qt"]).Qt.AlignmentFlag.AlignVCenter)
        placeholder.setStyleSheet(
            "color: #9EB0C8; padding: 18px; background: #101B2A; "
            "border: 1px dashed #2B405A; border-radius: 10px;"
        )
        map_panel.layout.addWidget(placeholder)

        explore = QPushButton("Explorar mapa")
        explore.setObjectName("PrimaryButton")
        explore.setEnabled(False)
        explore.setToolTip("Se habilitará cuando el mapa de afinidad esté implementado.")
        map_panel.layout.addWidget(explore)

        findings = Panel("Qué podrás descubrir")
        for title, description in [
            ("Conexiones inesperadas", "Canciones similares aunque sean de géneros distintos."),
            ("Agrupaciones acústicas", "Sonidos que comparten características."),
            ("Canciones distintivas", "Temas que se alejan del patrón de tu biblioteca."),
        ]:
            item = QLabel(f"<b>{title}</b><br><span style='color:#9EB0C8'>{description}</span>")
            item.setWordWrap(True)
            item.setTextFormat(__import__("PySide6.QtCore", fromlist=["Qt"]).Qt.TextFormat.RichText)
            item.setStyleSheet("padding: 8px 2px;")
            findings.layout.addWidget(item)

        lower.addWidget(map_panel, 3)
        lower.addWidget(findings, 2)
        self.layout.addLayout(lower)
        self.layout.addStretch()
