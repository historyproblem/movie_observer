import json
from typing import Dict, Iterator
from pathlib import Path
from back.Movie import Movie

class MovieCollection:
    def __init__(self):
        self.movies: Dict[str, Movie] = {}
        self.data_file = Path("movies_data.json")
        try:
            self.load_from_file()
        except Exception as e:
            raise RuntimeError(f"Ошибка загрузки данных: {str(e)}")

    def add_movie(self, movie: Movie) -> None:
        try:
            self.movies[movie.title] = movie
            self.save_to_file()
        except Exception as e:
            raise RuntimeError(f"Ошибка добавления фильма: {str(e)}")

    def remove_movie(self, title: str) -> None:
        if title in self.movies:
            del self.movies[title]
            self.save_to_file()

    def __iter__(self) -> Iterator[Movie]:
        return iter(self.movies.values())

    def save_to_file(self) -> None:
        try:
            data = [
                {"title": m.title, "year": m.year, "genre": m.genre}
                for m in self.movies.values()
            ]
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            raise RuntimeError(f"Ошибка сохранения: {str(e)}")

    def load_from_file(self) -> None:
        try:
            if self.data_file.exists():
                with open(self.data_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for item in data:
                        movie = Movie(
                            item["title"],
                            item["year"],
                            item["genre"]
                        )
                        self.movies[movie.title] = movie
        except Exception as e:
            raise RuntimeError(f"Ошибка загрузки: {str(e)}")