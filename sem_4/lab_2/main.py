import sys
from PyQt6.QtWidgets import QApplication
from model.Database import Database
from view.MainWindow import MainWindow
from controller.Controller import Controller

def main():
    app = QApplication(sys.argv)
    model = Database("data.xml") 
    view = MainWindow()
    controller = Controller(model, view)
    view.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()