# Instalación de las librerías necesarias
#!pip install langchain langchain_ollama
#!pip install chromadb sentence-transformers langchain_huggingface langchain_chroma

# Librerías necesarias
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain_ollama.chat_models import ChatOllama
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
import requests
from bs4 import BeautifulSoup
import re

# Cargar los datos desde una página WEB
url = 'https://en.wikipedia.org/wiki/Football'
response = requests.get(url)

if response.status_code == 200:
    # Usamos BeautifulSoup para analizar el HTML
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extraemos solo los párrafos de la página (con el tag <p>)
    paragraphs = soup.find_all('p')
    
    # Filtramos el contenido relevante de los párrafos
    clean_text = ''
    for paragraph in paragraphs:
        # Extraemos el texto de cada párrafo, eliminamos los saltos de línea y espacios innecesarios
        clean_text += paragraph.get_text(separator=' ', strip=True) + ' '
    
    # Limpieza adicional:
    # Elimina las referencias como [1], [2], etc.
    clean_text = re.sub(r'\[.*?\]', '', clean_text)
    # Elimina espacios extra
    clean_text = re.sub(r'\s+', ' ', clean_text)
    # Elimina posibles saltos de línea extra
    clean_text = clean_text.replace("\n", " ")

    print("Texto de la página cargado:")
    print(clean_text[:1000])  # Muestra los primeros 1000 caracteres del texto limpio
else:
    raise Exception(f"Error al cargar la página: {response.status_code}")

# Seleccionar el modelo para la vectorización
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

# Accedemos a la base de datos Chroma
vector_store = Chroma(
    collection_name="rag1",
    embedding_function=embeddings,
    persist_directory="./datasets",
)

# Ver cómo funciona la base de datos
retriever = vector_store.as_retriever()

# RAG Chain
# Plantilla de conversación
conversation_template = """Please answer the following question based only on the given context:
{context}

Question: {question}
"""

# Crear el prompt a partir de la plantilla
prompt_template = ChatPromptTemplate.from_template(conversation_template)

# LLM local
local_llm = "tinyllama"
local_model = ChatOllama(model=local_llm)

# Cadena de procesamiento
qa_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt_template
    | local_model
    | StrOutputParser()
)

# Ejecutamos una pregunta para probar el sistema
result = qa_chain.invoke("What is football?")
print("Respuesta de la IA:")
print(result)
