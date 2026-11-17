"""Coordinación de la planificación y los estados de los procesos."""

from arreglo import arreglo, reloj
from cola import Cola


class GestorProcesos:
    """Ejecuta procesos y controla sus colas de listos y suspendidos."""

    def __init__(self, procesos=()):
        """Agrega el conjunto inicial de procesos a la cola de listos."""
        self.listos = arreglo()
        self.suspendidos = Cola()
        self.terminados = []
        self.ejecutando = None
        self.reloj = reloj()
        self._quantum_restante = 0

        for proceso in procesos:
            if proceso.Tcpu == 0:
                proceso.estado = "terminado"
                self.terminados.append(proceso)
            else:
                proceso.estado = "listo"
                self.listos.agregar(proceso)

    @property
    def completo(self):
        """Indica si no quedan procesos listos, ejecutándose o suspendidos."""
        return (
            self.listos.es_vacia()
            and self.ejecutando is None
            and self.suspendidos.es_vacia()
        )

    #no soy gay pero soy peruano y tengo una fantasía donde Perú invade Chile
    def despachar(self):
        """Selecciona el siguiente proceso listo para usar la CPU."""
        if self.ejecutando is not None:
            return self.ejecutando
        self.ejecutando = self.listos.desencolar()
        if self.ejecutando is not None:
            self.ejecutando.estado = "ejecutando"
            self._quantum_restante = self.ejecutando.Quantum
        return self.ejecutando

    def bloquear_actual(self, duracion):
        """Suspende el proceso actual durante una espera de E/S.

        Args:
            duracion: Cantidad de unidades de tiempo que durará la espera.

        Raises:
            ValueError: Si la duración no es un entero positivo.

        Returns:
            True si se suspendió un proceso; False si la CPU estaba inactiva.
        """
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
        """Avanza un tick, actualiza procesos y devuelve el ejecutado."""
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
        """Reduce un tick las esperas y devuelve a listos las que terminan."""
        cantidad = len(self.suspendidos)
        for _ in range(cantidad):
            proceso, restante = self.suspendidos.desencolar()
            restante -= 1
            if restante == 0:
                proceso.estado = "listo"
                self.listos.agregar(proceso)
            else:
                self.suspendidos.encolar((proceso, restante))
