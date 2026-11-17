"""Nodos enlazados usados por las estructuras del proyecto."""


class NodoLSE:
    """Nodo de una lista simplemente enlazada."""

    def __init__(self, dato):
        """Crea un nodo con el dato indicado y sin sucesor."""
        self.dato = dato
        self.sig = None

    # def __repr__(self):
    #     return(str(self.dato)')

    def __str__(self):
        """Devuelve la representación textual del dato almacenado."""
        return str(self.dato)
