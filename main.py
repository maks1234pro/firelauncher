import sys
from PySide6.QtWidgets import QApplication
from launcher import Launcher

print("STEP 1: start")

app = QApplication(sys.argv)

print("STEP 2: QApplication created")

window = Launcher()
print("STEP 3: Launcher created")

window.show()
print("STEP 4: window show called")

exit_code = app.exec()
print("STEP 5: app exited:", exit_code)

sys.exit(exit_code)