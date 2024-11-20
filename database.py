# database.py
import sqlite3

def create_connection():
    connection = sqlite3.connect("data/fitness_app.db")
    return connection

def initialize_database():
    conn = create_connection()
    cursor = conn.cursor()
    
    # Tabla de Usuarios
    cursor.execute('''CREATE TABLE IF NOT EXISTS Usuarios (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      nombre TEXT NOT NULL,
                      edad INTEGER,
                      altura REAL
                      )''')
    
    # Tabla de Ejercicios
    cursor.execute('''CREATE TABLE IF NOT EXISTS Ejercicios (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      nombre TEXT NOT NULL,
                      categoria TEXT
                      )''')
    
    # Tabla de Entrenamientos
    cursor.execute('''CREATE TABLE IF NOT EXISTS Entrenamientos (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      id_usuario INTEGER,
                      id_ejercicio INTEGER,
                      repeticiones INTEGER,
                      peso REAL,
                      fecha TEXT,
                      serie INTEGER,
                      FOREIGN KEY (id_usuario) REFERENCES Usuarios(id),
                      FOREIGN KEY (id_ejercicio) REFERENCES Ejercicios(id)
                      )''')
    
    conn.commit()
    conn.close()

# Llamar a esta función en el inicio para crear las tablas si no existen
initialize_database()
