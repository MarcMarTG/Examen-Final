import flet as ft
from sqlite3 import connect
from components.cards import CustomDisplayCard  # Importa un componente personalizado para mostrar tarjetas con información
from components.fields import CustomTextField   # Importa un componente personalizado para campos de texto
from utilidades.colores import customBgColor, customBorderColor, customDashboardBG, customPrimaryColor, customSideBarIconColor, customTextHeaderColor, cutomTextColor  # Importa configuraciones de colores personalizadas
from utilidades.validaciones import validaciones  # Importa las validaciones personalizadas
from db.crud import database  # Importa las funciones de base de datos CRUD (Create, Read, Update, Delete)

class SideBar(ft.Container):  # Define la clase "SideBar" que hereda de ft.Container
    def __init__(self, page: ft.Page):
        super().__init__()  # Llama al constructor de la clase base (ft.Container)
        self.page = page  # Guarda la referencia de la página Flet
        self.visible = True  # Propiedad para controlar la visibilidad del sidebar

        # Configura el ancho y el color de fondo del sidebar
        self.width = 200
        self.bgcolor = "#003777"
        self.alignment = ft.alignment.center  # Centra el contenido del sidebar

        # Crea un menú en columna para el sidebar
        self.menu = ft.Column(
            spacing=0,
            horizontal_alignment=ft.MainAxisAlignment.CENTER,  # Centra los elementos horizontalmente
            controls=[
                ft.Container(
                    height=page.height,  # Establece la altura del contenedor como la altura de la página
                    margin=0,
                    padding=ft.padding.only(top=20, left=10),  # Padding para separar los elementos
                    content=ft.Column(
                        alignment=ft.CrossAxisAlignment.CENTER,  # Centra el contenido dentro de la columna
                        controls=[
                            # Primer ítem del menú: Título y ícono de "Terminal"
                            ft.Container(
                                padding=ft.padding.only(bottom=20, left=20),
                                content=ft.Row(
                                    controls=[
                                        ft.Icon(name=ft.icons.ADMIN_PANEL_SETTINGS_ROUNDED, color="gray"),  # Ícono del panel de administración
                                        ft.Text("TERMINAL", size=20, color="#BABABA", weight=ft.FontWeight.BOLD)  # Texto "Terminal"
                                    ]
                                )
                            ),
                            ft.Divider(color="#E8E8E8", height=1, thickness=1),  # Un separador entre los elementos del menú
                            # Ítem del menú para "Menú Principal"
                            ft.Container(
                                content=ft.Row(
                                    controls=[
                                        ft.Icon(name=ft.icons.DASHBOARD_OUTLINED, color="gray"),  # Ícono del dashboard
                                        ft.Text("Menu Principal", size=14, color="#BABABA", weight=ft.FontWeight.BOLD)  # Texto "Menú Principal"
                                    ]
                                ),
                                on_click=lambda _: self.page.go("/dashboard")  # Al hacer clic, navega al dashboard
                            ),
                            ft.Divider(color="#E8E8E8", height=1, thickness=1),
                            # Ítem del menú para "Productos"
                            ft.Container(
                                content=ft.Row(
                                    controls=[
                                        ft.Icon(name=ft.icons.DASHBOARD_OUTLINED, color="gray"),  # Ícono del dashboard
                                        ft.Text("Productos", size=14, color="#BABABA", weight=ft.FontWeight.BOLD)  # Texto "Productos"
                                    ]
                                ),
                                on_click=lambda _: self.page.go("/producto")  # Al hacer clic, navega a la sección de productos
                            ),
                            ft.Divider(color="#E8E8E8", height=1, thickness=1),  # Otro separador
                        ]
                    )
                )
            ]
        )

        self.content = self.menu  # Asigna el contenido del sidebar al menú creado

    def update_visibility(self):
        # Método para alternar la visibilidad del sidebar
        self.visible = not self.visible  # Cambia el estado de visibilidad
        self.page.update()  # Actualiza la página para reflejar el cambio
