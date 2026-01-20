import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self.G = nx.Graph()

    def crea_grafo(self, numero_album_minimo):

        self.G.clear()

        self._lista_artisti = DAO.get_artisti(numero_album_minimo)

        self._dict_artisti = {}
        for arstista in self._lista_artisti:
            self._dict_artisti[arstista.id] = arstista

        self.G.add_nodes_from(self._lista_artisti)

        self.connessioni = DAO.get_connessioni(self._dict_artisti)

        for connessione in self.connessioni:
            self.G.add_edge(connessione.artista1, connessione.artista2, weight=connessione.peso)

    def gestisci_dettagli_nodo(self, id_nodo):
        nodo_selezionato = self._dict_artisti[id_nodo]

        self.lista_vicini = nx.neighbors(self.G, nodo_selezionato)

        self._dict_vicini_attributi = {}

        for vicino in self.lista_vicini:
            peso = self.G[vicino][nodo_selezionato]["weight"]
            self._dict_vicini_attributi[vicino] = peso

        self._artista_selezionato = nodo_selezionato

        return self._dict_vicini_attributi

    def get_cammino(self, durata_minima, numero_artisti_minimo):

       self._durata_minima = durata_minima
       self._numero_artisti = numero_artisti_minimo


       self._lista_artisti_filtrata = DAO.get_artsiti_per_durata(self._dict_artisti, durata_minima)

       self._sequenza_finale = []
       self._peso_complessivo = -1

       peso_corrente =  0
       sequenza_parziale = [self._artista_selezionato]

       self.ricorsione(self._artista_selezionato, peso_corrente, sequenza_parziale)

       return self._sequenza_finale, self._peso_complessivo

    def ricorsione(self, nodo_partenza, peso_corrente, sequenza_parziale):

        if len(sequenza_parziale) > self._numero_artisti:
            return

        if len(sequenza_parziale) == self._numero_artisti and peso_corrente > self._peso_complessivo:
            self._peso_complessivo = peso_corrente
            self._sequenza_finale = list(sequenza_parziale)

        for nodo in self.G.neighbors(nodo_partenza):
            peso = self.G.get_edge_data(nodo_partenza, nodo)["weight"]

            sequenza_parziale.append(nodo)
            nuovo_peso = peso + peso_corrente
            self.ricorsione(nodo, nuovo_peso, sequenza_parziale)
            sequenza_parziale.pop()
            return



