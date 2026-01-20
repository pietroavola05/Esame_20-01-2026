from dataclasses import dataclass

from model.artist import Artist


@dataclass
class Connessione:
    artista1: Artist
    artista2: Artist
    peso: int
