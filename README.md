# Challenge

## Estructura del proyecto

```
.
├── README.md
├── data/
│   ├── departments.csv
│   ├── hired_employees.csv
│   └── jobs.csv
├── create_tables.py
├── database.py
├── main.py
├── models.py
├── operations.py
└── requeriments.txt

```


## Requerimientos Software

- **Sistema Operativo**: Windows 10, macOS 10.15 o superio, distribuciones de Linux.
- **Python**: Versiones >= 3.9. Se recomienda utilizar un entorno virtual para evitar conflictos de dependencias.
- **Librerías**: utilizar el archivo `requirements.txt` para la instalación de las mismas.

## Configuración e Instalación

> **NOTA** Asegúrese de tener instalado `git` en su máquina o `GitHub Desktop` para la clonación del repositorio.

En una ventana de comandos (cmd/terminal), ejecutar los comandos que a continuación se describen:

**Clonar el repositorio**:

Clone el repositorio en su entorno local:
   ```bash
   git clone https://github.com/diegoa-rodriguezc/DEG_Challenge.git
   ```
   Cambie al directorio del proyecto:
   ```bash
   cd DEG_Challenge
   ```

**Instalación**

1. Instalar la libería respectiva para crear un entorno virtual de trabajo

```bash 
pip install virtualenv
```

2. Creación de entorno virtual
```bash 
python -m venv env
```

3. Activación de entorno virtual, previamente creado
    * En Windows, ejecutar:
    ```bash
    .\env\Scripts\Activate.ps1
    ```
    * En Linux, ejecutar:
    ```bash
    source env/bin/activate
    ```

4. Posterior a la activación del entorno virtual, se procede a realizar la instalación de dependiencias, con el comando:
```bash
pip install -r requirements.txt
```

> **NOTA** Antes de iniciar el servidor se deben ajustar los parámetros de conexión al servidor de Base de datos (usuario, contraseña, servidor, puerto y nombre del esquema), para lo cual se debe modificar el archivo denominado `database.py`. La Base de Datos utilizada para el presente proyecto es MS SQL Server. Los atributos a modificar son `user`, `password`, `host`, `port` y `databasename` .

5. Una vez ajustado los atributos de la Base de Datos, ejecutar la creación de tablas mediante el comando: 
```bash
python create_tables.py
```

6. Posterior a la instalación de dependencias y ajuste del archivo de conexión a Base de Datos, iniciar el servidor para uso del API
```bash
uvicorn main:app --reload
```

7. Una vez el servidor presente el mensaje de inicio correcto, similar al siguiente:
   ```
   INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
   INFO:     Started reloader process [15952] using StatReload
   INFO:     Started server process [10220]
   INFO:     Waiting for application startup.
   INFO:     Application startup complete.
   ```

8. Una vez el servidor ha iniciado correctamente se puede ingresar mediante un navegador a la URL http://127.0.0.1:8000/docs , donde se presentan los métodos POST/GET para uso y pruebas del API.

> Los datos con los cuales se realizan las cargas de datos se encuentran en la carpeta `data/`

