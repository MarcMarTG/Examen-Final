from typing import Any  # Importa Any del módulo typing para uso de tipos genéricos
import flet as ft  # Importa la biblioteca Flet para construir interfaces gráficas

# Definición de colores
customTextColor = "#000000"  # Texto en color negro
customHintTextColor = "#000000"  # Color del texto de sugerencia (hint) en negro
customBorderColor = "#DDDDDD"  # Color de borde por defecto (gris claro)
focusedBorderColor = "#234A94"  # Color del borde al enfocar (azul)
errorBorderColor = "#FF4D4D"  # Color rojo para indicar errores

class CustomTextField(ft.TextField):  # Clase personalizada que hereda de ft.TextField
    def __init__(  # Inicializador de la clase
            self,
            label,  # Texto que aparece como etiqueta del campo
            icon=None,  # Ícono opcional que se puede añadir al campo
            border=ft.InputBorder.NONE,  # Borde visible por defecto (sin borde)
            error_text=None,  # Mensaje de error que se muestra si hay un error
            input_filter=None,  # Filtro de entrada para validar el contenido del campo
            label_color="#234A94",  # Color del texto de la etiqueta
            **kwargs  # Argumentos adicionales para la clase base
    ):
        # Llama al inicializador de la clase base ft.TextField con los parámetros personalizados
        super().__init__(
            label=label,  # Establece la etiqueta del campo
            border=border,  # Establece el tipo de borde
            error_text=error_text,  # Mensaje de error asociado al campo
            color=customTextColor,  # Establece el color del texto
            content_padding=ft.padding.symmetric(vertical=20, horizontal=25),  # Ajusta el espaciado del contenido
            hint_style=ft.TextStyle(size=14, color=customHintTextColor),  # Define el estilo del hint (sugerencia)
            input_filter=input_filter,  # Aplica el filtro de entrada definido
            focused_color=customTextColor,  # Color del texto cuando el campo está enfocado
            focused_border_color=focusedBorderColor,  # Color del borde cuando el campo está enfocado
            border_color=customBorderColor,  # Color del borde inicial
            border_radius=ft.border_radius.all(20),  # Establece bordes redondeados
            bgcolor="transparent",  # Establece el fondo como transparente
            label_style=ft.TextStyle(color=label_color),  # Establece el color del texto de la etiqueta
            **kwargs  # Pasa los argumentos adicionales a la clase base
        )


class CustomFormField(ft.Container):
    def __init__(  # Inicializador de la clase
            self,
            label,  # Texto que aparece como etiqueta del campo
            icon=None,  # Ícono opcional que se puede añadir al campo
            border=ft.border.all(width=1, color="black"),  # Borde visible por defecto (sin borde)
            error_text=None,  # Mensaje de error que se muestra si hay un error
            input_filter=None,  # Filtro de entrada para validar el contenido del campo
            label_color="#234A94",  # Color del texto de la etiqueta
            sm=12,
            md=6,
            xl=6,
            **kwargs  # Argumentos adicionales para la clase base
    ):
         super().__init__()
         self.border_radius = 5
         self.col ={"sm":sm, "md":md, "xl":xl}

         self.content = ft.Column(
             controls=[
                 ft.Text(label, color="black"),
                 CustomTextField(
                     label="",
                     icon=icon,
                     border=border,
                     error_text=error_text,
                     **kwargs
                 )
             ]
         )


class CustomDropDownField(ft.Container):
    def __init__(  # Inicializador de la clase
            self,
            label,
            sm=12,
            md=6,
            xl=6,
            dropdown_list=[]
    ):
        super().__init__()
        self.border_radius = 5
        self.col = {"sm": sm, "md": md, "xl": xl}

        # Crear opciones para el Dropdown
        options = []
        for item in dropdown_list:
            options.extend([ft.dropdown.Option(item)])

        # Usar la clase Dropdown correcta
        self.content = ft.Column(
            controls=[
                ft.Text(label, color="black"),
                ft.Dropdown(  # Cambiar a ft.Dropdown
                    color="black",
                    bgcolor="white",
                    focused_bgcolor="white",
                    options=options  # Asignar opciones correctamente
                )
            ]
        )
