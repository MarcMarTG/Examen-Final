import flet as ft
from sqlite3 import connect
from base.sidebar import SideBar  # Importa la clase SideBar (barra lateral)
from components.cards import CustomDisplayCard  # Importa tarjeta personalizada para mostrar información
from components.fields import CustomTextField  # Importa campo de texto personalizado
from utilidades.colores import customBgColor, customBorderColor, customDashboardBG, customPrimaryColor, customSideBarIconColor, customTextHeaderColor, cutomTextColor  # Colores personalizados para la interfaz
from utilidades.validaciones import validaciones  # Importa funciones de validación
from db.crud import database  # Importa funciones CRUD para interactuar con la base de datos

# Clase que representa la barra superior (TopBar) de la aplicación
class TopBar(ft.Container):
    def __init__(self, page: ft.Page, sidebar: SideBar):  # Se pasa el sidebar como argumento
        super().__init__()  # Inicializa la clase Container de Flet
        self.page = page  # Guarda la referencia a la página
        self.sidebar = sidebar  # Guarda una referencia al sidebar
        self.user_name = self.page.client_storage.get("user_name") or "Admin"  # Obtiene el nombre del usuario desde el almacenamiento de la página, si no existe, usa "Admin"

        # Establece el espaciado y márgenes de la barra superior
        self.padding = ft.padding.only(left=20, right=20)
        self.margin = 0  # Sin margen
        self.shadow = ft.BoxShadow(spread_radius=2, blur_radius=20, color="gray")  # Añade sombra a la barra
        self.bgcolor = "#001A5F"  # Define el color de fondo
        self.height = 50  # Define la altura de la barra superior

        # Crear el menú de la barra superior (TopBar)
        self.menu = ft.Row(
            controls=[
                # Botón de menú para alternar la visibilidad del sidebar
                ft.IconButton(
                    icon=ft.icons.MENU_OUTLINED,  # Icono de menú
                    icon_color="gray",  # Color del icono
                    on_click=self.toggle_sidebar  # Evento para cambiar la visibilidad del sidebar
                ),
                # Contenedor con el menú desplegable (popup) para el usuario
                ft.Container(
                    content=ft.PopupMenuButton(
                        content=ft.Container(
                            content=ft.Row(
                                controls=[
                                    # Icono del usuario
                                    ft.Icon(name=ft.icons.PERSON, color="gray"),
                                    # Texto de bienvenida dinámico con el nombre del usuario
                                    ft.Text(f"¡¡Bienvenido {self.user_name}!!", color="#BABABA", weight=ft.FontWeight.BOLD)
                                ]
                            ),
                            padding=ft.padding.symmetric(horizontal=10, vertical=5),  # Padding del contenido
                            bgcolor="#001A5F",  # Fondo del menú
                            border_radius=10,  # Radio de bordes redondeados
                            alignment=ft.Alignment(0, 0),  # Alineación central
                            shadow=ft.BoxShadow(blur_radius=5, spread_radius=2, color="gray"),  # Sombra del menú
                        ),
                        # Elementos del menú desplegable
                        items=[
                            ft.MenuItemButton(
                                width=150,
                                content=ft.Row(
                                    controls=[
                                        # Icono de cerrar sesión
                                        ft.Icon(name=ft.icons.LOGOUT_OUTLINED, color="#BABABA"),
                                        # Texto de opción de cerrar sesión
                                        ft.Text("Cerrar Sesión", color="#BABABA")
                                    ]
                                ),
                                on_click=lambda _: self.page.go("/login")  # Redirige a la página de login al hacer clic
                            ),
                        ]
                    )
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN  # Espaciado entre los elementos del menú
        )

        # Establece el contenido de la TopBar
        self.content = self.menu

    # Función que alterna la visibilidad del sidebar
    def toggle_sidebar(self, e):
        self.sidebar.visible = not self.sidebar.visible  # Cambia la visibilidad del sidebar
        self.page.update()  # Actualiza la página para reflejar el cambio
