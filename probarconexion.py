
from conexion import obtener_conexion

conexion = None

try:
    conexion = obtener_conexion()

    print("¡Conexión exitosa con MySQL!")

    cursor = conexion.cursor()
    cursor.execute("SHOW TABLES")

    for tabla in cursor.fetchall():
        print("Tabla encontrada:", tabla[0])

    cursor.close()

except Exception as error:
    print("Error al conectar:", error)

finally:
    if conexion is not None and conexion.is_connected():
        conexion.close()
