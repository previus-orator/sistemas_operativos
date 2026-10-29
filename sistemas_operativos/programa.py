class programa:
    def __init__(self, nombre, PID, Pr, Quantum, Tcpu):
        self.nombre = nombre
        self.Pid = PID
        self.Pr = Pr
        self.Quantum = Quantum
        self.Tcpu = Tcpu
        self.Tcpu_original = Tcpu
        self.estado = "inactivo"
    #malditos colombianos arruinaron Colombia 
