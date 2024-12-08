import flet as ft  # Importa el framework Flet para construir la interfaz gráfica
from paginas.autenticacion.login import login  # Importa la clase login para la página de inicio de sesión
from paginas.autenticacion.signup import signup  # Importa la clase signup para la página de registro
from paginas.dashboard.dashboard import dashboard  # Importa la clase dashboard para la página principal
from paginas.productos.act_product import ActProduct
from paginas.productos.producto import ProductList  # Importa la clase ProductList para la página de productos
from utilidades.colores import (customBgColor, customBorderColor, customDashboardBG, customPrimaryColor, customSideBarIconColor, customTextHeaderColor, cutomTextColor)  # Importa los colores personalizados usados en la interfaz
# Función que maneja las diferentes vistas de la aplicación según la ruta
def views_handler(page):
    # Retorna un diccionario que asocia cada ruta con una vista correspondiente
    return {
        # Vista del dashboard asociada a la ruta "/dashboard"
        "/dashboard": ft.View(route="/dashboard", controls=[dashboard(page)]),
        
        # Vista de productos asociada a la ruta "/producto"
        "/producto": ft.View(route="/producto", controls=[ProductList(page)]),

        "/act_product": ft.View(route="/act_product", controls=[ActProduct(page)]),
        
        # Vista de login asociada a la ruta "/login"
        "/login": ft.View(
            route="/login",  # Define la ruta como "/login"
            bgcolor="#000000",  # Fondo de la vista login en color negro
            padding=ft.padding.all(0),  # Sin relleno en la vista
            controls=[login(page)]  # Control principal de la vista es el login
        ),

        # Vista de registro asociada a la ruta "/signup"
        "/signup": ft.View(
            route="/signup",  # Define la ruta como "/signup"
            bgcolor="#000000",  # Fondo de la vista de registro en color negro
            padding=ft.padding.all(0),  # Sin relleno en la vista
            controls=[signup(page)]  # Control principal de la vista es el registro (signup)
        ),
    }
