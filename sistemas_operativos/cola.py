"""Cola FIFO enlazada utilizada para los procesos suspendidos por E/S."""

from nodos import NodoLSE


class Cola:
    """Implementa una cola FIFO de datos enlazados."""

    def __init__(self):
        """Crea una cola vacía."""
        self.__frente = None

    def es_vacia(self):
        """Indica si la cola no contiene elementos."""
        return self.__frente is None

    def encolar(self, nuevo_dato):
        """Agrega un dato al final, manteniendo el tipo de la cola.

        Devuelve False si el dato no coincide con el tipo de los elementos
        existentes; en caso contrario, devuelve True.
        """
        if self.es_vacia():
            self.__frente = NodoLSE(nuevo_dato)
            return True
        if type(nuevo_dato) != type(self.__frente.dato):
            return False

        nodo_actual = self.__frente
        while nodo_actual.sig:
            nodo_actual = nodo_actual.sig

        nuevo_nodo = NodoLSE(nuevo_dato)
        nodo_actual.sig = nuevo_nodo
        return True

    def desencolar(self):
        """Quita y devuelve el elemento más antiguo, o None si está vacía."""
        if self.es_vacia():
            return None
        dato = self.__frente.dato
        self.__frente = self.__frente.sig
        return dato

    def __len__(self):
        """Devuelve la cantidad de elementos en la cola."""
        nodos = 0
        nodo_actual = self.__frente
        while nodo_actual:
            nodos += 1
            nodo_actual = nodo_actual.sig
        return nodos
