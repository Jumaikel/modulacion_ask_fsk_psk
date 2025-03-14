import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel


class ModulationApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modulación Digital")
        self.setGeometry(100, 100, 350, 250)

        self.layout = QVBoxLayout()

        self.binary_input_label = QLabel("Ingrese la señal binaria (Ej: 10101001):", self)
        self.layout.addWidget(self.binary_input_label)

        input_layout = QHBoxLayout()

        self.binary_input = QLineEdit(self)
        input_layout.addWidget(self.binary_input)

        self.random_button = QPushButton("Generar Aleatoria", self)
        self.random_button.clicked.connect(self.generate_random_signal)
        input_layout.addWidget(self.random_button)

        self.layout.addLayout(input_layout)

        self.plot_button = QPushButton("Mostrar Gráfica", self)
        self.plot_button.clicked.connect(self.plot_signal)
        self.layout.addWidget(self.plot_button)

        self.setLayout(self.layout)

    def generate_random_signal(self):
        random_bits = np.random.randint(0, 2, 8)
        self.binary_input.setText(''.join(map(str, random_bits)))

    def plot_signal(self):
        fs = 10000
        bit_duration = 0.01
        f0 = 2000
        f1 = 5000
        fc = 5000

        binary_signal = self.binary_input.text().strip()

        if not binary_signal or any(b not in '01' for b in binary_signal):  # Verificar que sea binario
            print("Por favor ingrese una señal binaria válida.")
            return

        bits = np.array([int(b) for b in binary_signal])

        t = np.arange(0, bit_duration * len(bits), 1 / fs)
        bit_signal = np.repeat(bits, int(fs * bit_duration))

        ask_signal = bit_signal * np.sin(2 * np.pi * fc * t)
        fsk_signal = np.sin(2 * np.pi * (f0 + (f1 - f0) * bit_signal) * t)
        psk_signal = np.sin(2 * np.pi * fc * t + np.pi * bit_signal)

        plt.figure(figsize=(10, 6))

        plt.subplot(4, 1, 1)
        plt.title("Señal Binaria")
        plt.plot(t, bit_signal, 'r', lw=2)
        plt.ylim(-0.2, 1.2)

        plt.subplot(4, 1, 2)
        plt.title("Señal Modulada ASK")
        plt.plot(t, ask_signal, 'b')

        plt.subplot(4, 1, 3)
        plt.title("Señal Modulada FSK")
        plt.plot(t, fsk_signal, 'g')

        plt.subplot(4, 1, 4)
        plt.title("Señal Modulada PSK")
        plt.plot(t, psk_signal, 'm')

        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    app = QApplication([])
    window = ModulationApp()
    window.show()
    app.exec_()
