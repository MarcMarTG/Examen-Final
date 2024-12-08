from sqlite3 import connect  # Importa el módulo sqlite3 para manejar bases de datos SQLite
import time  # Importa el módulo time para manejar el tiempo (aunque no se usa en este fragmento)
import flet as ft  # Importa la biblioteca Flet para crear interfaces gráficas
from components.fields import CustomTextField  # Importa el campo de texto personalizado
from db.crud import database  # Importa la clase database para manejar operaciones con la base de datos
from utilidades.colores import customBgColor, customBorderColor, customDashboardBG, customPrimaryColor, customSideBarIconColor, customTextHeaderColor, cutomTextColor  # Importa colores personalizados
from utilidades.validaciones import validaciones  # Importa la clase de validaciones para validar datos de entrada
import hashlib

def on_change(e):
        # Solo permitir letras (mayúsculas y minúsculas)
        if not e.control.value.isalpha():
            e.control.error_text = "Solo se permiten letras."
        else:
            e.control.error_text = None
        e.control.update()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

class signup(ft.Container):  # Clase que representa la vista de registro, heredando de ft.Container
    def __init__(self, page: ft.Page):  # Inicializador que recibe la página de Flet
        super().__init__()  # Llama al inicializador de la clase base


        
        self.expand = True  # Permite que el contenedor se expanda para ocupar espacio disponible
        self.validaciones = validaciones()  # Instancia de la clase de validaciones
        self.default_border = ft.border.all(width=1, color="#000000")  # Borde por defecto (negro)
        self.error_border = ft.border.all(color="red", width=1)  # Borde rojo para indicar errores
        self.error_field = ft.Text(value="", color="red", size=0)  # Campo para mostrar mensajes de error, inicialmente vacío

        # Inicializa la base de datos
        self.db = database()  # Crea una instancia de la clase database para operaciones de DB

        # Crea el campo de entrada para el nombre
        self.nombre = ft.Container(
            content=CustomTextField(label="Nombre",on_change=on_change),  # Campo personalizado con etiqueta "Nombre"
            border=ft.border.all(width=1, color="#000000"),  # Borde negro
            border_radius=ft.border_radius.all(20)  # Bordes redondeados
        )

        # Crea el campo de entrada para el apellido
        self.apellido = ft.Container(
            content=CustomTextField(label="Apellido",on_change=on_change),  # Campo personalizado con etiqueta "Apellido"
            border=ft.border.all(width=1, color="#000000"),  # Borde negro
            border_radius=ft.border_radius.all(20)  # Bordes redondeados
        )

        # Crea el campo de entrada para el email
        self.email = ft.Container(
            content=CustomTextField(label="Email"),  # Campo personalizado con etiqueta "Email"
            border=ft.border.all(width=1, color="#000000"),  # Borde negro
            border_radius=ft.border_radius.all(20)  # Bordes redondeados
        )

        # Crea el campo de entrada para la contraseña
        self.password = ft.Container(
            content=CustomTextField(
                label="Password",  # Campo personalizado con etiqueta "Password"
                password=True,  # Indica que es un campo de contraseña
                can_reveal_password=True,  # Permite mostrar/ocultar la contraseña
            ),
            border=ft.border.all(width=1, color="#000000"),  # Borde negro
            border_radius=ft.border_radius.all(20),  # Bordes redondeados
        )

        # Crea el campo de entrada para confirmar la contraseña
        self.confirm_pass = ft.Container(
            content=CustomTextField(
                label="Confirmar Password",  # Campo personalizado con etiqueta "Confirmar Password"
                password=True,  # Indica que es un campo de contraseña
                can_reveal_password=True,  # Permite mostrar/ocultar la contraseña
            ),
            border=ft.border.all(width=1, color="#000000"),  # Borde negro
            border_radius=ft.border_radius.all(20),  # Bordes redondeados
        )

        # Contenedor principal que organiza los campos y botones
        self.content = ft.Row(
            controls=[  # Define los controles que se incluirán en la fila
                ft.Container(
                    expand=2,  # Permite que este contenedor expanda su espacio
                    image_src="img/bglogin.png",  # Fuente de la imagen de fondo
                    image_fit="cover",  # Ajusta la imagen para cubrir el área del contenedor
                    padding=ft.padding.all(40),  # Padding interno del contenedor
                    margin=ft.margin.all(0),  # Margen externo del contenedor
                    content=ft.Column(  # Contenedor vertical para alinear los elementos
                        alignment=ft.MainAxisAlignment.CENTER,  # Alinea los elementos verticalmente al centro
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Alinea los elementos horizontalmente al centro
                        controls=[  # Define los controles que se incluirán en la columna
                            ft.Text("REGISTRATE",  # Título del formulario
                                    color=customTextHeaderColor,  # Color del texto
                                    font_family="abeezee",  # Fuente del texto
                                    size=40,  # Tamaño de la fuente
                                    weight=ft.FontWeight.BOLD  # Estilo de la fuente en negrita
                                    ),
                            ft.Divider(color="black", height=0.5, thickness=0.5),  # Línea divisoria
                            self.error_field,  # Campo para mostrar errores
                            self.nombre,  # Campo de nombre
                            self.apellido,  # Campo de apellido
                            self.email,  # Campo de email
                            self.password,  # Campo de contraseña
                            self.confirm_pass,  # Campo de confirmación de contraseña
                            ft.Container(  # Botón de registro
                                alignment=ft.alignment.center,  # Alinea el contenido al centro
                                height=40,  # Altura del botón
                                bgcolor="#234A94",  # Color de fondo del botón
                                content=ft.Text("Registrarse"),  # Texto del botón
                                border_radius=ft.border_radius.all(20),  # Bordes redondeados
                                on_click=self.signup,  # Llama al método signup al hacer clic
                            ),
                            ft.Container(  # Botón para ir a la página de inicio de sesión
                                alignment=ft.alignment.center,  # Alinea el contenido al centro
                                height=40,  # Altura del botón
                                content=ft.Text("Iniciar Sesión", color=customTextHeaderColor, weight=ft.FontWeight.BOLD),  # Texto del botón
                                on_click=lambda e: page.go("/login")  # Navega a la página de inicio de sesión al hacer clic
                            ),
                        ],
                    ),
                ),
                ft.Container(  # Contenedor para la imagen de registro
                    expand=3,  # Permite que este contenedor expanda su espacio
                    image_src="img/signup.jpg",  # Fuente de la imagen de fondo
                    image_fit="cover",  # Ajusta la imagen para cubrir el área del contenedor
                    content=ft.Column(  # Contenedor vertical para alinear los elementos
                        alignment=ft.MainAxisAlignment.CENTER,  # Alinea los elementos verticalmente al centro
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Alinea los elementos horizontalmente al centro
                        controls=[  # Define los controles que se incluirán en la columna
                            ft.Icon(name=ft.icons.LOCK_PERSON_ROUNDED, size=200, color="white"),  # Ícono de candado
                            ft.Text("Registrarse",  # Texto que indica el propósito de la página
                                    color="white",  # Color del texto
                                    size=20, weight=ft.FontWeight.BOLD)  # Tamaño y estilo del texto
                        ]
                    )
                )
            ]
        )


    def signup(self, e):
        # Se obtienen los valores de los campos de entrada
        nombre = self.nombre.content.value
        apellido = self.apellido.content.value
        email_value = self.email.content.value
        password_value = self.password.content.value
        confirm_pass_value = self.confirm_pass.content.value

        # Verifica que todos los campos estén llenos
        if nombre and apellido and email_value and confirm_pass_value and password_value:

            # Verifica si las contraseñas coinciden
            if password_value == confirm_pass_value:

                # Valida si el correo electrónico tiene un formato válido
                if not self.validaciones.is_valid_email(email_value):
                    # Si no es válido, se muestra un error en el borde del campo email
                    self.email.border = self.error_border
                    self.error_field.value = "Ingrese los datos correctamente"
                    self.error_field.size = 16  # Muestra el mensaje de error
                    self.error_field.update()
                    self.email.update()
                    
                    # Espera un segundo y luego restablece el borde del campo email
                    time.sleep(1)
                    self.email.border = self.default_border
                    self.error_field.size = 0  # Oculta el mensaje de error
                    self.error_field.update()
                    self.email.update()

                # Si el email es válido, verifica si ya existe en la base de datos
                elif not self.db.check_data_exists(self.db.conn, "usuarios", f"email='{email_value}'"):
                    # Si el correo no está registrado, inserta los datos en la base de datos
                    self.db.insert_data(
                        self.db.conn,
                        "usuarios",
                        (nombre, apellido, email_value,hash_password(password_value))
                    )

                    # Muestra un mensaje de éxito al usuario
                    self.error_field.value = "Has sido registrado correctamente!"
                    self.error_field.color = "green"
                    self.error_field.size = 16  # Ajusta el tamaño del mensaje de éxito
                    self.page.update()
                    
                    # Espera un segundo y redirige al usuario a la página de inicio de sesión
                    time.sleep(1)
                    self.page.splash = None  # Desactiva cualquier pantalla de carga
                    self.page.update()
                    self.page.go("/login")  # Redirige a la página de login
                    
                else:
                    # Si el correo ya está registrado, muestra un error en el campo email
                    self.email.border = self.error_border
                    self.error_field.value = "El correo ya está registrado"
                    self.error_field.size = 16  # Muestra el mensaje de error
                    self.error_field.update()
                    self.email.update()
                    
                    # Espera un segundo y restablece el borde del campo email
                    time.sleep(1)
                    self.email.border = self.default_border
                    self.error_field.size = 0  # Oculta el mensaje de error
                    self.error_field.update()
                    self.email.update()

            else:
                # Si las contraseñas no coinciden, muestra un error en los campos de contraseña
                self.password.border = self.error_border
                self.confirm_pass.border = self.error_border
                self.error_field.value = "Las contraseñas no coinciden!"
                self.error_field.size = 16  # Muestra el mensaje de error
                self.error_field.update()
                self.confirm_pass.update()
                self.password.update()
                
                # Espera un segundo y restablece los bordes de los campos de contraseña
                time.sleep(1)
                self.password.border = self.default_border
                self.confirm_pass.border = self.default_border
                self.error_field.size = 0  # Oculta el mensaje de error
                self.error_field.update()
                self.confirm_pass.update()
                self.password.update()

        else:
            # Si no se completan todos los campos, muestra errores en todos los campos
            self.nombre.border = self.error_border
            self.apellido.border = self.error_border
            self.email.border = self.error_border
            self.password.border = self.error_border
            self.confirm_pass.border = self.error_border
            self.error_field.value = "Debes completar todos los campos"
            self.error_field.size = 16  # Muestra el mensaje de error
            self.error_field.update()
            self.confirm_pass.update()
            self.password.update()
            self.nombre.update()
            self.apellido.update()
            self.email.update()

            # Espera un segundo y restablece los bordes de todos los campos
            time.sleep(1)
            self.nombre.border = self.default_border
            self.apellido.border = self.default_border
            self.email.border = self.default_border
            self.password.border = self.default_border
            self.confirm_pass.border = self.default_border
            self.error_field.size = 0  # Oculta el mensaje de error
            self.error_field.update()
            self.confirm_pass.update()
            self.password.update()
            self.nombre.update()
            self.apellido.update()
            self.email.update()

    
