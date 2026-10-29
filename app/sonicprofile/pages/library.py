from PySide6.QtWidgets import QLabel, QHBoxLayout, QLineEdit, QPushButton, QTableWidget, QHeaderView
from .common import BasePage
from sonicprofile.widgets.panels import Panel

class LibraryPage(BasePage):
    def __init__(self):
        super().__init__("Biblioteca musical", "Consulta y organiza las canciones que forman parte de tu análisis.")
        controls = QHBoxLayout()
        search = QLineEdit()
        search.setPlaceholderText("Buscar canción, artista o género…")
        controls.addWidget(search, 1)
        add = QPushButton("Añadir música")
        add.setObjectName("PrimaryButton")
        controls.addWidget(add)
        self.layout.addLayout(controls)
        panel = Panel()
        table = QTableWidget(0, 4)
        table.setHorizontalHeaderLabels(["Canción", "Artista", "Género estimado", "Análisis"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setAlternatingRowColors(True)
        table.setMinimumHeight(330)
        panel.layout.addWidget(table)
        empty = QLabel("La biblioteca está vacía. La importación se añadirá en una siguiente etapa.")
        empty.setObjectName("Subtitle")
        panel.layout.addWidget(empty)
        self.layout.addWidget(panel)
        self.layout.addStretch()
