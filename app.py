import os  # Módulo para interactuar con el sistema operativo
import time  # Módulo para manejar operaciones relacionadas con el tiempo
import mysql.connector  # Conector de MySQL para interactuar con la base de datos
from flask import Flask  # Importa la clase Flask para crear la aplicación web
from dotenv import load_dotenv  # Importa la función load_dotenv para cargar variables de entorno desde un archivo .env

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Crear una instancia de la aplicación Flask
app = Flask(__name__)

# Configuración de la conexión a MySQL usando variables de entorno
db_config = {
    'user': os.getenv('MYSQL_USER'),            # Usuario de MySQL, obtenido de la variable de entorno MYSQL_USER
    'password': os.getenv('MYSQL_PASSWORD'),    # Contraseña de MySQL, obtenida de la variable de entorno MYSQL_PASSWORD
    'host': os.getenv('MYSQL_HOST'),            # Host de MySQL, obtenido de la variable de entorno MYSQL_HOST
    'database': os.getenv('MYSQL_DATABASE')     # Nombre de la base de datos de MySQL, obtenido de la variable de entorno MYSQL_DATABASE
}

def get_db_connection():
    """
    Crea y devuelve una conexión a la base de datos MySQL.
    
    Utiliza la configuración definida en `db_config` para conectarse a la base de datos.
    """
    return mysql.connector.connect(**db_config)

def get_hit_count():
    """
    Obtiene el conteo de visitas desde la base de datos MySQL y lo incrementa en 1.
    
    Este método intenta conectarse a la base de datos y realiza una consulta para
    obtener el conteo actual de visitas. Luego, incrementa el conteo y lo actualiza
    en la base de datos. En caso de fallo de conexión, reintenta hasta 5 veces antes de fallar.
    """
    retries = 5  # Número de intentos de reconexión en caso de error
    while True:
        try:
            # Conectarse a la base de datos
            conn = get_db_connection()
            cursor = conn.cursor()

            # Ejecutar una consulta SQL para obtener el conteo actual de visitas
            cursor.execute("SELECT count FROM hits WHERE id = 1;")
            result = cursor.fetchone()  # Recuperar el resultado de la consulta
            count = result[0] if result else 0  # Asignar el valor del conteo o 0 si no hay resultados

            # Incrementar el conteo de visitas
            new_count = count + 1
            cursor.execute("UPDATE hits SET count = %s WHERE id = 1;", (new_count,))
            conn.commit()  # Guardar los cambios en la base de datos

            # Cerrar el cursor y la conexión a la base de datos
            cursor.close()
            conn.close()
            return new_count  # Devolver el nuevo conteo de visitas
        except mysql.connector.Error as err:
            # Si ocurre un error, se reduce el número de reintentos
            if retries == 0:
                raise err  # Si se agotan los reintentos, se lanza la excepción
            retries -= 1
            time.sleep(0.5)  # Espera 0.5 segundos antes de intentar reconectar

# Definir una ruta para la raíz de la aplicación web
@app.route('/')
def hello():
    """
    Maneja la solicitud GET a la ruta raíz ('/').

    Llama a la función `get_hit_count` para obtener e incrementar el número de visitas,
    y devuelve un mensaje que incluye el conteo actual de visitas.
    """
    count = get_hit_count()  # Obtener el conteo de visitas
    return 'Hello World! I have been seen {} times.\n'.format(count)  # Respuesta HTTP con el conteo de visitas

# Ejecutar la aplicación Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0')  # Iniciar la aplicación en el host 0.0.0.0 (acepta conexiones desde cualquier IP)




