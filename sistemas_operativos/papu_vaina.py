"""Punto de entrada para ejecutar la simulación del gestor de procesos."""

#Aquí empieza este código de cagada 
import time

from programa import programa
from gestor_procesos import GestorProcesos

#esto lo puso la IA para que vean como funciona, porque el código lo hacía instantaneamente y no se apreciaba la ejecución 
PAUSA_SIMULACION = 0.5 #esta en segundos :v

Programas = [
    programa("Steam", 4050, 3, 5, 10),
    programa("VLC media player", 1001, 2, 3, 6),
    programa("Visual Studio Code", 1002, 3, 4, 8),
    programa("YouTube", 1003, 2, 3, 5),
    programa("Firefox", 1004, 3, 4, 7),
    programa("YouTube", 1005, 2, 3, 5),
    programa("umamusume", 1006, 4, 2, 9),
    programa("Busca minas", 1011, 5, 1, 5),
    programa("uTorrent", 1024, 2, 5, 9),
    programa("ThunderBird", 1025, 3, 5, 9),
    programa("Amarok", 1035, 4, 5, 6),
    programa("Krita", 3020, 1, 2, 10),
    programa("virtual box", 2029, 3, 2, 10),
    programa("GIMP", 2001, 5, 2, 10),
    programa("libre office writer", 1029, 5, 2, 10),
]

#mi cara cuándo uTorrent uwu
def main():
    """Muestra el catálogo y permite simular un programa por su PID."""
    while True:
        print("\nProgramas disponibles:")
        for proceso in Programas:
            print(
                f"PID: {proceso.Pid} | {proceso.nombre} | "
                f"Prioridad: {proceso.Pr} | Quantum: {proceso.Quantum} | "
                f"CPU: {proceso.Tcpu}"
            )

        seleccion = input(
            "\nEscribe el PID del programa que quieres ejecutar "
            "o 'salir' para terminar: "
        ).strip()
        if seleccion.casefold() == "salir":
            return

        proceso_seleccionado = next(
            (proceso for proceso in Programas if str(proceso.Pid) == seleccion),
            None,
        )
        if proceso_seleccionado is None:
            print("No se encontró un programa con ese PID.")
            continue

        proceso = programa(
            proceso_seleccionado.nombre,
            proceso_seleccionado.Pid,
            proceso_seleccionado.Pr,
            proceso_seleccionado.Quantum,
            proceso_seleccionado.Tcpu,
        )
        gestor = GestorProcesos([proceso])
        print(f"\nIniciando {proceso.nombre} (PID: {proceso.Pid}):")

        while not gestor.completo:
            proceso_ejecutado = gestor.avanzar()
            if proceso_ejecutado is None:
                print(
                    f"[t={gestor.reloj.tiempo}] CPU inactiva; "
                    "esperando procesos suspendidos."
                )
            else:
                print(
                    f"[t={gestor.reloj.tiempo}] Ejecutando "
                    f"{proceso_ejecutado.nombre} "
                    f"(PID: {proceso_ejecutado.Pid}) | "
                    f"CPU restante: {proceso_ejecutado.Tcpu} | "
                    f"Estado: {proceso_ejecutado.estado}"
                )
            time.sleep(PAUSA_SIMULACION)

        print(f"Simulación finalizada en {gestor.reloj.tiempo} unidades de tiempo.")
        print(
            f"Nombre: {proceso.nombre}, PID: {proceso.Pid}, "
            f"Estado: {proceso.estado}"
        )


if __name__ == "__main__":
    main()
