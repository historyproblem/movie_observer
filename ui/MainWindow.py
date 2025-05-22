from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QListWidget, QLabel, QStackedWidget
)
from back.Collection import MovieCollection
from back.Movie import Movie
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.collection = MovieCollection()
        self.setWindowTitle("Movie Manager")
        self.setGeometry(100, 100, 600, 400)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.add_movie_widget = QWidget()
        self.setup_add_movie_screen()

        self.view_movies_widget = QWidget()
        self.setup_view_movies_screen()

        self.stacked_widget.addWidget(self.add_movie_widget)
        self.stacked_widget.addWidget(self.view_movies_widget)

    def setup_add_movie_screen(self):
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
        view_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        layout.addWidget(add_btn)
        layout.addWidget(view_btn)
        self.add_movie_widget.setLayout(layout)

    def setup_view_movies_screen(self):
        layout = QVBoxLayout()
        self.movies_list = QListWidget()

        back_btn = QPushButton("Назад")
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))

        layout.addWidget(self.movies_list)
        layout.addWidget(back_btn)
        self.view_movies_widget.setLayout(layout)

    def add_movie(self):
        title = self.title_input.text()
        year = self.year_input.text()
        genre = self.genre_input.text()

        if title and year and genre:
            movie = Movie(title, year, genre)
            self.collection.add_movie(movie)
            self.title_input.clear()
            self.year_input.clear()
            self.genre_input.clear()

            self.movies_list.clear()
            for movie in self.collection:
                self.movies_list.addItem(
                    f"{movie.title} ({movie.year}) - {movie.genre}"
                )