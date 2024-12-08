import flet as ft
from sqlite3 import connect
from base.sidebar import SideBar
from base.topbar import TopBar
from components.cards import CustomDisplayCard  # Importa un componente personalizado para mostrar tarjetas con información
from components.fields import CustomTextField   # Importa un componente personalizado para campos de texto
from paginas.productos.add_product import CreateProduct
from paginas.productos.modify_product import ModifyProduct
from utilidades.colores import customBgColor, customBorderColor, customDashboardBG, customPrimaryColor, customSideBarIconColor, customTextHeaderColor, cutomTextColor  # Importa configuraciones de colores personalizadas
from utilidades.validaciones import validaciones  # Importa las validaciones personalizadas
from db.crud import database  # Importa las funciones de base de datos CRUD (Create, Read, Update, Delete)

# Define una clase "dashboard" que hereda de ft.Container
class ActProduct(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.expand = True
        self.bgcolor = customDashboardBG
        self.sidebar = SideBar(page)
        self.topbar = TopBar(page, self.sidebar)

        self.main_content = ft.Column(
            alignment=ft.MainAxisAlignment.START,
            spacing=20,
            controls=[
                self.topbar,  
                ft.Container()
            ]
        )

        self.content = ft.Row(
            spacing=0,
            controls=[
                self.sidebar, 
                ft.Stack(
                    controls=[
                        ft.Container(expand=True, content=self.main_content),
                    ],
                    expand=True
                ),
            ]
        )

    # Redirige automáticamente cuando se monta la página
    def did_mount(self):
        # Redirige a la página de productos
        self.page.go("/producto")

