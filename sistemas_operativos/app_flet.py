import asyncio
import os
import random
from pathlib import Path
import flet as ft
from gestor_procesos import GestorProcesos
from programa import programa


BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"

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
        self.page.title = "Simulador de Planificación de Procesos - SO"
        self.page.bgcolor = COLOR_FONDO
        self.page.padding = 20
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.theme = ft.Theme(color_scheme_seed=COLOR_ACENTO)

        self.gestor = GestorProcesos([
            programa("Steam", random.randint(1000, 99999), random.randint(1, 5), 5, 10),
            programa("VLC media player",random.randint(1000, 99999), random.randint(1, 5), 3, 6),
            programa("Visual Studio Code", random.randint(1000, 99999), random.randint(1, 5), 4, 8),
            programa("YouTube", random.randint(1000, 99999), random.randint(1, 5), 3, 5),
            programa("Firefox",random.randint(1000, 99999), random.randint(1, 5), 4, 7),
            programa("umamusume", random.randint(1000, 99999), random.randint(1, 5), 2, 9),
            programa("Busca minas", random.randint(1000, 99999), random.randint(1, 5), 1, 5),
            programa("uTorrent", random.randint(1000, 99999), random.randint(1, 5), 5, 9),
            programa("ThunderBird", random.randint(1000, 99999), random.randint(1, 5), 5, 9),
            programa("Amarok", random.randint(1000, 99999), random.randint(1, 5), 5, 6),
            programa("Krita", random.randint(1000, 99999), random.randint(1, 5), 2, 10),
            programa("virtual box", random.randint(1000, 99999), random.randint(1, 5), 2, 10),
            programa("GIMP", random.randint(1000, 99999), random.randint(1, 5), 2, 10),
            programa("libre office writer", random.randint(1000, 99999), random.randint(1, 5), 2, 10),
        ])
        self.simulacion_activa = False

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

    def _imagen_proceso(self, proceso: programa) -> ft.Control:
        nombre_archivo = f"{proceso.nombre.lower().replace(' ', '_')}.png"
        ruta = str(ASSETS_DIR / nombre_archivo)

        if os.path.isfile(ruta):
            return ft.Image(src=ruta, width=48, height=48, fit=ft.ImageFit.CONTAIN)
        return ft.Text("", size=34, width=48, text_align=ft.TextAlign.CENTER)

    def _tarjeta_proceso(self, proceso: programa) -> ft.Control:
        return ft.Container(
            content=ft.Row(
                [
                    self._imagen_proceso(proceso),
                    ft.Column(
                        [
                            ft.Text(
                                proceso.nombre,
                                weight=ft.FontWeight.BOLD,
                                color=COLOR_CLARO,
                            ),
                            ft.Text(
                                f"PID: {proceso.Pid}",
                                color=COLOR_SECUNDARIO,
                                size=12,
                            ),
                        ],
                        spacing=2,
                        expand=True,
                    ),
                    ft.FilledButton(
                        "Añadir",
                        style=self._estilo_boton(),
                        on_click=lambda _, seleccionado=proceso: self._enviar_a_cola(
                            seleccionado
                        ),
                    ),
                ],
                spacing=10,
            ),
            bgcolor=COLOR_TARJETA,
            border=ft.Border.all(1, COLOR_BORDE),
            border_radius=12,
            padding=12,
        )

    def _crear_vista(self) -> ft.Control:
        reloj = ft.Text(
            f"⏱️ Tiempo Reloj: t={self.gestor.reloj.tiempo}",
            color=COLOR_CLARO,
            weight=ft.FontWeight.BOLD,
            size=14,
        )
        encabezado = ft.Row(
            [
                ft.Text(
                    " Simulador de Planificación de Procesos - Sistemas Operativos",
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
            controls=[self._tarjeta_proceso(p) for p in self.gestor.inactivos],
            spacing=8,
            expand=True,
        )
        panel_inactivos = self._tarjeta(
            " Programas Inactivos",
            ft.Column(
                [
                    ft.Text(
                        "Añade procesos a la cola de preparación:",
                        color=COLOR_CLARO,
                        italic=True,
                    ),
                    lista_inactivos,
                ],
                expand=True,
                spacing=12,
            ),
        )

        proceso_actual = self.gestor.ejecutando
        if proceso_actual:
            cpu_nombre = f" {proceso_actual.nombre}"
            cpu_detalles = (
                f"PID: {proceso_actual.Pid} | Pr: {proceso_actual.Pr} | "
                f"Q restante: {self.gestor._quantum_restante} | "
                f"T.cpu: {proceso_actual.Tcpu}"
            )
            progreso = (
                (proceso_actual.Tcpu_original - proceso_actual.Tcpu)
                / proceso_actual.Tcpu_original
                if proceso_actual.Tcpu_original > 0
                else 1
            )
        else:
            cpu_nombre = "CPU Inactiva / Esperando Procesos"
            cpu_detalles = "Ningún proceso en ejecución"
            progreso = 0

        progreso = max(0, min(progreso, 1))
        porcentaje = round(progreso * 100)

        panel_cpu = self._tarjeta(
            " Ejecutando CPU",
            ft.Column(
                [
                    ft.Text(
                        cpu_nombre,
                        color=COLOR_CLARO,
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(cpu_detalles, color=COLOR_CLARO),
                    ft.Stack(
                        controls=[
                            ft.ProgressBar(
                                value=progreso,
                                color="#FFFFFF",
                                bgcolor=COLOR_TARJETA,
                                bar_height=24,
                            ),
                            ft.Text(
                                f"{porcentaje}%",
                                color=COLOR_FONDO,
                                size=12,
                                weight=ft.FontWeight.BOLD,
                            ),
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

        suspendidos = []
        cantidad_suspendidos = len(self.gestor.suspendidos)
        for _ in range(cantidad_suspendidos):
            elemento = self.gestor.suspendidos.desencolar()
            if elemento is not None:
                suspendidos.append(elemento)
                self.gestor.suspendidos.encolar(elemento)

        lista_suspendidos = ft.ListView(
            controls=[
                ft.Container(
                    content=ft.Text(
                        f" {proceso.nombre} (PID: {proceso.Pid})\n"
                        f"Restante E/S: {restante} ciclos",
                        color=COLOR_SECUNDARIO,
                    ),
                    bgcolor=COLOR_TARJETA,
                    border=ft.Border.all(1, COLOR_BORDE),
                    border_radius=12,
                    padding=10,
                )
                for proceso, restante in suspendidos
            ],
            spacing=8,
            expand=True,
        )
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
        self.page.clean()
        self.page.add(self._crear_vista())
        self.page.update()

    def _enviar_a_cola(self, proceso: programa) -> None:
        if not self.gestor.admitir(proceso):
            return
        self._actualizar_vistas()
        if not self.simulacion_activa:
            self.simulacion_activa = True
            self.page.run_task(self._ejecutar_simulacion)

    async def _ejecutar_simulacion(self) -> None:
        while self.simulacion_activa:
            await asyncio.sleep(0.9)
            if (
                self.gestor.reloj.tiempo % 6 == 0
                and self.gestor.ejecutando is not None
            ):
                self.gestor.bloquear_actual(3)

            self.gestor.avanzar()
            if self.gestor.terminados:
                self.gestor.terminados.clear()

            if self.gestor.completo:
                self.simulacion_activa = False
                self._actualizar_vistas()
                return
            self._actualizar_vistas()


def main(page: ft.Page) -> None:
    VentanaSimulador(page)


if __name__ == "__main__":
    ft.run(main)
