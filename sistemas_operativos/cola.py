from heapq import heappop, heappush
from itertools import count

from nodos import NodoLSE

class Cola:
    """ clase que implementa el funcionamiento del TAD cola (FIFO)"""
    def __init__(self):
        """ metodo constructor que realiza la creación e inicialización de una
        Cola"""
        self.__frente = None

    def es_vacia(self):
        """Método que verifica si la cola está vacía.

        Returns
        -------
        bool
            True si la cola está vacía, False en caso contrario.
        """
        return (self.__frente is None)

    def encolar(self, nuevo_dato):
        """Método que realiza la entrada de un nuevo dato a la cola, se
        realiza la validacion de homogeneidad para cada dato ingresado en la
        cola.

        Parameters
        -------
        nuevo_dato : object
            El nuevo dato a ser adicionado a la cola
        Returns
        -------
        bool
            True si nuevo_dato fue encolado, False en caso contrario.
        """
        if self.es_vacia():
            self.__frente = NodoLSE(nuevo_dato)
            return True
        if not self.es_vacia() and type(nuevo_dato) != type(self.__frente.dato):
            return False

        nodo_actual = self.__frente
        while nodo_actual.sig:
            nodo_actual = nodo_actual.sig

        nuevo_nodo = NodoLSE(nuevo_dato)
        nodo_actual.sig = nuevo_nodo
        return True

    def desencolar(self):
        """Método que saca/quita el primer nodo (elimina el nodo) de la cola y
        retorna su dato

        Returns
        -------
        object | None
            el dato del nodo desencolado, None en caso de que la cola no tenga
            datos/nodos.
        """
        if self.es_vacia():
            return None
        dato = self.__frente.dato
        self.__frente = self.__frente.sig
        return dato

    def frente(self):
        """Método que retorna el dato almacenado en el frente de la cola sin
        eliminarlo.

        Returns
        -------
        object | None
            el dato del frente de la cola, None si la cola está vacía.
        """
        if self.__frente:
            return self.__frente.dato
        return None

 
    def __len__(self):
        """Método que retorna el número de nodos que tiene la cola.

        Returns
        -------
        int
            Tamaño de la cola.
        """
        nodos = 0
        nodo_actual = self.__frente
        while nodo_actual:
            nodos += 1
            nodo_actual = nodo_actual.sig
        return nodos


class ColaTemporizada:
    "Cola de prioridad para mejorar la cosa de suspendidos supongo"

    def __init__(self):
        self.__elementos = []
        self.__secuencia = count()

    def es_vacia(self):
        return not self.__elementos

    def encolar(self, dato, tiempo_despertar):
        heappush(
            self.__elementos,
            (tiempo_despertar, next(self.__secuencia), dato),
        )
        return True

    def desencolar_vencidos(self, tiempo_actual):
        vencidos = []
        while self.__elementos and self.__elementos[0][0] <= tiempo_actual:
            _, _, dato = heappop(self.__elementos)
            vencidos.append(dato)
        return vencidos

    def __len__(self):
        return len(self.__elementos)
