from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QListWidget, QLabel, QStackedWidget,
    QFormLayout
)
from back.Collection import MovieCollection
from back.Movie import Movie


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.collection = MovieCollection()
        self.current_filters = {}
        self.setup_ui()  # Вызываем метод настройки интерфейса

    def setup_ui(self):
        """Инициализация всего интерфейса"""
        self.setWindowTitle("Movie Manager")
        self.setGeometry(100, 100, 600, 400)

        # Создаем stacked widget для переключения экранов
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Инициализация экранов
        self.setup_add_movie_screen()
        self.setup_view_movies_screen()

        # Добавляем экраны в stacked widget
        self.stacked_widget.addWidget(self.add_movie_widget)
        self.stacked_widget.addWidget(self.view_movies_widget)

    def setup_view_movies_screen(self):
        """Экран просмотра и поиска фильмов"""
        self.view_movies_widget = QWidget()
        layout = QVBoxLayout()

        # Форма для поиска
        search_form = QWidget()
        form_layout = QFormLayout()

        self.search_title = QLineEdit()
        self.search_year = QLineEdit()
        self.search_genre = QLineEdit()

        form_layout.addRow("Название:", self.search_title)
        form_layout.addRow("Год:", self.search_year)
        form_layout.addRow("Жанр:", self.search_genre)
        search_form.setLayout(form_layout)

        # Кнопки поиска и сброса
        btn_layout = QHBoxLayout()
        search_btn = QPushButton("Поиск")
        search_btn.clicked.connect(self.apply_filters)

        reset_btn = QPushButton("Сбросить")
        reset_btn.clicked.connect(self.reset_filters)

        btn_layout.addWidget(search_btn)
        btn_layout.addWidget(reset_btn)

        # Список фильмов
        self.movies_list = QListWidget()

        # Кнопка назад
        back_btn = QPushButton("Назад")
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))

        layout.addWidget(search_form)
        layout.addLayout(btn_layout)
        layout.addWidget(self.movies_list)
        layout.addWidget(back_btn)
        self.view_movies_widget.setLayout(layout)

    def setup_add_movie_screen(self):
        """Экран добавления фильма"""
        self.add_movie_widget = QWidget()
        layout = QVBoxLayout()

        # Поля ввода
        self.title_input = QLineEdit()
        self.year_input = QLineEdit()
        self.genre_input = QLineEdit()

        # Добавляем элементы
        layout.addWidget(QLabel("Название фильма:"))
        layout.addWidget(self.title_input)
        layout.addWidget(QLabel("Год выпуска:"))
        layout.addWidget(self.year_input)
        layout.addWidget(QLabel("Жанр:"))
        layout.addWidget(self.genre_input)

        # Кнопки
        add_btn = QPushButton("Добавить фильм")
        add_btn.clicked.connect(self.add_movie)

        view_btn = QPushButton("Просмотр фильмов")
        view_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        layout.addWidget(add_btn)
        layout.addWidget(view_btn)
        self.add_movie_widget.setLayout(layout)

    def apply_filters(self):
        # Собираем критерии поиска
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
        title = self.title_input.text().strip()
        year = self.year_input.text().strip()
        genre = self.genre_input.text().strip()

        if title and year and genre:
            movie = Movie(title, year, genre)
            self.collection.add_movie(movie)
            self.title_input.clear()
            self.year_input.clear()
            self.genre_input.clear()
            self.update_movies_list()



    def update_movies_list(self):
        self.movies_list.clear()
        for movie in self.collection:
            # Проверяем соответствие фильтрам
            match = True

            # Проверка названия
            if self.current_filters.get("title"):
                if self.current_filters["title"] not in movie.title.lower():
                    match = False

            # Проверка года
            if self.current_filters.get("year"):
                if self.current_filters["year"] != movie.year:
                    match = False

            # Проверка жанра
            if self.current_filters.get("genre"):
                if self.current_filters["genre"] not in movie.genre.lower():
                    match = False

            if match:
                self.movies_list.addItem(
                    f"{movie.title} ({movie.year}) - {movie.genre}"
                )
