import flet as ft  # Importa la biblioteca flet para crear interfaces gráficas.
from sqlite3 import connect  # Importa el módulo sqlite3 para la conexión a bases de datos SQLite.
from base.sidebar import SideBar  # Importa la clase SideBar desde el módulo base para crear un menú lateral.
from base.topbar import TopBar  # Importa la clase TopBar desde el módulo base para crear una barra superior.
from components.cards import CustomDisplayCard  # Importa el componente CustomDisplayCard, usado para mostrar tarjetas personalizadas.
from components.fields import CustomTextField  # Importa el componente CustomTextField, un campo de texto personalizado.
from utilidades.colores import customBgColor, customBorderColor, customDashboardBG, customPrimaryColor, customSideBarIconColor, customTextHeaderColor, cutomTextColor  # Importa los colores personalizados.
from utilidades.validaciones import validaciones  # Importa las funciones de validación.
from db.crud import database  # Importa la base de datos y las funciones CRUD.

# Define una clase "dashboard" que hereda de ft.Container
class dashboard(ft.Container):
    
    # Inicializa la clase dashboard con la página flet.
    def __init__(self, page: ft.Page):
        super().__init__()

        # Establece que el contenedor se expanda para llenar el área disponible
        self.expand = True
        # Define el color de fondo del dashboard
        self.bgcolor = "#281CCC"
        
        # Crea un contenedor de columna para la lista de productos
        self.product_list = ft.Column()

        # Asegura que el contenedor de productos esté dentro del diseño principal
        self.content = ft.Column(controls=[self.product_list])

        # Establece la imagen de fondo para toda la página
        page.bg_image = "img/bglogin.png"  # Ruta de la imagen
        page.bg_image_fit = ft.ImageFit.COVER  # Ajuste para que la imagen cubra el área completamente
        
        # Crea el sidebar y topbar usando las clases SideBar y TopBar importadas
        self.sidebar = SideBar(page)
        self.topbar = TopBar(page, self.sidebar)
        
        # Define el contenido principal del dashboard
        self.main_content = ft.Column(
            alignment=ft.MainAxisAlignment.START,  # Alinea los elementos dentro de la columna al inicio
            controls=[
                self.topbar,  # Agrega la barra superior al contenido
                ft.Container(
                    bgcolor="transparent",  # Establece el color de fondo como transparente
                    padding=ft.padding.only(top=20, left=20, right=20),  # Establece el padding del contenedor
                    content=ft.Text(
                        "Menu Principal",  # Título del menú
                        color="#BABABA",  # Color del texto
                        size=20,  # Tamaño del texto
                        weight=ft.FontWeight.BOLD,  # Negrita
                    ),
                ),
                ft.Divider(color="#E8E8E8", height=1, thickness=1),  # Añade un separador con un color específico
                
                # Contenedor con imagen de fondo
                ft.Container(
                    expand=True,  # Asegura que el contenedor se expanda completamente
                    image_src="img/menu4.jpeg",  # Ruta de la imagen
                    image_fit="COVER",  # Ajuste de la imagen para cubrir todo el contenedor
                    width=page.width,  # Asegura que la imagen tenga el mismo ancho que la página
                    height=page.height,  # Asegura que la imagen tenga el mismo alto que la página
                    content=ft.Column(  # Columna que contiene elementos sobre la imagen
                        alignment=ft.MainAxisAlignment.CENTER,  # Alineación vertical centrada
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Alineación horizontal centrada
                        controls=[
                            # Contenedor con un ícono centrado
                            ft.Container(
                                content=ft.Icon(
                                    name=ft.icons.PRODUCTION_QUANTITY_LIMITS_ROUNDED,  # Ícono de cantidad de producción
                                    size=150,  # Tamaño del ícono
                                    color="#AED3E3"  # Color del ícono
                                ),
                                shadow=ft.BoxShadow(  # Agrega sombra al ícono
                                    spread_radius=1,
                                    blur_radius=50,
                                    color="#4344DE",  # Color de la sombra
                                    offset=ft.Offset(1, 1),  # Desplazamiento de la sombra
                                )
                            ),
                            # Contenedor con texto "Bienvenidos al"
                            ft.Container(
                                content=ft.Text(
                                    "¡¡BIENVENIDOS AL",  # Texto que se muestra
                                    color="#AED3E3",  # Color del texto
                                    size=40,  # Tamaño del texto
                                    weight=ft.FontWeight.BOLD  # Negrita
                                ),
                                shadow=ft.BoxShadow(  # Sombra para el texto
                                    spread_radius=1,
                                    blur_radius=50,
                                    color="#4344DE",
                                    offset=ft.Offset(1, 1),
                                )
                            ),
                            # Contenedor con texto "Administrador de Productos"
                            ft.Container(
                                content=ft.Text(
                                    "ADMINISTRADOR DE PRODUCTOS!!",
                                    color="#AED3E3",
                                    size=40,
                                    weight=ft.FontWeight.BOLD
                                ),
                                shadow=ft.BoxShadow(  # Sombra para el texto
                                    spread_radius=1,
                                    blur_radius=50,
                                    color="#4344DE",
                                    offset=ft.Offset(1, 1),
                                )
                            )
                        ]
                    )
                )
            ]
        )

        # Diseño principal, colocando el contenido principal dentro de un contenedor
        self.content = ft.Row(
            spacing=0,  # Define el espaciado entre los elementos de la fila
            controls=[
                self.sidebar,  # Agrega el sidebar al diseño
                ft.Container(
                    expand=True,  # Hace que el contenedor se expanda completamente
                    content=self.main_content  # Inserta el contenido principal dentro del contenedor
                )
            ]
        )

        # Actualiza la página para reflejar los cambios
        page.update()  # Asegúrate de actualizar la página si es necesario
