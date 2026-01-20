from database.DB_connect import DBConnect
from model.artist import Artist
from model.connessione import Connessione


class DAO:

    @staticmethod
    def get_artisti(numero_album):

        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select a.id, a.name 
                from artist a, album al
                where a.id = al.artist_id
                group by a.id 
                having count(*) >= %s
                 """

        cursor.execute(query, (numero_album,))
        for row in cursor:
            artist = Artist(id=row['id'], name=row['name'])
            result.append(artist)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_connessioni(dict_artisti):

        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                select a1.artist_id as id1, a2.artist_id as id2, count(distinct t1.genre_id ) as conteggio
                from album a1, album a2, track t1, track t2 
                where a1.id = t1.album_id and a2.id = t2.album_id and a1.artist_id < a2.artist_id and t1.genre_id = t2.genre_id 
                group by a1.artist_id, a2.artist_id  """

        cursor.execute(query)
        for row in cursor:
            if row["id1"] in dict_artisti.keys() and row["id2"] in dict_artisti.keys():
                artista1 = dict_artisti[row["id1"]]
                artista2 = dict_artisti[row["id2"]]
                peso = row["conteggio"]

                connessione = Connessione(
                    artista1=artista1,
                    artista2=artista2,
                    peso=peso,
                )

                result.append(connessione)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_artsiti_per_durata(dict_artisti, durata):

        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                select distinct(a.artist_id)
                from album a, track t 
                where a.id = t.album_id 
                group by a.artist_id, t.milliseconds 
                having (t.milliseconds/60000) > %s """

        cursor.execute(query, (durata,))
        for row in cursor:
            if row["artist_id"] in dict_artisti.keys():
                artista1 = dict_artisti[row["artist_id"]]
                result.append(artista1)
        cursor.close()
        conn.close()
        return result




