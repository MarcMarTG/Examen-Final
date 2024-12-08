from typing import Any
import flet as ft

# Definición de colores personalizados utilizados en la tarjeta
customTextColor = "#000000"  # Color del texto: negro
customHintTextColor = "#000000"  # Color del hint (sugerencia) en negro
customBorderColor = "#DDDDDD"  # Color del borde por defecto: gris claro
focusedBorderColor = "#234A94"  # Color del borde cuando está enfocado: azul
errorBorderColor = "#FF4D4D"  # Color del borde en caso de error: rojo

# Definición de la clase CustomDisplayCard que hereda de ft.Container
class CustomDisplayCard(ft.Container):
    def __init__(self, iconbg, title, value):
        super().__init__()

        # Asignación de parámetros iniciales de la tarjeta: icono, título y valor
        self.iconbg = iconbg  # Color de fondo del ícono (personalizable)
        self.title = title  # Título que se mostrará en la tarjeta
        self.value = value  # Valor numérico o información adicional

        # Definición de la sombra que tendrá la tarjeta
        self.shadow = (
            ft.BoxShadow(spread_radius=1, blur_radius=5, color="#1a000000"),  # Sombra ligera con desenfoque
        )

        # Establecimiento del tamaño de la tarjeta
        self.width = 250  # Ancho de la tarjeta
        self.height = 80  # Altura de la tarjeta
        self.bgcolor = "white"  # Fondo blanco para la tarjeta

        # Definición del contenido principal de la tarjeta como una fila (Row)
        self.card = ft.Row(
            controls=[
                # Primer contenedor: ícono a la izquierda con color de fondo personalizado
                ft.Container(
                    height=100,  # Altura del contenedor del ícono
                    width=80,  # Ancho del contenedor del ícono
                    bgcolor=self.iconbg,  # Color de fondo del ícono
                    content= ft.Icon(  # Ícono que se mostrará en el contenedor
                        name= ft.icons.PERSON_SHARP,  # Nombre del ícono (persona)
                        color="white",  # El ícono será de color blanco
                        size=50,  # Tamaño del ícono
                    ),
                ), 
                # Segundo contenedor: texto del título y el valor
                ft.Container(
                    padding=ft.padding.only(left=5, right=5),  # Padding de 5 unidades en los lados izquierdo y derecho
                    content= ft.Column(  # Columna que contiene los textos del título y el valor
                        controls=[
                            # Texto del título
                            ft.Text(
                                self.title,  # Texto dinámico del título
                                color=customTextColor,  # Color negro para el título
                                size=15,  # Tamaño de la fuente: 15
                                weight=ft.FontWeight.BOLD  # Negrita
                            ),
                            # Texto del valor
                            ft.Text(
                                self.value,  # Texto dinámico del valor
                                color=customTextColor,  # Color negro para el valor
                                size=25,  # Tamaño de la fuente: 25 (más grande que el título)
                                weight=ft.FontWeight.BOLD  # Negrita
                            ),
                        ]
                    )
                )
            ]
        )

        # Asigna la tarjeta generada (self.card) como contenido del contenedor principal
        self.content = self.card
