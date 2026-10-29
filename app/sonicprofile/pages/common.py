from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class BasePage(QWidget):
    def __init__(self, title, subtitle):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(8)
        heading = QLabel(title)
        heading.setObjectName("PageTitle")
        desc = QLabel(subtitle)
        desc.setObjectName("Subtitle")
        desc.setWordWrap(True)
        self.layout.addWidget(heading)
        self.layout.addWidget(desc)
        self.layout.addSpacing(16)
