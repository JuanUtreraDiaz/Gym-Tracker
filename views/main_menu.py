# main_menu.py
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget

class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menú Principal")
        self.setGeometry(100, 100, 300, 200)
        
        # Crear los botones como atributos de la clase
        self.btn_users = QPushButton("Administrar Usuarios")
        self.btn_exercises = QPushButton("Administrar Ejercicios")
        self.btn_workouts = QPushButton("Administrar Entrenamientos")
        self.btn_export = QPushButton("Exportar a Excel")

        # Configurar el layout
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        
        # Añadir los botones al layout
        layout.addWidget(self.btn_users)
        layout.addWidget(self.btn_exercises)
        layout.addWidget(self.btn_workouts)
        layout.addWidget(self.btn_export)
        
        # Crear widget central y asignar el layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    # Métodos de apertura para cada ventana (puedes añadir la lógica después)
    def open_manage_users(self):
        print("Abrir gestión de usuarios")

    def open_manage_exercises(self):
        print("Abrir gestión de ejercicios")

    def open_manage_workouts(self):
        print("Abrir gestión de entrenamientos")

    def export_to_excel(self):
        print("Exportar a Excel")

# Para pruebas, puedes ejecutar esta parte si deseas probar la ventana principal
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainMenu()
    main_window.show()
    sys.exit(app.exec_())
