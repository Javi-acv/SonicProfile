from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QWidget, QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QStackedWidget
from sonicprofile.pages import HomePage, AffinityPage, FindingsPage, LibraryPage, ProfilePage, StatsPage
from sonicprofile.pages.audio import AudioPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SonicProfile | Perfil musical")
        self.resize(1320, 820)
        self.setMinimumSize(1050, 680)
        root = QWidget()
        root_layout = QHBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)
        self.setCentralWidget(root)

        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(238)
        side = QVBoxLayout(sidebar)
        side.setContentsMargins(16, 24, 16, 18)
        side.setSpacing(8)
        brand = QLabel("SONICPROFILE")
        brand.setObjectName("Brand")
        subtitle = QLabel("ANÁLISIS Y PERFIL MUSICAL")
        subtitle.setObjectName("BrandSub")
        side.addWidget(brand)
        side.addWidget(subtitle)
        side.addSpacing(25)

        self.stack = QStackedWidget()
        page_defs = [
            ("⌂   Inicio", HomePage()),
            ("◉   Mapa de afinidad", AffinityPage()),
            ("✦   Hallazgos", FindingsPage()),
            ("♫   Biblioteca", LibraryPage()),
            ("◌   Perfil musical", ProfilePage()),
            ("▥   Estadísticas", StatsPage()),
            ("♫   Audio en tiempo real", AudioPage()),
        ]
        self.buttons = []
        for index, (label, page) in enumerate(page_defs):
            button = QPushButton(label)
            button.setObjectName("NavButton")
            button.setCheckable(True)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(lambda checked=False, i=index: self.navigate(i))
            side.addWidget(button)
            self.buttons.append(button)
            self.stack.addWidget(page)
        side.addStretch()
        footer = QLabel("PROTOTIPO · VERSIÓN 0.1")
        footer.setObjectName("BrandSub")
        side.addWidget(footer)

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(28, 20, 28, 24)
        content_layout.setSpacing(14)

        topbar = QHBoxLayout()
        context = QLabel("ESPACIO DE ANÁLISIS")
        context.setStyleSheet(
            "color: #7892B1; font-size: 8pt; font-weight: 700; letter-spacing: 1.2px;"
        )
        topbar.addWidget(context)
        topbar.addStretch()
        edition = QLabel("SONICPROFILE  /  BETA")
        edition.setStyleSheet(
            "color: #8FA5C2; background: #141F2F; border: 1px solid #263A52; "
            "border-radius: 8px; padding: 6px 10px; font-size: 8pt; font-weight: 600;"
        )
        topbar.addWidget(edition)
        content_layout.addLayout(topbar)
        content_layout.addWidget(self.stack)
        root_layout.addWidget(sidebar)
        root_layout.addWidget(content, 1)
        self.navigate(0)

    def navigate(self, index):
        self.stack.setCurrentIndex(index)
        for i, button in enumerate(self.buttons):
            button.setChecked(i == index)
