import os
import subprocess
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QListWidget
from PySide6.QtCore import Qt


class Launcher(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("🔥 FIRE Launcher v2 FIX")
        self.resize(700, 450)

        layout = QVBoxLayout()

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search apps...")
        self.search.textChanged.connect(self.update_list)
        self.search.returnPressed.connect(self.run_first)

        self.list = QListWidget()
        self.list.itemActivated.connect(self.run_app)

        layout.addWidget(self.search)
        layout.addWidget(self.list)
        self.setLayout(layout)

        self.apps = self.load_apps()
        self.update_list()

    # 📦 читаємо .desktop файли
    def load_apps(self):
        apps = {}

        paths = [
            "/usr/share/applications",
            os.path.expanduser("~/.local/share/applications")
        ]

        for path in paths:
            if not os.path.exists(path):
                continue

            for file in os.listdir(path):
                if not file.endswith(".desktop"):
                    continue

                full_path = os.path.join(path, file)

                try:
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()

                    # ❌ фільтр сміття
                    if "NoDisplay=true" in content:
                        continue
                    if "OnlyShowIn=" in content:
                        continue

                    name = file.replace(".desktop", "")

                    exec_cmd = None

                    # беремо нормальне ім’я
                    for line in content.splitlines():
                        if line.startswith("Name="):
                            name = line.split("=", 1)[1]
                        if line.startswith("Exec="):
                            exec_cmd = line.split("=", 1)[1]

                    if exec_cmd:
                        # 🔥 ВАЖЛИВИЙ ФІКС:
                        # прибираємо %u %F і аргументи
                        exec_cmd = exec_cmd.split()[0]

                        apps[name] = exec_cmd

                except Exception as e:
                    print("LOAD ERROR:", e)

        return apps

    # 🔍 пошук
    def update_list(self):
        text = self.search.text().lower()
        self.list.clear()

        for name in self.apps:
            if text in name.lower():
                self.list.addItem(name)

    # 🚀 запуск програми
    def run_app(self, item):
        name = item.text()
        cmd = self.apps.get(name)

        if cmd:
            try:
                subprocess.Popen([cmd])
            except Exception as e:
                print("RUN ERROR:", e)

    # Enter = перший результат
    def run_first(self):
        if self.list.count() > 0:
            self.run_app(self.list.item(0))