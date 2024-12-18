# Creación de sistemas RAG sobre bases de datos vectoriais!

El objetivo del ejercicio es desarrollar un sistema RAG (Generación Aumentada Recuperada). Este tipo de sistema integra o utiliza el LLM y su propia base de datos para responder más preguntas que el usuario haga.


## Guía para Configurar y Ejecutar el Modelo Llama 3.2

 #### **1. Crear una Red en Docker**

Primero, crea una red personalizada que permita la comunicación entre los servicios involucrados en el proyecto:

    docker network create llama_network

#### **2. Iniciar el Contenedor de Ollama**

Levanta el contenedor de Ollama, encargado de gestionar el modelo de lenguaje. Ejecuta este comando para iniciar sin soporte para GPU:

    docker run -d -v llama_data:/root/.ollama -p 11434:11434 --name llama_service --net=llama_network ollama/ollama

#### **3. Comprobar el Estado del Servicio Ollama**

Asegúrate de que Ollama se está ejecutando correctamente ejecutando el siguiente comando:

    curl http://localhost:11434
Si todo está configurado correctamente, deberías recibir como respuesta:

    Ollama is running

#### **4. Configurar Open-WebUI**

Open-WebUI proporciona una interfaz visual para gestionar modelos y permitir interacción mediante chat.

Inicia el contenedor de Open-WebUI con el siguiente comando:

    docker run -d -p 3000:8080 -e OLLAMA_BASE_URL=http://llama_service:11434 -v webui_data:/app/backend/data --name open_web_ui --net=llama_network --restart always ghcr.io/open-webui/open-webui:main

#### **5. Descargar un Modelo de Lenguaje**

-   Accede a Open-WebUI desde el navegador.
-   Busca el modelo **Llama 3.2** y descárgalo.
-   Verifica que el modelo aparece como instalado en la lista disponible.

**Nota**: Asegúrate de mantener activo el contenedor de Ollama para ejecutar cuadernos de trabajo. Open-WebUI solo es necesario para la descarga del modelo.

## Configurar el Entorno e Instalar Dependencias
#### **1. Crear y Activar un Entorno Virtual**

Utiliza **Conda** para gestionar un entorno virtual para el proyecto. Ejecuta los siguientes comandos en la terminal:

    conda create --name rag_env python=3.13.1
    conda activate rag_env
    conda install pip
#### **2. Instalar Librerías Necesarias**

Con el entorno activado, instala las dependencias listadas en el archivo `requirements.txt`:

    pip install -r requirements.txt

## Implementación de un Sistema RAG
El objetivo principal es desarrollar un sistema **RAG (Retrieve-Augmented Generation)**, que combine un modelo de lenguaje grande (**LLM**) con una base de datos personalizada para responder preguntas fundamentadas en información previamente almacenada.

#### Apartados del Proyecto

1.  **RAG en Inglés usando Datos de una Página Web**
    
    -   Crear un sistema que utilice datos de una página web como fuente de información.
    -   Almacenar los datos en una base de datos vectorial y procesar las consultas de los usuarios basándose en la información extraída.
2.  **RAG en Español a partir de Archivos PDF**
    
    -   Desarrollar un sistema que procese archivos PDF.
    -   Dividir el contenido en fragmentos, almacenarlo en una base de datos vectorial y responder preguntas en español basándose en dichos datos.
3.  **Diseñar una Interfaz Gráfica (GUI)**
    
    -   Implementar una GUI para interactuar con uno de los sistemas RAG creados.
    -   La interfaz debe ser intuitiva, permitiendo a los usuarios enviar preguntas y recibir respuestas fácilmente.
4.  **RAG Dockerizado con MongoDB Atlas**
    
    -   Configurar un sistema RAG que use MongoDB Atlas para almacenar y gestionar la base de datos vectorial.
    -   Ofrecer una solución robusta y escalable para manejar consultas y datos.
### **Notas Finales**

Cada sección debe completarse siguiendo las instrucciones específicas y asegurándose de cumplir los objetivos del proyecto de forma estructurada y eficiente.
