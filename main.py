import flet as ft  # Importa la biblioteca Flet para construir la interfaz gráfica
from router import views_handler  # Importa la función views_handler que gestiona las vistas basadas en rutas


# Función principal que se ejecuta cuando la aplicación se inicia
def main(page: ft.Page):
    page.window.center()  # Centra la ventana de la aplicación en la pantalla
    
    # Función que maneja los cambios de ruta (navegación entre vistas)
    def route_change(route):
        page.views.clear()  # Limpia la lista de vistas actuales
        page.views.append(views_handler(page)[page.route])  # Añade la vista correspondiente a la ruta actual
        
        # Asigna la fuente personalizada a la página
        page.fonts = {
            "abeezee" : "font/ABeeZee-Regular.ttf"  # Define una fuente personalizada llamada "abeezee"
        }

        page.update()  # Actualiza la página para reflejar los cambios

    # Asocia la función route_change al evento de cambio de ruta
    page.on_route_change = route_change

    # Inicia la aplicación mostrando la vista de login al cargar la aplicación
    page.go("/login")


# Inicia la aplicación Flet, estableciendo `main` como la función objetivo y la carpeta de recursos como "assets"
ft.app(target=main, assets_dir="assets")
