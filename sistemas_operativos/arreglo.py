class reloj:
    def __init__(self):
        self.tiempo = 0

    def avanzar(self):
        self.tiempo += 1
        return self.tiempo


class arreglo:
    def __init__(self):
        self.arreglo = []

    def agregar(self, nuevo_programa):
        papu_cosa = (-nuevo_programa.Pr, nuevo_programa.Quantum, nuevo_programa.Pid)
        i = 0
        while i < len(self.arreglo):
            programa_actual = self.arreglo[i]
            papu_cosa_actual = (
                -programa_actual.Pr,
                programa_actual.Quantum,
                programa_actual.Pid,
            )
            if papu_cosa < papu_cosa_actual:
                break
            i += 1
        #código hijueputa como Abelardo
        self.arreglo.insert(i, nuevo_programa)
        return True

    def obtener(self, i=0):
        if not isinstance(i, int) or i < 0:
            return None
        if i >= len(self.arreglo):
            return None
        return self.arreglo[i]

    def desencolar(self):
        if not self.arreglo:
            return None
        return self.arreglo.pop(0)

    def es_vacia(self):
        return not self.arreglo

    def __len__(self):
        return len(self.arreglo)

    def __iter__(self):
        return iter(self.arreglo)


class ejecutar:
    def __init__(self, arreglo):
        self.arreglo = arreglo

    def ejecutar(self):
        #ejecuta el programa activo y lo elimina de la lista de prioridad si su tiempo de CPU es 0, de lo contrario lo envía a la cola de espera bla bla bla
        proceso = self.arreglo.desencolar()
        if proceso is None:
            return None
        proceso.Tcpu = max(0, proceso.Tcpu - proceso.Quantum)
        if proceso.Tcpu > 0:
            self.arreglo.agregar(proceso)
        else:
            proceso.estado = "terminado"
        return proceso
    #fernando si lees esto, me hiciste estafar (ve a cali *inserte el gato que siempre mando*)


class cola:
    def __init__(self):
        self.cola = []

    def agregar(self, nuevo_programa):
        self.cola.append(nuevo_programa)
        return True

    def desencolar(self):
        if not self.cola:
            return None
        return self.cola.pop(0)

    def es_vacia(self):
        return not self.cola

    def __len__(self):
        return len(self.cola)

    def mover_a_lista(self, arreglo):
        #mueve los programas de la cola a la lista de prioridad si su tiempo de CPU es 0
        cantidad = len(self.cola)
        for _ in range(cantidad):
            proceso = self.desencolar()
            if proceso is not None and proceso.Tcpu > 0:
                proceso.estado = "listo"
                arreglo.agregar(proceso)
        return cantidad
