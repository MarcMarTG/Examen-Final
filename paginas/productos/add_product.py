import time
import flet as ft
from sqlite3 import connect
from base.sidebar import SideBar  # Importa la barra lateral personalizada
from base.topbar import TopBar  # Importa la barra superior personalizada
from components.cards import CustomDisplayCard  # Importa un componente personalizado para mostrar tarjetas con información
from components.fields import CustomDropDownField, CustomFormField, CustomTextField   # Importa componentes personalizados para campos de texto
from utilidades.colores import customBgColor, customBorderColor, customDashboardBG, customPrimaryColor, customSideBarIconColor, customTextHeaderColor, cutomTextColor  # Importa configuraciones de colores personalizadas
from utilidades.validaciones import validaciones  # Importa las validaciones personalizadas
from db.crud import database  # Importa funciones CRUD para interactuar con la base de datos

# Define una clase "CreateProduct" que hereda de ft.Container para representar un contenedor en la interfaz
class CreateProduct(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()

        # Inicialización de la base de datos y propiedades predeterminadas
        self.db = database()
        self.default_border = ft.border.all(width=1, color="#000000")
        self.error_border = ft.border.all(color="red", width=1)
        self.error_field = ft.Text(value="", color="red", size=0)
        self.expand = True
        self.bgcolor = "#E8E8E8"
        self.visible = False
        self.width = 1050
        self.height = 1920

        # Contenedores de los campos de entrada de información del producto
        self.product_name = ft.Container(content=CustomTextField(label="Nombre del Producto"), border=ft.border.all(width=1, color="#000000"), border_radius=ft.border_radius.all(20))
        self.product_price = ft.Container(content=CustomTextField(label="Precio del Producto"), border=ft.border.all(width=1, color="#000000"), border_radius=ft.border_radius.all(20))
        self.product_stock = ft.Container(content=CustomTextField(label="Stock del Producto"), border=ft.border.all(width=1, color="#000000"), border_radius=ft.border_radius.all(20))
        self.product_description = ft.Container(content=CustomTextField(label="Descripción del Producto"), border=ft.border.all(width=1, color="#000000"), border_radius=ft.border_radius.all(20))

        # Construcción del menú de la página de agregar producto
        self.menu = ft.Container(
            padding=ft.padding.all(20),
            content=ft.Column(
                controls=[
                    # Título y botón de cerrar
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text("Agregar Producto", color="#5D6163", size=20, weight=ft.FontWeight.BOLD),
                            ft.IconButton(
                                icon=ft.icons.CANCEL_PRESENTATION_ROUNDED,
                                icon_color="#5D6163",
                                icon_size=20,
                                tooltip="Cerrar la pestaña",
                                on_click=lambda e, page=page: self.close_product_modal(page, e),  # Llamada a la función para cerrar el modal
                            ),
                        ]
                    ),
                    ft.Divider(color="#434343", height=0.5, thickness=0.5),  # Línea divisoria
                    # Campos de entrada y botón de agregar
                    ft.Column(
                        controls=[
                            ft.ResponsiveRow([self.product_name, self.product_price, self.product_stock, self.product_description]),
                            self.error_field,
                            ft.Container(
                                alignment=ft.alignment.center,
                                height=40,
                                bgcolor="#234A94",
                                content=ft.Text("Agregar"),
                                border_radius=ft.border_radius.all(20),
                                on_click=self.add_product_db,  # Llamada a la función para agregar el producto
                            ),
                        ]
                    )
                ]
            )
        )
        self.content = self.menu  # Asigna el contenido del contenedor

    def update_product_list(self):
        # Limpia la lista de productos actual en la página
        self.product_list.controls.clear()

        # Obtiene todos los productos de la base de datos
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT id, nombre, precio, stock, descripcion FROM productos")
        productos = cursor.fetchall()

        # Añade cada producto a la lista de la página
        for producto in productos:
            producto_card = CustomDisplayCard(
                product_id=producto[0],
                product_name=producto[1],
                product_price=producto[2],
                product_stock=producto[3],
                product_description=producto[4],
            )
            self.product_list.controls.append(producto_card)

        # Actualiza la página para reflejar los cambios
        self.page.update()

    def close_product_modal(self, page, e):
        # Cierra el modal de agregar producto y limpia los campos de entrada
        self.visible = False
        self.product_name.content.value = ""
        self.product_price.content.value = ""
        self.product_stock.content.value = ""
        self.product_description.content.value = ""

        self.page.update()

    def add_product_db(self, e):
        # Obtiene los valores de los campos de entrada
        pro_nombre = self.product_name.content.value
        pro_precio = self.product_price.content.value
        pro_stock = self.product_stock.content.value
        pro_descripcion = self.product_description.content.value

        # Valida si todos los campos están completos
        if pro_nombre and pro_precio and pro_stock and pro_descripcion:
            # Valida si los valores de precio y stock son números válidos
            if self.es_numero_valido(pro_precio) and self.es_numero_valido(pro_stock):
                # Inserta el nuevo producto en la base de datos
                self.db.insert_data_prdoct(self.db.conn, "productos", (pro_nombre, pro_precio, pro_stock, pro_descripcion))

                # Muestra un mensaje de éxito
                self.error_field.value = "El producto ha sido cargado correctamente!"
                self.error_field.color = "green"
                self.error_field.size = 16
                self.page.update()
                self.page.go("/producto")  # Redirige a la página de productos

                # Limpia los campos de entrada
                self.product_name.content.value = ""
                self.product_price.content.value = ""
                self.product_stock.content.value = ""
                self.product_description.content.value = ""

                # Actualiza la lista de productos en la página de productos (sin cambiar de vista)
                if hasattr(self.page, 'product_list'):
                    self.page.product_list.update_product_list()

                # Solo actualiza la página sin cerrar el modal
                self.page.update()

            else:
                # Si el precio o el stock no son válidos, resalta los campos con error
                if not self.es_numero_valido(pro_precio):
                    self.product_price.border = self.error_border
                    self.product_price.update()

                if not self.es_numero_valido(pro_stock):
                    self.product_stock.border = self.error_border
                    self.product_stock.update()

                # Muestra el mensaje de error
                self.error_field.value = "Verifica los campos numéricos."
                self.error_field.color = "red"
                self.error_field.size = 16
                self.error_field.update()

                # Resetea los bordes de los campos de entrada después de un breve tiempo
                time.sleep(1)
                self.product_price.border = self.default_border
                self.product_stock.border = self.default_border
                self.error_field.size = 0
                self.error_field.update()
                self.product_price.update()
                self.product_stock.update()

        else:
            # Si falta algún campo, resalta los campos vacíos y muestra el mensaje de error
            if not pro_nombre:
                self.product_name.border = self.error_border
                self.product_name.update()

            if not pro_precio:
                self.product_price.border = self.error_border
                self.product_price.update()

            if not pro_stock:
                self.product_stock.border = self.error_border
                self.product_stock.update()

            if not pro_descripcion:
                self.product_description.border = self.error_border
                self.product_description.update()

            # Muestra el mensaje de error
            self.error_field.value = "Debes completar todos los campos"
            self.error_field.color = "red"
            self.error_field.size = 16
            self.error_field.update()

            # Resetea los bordes de los campos de entrada después de un breve tiempo
            time.sleep(1)
            self.product_price.border = self.default_border
            self.product_stock.border = self.default_border
            self.product_name.border = self.default_border
            self.product_description.border = self.default_border
            self.error_field.size = 0
            self.error_field.update()
            self.product_price.update()
            self.product_stock.update()
            self.product_name.update()
            self.product_description.update()

    def es_numero_valido(self, valor):
        # Verifica si un valor es numérico
        try:
            float(valor)
            return True
        except ValueError:
            return False
