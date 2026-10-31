
import time

from programa import programa
from gestor_procesos import GestorProcesos


PAUSA_SIMULACION = 0.5 

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

def main():
    seleccionados = []

    while True:
        print("\nProgramas disponibles:")
        if Programas:
            for proceso in Programas:
                print(f"- {proceso.nombre} (PID: {proceso.Pid})")
        else:

            print("- No hay programas disponibles")

        if seleccionados:
            print("Seleccionados: " + ", ".join(
                f"{proceso.nombre} (PID: {proceso.Pid})"
                for proceso in seleccionados
            ))

        opción = input(
            "Escribir un nombre para añadirlo, ejecutar para iniciar o salir para terminar: "
        )

        if opción in {"salir", "Salir", "SALIR"}:
            return

        if opción in {"ejecutar", "Ejecutar", "EJECUTAR"}:
            if not seleccionados:
                print("No hay procesos añadidos. Añade un proceso pendejo.")
                continue

            gestor = GestorProcesos(seleccionados)
            gestor.admitir_todos()
            print("\nIniciando simulación:")
            while not gestor.completo:
                proceso = gestor.avanzar()
                if proceso is None:
                    print(
                        f"[t={gestor.reloj.tiempo}] CPU inactiva; "
                        "esperando procesos suspendidos."
                    )
                else:
                    print(
                        f"[t={gestor.reloj.tiempo}] Ejecutando "
                        f"{proceso.nombre} (PID: {proceso.Pid}) | "
                        f"CPU restante: {proceso.Tcpu} | "
                        f"Estado: {proceso.estado}"
                    )
                time.sleep(PAUSA_SIMULACION)

            print(f"Simulación finalizada en {gestor.reloj.tiempo} (alguna vaina de tiempo).")
            for proceso in gestor.terminados:
                print(
                    f"Nombre: {proceso.nombre}, PID: {proceso.Pid}, "
                    f"Prioridad: {proceso.Pr}, Quantum: {proceso.Quantum}, "
                    f"Estado: {proceso.estado}"
                )
                proceso.Tcpu = proceso.Tcpu_original
                proceso.estado = "inactivo"
                Programas.append(proceso)
            seleccionados.clear()
            continue
      
        proceso_seleccionado = next(
            (
                proceso for proceso in Programas
                if proceso.nombre == opción
            ),
            None,
        )
        if proceso_seleccionado is None:
            print("Escribe bien (┬┬﹏┬┬).")
            continue

        Programas.remove(proceso_seleccionado)
        proceso_seleccionado.estado = "listo"
        seleccionados.append(proceso_seleccionado)
        print(f"{proceso_seleccionado.nombre} añadido al gestor.")

if __name__ == "__main__":
    main()