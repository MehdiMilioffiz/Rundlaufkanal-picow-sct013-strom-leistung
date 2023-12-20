import sys
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QComboBox, QSizePolicy
from PyQt5.QtGui import QPixmap, QFont, QPalette, QColor
from PyQt5.QtCore import QTimer, Qt
import serial
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from datetime import datetime


class AppDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('STROMMESSUNG APP zum OPS-Strömungskanals')

        self.data = []

        self.layout = QVBoxLayout()

        # Farbschema anpassen
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor('#3A1F5D'))  # Dunkelviolett
        palette.setColor(QPalette.WindowText, QColor('#FAFAFA'))  # Weiß
        self.setPalette(palette)

        # Logo und Name hinzufügen
        self.top_layout = QHBoxLayout()
        self.logo = QLabel(self)
        logo_pixmap = QPixmap('GUIpythonWindowsapp/UniversitaetLogo.png')
        self.logo.setPixmap(logo_pixmap.scaled(70, 70, Qt.KeepAspectRatio))
        self.top_layout.addWidget(self.logo)

        self.name_label = QLabel("M.Mili")
        self.name_label.setFont(QFont('Arial', 16))  # Schriftgröße und -stil anpassen
        self.name_label.setAlignment(Qt.AlignRight)
        self.top_layout.addWidget(self.name_label)
        self.layout.addLayout(self.top_layout)

        self.combo = QComboBox(self)
        self.combo.setFont(QFont('Arial', 18))
        self.combo.addItems(["COM1", "COM2", "COM3", "COM4", "COM5"])
        self.combo.currentIndexChanged.connect(self.select_serial_port)

        self.image_label = QLabel(self)
        pixmap = QPixmap('GUIpythonWindowsapp/IhrBild.png')
        pixmap_scaled = pixmap.scaled(600, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_label.setPixmap(pixmap_scaled)
        self.image_label.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(self.image_label)

        self.com_info = QLabel("Wählen Sie den richtigen COM-Port aus der Dropdown-Liste aus.")
        self.com_info.setFont(QFont('Arial', 16))  # Schriftgröße und -stil anpassen
        self.com_info.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.com_info)

        self.layout.addWidget(self.combo)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas, 2)

        self.button = QPushButton('Speichern')
        self.button.setFont(QFont('Arial', 14))  # Schriftgröße und -stil anpassen
        self.button.setStyleSheet("background-color: #3E82F7; color: #FAFAFA;")  # Hintergrund und Textfarbe ändern
        self.button.clicked.connect(self.save_plot)
        self.layout.addWidget(self.button)

        self.ser = self.create_serial_connection(self.combo.currentText(), 9600)

        self.layout.setSpacing(20)  # Zwischenraum zwischen den Widgets hinzufügen

        self.setLayout(self.layout)

        self.resize(1600, 1200)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(100)

    def select_serial_port(self):
        if self.ser:
            self.ser.close()
        self.ser = self.create_serial_connection(self.combo.currentText(), 9600)

    def create_serial_connection(self, port, baud_rate):
        try:
            ser = serial.Serial(port, baud_rate)
            return ser
        except serial.SerialException as e:
            print(f"Failed to connect to port {port}. Error: {e}")
            return None

    def update_plot(self):
        if self.ser and self.ser.in_waiting > 0:
            line = self.ser.readline().decode('utf-8').rstrip()
            wert = float(line)
            self.data.append(wert)

            self.figure.clear()
            plt.plot(self.data)
            plt.xlabel('Zeit (s)')
            plt.ylabel('Strom (A)')
            plt.title(f'Daten aufgenommen am {datetime.now().date()}')
            plt.autoscale(tight=True)
            self.canvas.draw()

    def save_plot(self):
        self.figure.savefig('plot.png')


app = QApplication(sys.argv)

demo = AppDemo()
demo.show()

sys.exit(app.exec_())
