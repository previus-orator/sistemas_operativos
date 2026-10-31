class programa:
    def __init__(self, nombre, PID, Pr, Quantum, Tcpu, interactividad=1):
        if type(interactividad) is not int or not 1 <= interactividad <= 3:
            raise ValueError("El nivel de interactividad debe ser un entero entre 1 y 3.")
        self.nombre = nombre
        self.Pid = PID
        self.Pr = Pr
        self.Quantum = Quantum
        self.Tcpu = Tcpu
        self.Tcpu_original = Tcpu
        self.interactividad = interactividad
        self.estado = "inactivo"
    #malditos colombianos arruinaron Colombia 
