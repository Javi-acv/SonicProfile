APP_STYLE = """
QWidget {
    background: #0D1420;
    color: #E8EEF8;
    font-family: "Segoe UI Variable", "Segoe UI";
    font-size: 10pt;
    font-weight: 400;
}
QMainWindow { background: #0D1420; }
QFrame#Sidebar {
    background: #101B2B;
    border-right: 1px solid #24364D;
}
QLabel#Brand {
    color: #F2F6FC;
    font-size: 17pt;
    font-weight: 700;
    letter-spacing: 1.1px;
}
QLabel#BrandSub {
    color: #8FA5C2;
    font-size: 8pt;
    font-weight: 600;
    letter-spacing: 0.8px;
}
QPushButton#NavButton {
    text-align: left;
    padding: 12px 13px;
    border: 1px solid transparent;
    border-radius: 9px;
    color: #AEBED3;
    background: transparent;
    font-size: 10pt;
    font-weight: 500;
}
QPushButton#NavButton:hover {
    background: #1A2A40;
    color: #F5F8FD;
}
QPushButton#NavButton:checked {
    background: #203A59;
    border: 1px solid #2D5278;
    color: #C6E2FF;
    font-weight: 650;
}
QLabel#PageTitle {
    font-size: 23pt;
    font-weight: 700;
    color: #F4F7FC;
}
QLabel#Subtitle {
    color: #9EB0C8;
    font-size: 10pt;
    font-weight: 400;
}
QFrame#Panel, QFrame#MetricCard {
    background: #141F2F;
    border: 1px solid #263A52;
    border-radius: 14px;
}
QLabel#PanelTitle {
    font-size: 12pt;
    font-weight: 650;
    color: #EAF2FC;
}
QLabel#MetricValue {
    font-size: 22pt;
    font-weight: 700;
    color: #8CC8FF;
}
QLabel#MetricCaption {
    color: #9EB0C8;
    font-size: 9pt;
    font-weight: 500;
}
QPushButton#PrimaryButton {
    background: #356FA6;
    color: #FFFFFF;
    border: 1px solid #447FB7;
    border-radius: 9px;
    padding: 10px 14px;
    font-weight: 650;
}
QPushButton#PrimaryButton:hover { background: #4384BE; }
QPushButton#PrimaryButton:disabled {
    background: #263A52;
    color: #7288A4;
    border-color: #263A52;
}
QPushButton {
    border-radius: 8px;
    padding: 8px 12px;
}
QPushButton:focus, QLineEdit:focus, QComboBox:focus {
    border: 1px solid #6FADE0;
}
QLineEdit, QComboBox {
    background: #101B2A;
    border: 1px solid #2B405A;
    border-radius: 8px;
    padding: 9px;
    color: #E8EEF8;
    selection-background-color: #356FA6;
}
QTableWidget {
    background: #141F2F;
    alternate-background-color: #19283B;
    gridline-color: #263A52;
    border: 1px solid #263A52;
    border-radius: 10px;
    selection-background-color: #254B70;
    selection-color: #FFFFFF;
}
QHeaderView::section {
    background: #1A2A40;
    color: #BFD0E5;
    padding: 9px;
    border: 0;
    border-bottom: 1px solid #2B405A;
    font-weight: 600;
}
QProgressBar {
    background: #0E1826;
    border: 1px solid #2A4058;
    border-radius: 4px;
}
QProgressBar::chunk {
    background: #5595CA;
    border-radius: 3px;
}
QScrollArea { border: 0; background: transparent; }
QToolTip {
    background: #1A2A40;
    color: #F4F7FC;
    border: 1px solid #355575;
    padding: 5px;
}
"""
