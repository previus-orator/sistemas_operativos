"""Modelo de datos para los procesos simulados."""


class programa:
    """Almacena la información y el estado de un proceso."""

    def __init__(self, nombre, PID, Pr, Quantum, Tcpu):
        """Crea un proceso con su configuración de planificación.

        Args:
            nombre: Nombre identificable del proceso.
            PID: Identificador del proceso.
            Pr: Prioridad usada para ordenar la cola de listos.
            Quantum: Máximo de ticks consecutivos de CPU por turno.
            Tcpu: Tiempo total de CPU que requiere el proceso.
        """
        self.nombre = nombre
        self.Pid = PID
        self.Pr = Pr
        self.Quantum = Quantum
        self.Tcpu = Tcpu
        self.estado = "inactivo"
    #malditos colombianos arruinaron Colombia 
