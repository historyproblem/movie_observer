from PyQt6.QtGui import QCloseEvent, QIntValidator
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QListWidget, QLabel, QStackedWidget,
    QFormLayout, QMessageBox
)
from back.Collection import MovieCollection
from back.Movie import Movie
from datetime import datetime

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.collection = MovieCollection()
        self.current_filters = {}
        self.setup_ui()
        self.setup_validators()

    def setup_ui(self):
        self.setWindowTitle("Movie Manager")
        self.setGeometry(100, 100, 600, 400)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.setup_add_movie_screen()
        self.setup_view_movies_screen()

        self.stacked_widget.addWidget(self.add_movie_widget)
        self.stacked_widget.addWidget(self.view_movies_widget)

    def setup_validators(self):
        current_year = datetime.now().year
        self.year_input.setValidator(QIntValidator(1900, current_year, self))

    def setup_view_movies_screen(self):
        self.view_movies_widget = QWidget()
        layout = QVBoxLayout()

        search_form = QWidget()
        form_layout = QFormLayout()

        self.search_title = QLineEdit()
        self.search_year = QLineEdit()
        self.search_genre = QLineEdit()

        form_layout.addRow("Название:", self.search_title)
        form_layout.addRow("Год:", self.search_year)
        form_layout.addRow("Жанр:", self.search_genre)
        search_form.setLayout(form_layout)

        btn_layout = QHBoxLayout()
        search_btn = QPushButton("Поиск")
        search_btn.clicked.connect(self.apply_filters)

        reset_btn = QPushButton("Сбросить")
        reset_btn.clicked.connect(self.reset_filters)

        btn_layout.addWidget(search_btn)
        btn_layout.addWidget(reset_btn)

        self.movies_list = QListWidget()

        back_btn = QPushButton("Назад")
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))

        layout.addWidget(search_form)
        layout.addLayout(btn_layout)
        layout.addWidget(self.movies_list)
        layout.addWidget(back_btn)
        self.view_movies_widget.setLayout(layout)
        self.update_movies_list()

    def setup_add_movie_screen(self):
        self.add_movie_widget = QWidget()
        layout = QVBoxLayout()

        self.title_input = QLineEdit()
        self.year_input = QLineEdit()
        self.genre_input = QLineEdit()

        layout.addWidget(QLabel("Название фильма:"))
        layout.addWidget(self.title_input)
        layout.addWidget(QLabel("Год выпуска:"))
        layout.addWidget(self.year_input)
        layout.addWidget(QLabel("Жанр:"))
        layout.addWidget(self.genre_input)

        add_btn = QPushButton("Добавить фильм")
        add_btn.clicked.connect(self.add_movie)

        view_btn = QPushButton("Просмотр фильмов")
        view_btn.clicked.connect(lambda: [
            self.stacked_widget.setCurrentIndex(1),
            self.update_movies_list()  # Обновление при каждом переходе
        ])

        layout.addWidget(add_btn)
        layout.addWidget(view_btn)
        self.add_movie_widget.setLayout(layout)

    def apply_filters(self):
        self.current_filters = {
            "title": self.search_title.text().strip().lower(),
            "year": self.search_year.text().strip(),
            "genre": self.search_genre.text().strip().lower()
        }
        self.update_movies_list()

    def reset_filters(self):
        self.search_title.clear()
        self.search_year.clear()
        self.search_genre.clear()
        self.current_filters = {}
        self.update_movies_list()

    def add_movie(self):
        try:
            title = self.title_input.text().strip()
            year = self.year_input.text().strip()
            genre = self.genre_input.text().strip()

            # Проверка на пустые поля
            if not (title and year and genre):
                QMessageBox.warning(self, "Ошибка", "Все поля обязательны для заполнения!")
                return

            # Проверка, что год - число
            if not year.isdigit():
                QMessageBox.warning(
                    self,
                    "Ошибка",
                    "Год должен содержать только цифры"
                )
                return

            # Валидация года
            current_year = datetime.now().year  # Определяем ДО блока try
            year_int = int(year)

            if year_int < 1900 or year_int > current_year:
                QMessageBox.warning(
                    self,
                    "Ошибка",
                    f"Год должен быть между 1900 и {current_year}"
                )
                return

            # Добавление фильма
            movie = Movie(title, year, genre)
            self.collection.add_movie(movie)
            self.title_input.clear()
            self.year_input.clear()
            self.genre_input.clear()
            self.update_movies_list()

        except Exception as e:
            QMessageBox.critical(
                self,
                "Ошибка",
                f"Не удалось добавить фильм: {str(e)}"
            )

    def update_movies_list(self):
        try:
            self.movies_list.clear()
            for movie in self.collection:
                match = True

                if self.current_filters.get("title"):
                    if self.current_filters["title"] not in movie.title.lower():
                        match = False

                if self.current_filters.get("year"):
                    if self.current_filters["year"] != movie.year:
                        match = False

                if self.current_filters.get("genre"):
                    if self.current_filters["genre"] not in movie.genre.lower():
                        match = False

                if match:
                    self.movies_list.addItem(
                        f"{movie.title} ({movie.year}) - {movie.genre}"
                    )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Ошибка",
                f"Не удалось обновить список: {str(e)}"
            )

    def closeEvent(self, event: QCloseEvent) -> None:
        try:
            self.collection.save_to_file()
        except Exception as e:
            QMessageBox.critical(
                self,
                "Ошибка сохранения",
                f"Не удалось сохранить данные: {str(e)}"
            )
        finally:
            event.accept()
