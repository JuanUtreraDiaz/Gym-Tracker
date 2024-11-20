# manage_workouts.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QLineEdit, QListWidget, QMessageBox
from database import create_connection

class ManageWorkouts(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Administrar Entrenamientos")
        
        layout = QVBoxLayout()
        self.workout_list = QListWidget()
        self.user_select = QComboBox()
        self.exercise_select = QComboBox()
        self.repetitions = QLineEdit()
        self.weight = QLineEdit()
        self.date = QLineEdit()
        
        add_workout_btn = QPushButton("Agregar Entrenamiento")
        delete_workout_btn = QPushButton("Eliminar Entrenamiento")
        back_btn = QPushButton("Volver al Menú Principal")
        
        layout.addWidget(QLabel("Lista de Entrenamientos"))
        layout.addWidget(self.workout_list)
        layout.addWidget(QLabel("Usuario:"))
        layout.addWidget(self.user_select)
        layout.addWidget(QLabel("Ejercicio:"))
        layout.addWidget(self.exercise_select)
        layout.addWidget(QLabel("Repeticiones:"))
        layout.addWidget(self.repetitions)
        layout.addWidget(QLabel("Peso:"))
        layout.addWidget(self.weight)
        layout.addWidget(QLabel("Fecha (YYYY-MM-DD):"))
        layout.addWidget(self.date)
        
        layout.addWidget(add_workout_btn)
        layout.addWidget(delete_workout_btn)
        layout.addWidget(back_btn)
        
        self.setLayout(layout)

        # Conexiones
        add_workout_btn.clicked.connect(self.add_workout)
        delete_workout_btn.clicked.connect(self.delete_workout)
        back_btn.clicked.connect(self.close)

        # Cargar entrenamientos existentes
        self.load_workouts()

    def showEvent(self, event):
        """Actualizar listas de usuarios y ejercicios cada vez que se muestra la ventana."""
        self.load_users()
        self.load_exercises()
        super().showEvent(event)

    def load_users(self):
        """Cargar los usuarios en el combobox de selección."""
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre FROM Usuarios")
        users = cursor.fetchall()
        conn.close()

        self.user_select.clear()
        for user in users:
            self.user_select.addItem(f"{user[1]}", user[0])  # Mostrar nombre, almacenar ID

    def load_exercises(self):
        """Cargar los ejercicios en el combobox de selección."""
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre FROM Ejercicios")
        exercises = cursor.fetchall()
        conn.close()

        self.exercise_select.clear()
        for exercise in exercises:
            self.exercise_select.addItem(f"{exercise[1]}", exercise[0])  # Mostrar nombre, almacenar ID

    def load_workouts(self):
        """Cargar los entrenamientos existentes en la lista."""
        self.workout_list.clear()
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, id_usuario, id_ejercicio, repeticiones, peso, fecha FROM Entrenamientos")
        workouts = cursor.fetchall()
        conn.close()

        for workout in workouts:
            self.workout_list.addItem(f"{workout[0]} - Usuario {workout[1]}, Ejercicio {workout[2]}, {workout[3]} reps, {workout[4]} kg, {workout[5]}")

    def add_workout(self):
        """Agregar un nuevo entrenamiento a la base de datos."""
        user_id = self.user_select.currentData()
        exercise_id = self.exercise_select.currentData()
        repeticiones = self.repetitions.text()
        peso = self.weight.text()
        fecha = self.date.text()

        # Validación de entrada
        if not repeticiones.isdigit() or not peso.replace('.', '', 1).isdigit():
            QMessageBox.warning(self, "Error", "Por favor, ingrese datos válidos para repeticiones y peso.")
            return

        # Calcular el número de serie para este entrenamiento en la misma fecha y ejercicio
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM Entrenamientos 
            WHERE id_usuario = ? AND id_ejercicio = ? AND fecha = ?
        """, (user_id, exercise_id, fecha))
        
        # La serie actual será el número de veces que el ejercicio ha sido registrado en la misma fecha + 1
        current_series_count = cursor.fetchone()[0]
        serie = current_series_count + 1

        # Insertar entrenamiento en la base de datos con la serie calculada
        cursor.execute("""
            INSERT INTO Entrenamientos (id_usuario, id_ejercicio, repeticiones, peso, fecha, serie) 
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, exercise_id, int(repeticiones), float(peso), fecha, serie))
        conn.commit()
        conn.close()

        # Limpiar campos y actualizar lista
        self.repetitions.clear()
        self.weight.clear()
        self.date.clear()
        self.load_workouts()
        QMessageBox.information(self, "Éxito", "Entrenamiento agregado con éxito.")

    def delete_workout(self):
        """Eliminar el entrenamiento seleccionado de la base de datos."""
        selected_item = self.workout_list.currentItem()
        
        if not selected_item:
            QMessageBox.warning(self, "Error", "Seleccione un entrenamiento para eliminar.")
            return
        
        workout_id = int(selected_item.text().split(" - ")[0])

        # Eliminar el entrenamiento de la base de datos
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Entrenamientos WHERE id = ?", (workout_id,))
        conn.commit()
        conn.close()

        # Actualizar lista
        self.load_workouts()
        QMessageBox.information(self, "Éxito", "Entrenamiento eliminado con éxito.")
