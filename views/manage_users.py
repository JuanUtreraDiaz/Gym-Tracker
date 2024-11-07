# manage_users.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QListWidget, QMessageBox
from database import create_connection

class ManageUsers(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Administrar Usuarios")
        
        layout = QVBoxLayout()
        self.user_list = QListWidget()
        self.user_name = QLineEdit()
        self.user_age = QLineEdit()
        self.user_height = QLineEdit()
        
        add_user_btn = QPushButton("Agregar Usuario")
        delete_user_btn = QPushButton("Eliminar Usuario")
        back_btn = QPushButton("Volver al Menú Principal")
        
        layout.addWidget(QLabel("Lista de Usuarios"))
        layout.addWidget(self.user_list)
        layout.addWidget(QLabel("Nombre:"))
        layout.addWidget(self.user_name)
        layout.addWidget(QLabel("Edad:"))
        layout.addWidget(self.user_age)
        layout.addWidget(QLabel("Altura:"))
        layout.addWidget(self.user_height)
        
        layout.addWidget(add_user_btn)
        layout.addWidget(delete_user_btn)
        layout.addWidget(back_btn)
        
        self.setLayout(layout)

        # Conexiones
        add_user_btn.clicked.connect(self.add_user)
        delete_user_btn.clicked.connect(self.delete_user)
        back_btn.clicked.connect(self.close)

        # Cargar usuarios existentes
        self.load_users()

    def load_users(self):
        """Cargar los usuarios desde la base de datos y mostrarlos en la lista."""
        self.user_list.clear()
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre FROM Usuarios")
        users = cursor.fetchall()
        conn.close()

        for user in users:
            self.user_list.addItem(f"{user[0]} - {user[1]}")

    def add_user(self):
        """Agregar un nuevo usuario a la base de datos."""
        nombre = self.user_name.text()
        edad = self.user_age.text()
        altura = self.user_height.text()
        
        # Validación de entrada
        if not nombre or not edad.isdigit() or not altura.replace('.', '', 1).isdigit():
            QMessageBox.warning(self, "Error", "Por favor, ingrese datos válidos.")
            return

        # Insertar usuario en la base de datos
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Usuarios (nombre, edad, altura) VALUES (?, ?, ?)", (nombre, int(edad), float(altura)))
        conn.commit()
        conn.close()

        # Limpiar campos y actualizar lista
        self.user_name.clear()
        self.user_age.clear()
        self.user_height.clear()
        self.load_users()
        QMessageBox.information(self, "Éxito", "Usuario agregado con éxito.")

    def delete_user(self):
        """Eliminar el usuario seleccionado de la base de datos."""
        selected_item = self.user_list.currentItem()
        
        if not selected_item:
            QMessageBox.warning(self, "Error", "Seleccione un usuario para eliminar.")
            return
        
        user_id = int(selected_item.text().split(" - ")[0])

        # Eliminar el usuario de la base de datos
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Usuarios WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()

        # Actualizar lista
        self.load_users()
        QMessageBox.information(self, "Éxito", "Usuario eliminado con éxito.")
