import sqlite3

class database:
    
    # Inicializa la clase y crea una conexión a la base de datos SQLite
    def __init__(self) -> None:
        # Conexión a la base de datos "db.db" con check_same_thread deshabilitado
        self.conn = sqlite3.connect("db/db.db", check_same_thread=False)

    # Método para obtener datos de una tabla con o sin condiciones
    def get_data(self, conn, table_name, conditions=None):
        cursor = conn.cursor()  # Crea un cursor para ejecutar comandos SQL
        if conditions:
            # Si hay condiciones, ejecuta una consulta SQL con esas condiciones
            cursor.execute(f"SELECT * FROM {table_name} WHERE {conditions}")
        else:
            # Si no hay condiciones, selecciona todos los datos de la tabla
            cursor.execute(f"SELECT * FROM {table_name}")
        
        rows = cursor.fetchall()  # Obtiene todas las filas de la consulta
        columns = [col[0] for col in cursor.description]  # Obtiene los nombres de las columnas
        
        # Estructura los datos en un formato de lista de diccionarios
        result = [{columns[i]: row[i] for i in range(len(columns))} for row in rows]
        
        return result  # Devuelve el resultado estructurado como lista de diccionarios

    # Método para verificar si existen datos que cumplan una condición
    def check_data_exists(self, conn, table_name, condition):
        cursor = conn.cursor()  # Crea un cursor para ejecutar comandos SQL
        # Ejecuta una consulta que devuelve si existe al menos un registro que cumpla la condición
        cursor.execute(f"SELECT EXISTS (SELECT 1 FROM {table_name} WHERE {condition})")
        # Devuelve True si existe algún registro, False en caso contrario
        return cursor.fetchone()[0] == 1

    # Método para insertar datos en la tabla
    def insert_data(self, conn, table_name, values):
        cursor = conn.cursor()  # Crea un cursor para ejecutar comandos SQL
        # Inserta los valores proporcionados en las columnas "nombre", "apellido", "email" y "password"
        cursor.execute(
            f"INSERT INTO {table_name} (nombre, apellido, email, password) VALUES (?, ?, ?, ?)",
            values  # Valores a insertar en la tabla
        )
        conn.commit()  # Confirma los cambios en la base de datos


    def insert_data_prdoct(self, conn, table_name, values):
        cursor = conn.cursor()  # Crea un cursor para ejecutar comandos SQL
        
        cursor.execute(
            f"INSERT INTO {table_name} (nombre, precio, stock, descripcion) VALUES (?, ?, ?, ?)",
            values  # Valores a insertar en la tabla
        )
        conn.commit()  # Confirma los cambios en la base de datos



    def update_data_product(self, conn, table_name, values, product_id):
        cursor = conn.cursor()  # Crea un cursor para ejecutar comandos SQL
        
        # Construye la consulta SQL con los valores a modificar
        cursor.execute(
            f"""
            UPDATE {table_name}
            SET nombre = ?, precio = ?, stock = ?, descripcion = ?
            WHERE id = ?
            """,
            (*values, product_id)  # Los valores que se actualizan, seguido por el ID del producto
        )
        
        conn.commit()  # Confirma los cambios en la base de datos


    
