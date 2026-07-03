from PySide6.QtWidgets import QApplication, QLabel

app = QApplication([])

label = QLabel("Hello FIRE!")
label.resize(300, 100)
label.show()

app.exec()