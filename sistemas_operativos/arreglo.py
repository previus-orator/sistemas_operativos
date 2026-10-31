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

