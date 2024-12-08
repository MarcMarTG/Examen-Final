import time
import flet as ft
from sqlite3 import connect
from base.sidebar import SideBar
from base.topbar import TopBar
from components.cards import CustomDisplayCard  # Importa un componente personalizado para mostrar tarjetas con información
from components.fields import CustomDropDownField, CustomFormField, CustomTextField   # Importa un componente personalizado para campos de texto
from utilidades.colores import customBgColor, customBorderColor, customDashboardBG, customPrimaryColor, customSideBarIconColor, customTextHeaderColor, cutomTextColor  # Importa configuraciones de colores personalizadas
from utilidades.validaciones import validaciones  # Importa las validaciones personalizadas
from db.crud import database  # Importa las funciones de base de datos CRUD (Create, Read, Update, Delete)


# Define una clase "ModifyProduct" que hereda de ft.Container
class ModifyProduct(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()  # Inicializa la clase base Container

        # Crea una instancia de la base de datos
        self.db = database()
        # Define los estilos predeterminados para los bordes y los campos de error
        self.default_border = ft.border.all(width=1, color="#000000")
        self.error_border = ft.border.all(color="red", width=1)
        self.error_field = ft.Text(value="", color="red", size=0)  # Campo para mostrar mensajes de error
        self.expand = True
        self.bgcolor = "#E8E8E8"
        self.visible = False
        self.width = 1050
        self.height = 1920

        self.product_id = None  # Inicializa el atributo product_id como None

        # Define los campos de entrada para modificar el producto
        self.product_name = ft.Container(content=CustomTextField(label="Nombre del Producto"), border=ft.border.all(width=1, color="#000000"), border_radius=ft.border_radius.all(20))
        self.product_price = ft.Container(content=CustomTextField(label="Precio del Producto"), border=ft.border.all(width=1, color="#000000"), border_radius=ft.border_radius.all(20))
        self.product_stock = ft.Container(content=CustomTextField(label="Stock del Producto"), border=ft.border.all(width=1, color="#000000"), border_radius=ft.border_radius.all(20))
        self.product_description = ft.Container(content=CustomTextField(label="Descripción del Producto"), border=ft.border.all(width=1, color="#000000"), border_radius=ft.border_radius.all(20))

        # Define el contenedor principal del formulario
        self.menu = ft.Container(
            padding=ft.padding.all(20),
            content=ft.Column(
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text("Modificar Producto", color="#5D6163", size=20, weight=ft.FontWeight.BOLD),
                            ft.IconButton(
                                icon=ft.icons.CANCEL_PRESENTATION_ROUNDED,
                                icon_color="#5D6163",
                                icon_size=20,
                                tooltip="Cerrar la pestaña",
                                on_click=lambda e, page=page: self.close_modproduct_modal(page, e),  # Cierra la ventana al hacer clic en el icono
                            ),
                        ]
                    ),
                    ft.Divider(color="#434343", height=0.5, thickness=0.5),  # Divide el encabezado de la sección de formulario
                    ft.Column(
                        controls=[
                            ft.ResponsiveRow([self.product_name, self.product_price, self.product_stock, self.product_description]),
                            self.error_field,  # Muestra el mensaje de error si es necesario
                            ft.Container(
                                alignment=ft.alignment.center,
                                height=40,
                                bgcolor="#234A94",
                                content=ft.Text("Modificar"),
                                border_radius=ft.border_radius.all(20),
                                on_click=self.mod_product_db,  # Actualiza el producto al hacer clic
                            ),
                        ]
                    )
                ]
            )
        )
        self.content = self.menu  # Define el contenido del contenedor como el menú

    # Función para cerrar la ventana modal y limpiar los campos
    def close_modproduct_modal(self, page, e):
        self.visible = False
        self.product_name.content.value = ""
        self.product_price.content.value = ""
        self.product_stock.content.value = ""
        self.product_description.content.value = ""
        self.page.update()

    # Función para verificar si un valor es un número válido
    def es_numero_valido(self, valor):
        try:
            float(valor)
            return True
        except ValueError:
            return False
        
    # Función para actualizar la lista de productos desde la base de datos
    def update_product_list(self):
        # Limpia la lista de productos actual
        self.product_list.controls.clear()

        # Obtiene todos los productos de la base de datos
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT id, nombre, precio, stock, descripcion FROM productos")
        productos = cursor.fetchall()

        # Agrega cada producto a la lista de tarjetas
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

    # Función para modificar los datos de un producto en la base de datos
    def mod_product_db(self, e):
        # Obtiene los valores de los campos del formulario
        pro_nombre = self.product_name.content.value
        pro_precio = self.product_price.content.value
        pro_stock = self.product_stock.content.value
        pro_descripcion = self.product_description.content.value

        # Verifica si el producto existe en la base de datos
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT nombre, precio, stock, descripcion FROM productos WHERE id = ?", (self.product_id,))
        producto_actual = cursor.fetchone()

        if producto_actual is None:
            self.error_field.value = "Error: No se encontró el producto en la base de datos."
            self.error_field.color = "red"
            self.error_field.size = 16
            self.error_field.update()
            return

        nombre_actual, precio_actual, stock_actual, descripcion_actual = producto_actual

        # Verifica si los datos ingresados son los mismos que los actuales
        if (pro_nombre == nombre_actual and
            pro_precio == str(precio_actual) and
            pro_stock == str(stock_actual) and
            pro_descripcion == descripcion_actual):
            self.error_field.value = "Debe realizar alguna modificación antes de guardar."
            self.error_field.color = "red"
            self.error_field.size = 16
            self.error_field.update()
            return

        # Verifica si todos los campos están completos
        if pro_nombre and pro_precio and pro_stock and pro_descripcion:
            # Verifica si los campos numéricos son válidos
            if self.es_numero_valido(pro_precio) and self.es_numero_valido(pro_stock):
                # Actualiza los datos del producto en la base de datos
                cursor.execute(
                    "UPDATE productos SET nombre = ?, precio = ?, stock = ?, descripcion = ? WHERE id = ?",
                    (pro_nombre, pro_precio, pro_stock, pro_descripcion, self.product_id)
                )
                self.db.conn.commit()

                # Muestra un mensaje de éxito
                self.error_field.value = "El producto ha sido modificado correctamente!"
                self.error_field.color = "green"
                self.error_field.size = 16
                self.page.update()

                # Limpia los campos del formulario
                self.product_name.content.value = ""
                self.product_price.content.value = ""
                self.product_stock.content.value = ""
                self.product_description.content.value = ""

                # Actualiza la página para reflejar los cambios
                time.sleep(1)
                self.error_field.size = 0
                self.error_field.update()
                self.page.update()

                # Actualiza la lista de productos
                if hasattr(self.page, 'product_list'):
                    self.page.product_list.update_product_list()

            else:
                # Si no son números válidos, marca los campos con errores
                if not self.es_numero_valido(pro_precio):
                    self.product_price.border = self.error_border
                    self.product_price.update()

                if not self.es_numero_valido(pro_stock):
                    self.product_stock.border = self.error_border
                    self.product_stock.update()

                self.error_field.value = "Verifica los campos numéricos."
                self.error_field.color = "red"
                self.error_field.size = 16
                self.error_field.update()

                time.sleep(1)
                self.product_price.border = self.default_border
                self.product_stock.border = self.default_border
                self.error_field.size = 0
                self.error_field.update()
                self.product_price.update()
                self.product_stock.update()

        else:
            # Si los campos no están completos, marca los campos con errores
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

            # Actualiza la página para reflejar los cambios
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
