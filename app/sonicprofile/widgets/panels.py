from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel

class Panel(QFrame):
    def __init__(self, title=None, parent=None):
        super().__init__(parent)
        self.setObjectName("Panel")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(18, 16, 18, 18)
        self.layout.setSpacing(12)
        if title:
            label = QLabel(title)
            label.setObjectName("PanelTitle")
            self.layout.addWidget(label)

class MetricCard(QFrame):
    def __init__(self, value, caption, parent=None):
        super().__init__(parent)
        self.setObjectName("MetricCard")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(5)
        number = QLabel(value)
        number.setObjectName("MetricValue")
        text = QLabel(caption)
        text.setObjectName("MetricCaption")
        layout.addWidget(number)
        layout.addWidget(text)
