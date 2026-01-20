import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

        self.numero_album_minimo = None

    def get_dato_from_view(self):

        print("Sono nel get dato")






    def handle_create_graph(self, e):

        print("Sono qui")

        valore = self._view.txtNumAlbumMin.value
        try:
            self.numero_album_minimo = int(valore)
            if self.numero_album_minimo <= 0:
                self._view.show_alert("Numero album minimo negativo")
                self._view._page.update()
                return
        except:
            self._view.show_alert("Numero album non numerico")
            self._view._page.update()
            return

        print(self.numero_album_minimo)

        if self.numero_album_minimo:
            self._model.crea_grafo(self.numero_album_minimo)

            if self._model.G.number_of_nodes() > 0:

                print("Ora sono qui")

                numero_nodi = self._model.G.number_of_nodes()
                numero_archi = self._model.G.number_of_edges()

                self._view.txt_result.controls.clear()
                self._view.txt_result.controls.append(ft.Text(f"{numero_nodi} nodi"))
                self._view.txt_result.controls.append(ft.Text(f"{numero_archi} archi"))

                self._view.ddArtist.disabled = False
                self._view.btnArtistsConnected.disabled = False
                self.popola_dropdown_artisti()

                self._view._page.update()

    def popola_dropdown_artisti(self):

        """ Metodo per popolare i dropdown"""
        for elemento in self._model._lista_artisti:
            self._view.ddArtist.options.append(ft.dropdown.Option(key=elemento.id, text=elemento.name))

        self._view._page.update()

    def on_change_artista(self, e):
        valore_anno = e.control.value

        try:
            self.id_artista_selezionato = int(valore_anno)
        except ValueError:
            self._view.show_alert("Errore in valore id_Artista")
            self._view._page.update()


    def handle_connected_artists(self, e):

        if self.id_artista_selezionato is None:
            self._view.show_alert("Scegli Squadra")
            return

        dizionario = self._model.gestisci_dettagli_nodo(self.id_artista_selezionato)

        self._lista_ordinata = sorted(dizionario.items(), key=lambda x: x[0].id, reverse=False)
        """x rappresenta la singola tupla, x[0] è la chiave, x[1] è il valore"""

        if dizionario:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Artisti collegati all'artista {self.id_artista_selezionato}"))
            self._view.txtMinDuration.disabled = False
            self._view.txtMaxArtists.disabled = False
            self._view.btnSearchArtists.disabled = False

            for nodo, peso in self._lista_ordinata:
                self._view.txt_result.controls.append(ft.Text(f"{nodo} -> Numero di generi in comune {peso}"))
        else:
            self._view.show_alert("Dettagli non disponibili")

        self._view._page.update()


    def genera_cammino(self, e):

        durata_minima = self._view.txtMinDuration.value

        try:
            self.durata_minima = float(durata_minima)
            if self.numero_album_minimo <= 0:
                self._view.show_alert("Numero durata minima negativo")
                self._view._page.update()
                return
        except:
            self._view.show_alert("Numero durata non numerico")
            self._view._page.update()
            return

        numero_max_artista = self._view.txtMaxArtists.value

        try:
            self.numero_max_artisti = int(numero_max_artista)
            if self.numero_album_minimo <= 0 or self.numero_album_minimo > len(self._lista_ordinata) :
                self._view.show_alert("Numero max artisti negativo o maggiore di artisti in dropdown")
                self._view._page.update()
                return
        except:
            self._view.show_alert("Numero max artisti non numerico")
            self._view._page.update()
            return


        percorso, peso_totale = self._model.get_cammino(self.durata_minima, self.numero_max_artisti)

        if percorso:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text(f"Percorso trovato:"))

            for i in range(len(percorso) - 1):
                nodo1 = percorso[i]
                nodo2 = percorso[i + 1]

                # distanza_nodi = distance.geodesic((nodo1.lat, nodo1.lng), (nodo2.lat, nodo2.lng)).km
                peso_arco = self._model.G.get_edge_data(nodo1, nodo2)['weight']

                testo_arco = f"[{nodo1}] --> [{nodo2}] [peso: {peso_arco:.2f}]"
                self._view.txt_result.controls.append(ft.Text(testo_arco))

            self._view.txt_result.controls.append(
                ft.Text(f"\nDistanza Totale: {peso_totale:.2f}"))

        else:
            self._view.txt_result.controls.append(
                ft.Text("Nessun percorso valido trovato."))

        self._view._page.update()







