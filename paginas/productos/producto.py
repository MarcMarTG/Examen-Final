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
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from flet import Checkbox
import os
import time

# Clase principal de la interfaz que hereda de ft.Container
class ProductList(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.error_border = ft.border.all(color="red", width=1)  # Define estilo de borde para errores
        self.error_field = ft.Text(value="", color="red", size=0)  # Define campo de texto para mostrar errores
        self.expand = True  # Permite que el contenedor se expanda para ocupar el espacio disponible
        self.bgcolor = "#E8E8E8"  # Define el color de fondo
        padding = ft.padding.only(left=20)  # Configura el padding de la izquierda

        # Inicializa los componentes de la interfaz
        self.mod_product = ModifyProduct(page)
        self.add_product = CreateProduct(page)
        self.sidebar = SideBar(page)
        self.topbar = TopBar(page, self.sidebar)

        self.db = database()  # Instancia el objeto de base de datos
        self.conn = self.db.conn  # Conexión a la base de datos

        # Obtiene los productos de la base de datos
        self.products = self.db.get_data(self.conn, "productos")
        self.selected_products = []  # Lista para almacenar los productos seleccionados

        # Contenido principal de la página
        self.main_content = ft.Column(
            alignment=ft.MainAxisAlignment.START,
            spacing=20,
            controls=[
                self.topbar,  # Agrega la barra superior
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text(
                                "   Lista de Productos",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                color="#5D6163",
                            ),
                            ft.IconButton(
                                icon=ft.icons.PICTURE_AS_PDF,
                                icon_color="#5D6163",
                                icon_size=20,
                                tooltip="Generar PDF",
                                on_click=lambda e: self.generate_pdf()  # Llama a la función de generación de PDF
                            ),
                            ft.IconButton(
                                icon=ft.icons.REFRESH_ROUNDED,
                                icon_color="green",
                                icon_size=20,
                                tooltip="Refrescar",
                                on_click=lambda e: page.go("/act_product")  # Refresca la página
                            ),
                            ft.IconButton(
                                icon=ft.icons.ADD_CIRCLE,
                                icon_color="green",
                                icon_size=20,
                                tooltip="Agregar Productos",
                                on_click=lambda e, page=page: self.add_product_modal(page, e)  # Muestra el modal para agregar productos
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    )
                ),
                ft.Divider(color="#434343", height=1, thickness=1),  # Agrega una línea divisoria
                # Agrega un contenedor con altura fija y habilita el scroll
                ft.Container(
                    height=400,
                    content=ft.Column(
                        controls=[
                            ft.DataTable(
                                expand=5,
                                columns=[
                                    ft.DataColumn(ft.Text("Seleccionar", color="#5D6163", weight=ft.FontWeight.BOLD)),
                                    ft.DataColumn(ft.Text("Nombre del Producto", color="#5D6163", weight=ft.FontWeight.BOLD)),
                                    ft.DataColumn(ft.Text("Precio", color="#5D6163", weight=ft.FontWeight.BOLD)),
                                    ft.DataColumn(ft.Text("Cantidad", color="#5D6163", weight=ft.FontWeight.BOLD)),
                                    ft.DataColumn(ft.Text("Descripción", color="#5D6163", weight=ft.FontWeight.BOLD)),
                                    ft.DataColumn(ft.Text("Acción", color="#5D6163", weight=ft.FontWeight.BOLD)),
                                ],
                                rows=self.create_rows(),  # Función que genera las filas de la tabla
                            )
                        ],
                        scroll=ft.ScrollMode.AUTO,  # Habilita el desplazamiento
                    ),
                ),
            ],
        )

        # Estructura de la página
        self.content = ft.Row(
            spacing=0,
            controls=[
                self.sidebar,  # Barra lateral
                ft.Stack(
                    controls=[
                        ft.Container(expand=True, content=self.main_content),  # Contenedor principal
                        ft.Container(top=55, right=0, bottom=0, content=self.add_product),  # Modal para agregar producto
                        ft.Container(top=55, right=0, bottom=0, content=self.mod_product)  # Modal para modificar producto
                    ],
                    expand=True
                ),
            ]
        )

    def update_product_list(self):
        """Actualizar la lista de productos cuando se agrega un nuevo producto."""
        # Obtiene los productos más recientes de la base de datos
        self.products = self.db.get_data(self.conn, "productos")
        # Actualiza las filas de la tabla
        self.main_content.controls[2].controls[0].rows = self.create_rows()
        self.page.update()

    def create_rows(self):
        """Crea las filas de la tabla de productos con checkboxes."""
        rows = []
        for product in self.products:
            # Crea un checkbox para cada producto
            checkbox = ft.Checkbox(
                label="Seleccionar",
                label_style=ft.TextStyle(color="#5D6163"),
                value=False,  # Valor inicial (no seleccionado)
                on_change=lambda e, product=product: self.on_checkbox_change(e, product)  # Maneja el cambio de estado del checkbox
            )

            rows.append(ft.DataRow(
                cells=[
                    ft.DataCell(checkbox),  # Columna para el checkbox
                    ft.DataCell(ft.Text(product["nombre"], color="#5D6163")),
                    ft.DataCell(ft.Text(str(product["precio"]), color="#5D6163")),
                    ft.DataCell(ft.Text(str(product["stock"]), color="#5D6163")),
                    ft.DataCell(ft.Text(product["descripcion"], color="#5D6163")),
                    ft.DataCell(
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.START,
                            controls=[
                                ft.IconButton(
                                    icon=ft.icons.MODE_EDIT_SHARP,
                                    icon_color="#5D6163",
                                    icon_size=20,
                                    tooltip="Editar Registro",
                                    on_click=lambda e, product=product: self.mod_product_modal(self.page, e, product)  # Muestra el modal para editar producto
                                ),
                                ft.IconButton(
                                    icon=ft.icons.DELETE_FOREVER_ROUNDED,
                                    icon_color="red",
                                    icon_size=20,
                                    tooltip="Eliminar Registro",
                                    on_click=lambda e, product_id=product["id"]: self.delete_product(self.conn, product_id)  # Elimina el producto
                                )
                            ]
                        )
                    ),
                ]
            ))

        return rows

    def on_checkbox_change(self, e, product):
        """Función que maneja el cambio de estado de un checkbox."""
        # Agrega o elimina el producto de la lista de productos seleccionados
        if e.control.value:
            self.selected_products.append(product)
        else:
            self.selected_products.remove(product)

    def add_product_modal(self, page, e):
        """Muestra el modal para agregar un producto."""
        self.add_product.visible = True
        self.page.update()  # Actualiza la página para mostrar el modal

    def close_product_modal(self, page, e):
        """Cierra el modal de agregar producto y actualiza la lista."""
        self.add_product.visible = False
        self.page.update()  # Actualiza la página
        self.update_product_list()  # Actualiza la lista de productos

    def mod_product_modal(self, page, e, product):
        """Muestra el modal de modificación de producto con los datos precargados."""
        self.mod_product.visible = True  # Muestra el modal
        # Precarga los datos del producto
        self.mod_product.product_name.content.value = product["nombre"]
        self.mod_product.product_price.content.value = str(product["precio"])
        self.mod_product.product_stock.content.value = str(product["stock"])
        self.mod_product.product_description.content.value = product["descripcion"]
        self.mod_product.product_id = product["id"]  # Asigna el ID del producto al modal
        self.page.update()  # Actualiza la página para reflejar los cambios

    def delete_product(self, conn, product_id):
        """Elimina un producto de la base de datos y de la lista."""
        cursor = conn.cursor()  # Crea un cursor para ejecutar comandos SQL
        cursor.execute("DELETE FROM productos WHERE id = ?", (product_id,))  # Elimina el producto
        conn.commit()  # Confirma los cambios en la base de datos

        # Elimina el producto de la lista en la página
        self.products = [product for product in self.products if product["id"] != product_id]

        # Actualiza la lista de productos en la página
        self.page.update()

    def generate_pdf(self):
        """Genera un PDF con los productos seleccionados y lo guarda en una carpeta predeterminada."""
        folder_path = r"C:\Users\marcm\OneDrive\Escritorio\Marcos\8º Semestre\Programación VI\EF_MarcosA.Martinez.G\Examen Final\PDF"  # Carpeta donde se guardará el PDF

        # Verifica si la carpeta existe, y la crea si no
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        self.generate_single_pdf(folder_path)  # Llama a la función para generar el PDF

    def generate_single_pdf(self, folder_path):
        """Genera un archivo PDF con todos los productos seleccionados."""
        if not self.selected_products:  # Verifica si no hay productos seleccionados
            print("Error: No se seleccionaron productos.")
            return

        base_file_name = "productos_seleccionados.pdf"  # Nombre base para el archivo PDF
        file_path = os.path.join(folder_path, base_file_name)  # Ruta completa del archivo PDF

        count = 1  # Contador para evitar sobrescribir archivos existentes
        while os.path.exists(file_path):
            file_name = f"productos_seleccionados_{count}.pdf"
            file_path = os.path.join(folder_path, file_name)
            count += 1

        # Crea el documento PDF
        c = canvas.Canvas(file_path, pagesize=letter)
        c.drawString(100, 750, "Nombre del Producto")
        c.drawString(300, 750, "Precio")
        c.drawString(400, 750, "Cantidad")
        c.drawString(500, 750, "Descripción")

        # Agrega los productos seleccionados al PDF
        y_position = 730
        for product in self.selected_products:
            c.drawString(100, y_position, product["nombre"])
            c.drawString(300, y_position, str(product["precio"]))
            c.drawString(400, y_position, str(product["stock"]))
            c.drawString(500, y_position, product["descripcion"])
            y_position -= 20  # Espacio entre productos

            # Si se alcanza el final de la página, crea una nueva
            if y_position < 50:
                c.showPage()  # Nueva página
                y_position = 750  # Restablece la posición

        c.save()  # Guarda el archivo PDF
        print("Éxito: PDF con productos seleccionados ha sido generado correctamente!")
