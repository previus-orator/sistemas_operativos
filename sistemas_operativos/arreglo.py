"""Reloj de simulación y cola de procesos listos ordenada por planificación."""


class reloj:
    """Cuenta las unidades de tiempo transcurridas en la simulación."""

    def __init__(self):
        """Inicializa el reloj en cero."""
        self.tiempo = 0

    def avanzar(self):
        """Incrementa el reloj una unidad."""
        self.tiempo += 1


class arreglo:
    """Mantiene los procesos listos según prioridad, quantum y PID."""

    def __init__(self):
        """Crea una cola de procesos listos vacía."""
        self.arreglo = []

    def agregar(self, nuevo_programa):
        """Inserta un proceso en el orden de planificación.

        Se ordena por prioridad descendente, quantum ascendente y PID
        ascendente.
        """
        clave = (-nuevo_programa.Pr, nuevo_programa.Quantum, nuevo_programa.Pid)
        posicion = 0
        while posicion < len(self.arreglo):
            programa_actual = self.arreglo[posicion]
            clave_actual = (
                -programa_actual.Pr,
                programa_actual.Quantum,
                programa_actual.Pid,
            )
            if clave < clave_actual:
                break
            posicion += 1
        #código hijueputa como Abelardo
        self.arreglo.insert(posicion, nuevo_programa)

    def desencolar(self):
        """Extrae y devuelve el proceso con mayor preferencia, si existe."""
        if not self.arreglo:
            return None
        return self.arreglo.pop(0)

    def es_vacia(self):
        """Indica si no hay procesos listos."""
        return not self.arreglo
