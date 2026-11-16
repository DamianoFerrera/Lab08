from database.distributore_DAO import DistributoreDAO
from database.prezzo_DAO import PrezzoDAO
from UI.view import View

'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class Model:
    def __init__(self, view : View):
        self._distributori = None
        self.load_distributori()
        self._view = view

        self.__sequenza_ottima = []
        self.__costo_ottimo = -1

    def load_distributori(self):
        """ Carica tutti i distributori e li setta nella variabile self._distributori """
        self._distributori = DistributoreDAO.get_distributori()

    def get_prezzo_medio(self, mese:int):

        """Calcola, per ogni distributore, il prezzo medio al litro per il mese selezionato.
                :param mese: Mese selezionato (un intero da 1 a 12)
                :return: lista di tuple --> (nome del distributore, media), es. (Distributore A, 1.789) """

        self._prezzi_A = PrezzoDAO.get_prezzi('1')
        self._prezzi_B = PrezzoDAO.get_prezzi('2')
        self._contenitore_prezzi_A = []
        self._contenitore_prezzi_B = []
        self._media_A = None
        self._media_B = None
        if self._prezzi_A is None :
            self._view.show_alert('Errore connessione database (DIstributore A in get_prezzo_medio')
            return None

        else:
            self._contenitore_prezzi_A.clear()
            for prezzo_A in self._prezzi_A:
                if prezzo_A.data.month == mese:
                    self._contenitore_prezzi_A.append(float(prezzo_A.prezzo_litro))
            self._media_A = sum(self._contenitore_prezzi_A)/len(self._contenitore_prezzi_A)

        if self._prezzi_B is None :
            self._view.show_alert('Errore connessione database (DIstributore B in get_prezzo_medio')
            return None

        else:
            self._contenitore_prezzi_B.clear()
            for prezzo_B in self._prezzi_B:
                if prezzo_B.data.month == mese:
                    self._contenitore_prezzi_B.append(float(prezzo_B.prezzo_litro))
            self._media_B = sum(self._contenitore_prezzi_B)/len(self._contenitore_prezzi_B)

        return [('DIstributore A', self._media_A),('Distributore B',self._media_B)]
      # TODO

    def get_sequenza_ottima(self, mese:int):
        """
        Calcola la sequenza ottimale di rifornimenti nei primi 7 giorni
        :return: sequenza di nomi distributore ottimale
        :return: costo ottimale (cioè quello minimizzato dalla sequenza scelta)
        """
        self.__sequenza_ottima = []
        self.__costo_ottimo = -1
        prezzi_settimana = self.__get_prezzi_prima_settimana_mese(mese)

        self.__ricorsione([], 1, None, 0, prezzi_settimana)

        # Traduci gli ID in nomi
        id_to_nome = {distributore.id: distributore.nome for distributore in self._distributori}
        sequenza_nomi = [f"Giorno {giorno}: {id_to_nome[i]}" for giorno, i in enumerate(self.__sequenza_ottima, start=1)]
        return sequenza_nomi, round(self.__costo_ottimo, 2)

    def __ricorsione(self, sequenza_parziale, giorno, ultimo_distributore, costo_corrente, prezzi_settimana):
        """ Implementa la ricorsione """
        # TODO

    def __get_prezzi_prima_settimana_mese(self, mese: int):
        """
        Restituisce i prezzi dei primi 7 giorni del mese selezionato per ciascun distributore.
        :return: un dizionario: {id_distributore: [prezzo_giorno1, ..., prezzo_giorno7]}
        """
        self._prezzi_A = PrezzoDAO.get_prezzi('1')
        self._prezzi_B = PrezzoDAO.get_prezzi('2')
        self.primi_7_giorni_A = []
        self.primi_7_giorni_B = []
        if self._prezzi_A is None :
            self._view.show_alert('Errore connessione database (DIstributore A in get_prezzi_prima_settimana_mese')
            return None
        else:
            self.primi_7_giorni_A.clear()
            for prezzo_A in self._prezzi_A:
                if prezzo_A.data.month == mese:
                    if prezzo_A.data.day <= 7:
                        self.primi_7_giorni_A.append(float(prezzo_A.prezzo_litro))

        if self._prezzi_B is None :
            self._view.show_alert('Errore connessione database (DIstributore B in get_prezzi_prima_settimana_mese')
            return None
        else:
            self.primi_7_giorni_B.clear()
            for prezzo_B in self._prezzi_B:
                if prezzo_B.data.month == mese:
                    if prezzo_B.data.day <= 7:
                        self.primi_7_giorni_B.append(float(prezzo_B.prezzo_litro))
        return {'1':self.primi_7_giorni_A, '2':self.primi_7_giorni_B}
        # TODO