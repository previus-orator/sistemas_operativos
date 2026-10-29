class NodoLSE:
    """Clase que implementa el funcionamiento de un nodo para una lista
    simplemente enlazada.
    """
    def __init__(self, dato):
        """método que inicializa la creación de un objeto de tipo nodo
        para una lista simplemente enlazada.

        Parameters
        ----------
        dato : object
            Dato que se almacenará en el nodo.

        """
        self.dato = dato
        self.sig = None

    # def __repr__(self):
    #     return(str(self.dato)')

    def __str__(self):
        """metodo que retorna la cadena correspondiente al dato del nodo

        Returns
        -------
        str
            cadena que representa al dato del nodo.
        """
        return (str(self.dato))


class NodoLDE:
    """Clase que implementa el funcionamiento de un nodo para una lista
    doblemente enlazada.
    """
    def __init__(self, dato):
        """método que inicializa la creación de un objeto de tipo nodo
        para una lista doblemente enlazada.

        Parameters
        ----------
        dato : object
            Dato que se almacenará en el nodo.

        """
        self.dato = dato
        self.ant = None
        self.sig = None

    def __str__(self):
        """metodo que retorna la cadena correspondiente al dato del nodo

        Returns
        -------
        str
            cadena que representa al dato del nodo.
        """
        return (str(self.dato))


