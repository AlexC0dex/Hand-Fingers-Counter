Instalación y Configuración
## 1. Instalar las dependencias

Antes de iniciar, asegúrate de estar dentro de tu entorno virtual (Conda o venv) para evitar conflictos globales. Ejecuta el siguiente comando en la raíz del proyecto:
Bash

pip install -r requirements.txt

## 2. Descargar el modelo de MediaPipe (.task)

El motor de detección de manos no incluye los pesos neuronales por defecto. Para que la API pueda inicializarse, debes descargar el modelo oficial.
Para hacerlo de forma automática:

    Abre tu entorno de Jupyter.

    Ingresa al archivo notebooks/testing.ipynb.

    Ejecuta la segunda celda del notebook. Esto descargará el archivo hand_landmarker.task y lo colocará correctamente dentro de la carpeta model/.

### Cómo ejecutar la API localmente

Una vez instaladas las dependencias y con el modelo ubicado en su carpeta, levanta el servidor ejecutando el siguiente comando desde la raíz de tu proyecto:
Bash

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

    --reload: Permite que el servidor se actualice automáticamente en tiempo real si modificas el código fuente.