import asyncio
import flet as ft
from sqlite3 import connect
import time
from components.fields import CustomTextField
from utilidades.colores import customBgColor, customBorderColor, customDashboardBG, customPrimaryColor, customSideBarIconColor, customTextHeaderColor, cutomTextColor
from utilidades.validaciones import validaciones
from db.crud import database
#from db.token import generate_token
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Clase para la vista de login
class login(ft.Container):
    
    def __init__(self, page: ft.Page):
        super().__init__()
       
        # Expande el contenedor para ocupar todo el espacio
        self.expand = True
        # Instancia para validaciones externas
        self.validaciones = validaciones()
        # Bordes por defecto y en caso de error
        self.default_border = ft.border.all(width=1, color="#000000")  # Borde negro por defecto
        self.error_border = ft.border.all(color="red", width=1)  # Borde rojo para mostrar errores
        self.error_field = ft.Text(value="", color="red", size=0)  # Campo de texto para mostrar mensajes de error
        # Conexión a la base de datos
        self.db = database()

        # Campo de email con borde redondeado
        self.email = ft.Container(
            content=CustomTextField(label="Email"),  # Campo de texto personalizado para el email
            border=ft.border.all(width=1, color="#000000"),  # Borde del campo de email
            border_radius=ft.border_radius.all(20)  # Bordes redondeados en todo el contenedor del email
        )

        # Campo de contraseña con opción para mostrar/ocultar el texto
        self.password = ft.Container(
            content=CustomTextField(
                label="Password",
                password=True,  # Campo de contraseña (el texto estará oculto)
                can_reveal_password=True,  # Opción para mostrar/ocultar la contraseña
            ),
            border=ft.border.all(width=1, color="#000000"),  # Borde del campo de contraseña
            border_radius=ft.border_radius.all(20),  # Bordes redondeados en todo el contenedor de la contraseña
        )

        # Definición del contenido principal de la interfaz
        self.content = ft.Row(
            controls=[
                # Primera columna: imagen de fondo y formulario
                ft.Container(
                    expand=2,  # La primera columna ocupa el doble de espacio que la segunda
                    image_src="img/bglogin.png",  # Imagen de fondo para la sección izquierda
                    image_fit="cover",  # La imagen cubrirá toda el área
                    padding=ft.padding.all(40),  # Espaciado interno de 40
                    margin=ft.margin.all(0),  # Sin margen
                    content=ft.Column(  # Contenido en forma de columna
                        alignment=ft.MainAxisAlignment.CENTER,  # Alineación vertical en el centro
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Alineación horizontal en el centro
                        controls=[
                            # Título de bienvenida
                            ft.Text("BIENVENIDOS",
                                    color=customTextHeaderColor,  # Color de texto personalizado
                                    font_family="abeezee",  # Familia de fuentes
                                    size=40,  # Tamaño de la fuente
                                    weight=ft.FontWeight.BOLD  # Negrita
                                    ),
                            self.error_field,  # Mensaje de error dinámico
                            self.email,  # Campo de email
                            self.password,  # Campo de contraseña
                            # Botón para iniciar sesión
                            ft.Container(
                                alignment=ft.alignment.center,  # Alineado en el centro
                                height=40,  # Altura del botón
                                bgcolor="#234A94",  # Color de fondo del botón
                                content=ft.Text("Iniciar Sesión"),  # Texto del botón
                                border_radius=ft.border_radius.all(20),  # Bordes redondeados
                                on_click=self.login,  # Acción al hacer clic (método login)
                            ),
                            # Botón para registrarse
                            ft.Container(
                                alignment=ft.alignment.center,  # Alineado en el centro
                                height=40,  # Altura del botón
                                content=ft.Text("Registrase", color=customTextHeaderColor, weight=ft.FontWeight.BOLD),  # Texto del botón con color personalizado
                                on_click=lambda e: page.go("/signup")  # Redirección a la página de registro
                            ),
                        ],
                    ),
                ),
                # Segunda columna: imagen decorativa
                ft.Container(
                    expand=3,  # Esta columna ocupa más espacio que la primera
                    image_src="img/login.jpeg",  # Imagen para la sección derecha
                    image_fit="cover",  # La imagen cubrirá todo el espacio
                    content=ft.Column(  # Columna con contenido decorativo
                        alignment=ft.MainAxisAlignment.CENTER,  # Alineación vertical en el centro
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Alineación horizontal en el centro
                        controls=[
                            # Icono decorativo
                            ft.Icon(name=ft.icons.LOCK_PERSON_ROUNDED, size=200, color="white"),  # Icono de persona con candado
                            # Texto decorativo
                            ft.Text("Inicio de Sesión",
                                    color="white",  # Texto en blanco
                                    size=20, weight=ft.FontWeight.BOLD)  # Tamaño y negrita
                        ]
                    )
                )
            ]
        )

    # Método para manejar el inicio de sesión
    def login(self, e):
        # Obtiene los valores de email y contraseña del formulario
        email_value = self.email.content.value
        password_value = self.password.content.value

        # Validación si ambos campos están llenos
        if email_value and password_value:
            # Verifica si el email existe en la base de datos
            if self.db.check_data_exists(self.db.conn, "usuarios", f"email='{email_value}'"):
                get_user = self.db.get_data(self.db.conn, "usuarios", f"email='{email_value}'")  # Recupera los datos del usuario
                is_email_match = get_user[0].get("email") == email_value  # Verifica si el email coincide
                is_password_match = get_user[0].get('password') == hash_password(password_value)  # Verifica si la contraseña coincide

                # Si el email y la contraseña son correctos
                if is_email_match and is_password_match:
                    # Obtener el nombre del usuario
                    user_name = get_user[0].get("nombre")  # Suponiendo que el nombre está en el campo 'nombre' de la base de datos

                    # Guardamos el nombre en client_storage
                    self.page.client_storage.set("user_name", user_name)

                    self.page.update()  # Actualiza la página
                    time.sleep(1)  # Pausa de 1 segundo
                    self.page.update()  # Actualiza la página de nuevo
                    
                    # Redirige al dashboard
                    self.page.go("/dashboard")
                else:
                    # Si el email coincide pero la contraseña no
                    if is_email_match and not is_password_match:
                        self.password.border = self.error_border  # Muestra error en el campo de contraseña
                        self.error_field.value = "La contraseña es incorrecta"  # Mensaje de error
                    else:
                        # Si el email no coincide
                        self.email.border = self.error_border  # Muestra error en el campo de email
                        self.error_field.value = "El correo no está registrado"  # Mensaje de error

                    # Actualiza el estado visual de los campos
                    self.error_field.size = 16  # Aumenta el tamaño del mensaje de error
                    self.error_field.update()  # Actualiza el mensaje de error
                    self.email.update()  # Actualiza el campo de email
                    self.password.update()  # Actualiza el campo de contraseña
                    
                    # Pausa antes de restablecer los bordes y el mensaje de error
                    time.sleep(1)
                    self.email.border = self.default_border  # Restablece el borde por defecto del email
                    self.password.border = self.default_border  # Restablece el borde por defecto de la contraseña
                    self.error_field.size = 0  # Oculta el mensaje de error
                    self.error_field.update()  # Actualiza el mensaje de error
                    self.email.update()  # Actualiza el campo de email
                    self.password.update()  # Actualiza el campo de contraseña
            else:
                # Si el correo no existe en la base de datos
                self.email.border = self.error_border  # Borde rojo para indicar error
                self.error_field.value = "El correo no está registrado"  # Mensaje de error
                self.error_field.size = 16  # Aumenta el tamaño del mensaje de error
                self.error_field.update()  # Actualiza el mensaje de error
                self.email.update()  # Actualiza el campo de email
                time.sleep(1)
                self.email.border = self.default_border  # Restablece el borde por defecto
                self.error_field.size = 0  # Oculta el mensaje de error
                self.error_field.update()  # Actualiza el mensaje de error
                self.email.update()  # Actualiza el campo de email
        else:
            # Validación si faltan campos por completar
            if not email_value:
                self.email.border = self.error_border  # Borde rojo para el email si está vacío
            if not password_value:
                self.password.border = self.error_border  # Borde rojo para la contraseña si está vacía

            self.error_field.value = "Debes completar todos los campos"  # Mensaje de error por campos vacíos
           
            # Muestra el mensaje de error en tamaño 16 para hacerlo visible
            self.error_field.size = 16  
            self.error_field.update()  # Actualiza el mensaje de error en la interfaz

            # Actualiza los campos de email y contraseña en la interfaz
            self.email.update()
            self.password.update()

            # Pausa de 1 segundo antes de restablecer los valores por defecto
            time.sleep(1)

            # Restablece los bordes por defecto del email y la contraseña
            self.email.border = self.default_border  
            self.password.border = self.default_border

            # Oculta el mensaje de error reduciendo su tamaño a 0
            self.error_field.size = 0  
            self.error_field.update()  # Actualiza el campo de error en la interfaz

            # Actualiza nuevamente los campos de email y contraseña con los bordes por defecto
            self.email.update()
            self.password.update()




