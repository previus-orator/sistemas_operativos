import asyncio
import random
import flet as ft
from gestor_procesos import GestorProcesos
from programa import programa


COLOR_FONDO = "#0B1220"
COLOR_PANEL = "#111B2E"
COLOR_ACENTO = "#38BDF8"
COLOR_TARJETA = "#1B2940"
COLOR_COLA = COLOR_TARJETA
COLOR_SUSPENDIDO = COLOR_TARJETA
COLOR_TEXTO_OSCURO = COLOR_FONDO
COLOR_COLA_TEXTO = "#E2E8F0"
COLOR_CLARO = "#E2E8F0"
COLOR_SECUNDARIO = "#94A3B8"
COLOR_BORDE = "#26364F"


class VentanaSimulador:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Simulador de Planificación de Procesos"
        self.page.bgcolor = COLOR_FONDO
        self.page.padding = 20
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.theme = ft.Theme(color_scheme_seed=COLOR_ACENTO)

        nombres_programas = (
            "Steam",
            "VLC media player",
            "Visual Studio Code",
            "YouTube",
            "Firefox",
            "umamusume",
            "Busca minas",
            "uTorrent",
            "ThunderBird",
            "Amarok",
            "Krita",
            "virtual box",
            "GIMP",
            "libre office writer",
        )
        self.gestor = GestorProcesos([
            programa(
                nombre,
                random.randint(1000, 99999),
                random.randint(1, 5),
                random.randint(1, 5),
                random.randint(5, 10),
                random.randint(1, 3),
            )
            for nombre in nombres_programas
        ])
        self.programas = list(self.gestor.inactivos)
        self.simulacion_activa = False
        self._procesos_en_simulacion: set[programa] = set()
        self._ciclos_cpu_para_io: dict[programa, int] = {}
        self._vista = None
        self._estados_programas: dict[int, ft.Text] = {}
        self._botones_programas: dict[int, ft.FilledButton] = {}
        self._progresos_programas: dict[int, ft.ProgressBar] = {}
        self._porcentajes_programas: dict[int, ft.Text] = {}
        self._detalles_programas: dict[int, ft.Column] = {}

        self._actualizar_vistas()

    def _tarjeta(self, titulo: str, contenido: ft.Control, expand: int = 1) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(titulo, size=16, weight=ft.FontWeight.BOLD, color=COLOR_CLARO),
                    contenido,
                ],
                expand=True,
                spacing=12,
            ),
            bgcolor=COLOR_PANEL,
            border=ft.Border.all(1, COLOR_BORDE),
            border_radius=16,
            padding=18,
            expand=expand,
        )

    def _progreso_proceso(self, proceso: programa) -> float:
        if proceso.Tcpu_original <= 0:
            return 0
        return max(
            0,
            min(
                (proceso.Tcpu_original - proceso.Tcpu)
                / proceso.Tcpu_original,
                1,
            ),
        )

    def _estilo_boton(
        self,
        color_fondo: str = COLOR_ACENTO,
        color_texto: str = COLOR_FONDO,
    ) -> ft.ButtonStyle:
        return ft.ButtonStyle(
            bgcolor=color_fondo,
            color=color_texto,
            elevation=0,
            padding=12,
            shape=ft.RoundedRectangleBorder(radius=10),
        )

    def _tarjeta_proceso(self, proceso: programa) -> ft.Control:
        estado = ft.Text(
            f"Estado: {proceso.estado}",
            color=COLOR_SECUNDARIO,
            size=12,
        )
        progreso = self._progreso_proceso(proceso)
        barra_progreso = ft.ProgressBar(
            value=progreso,
            color=COLOR_ACENTO,
            bgcolor=COLOR_PANEL,
            bar_height=8,
        )
        porcentaje = ft.Text(
            f"Avance: {round(progreso * 100)}%",
            color=COLOR_SECUNDARIO,
            size=11,
        )
        detalles = ft.Column(
            [
                ft.Text(
                    f"Interactividad: {proceso.interactividad}/3",
                    color=COLOR_SECUNDARIO,
                    size=12,
                ),
                ft.Text(
                    f"PID: {proceso.Pid}",
                    color=COLOR_SECUNDARIO,
                    size=12,
                ),
                barra_progreso,
                porcentaje,
            ],
            spacing=4,
            visible=proceso not in self.gestor.inactivos,
        )
        boton = ft.FilledButton(
            "Añadir",
            style=self._estilo_boton(),
            on_click=lambda _, seleccionado=proceso: self._enviar_a_cola(
                seleccionado
            ),
        )
        self._estados_programas[proceso.Pid] = estado
        self._botones_programas[proceso.Pid] = boton
        self._progresos_programas[proceso.Pid] = barra_progreso
        self._porcentajes_programas[proceso.Pid] = porcentaje
        self._detalles_programas[proceso.Pid] = detalles
        return ft.Container(
            content=ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text(
                                proceso.nombre,
                                weight=ft.FontWeight.BOLD,
                                color=COLOR_CLARO,
                            ),
                            detalles,
                            estado,
                        ],
                        spacing=4,
                        expand=True,
                    ),
                    boton,
                ],
                spacing=10,
            ),
            bgcolor=COLOR_TARJETA,
            border=ft.Border.all(1, COLOR_BORDE),
            border_radius=12,
            padding=12,
        )

    def _tarjetas_suspendidos(self) -> list[ft.Control]:
        elementos = self.gestor.suspendidos._ColaTemporizada__elementos
        suspendidos = sorted(elementos, key=lambda elemento: elemento[:2])
        return [
            ft.Container(
                content=ft.Text(
                    f" {proceso.nombre} (PID: {proceso.Pid})\n"
                    f"Restante E/S: "
                    f"{max(0, despertar - self.gestor.reloj.tiempo)} ciclos",
                    color=COLOR_SECUNDARIO,
                ),
                bgcolor=COLOR_TARJETA,
                border=ft.Border.all(1, COLOR_BORDE),
                border_radius=12,
                padding=10,
            )
            for despertar, _, proceso in suspendidos
        ]

    def _crear_vista(self) -> ft.Control:
        reloj = ft.Text(
            f"Tiempo Reloj: t={self.gestor.reloj.tiempo}",
            color=COLOR_CLARO,
            weight=ft.FontWeight.BOLD,
            size=14,
        )
        self._reloj_texto = reloj
        encabezado = ft.Row(
            [
                ft.Text(
                    " Simulador de Planificación de Procesos",
                    color=COLOR_CLARO,
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    expand=True,
                ),
                reloj,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        lista_inactivos = ft.ListView(
            controls=[self._tarjeta_proceso(p) for p in self.programas],
            spacing=8,
            expand=True,
        )
        self._lista_programas = lista_inactivos
        panel_inactivos = self._tarjeta(
            " Programas",
            lista_inactivos,
        )

        proceso_actual = self.gestor.ejecutando
        if proceso_actual:
            cpu_nombre = f" {proceso_actual.nombre}"
            cpu_detalles = (
                f"PID: {proceso_actual.Pid} | Pr: {proceso_actual.Pr} | "
                f"Q restante: {self.gestor._quantum_restante} | "
                f"T.cpu: {proceso_actual.Tcpu} | "
                f"Interactividad: {proceso_actual.interactividad}/3"
            )
            progreso = self._progreso_proceso(proceso_actual)
        else:
            cpu_nombre = "CPU Inactiva / Esperando Procesos"
            cpu_detalles = "Ningún proceso en ejecución"
            progreso = 0

        progreso = max(0, min(progreso, 1))
        porcentaje = round(progreso * 100)

        self._cpu_nombre = ft.Text(
            cpu_nombre,
            color=COLOR_CLARO,
            size=18,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        )
        self._cpu_detalles = ft.Text(cpu_detalles, color=COLOR_CLARO)
        self._cpu_progreso = ft.ProgressBar(
            value=progreso,
            color="#FFFFFF",
            bgcolor=COLOR_TARJETA,
            bar_height=24,
        )
        self._cpu_porcentaje = ft.Text(
            f"{porcentaje}%",
            color=COLOR_FONDO,
            size=12,
            weight=ft.FontWeight.BOLD,
        )
        panel_cpu = self._tarjeta(
            " Ejecutando CPU",
            ft.Column(
                [
                    self._cpu_nombre,
                    self._cpu_detalles,
                    ft.Stack(
                        controls=[
                            self._cpu_progreso,
                            self._cpu_porcentaje,
                        ],
                        alignment=ft.Alignment(0, 0),
                        height=24,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=14,
            ),
        )

        lista_suspendidos = ft.ListView(
            controls=self._tarjetas_suspendidos(),
            spacing=8,
            expand=True,
        )
        self._lista_suspendidos = lista_suspendidos
        panel_suspendidos = self._tarjeta(
            " Suspendidos (E/S - Automático)",
            lista_suspendidos,
        )

        lista_preparacion = ft.ListView(
            controls=[
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                f" {p.nombre}",
                                weight=ft.FontWeight.BOLD,
                                color=COLOR_CLARO,
                            ),
                            ft.Text(f"PID: {p.Pid}", color=COLOR_SECUNDARIO),
                            ft.Text(
                                f"Pr: {p.Pr} | Q: {p.Quantum}",
                                color=COLOR_SECUNDARIO,
                            ),
                            ft.Text(f"T.cpu: {p.Tcpu}", color=COLOR_SECUNDARIO),
                        ],
                        spacing=3,
                    ),
                    bgcolor=COLOR_COLA,
                    border=ft.Border.all(1, COLOR_BORDE),
                    border_radius=12,
                    padding=14,
                    width=220,
                )
                for p in self.gestor.listos.arreglo
                if p and p.Tcpu > 0
            ],
            horizontal=True,
            spacing=8,
            expand=True,
        )
        self._lista_preparacion = lista_preparacion
        panel_preparacion = self._tarjeta(
            " Cola de Preparación (Pr > Quantum > PID)",
            lista_preparacion,
        )

        panel_derecho = ft.Column(
            [
                ft.Row(
                    [panel_cpu, panel_suspendidos],
                    expand=True,
                    spacing=12,
                    vertical_alignment=ft.CrossAxisAlignment.STRETCH,
                ),
                panel_preparacion,
            ],
            expand=2,
            spacing=12,
        )
        return ft.Column(
            [
                encabezado,
                ft.Row(
                    [panel_inactivos, panel_derecho],
                    expand=True,
                    spacing=12,
                    vertical_alignment=ft.CrossAxisAlignment.STRETCH,
                ),
            ],
            expand=True,
            spacing=16,
        )

    def _actualizar_vistas(self) -> None:
        if self._vista is None:
            self._vista = self._crear_vista()
            self.page.add(self._vista)

        self._reloj_texto.value = f"Tiempo Reloj: t={self.gestor.reloj.tiempo}"

        proceso_actual = self.gestor.ejecutando
        if proceso_actual:
            self._cpu_nombre.value = f" {proceso_actual.nombre}"
            self._cpu_detalles.value = (
                f"PID: {proceso_actual.Pid} | Pr: {proceso_actual.Pr} | "
                f"Q restante: {self.gestor._quantum_restante} | "
                f"T.cpu: {proceso_actual.Tcpu} | "
                f"Interactividad: {proceso_actual.interactividad}/3"
            )
            progreso = self._progreso_proceso(proceso_actual)
        else:
            self._cpu_nombre.value = "CPU Inactiva / Esperando Procesos"
            self._cpu_detalles.value = "Ningún proceso en ejecución"
            progreso = 0

        progreso = max(0, min(progreso, 1))
        self._cpu_progreso.value = progreso
        self._cpu_porcentaje.value = f"{round(progreso * 100)}%"

        for proceso in self.programas:
            self._estados_programas[proceso.Pid].value = (
                f"Estado: {proceso.estado}"
            )
            avance = self._progreso_proceso(proceso)
            self._progresos_programas[proceso.Pid].value = avance
            self._porcentajes_programas[proceso.Pid].value = (
                f"Avance: {round(avance * 100)}%"
            )
            self._detalles_programas[proceso.Pid].visible = (
                proceso not in self.gestor.inactivos
            )
            self._botones_programas[proceso.Pid].disabled = (
                proceso not in self.gestor.inactivos
            )

        self._lista_suspendidos.controls = self._tarjetas_suspendidos()
        self._lista_preparacion.controls = [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            f" {proceso.nombre}",
                            weight=ft.FontWeight.BOLD,
                            color=COLOR_CLARO,
                        ),
                        ft.Text(f"PID: {proceso.Pid}", color=COLOR_SECUNDARIO),
                        ft.Text(
                            f"Pr: {proceso.Pr} | Q: {proceso.Quantum}",
                            color=COLOR_SECUNDARIO,
                        ),
                        ft.Text(f"T.cpu: {proceso.Tcpu}", color=COLOR_SECUNDARIO),
                    ],
                    spacing=3,
                ),
                bgcolor=COLOR_COLA,
                border=ft.Border.all(1, COLOR_BORDE),
                border_radius=12,
                padding=14,
                width=220,
            )
            for proceso in self.gestor.listos.arreglo
            if proceso and proceso.Tcpu > 0
        ]
        self.page.update()

    def _enviar_a_cola(self, proceso: programa) -> None:
        if not self.gestor.admitir(proceso):
            return
        self._procesos_en_simulacion.add(proceso)
        self._ciclos_cpu_para_io[proceso] = 0
        self._actualizar_vistas()
        if not self.simulacion_activa:
            self.simulacion_activa = True
            self.page.run_task(self._ejecutar_simulacion)

    async def _ejecutar_simulacion(self) -> None:
        while self._procesos_en_simulacion:
            await asyncio.sleep(0.9)

            proceso_actual = self.gestor.despachar()
            if (
                proceso_actual is not None
                and self._ciclos_cpu_para_io[proceso_actual]
                >= proceso_actual.interactividad
                and self.gestor.bloquear_actual(proceso_actual.interactividad)
            ):
                self._ciclos_cpu_para_io[proceso_actual] = 0
            else:
                proceso_ejecutado = self.gestor.avanzar()
                if proceso_ejecutado is not None and proceso_ejecutado.Tcpu > 0:
                    self._ciclos_cpu_para_io[proceso_ejecutado] += 1

            for proceso in self.gestor.terminados:
                proceso.Tcpu = proceso.Tcpu_original
                proceso.estado = "inactivo"
                if proceso not in self.gestor.inactivos:
                    self.gestor.inactivos.append(proceso)
                self._procesos_en_simulacion.discard(proceso)
                self._ciclos_cpu_para_io.pop(proceso, None)
            self.gestor.terminados.clear()
            self._actualizar_vistas()

        self.simulacion_activa = False


def main(page: ft.Page) -> None:
    VentanaSimulador(page)


if __name__ == "__main__":
    ft.run(main)
