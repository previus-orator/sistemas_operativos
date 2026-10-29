from arreglo import arreglo, reloj
from cola import Cola


class GestorProcesos:
    def __init__(self, procesos=()):
        self.inactivos = list(procesos)
        self.listos = arreglo()
        self.suspendidos = Cola()
        self.terminados = []
        self.ejecutando = None
        self.reloj = reloj()
        self._quantum_restante = 0

        identificadores = [proceso.Pid for proceso in self.inactivos]
        if len(identificadores) != len(set(identificadores)):
            raise ValueError("Cada proceso debe tener un PID único.")

        for proceso in self.inactivos:
            proceso.estado = "inactivo"

    @property
    def completo(self):
        return (
            not self.inactivos
            and self.listos.es_vacia()
            and self.ejecutando is None
            and self.suspendidos.es_vacia()
        )

    def admitir(self, proceso):
        if proceso not in self.inactivos:
            return False
        self.inactivos.remove(proceso)
        if proceso.Tcpu == 0:
            proceso.estado = "terminado"
            self.terminados.append(proceso)
        else:
            proceso.estado = "listo"
            self.listos.agregar(proceso)
        return True
#no soy gay pero soy peruano y tengo una fantasía donde Perú invade Chile
    def admitir_todos(self):
        while self.inactivos:
            self.admitir(self.inactivos[0])

    def despachar(self):
        if self.ejecutando is not None:
            return self.ejecutando
        self.ejecutando = self.listos.desencolar()
        if self.ejecutando is not None:
            self.ejecutando.estado = "ejecutando"
            self._quantum_restante = self.ejecutando.Quantum
        return self.ejecutando

    def bloquear_actual(self, duracion):
        if not isinstance(duracion, int) or isinstance(duracion, bool) or duracion <= 0:
            raise ValueError("La duración de E/S debe ser un entero positivo.")
        if self.ejecutando is None:
            return False
        proceso = self.ejecutando
        proceso.estado = "suspendido"
        self.suspendidos.encolar((proceso, duracion))
        self.ejecutando = None
        self._quantum_restante = 0
        return True

    def avanzar(self):
        if self.completo:
            return None

        if self.ejecutando is None:
            self.despachar()

        proceso_ejecutado = self.ejecutando
        if proceso_ejecutado is not None:
            proceso_ejecutado.Tcpu -= 1
            self._quantum_restante -= 1

        self.reloj.avanzar()
        self._avanzar_esperas_es()

        if proceso_ejecutado is not None:
            if proceso_ejecutado.Tcpu == 0:
                proceso_ejecutado.estado = "terminado"
                self.terminados.append(proceso_ejecutado)
                self.ejecutando = None
                self._quantum_restante = 0
            elif self._quantum_restante == 0:
                proceso_ejecutado.estado = "listo"
                self.listos.agregar(proceso_ejecutado)
                self.ejecutando = None

        return proceso_ejecutado

    def _avanzar_esperas_es(self):
        cantidad = len(self.suspendidos)
        for _ in range(cantidad):
            proceso, restante = self.suspendidos.desencolar()
            restante -= 1
            if restante == 0:
                proceso.estado = "listo"
                self.listos.agregar(proceso)
            else:
                self.suspendidos.encolar((proceso, restante))
