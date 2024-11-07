# app.py
from views.main_menu import MainMenu
from views.manage_users import ManageUsers
from views.manage_exercises import ManageExercises
from views.manage_workouts import ManageWorkouts
from export_to_excel import export_to_excel
import sys
from PyQt5.QtWidgets import QApplication

class App:
    def __init__(self):
        self.main_menu = MainMenu()
        self.manage_users = ManageUsers()
        self.manage_exercises = ManageExercises()
        self.manage_workouts = ManageWorkouts()

        # Conectar botones
        self.main_menu.btn_users.clicked.connect(self.show_users)
        self.main_menu.btn_exercises.clicked.connect(self.show_exercises)
        self.main_menu.btn_workouts.clicked.connect(self.show_workouts)
        self.main_menu.btn_export.clicked.connect(self.export_to_excel)

    def show_users(self):
        self.manage_users.show()

    def show_exercises(self):
        self.manage_exercises.show()

    def show_workouts(self):
        self.manage_workouts.show()

    def export_to_excel(self):
        export_to_excel()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = App()
    main_app.main_menu.show()
    sys.exit(app.exec_())
