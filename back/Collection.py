from typing import Dict, Iterator
from back.Movie import Movie


class MovieCollection:
    def __init__(self):
        self.movies: Dict[str, Movie] = {}

    def add_movie(self, movie: Movie) -> None:
        self.movies[movie.title] = movie

    def remove_movie(self, title: str) -> None:
        if title in self.movies:
            del self.movies[title]

    def __iter__(self) -> Iterator[Movie]:
        return iter(self.movies.values())