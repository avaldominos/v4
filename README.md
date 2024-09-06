KeepCoding - Tech School\
BootCamp - DevOps & Cloud Computing - Edicion X.

Módulo - Contenedores, más que VMs.\
Alumno: Alberto Valdominos Martín


### Práctica Final.

Despliegue de una aplicación Python/Flask con lectura/escritura en base de datos MySQL mediante Docker Compose.



## Tabla de Contenidos

1. [Descripción](#1-descripción)
2. [Funcionamiento](#2-funcionamiento)
3. [Componentes](#3-componentes)
4. [Instalación](#4-instalación)
5. [Notas Adicionales](#5-notas-adicionales)
6. [Solución de Problemas](#6-solución-de-problemas)
7. [Recursos](#7-recursos)
8. [Licencia](#8-licencia)



## 1. Descripción

Esta aplicación Flask es un sitio web sencillo que registra cuántas veces se ha visitado su página principal. Funciona de la siguiente manera:

1. **Carga de configuración**: Utiliza un archivo `.env` para obtener las credenciales de acceso a una base de datos MySQL (usuario, contraseña, host, nombre de la base de datos).
2. **Conexión a la base de datos**: Se conecta a una base de datos MySQL para almacenar y recuperar el número de visitas a la página.
3. **Conteo de visitas**: Cada vez que alguien visita la página principal (ruta `'/'`), se obtiene el conteo actual de visitas desde la base de datos, se incrementa en 1, y luego se actualiza en la base de datos.
4. **Respuesta**: Devuelve un mensaje simple como "Hello World! I have been seen X times", donde `X` es el número de veces que se ha visitado la página.

Es un ejemplo básico de una aplicación web que interactúa con una base de datos para registrar el número de visitas.

## 2. Funcionamiento

A continuación se incluye una explicacion más detallada de como funciona esta aplicación Flask `app.py`:


### 2.1. **Importación de Módulos**
   - `os`: Se utiliza para interactuar con el sistema operativo, específicamente para obtener variables de entorno.
   - `time`: Permite realizar operaciones relacionadas con el tiempo, en este caso se usa para controlar los intervalos entre intentos de conexión a la base de datos en caso de error.
   - `mysql.connector`: Es el conector que permite a la aplicación interactuar con una base de datos MySQL.
   - `Flask`: Es el framework que permite construir aplicaciones web en Python.
   - `load_dotenv`: Permite cargar variables de entorno desde un archivo `.env`, facilitando la configuración de la aplicación sin exponer credenciales en el código.

### 2.2. **Carga de Variables de Entorno**
   ```python
   load_dotenv()
   ```
   Esta línea carga el contenido del archivo `.env` en las variables de entorno de la aplicación. Esto es útil porque puedes definir valores como `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_HOST` y `MYSQL_DATABASE` en el archivo `.env` en lugar de escribirlos directamente en el código.

### 2.3. **Configuración de la Base de Datos**
   ```python
   db_config = {
       'user': os.getenv('MYSQL_USER'),
       'password': os.getenv('MYSQL_PASSWORD'),
       'host': os.getenv('MYSQL_HOST'),
       'database': os.getenv('MYSQL_DATABASE')
   }
   ```
   Aquí se configura la conexión a MySQL utilizando las variables de entorno. La función `os.getenv()` obtiene el valor de la variable de entorno correspondiente. La configuración (`db_config`) incluye el nombre de usuario, contraseña, host y base de datos de MySQL.

### 2.4. **Función para Obtener la Conexión a la Base de Datos**
   ```python
   def get_db_connection():
       return mysql.connector.connect(**db_config)
   ```
   Esta función crea y devuelve una conexión a la base de datos MySQL usando la configuración definida en el diccionario `db_config`. El operador `**` descompone el diccionario para pasar los parámetros de conexión de manera correcta.

### 2.5. **Función para Obtener y Actualizar el Conteo de Visitas**
   ```python
   def get_hit_count():
       retries = 5
       while True:
           try:
               conn = get_db_connection()
               cursor = conn.cursor()

               cursor.execute("SELECT count FROM hits WHERE id = 1;")
               result = cursor.fetchone()
               count = result[0] if result else 0

               new_count = count + 1
               cursor.execute("UPDATE hits SET count = %s WHERE id = 1;", (new_count,))
               conn.commit()

               cursor.close()
               conn.close()
               return new_count
           except mysql.connector.Error as err:
               if retries == 0:
                   raise err
               retries -= 1
               time.sleep(0.5)
   ```
   Esta función realiza los siguientes pasos:

   1. **Reintentos de Conexión**: Intenta hasta 5 veces conectarse a la base de datos en caso de fallo. Si tras 5 intentos sigue fallando, levanta una excepción.
   2. **Consulta de Visitas**: Se conecta a la base de datos, ejecuta una consulta SQL para obtener el valor del campo `count` en la tabla `hits` (supuestamente tiene solo una fila con `id = 1`).
   3. **Incremento del Conteo**: Si el valor existe, lo incrementa en 1. Si no existe (por ejemplo, si la tabla está vacía), lo inicializa a 0.
   4. **Actualización en la Base de Datos**: El nuevo valor del conteo se actualiza en la tabla mediante una consulta SQL `UPDATE`.
   5. **Cierre de Conexión**: Cierra la conexión a la base de datos después de realizar la consulta y actualización.
   6. **Devolución del Conteo**: Finalmente, devuelve el nuevo valor del conteo de visitas.

### 2.6. **Definición de la Ruta Principal de la Aplicación**
   ```python
   @app.route('/')
   def hello():
       count = get_hit_count()
       return 'Hello World! I have been seen {} times.\n'.format(count)
   ```
   Aquí se define la ruta `'/'`, es decir, la página principal de la aplicación web. Cada vez que un usuario visita esta página, Flask ejecuta la función `hello()` que:
   
   1. Llama a `get_hit_count()` para obtener e incrementar el número de visitas.
   2. Devuelve una cadena de texto que muestra el número de veces que la página ha sido vista.

   La función `@app.route('/')` define la URL que manejará esta vista, en este caso la raíz del sitio web (`'/'`).

### 2.7. **Ejecución de la Aplicación**
   ```python
   if __name__ == '__main__':
       app.run(host='0.0.0.0')
   ```
   Esta es la sección que inicia la aplicación si el script se ejecuta directamente. `app.run()` inicia el servidor de Flask en el host `0.0.0.0`, lo que significa que estará accesible desde cualquier dirección IP (útil si se despliega en un servidor remoto). La aplicación por defecto escucha en el puerto 5000, aunque esto se puede cambiar si es necesario.



## 3. Componentes

Este repositorio contiene la configuración necesaria para desplegar una aplicación Flask junto con una base de datos MySQL utilizando Docker Compose.

La estructura del proyecto es la siquiente:


```plaintext
├── Dockerfile                  
├── requirements.txt            
├── compose.yaml                
├── .env                        
├── mysql-init-files/           
│   └── ini.sql                 
└── README.md                   

```

Descripción de los archivos:

- **Dockerfile**: Define cómo construir la imagen de la aplicación Flask.
- **requirements.txt**: Lista de dependencias que la aplicación necesita para funcionar.
- **compose.yaml**: Orquesta varios servicios (Flask y MySQL) y define cómo deben interactuar. El servicio `app` es para Flask y `mysql` es para MySQL. El archivo gestiona automáticamente la creación de contenedores, redes y volúmenes necesarios para que ambos servicios funcionen juntos.
- **.env**: contiene las credenciales de conexión para la base de datos MySQL
- **/mysql-init-files/ini.sql**: subidrectorio dentro del directorio principal con archivo de inicialización de la base de datos.
- **README.md**: Documentación del proyecto.
  

## 4. Instalación

Para desplegar la aplicación en docker debes seguir estos pasos:

1. **Instala Docker y Docker Compose**:
   
   Antes de comenzar asegúrate de tener Docker y Docker Compose instalados en tu máquina.

   - [Docker](https://docs.docker.com/get-docker/)
   - [Docker Compose](https://docs.docker.com/compose/install/)

2. **Clona el repositorio**:

   ```bash
   git clone https://github.com/avaldominos/v4.git

3. **Construye los contenedores**:
   
   En el terminal, desde la carpeta donde están tus archivos (incluyendo el `Dockerfile` y `compose.yaml`), ejecuta:

   ```bash
   docker compose up 
   ```

   Este comando hará lo siguiente:
      - Construirá la imagen de la aplicación Flask utilizando el `Dockerfile`.
      - Creará un contenedor para la aplicación y otro para MySQL con la configuración del archivo `compose.yaml`.
      - Si es la primera vez que ejecutas esto, descargará la imagen de MySQL desde Docker Hub.
      - Iniciará ambos contenedores, conectándolos en una red virtual para que se puedan comunicar.

4. **Verifica que los contenedores están corriendo**:

   Puedes verificar que ambos contenedores estén en ejecución con el siguiente comando (ejecutado en la carpeta del proyecto):

   ```
   docker compose ps
   ```

   Deberias ver una salida similar a:
   
   ```
         Name                    Command               Status           Ports         
   ----------------------------------------------------------------------------------
   flask_app           python app.py                     Up      0.0.0.0:5000->5000/tcp
   flask_mysql         docker-entrypoint.sh mysqld       Up      0.0.0.0:3306->3306/tcp, 33060/tcp
   ```



5. **Acceder a la aplicación**:
   
   Una vez que todo esté en marcha, podrás acceder a la aplicación Flask en tu navegador en `http://localhost:5000`, y Flask estará conectado a la base de datos MySQL dentro de su propio contenedor.

   Deberías ver una salida similar a:

   ````
   Hello World! I have been seen 1 times.
   ````

   Actualizando el navegador, el contador debería incrementarse.


6. **Detener los contenedores**:

   Para detener los contenedores, presiona `CTRL + C` en la terminal donde ejecutaste `docker compose up`. Una vez parados puedes volverlos a arrancar con:
    ```
   docker compose start
   ```  
   Si actualizamos nuevamente el navegador, el contador debería añadir 1 a la ultima visualización realizada.
   
   Luego, para eliminar los contenedores parados, ejecuta:

   ```
   docker compose down
   ```



## 5. Notas Adicionales

- **Persistencia de datos**: El volumen `mysql_data` se utiliza para la persistencia de los datos de MySQL, por lo que los datos no se perderán al detener los contenedores..
- **Networking**: Docker Compose crea una red entre los contenedores, permitiendo que Flask acceda a MySQL a través del alias `mysql` (el servicio MySQL se llama `mysql` en el archivo `compose.yaml`).
- **Seguridad**: En producción, sería recomendable utilizar un gestor de secretos en lugar de exponer las credenciales en el archivo `.env`.

## 6. Solución de Problemas

- **Error de Conexión a la Base de Datos**: Si la aplicación Flask no puede conectarse a la base de datos MySQL, asegúrate de que las credenciales en el archivo .env sean correctas y que el contenedor de MySQL esté en ejecución.

- **Puerto Ya en Uso**: Si obtienes un error indicando que el puerto 5000 o 3306 ya está en uso, asegúrate de que ninguna otra aplicación esté utilizando esos puertos o cambia los puertos en el archivo `compose.yaml`.


## 7. Recursos

- [Referencia oficial Dockerfile](https://docs.docker.com/reference/dockerfile/)
- [Referencia oficial Docker Compose](https://docs.docker.com/reference/compose-file/)
- [Ejemplos oficiales de Docker](https://docs.docker.com/samples/)


## 8. Licencia
Este proyecto está bajo la licencia GNU GPL.


