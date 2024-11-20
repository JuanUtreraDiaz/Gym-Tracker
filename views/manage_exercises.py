# manage_exercises.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QListWidget, QMessageBox
from database import create_connection

class ManageExercises(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Administrar Ejercicios")
        
        layout = QVBoxLayout()
        self.exercise_list = QListWidget()
        self.exercise_name = QLineEdit()
        self.exercise_category = QLineEdit()
        
        add_exercise_btn = QPushButton("Agregar Ejercicio")
        delete_exercise_btn = QPushButton("Eliminar Ejercicio")
        back_btn = QPushButton("Volver al Menú Principal")
        
        layout.addWidget(QLabel("Lista de Ejercicios"))
        layout.addWidget(self.exercise_list)
        layout.addWidget(QLabel("Nombre:"))
        layout.addWidget(self.exercise_name)
        layout.addWidget(QLabel("Categoría:"))
        layout.addWidget(self.exercise_category)
        
        layout.addWidget(add_exercise_btn)
        layout.addWidget(delete_exercise_btn)
        layout.addWidget(back_btn)
        
        self.setLayout(layout)

        # Conexiones
        add_exercise_btn.clicked.connect(self.add_exercise)
        delete_exercise_btn.clicked.connect(self.delete_exercise)
        back_btn.clicked.connect(self.close)

        # Cargar ejercicios existentes
        self.load_exercises()

    def load_exercises(self):
        """Cargar los ejercicios desde la base de datos y mostrarlos en la lista."""
        self.exercise_list.clear()
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, categoria FROM Ejercicios")
        exercises = cursor.fetchall()
        conn.close()

        for exercise in exercises:
            self.exercise_list.addItem(f"{exercise[0]} - {exercise[1]} ({exercise[2]})")

    def add_exercise(self):
        """Agregar un nuevo ejercicio a la base de datos."""
        nombre = self.exercise_name.text()
        categoria = self.exercise_category.text()
        
        # Validación de entrada
        if not nombre or not categoria:
            QMessageBox.warning(self, "Error", "Por favor, ingrese un nombre y una categoría.")
            return

        # Insertar ejercicio en la base de datos
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Ejercicios (nombre, categoria) VALUES (?, ?)", (nombre, categoria))
        conn.commit()
        conn.close()

        # Limpiar campos y actualizar lista
        self.exercise_name.clear()
        self.exercise_category.clear()
        self.load_exercises()
        QMessageBox.information(self, "Éxito", "Ejercicio agregado con éxito.")

    def delete_exercise(self):
        """Eliminar el ejercicio seleccionado de la base de datos."""
        selected_item = self.exercise_list.currentItem()
        
        if not selected_item:
            QMessageBox.warning(self, "Error", "Seleccione un ejercicio para eliminar.")
            return
        
        exercise_id = int(selected_item.text().split(" - ")[0])

        # Eliminar el ejercicio de la base de datos
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Ejercicios WHERE id = ?", (exercise_id,))
        conn.commit()
        conn.close()

        # Actualizar lista
        self.load_exercises()
        QMessageBox.information(self, "Éxito", "Ejercicio eliminado con éxito.")
