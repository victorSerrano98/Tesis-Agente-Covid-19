# Agente virtual para brindar asistencia acerca del Covid-19
<p></p>
Agente virtual desarrollado con el modelo de lenguaje BERT, el cual fue previamente afinado para responder preguntas comunes del covid-19.
<p></p>
<div align="center">
	 <img src ="https://user-images.githubusercontent.com/33547749/159361179-e5cae02e-8a26-42cc-acb7-e1c4a0401e1f.png" width="600" height="350" />
</div>
<p></p>
 
<b>Autores:</b>
	Victor Yamil Serrano Zari,  José Alexis Carrión Ojeda

# Introducción
En este repositorio se encuentran los archivos utilizados para el desarrollo del trabajo de titulacion "Agente virtual para brindar asistencia acerca del Covid-19", se encuentra divido en carpetas en las cuales se pueden encontrar los archivos que fueron necesarios para el ajuste de modelo BERT, la creacion de la base conocimientos utilizando Elasticsearch, la Api con ayuda del frameword FastApi y la interfaz desarrollada con Elasticsearch.

# librerias utilizadas
<A HREF="https://huggingface.co/bert-base-uncased">BERT: </A> es un modelo de representación de lenguaje, que significa Representaciones de codificador bidireccional de Transformers. Está diseñado para entrenar representaciones bidireccionales profundas a partir de texto sin etiquetar a través de una capa contextual, que se compone de capas de atención apiladas y redes de retroalimentación con incorporaciones de entrada y salida de la secuencia.
<p></p>
<A HREF="https://pytorch.org/"> Pytorch: </A>   es una biblioteca de tensores optimizada para el aprendizaje profundo mediante GPU y CPU, proporciona dos funciones de alto nivel: Cálculo de tensor (como NumPy) con fuerte aceleración de GPU y Redes neuronales profundas construidas en un sistema de autogrado basado en cintas.
<p></p>
<A HREF="https://haystack.deepset.ai/overview/intro">Haystack: </A>  Es un framework de Python para el desarrollo de sistemas de búsqueda en grandes colecciones de documentos, está disponible como una biblioteca de código abierto que proporciona diferentes aplicaciones entra las que destaca la recuperación de respuestas a preguntas.
<p></p>
<A HREF="https://fastapi.tiangolo.com/">FastAPI: </A> Se trata de un framework que permite construir APIs (Application Programming Interfaces o Interfaz de programación de aplicaciones) de forma rápida con Python, con la finalidad intercambiar datos entre los distintos módulos de un sistema.
<p></p>
<A HREF="https://www.elastic.co/es/">Elasticserch: </A> es un motor de búsqueda y recuperación de documentos de tipo JSON basado en Apache Lucene, el cual permite realizar búsquedas por una gran cantidad de datos de un texto específico.
<p></p>
<A HREF="https://streamlit.io/">Streamlit: </A> Es un framework de creación de aplicaciones de código abierto y gratuito creado para proyectos de aprendizaje automático y ciencia de datos, esta herramienta basada en Python permite crear aplicaciones web en tiempo real mientras se va codificando, sin la necesidad de saber HTML o CSS, permite la integración de Bootstrap y crea una interfaz interactiva y amigable con los usuarios.

# Desarrollo

## Ajuste del modelo 
Para el afinado del modelo se utilizó la herramienta Google Colab, ya que permite la utilización de GPU’s con mejores características que las que se poseía. Cada archivo json de entrenamiento está estructurado con una serie de preguntas, respuestas, contexto, y la posición inicial de la respuesta en el contexto. (Los contextos se pueden repitir ya que pueden existir varias preguntas por contexto).
Primero, se obtiene la posición de la respuesta en el pasaje (se nos da la posición inicial en el json) y con ella calculamos la posición final de la respuesta.
 ![image](https://user-images.githubusercontent.com/33547749/159567671-47c105d7-3b39-48ed-9bc7-19e735f6544d.png)

A continuación, debemos convertir las posiciones de inicio y fin de la respuesta en posiciones de inicio y fin de token.
 ![image](https://user-images.githubusercontent.com/33547749/159567689-b2da3a20-994e-4775-b6c4-b48fb63408bd.png)

Se colocan los datos en conjunto de datos de PyTorch para poder usarlos fácilmente para el entrenamiento.
 ![image](https://user-images.githubusercontent.com/33547749/159567700-e545c218-ee1f-44fd-a357-8e91596b94f6.png)

Finalmente se realiza el entrenamiento y se procede a guardar el modelo entrenado.
 ![image](https://user-images.githubusercontent.com/33547749/159567709-064b4cc9-d733-4447-a937-ceb06f1a797b.png)




## Arquitectura del Agente
La arquitectura fue destinada para implementarla en una aplicación web en donde se emplearon las plataformas de Microsoft Azure y Google Cloud junto herramienta Docker con los contenedores que almacenaron cada módulo del sistema para su desarrollo y posterior levantamiento web, gracias a que permite exponer hacia el exterior cualquier servicio web local que haya desarrollado como en este caso, además permite especificar en qué puerto realizar la conexión al servicio de Streamlit (puerto 9200), FastAPI (puerto 8080) y Streamlit y así facilitar el acceso al modelo ajustado desde cualquier navegador web.

<div align="center">
	 <img src ="https://user-images.githubusercontent.com/33547749/159567740-783793af-ef01-4b1c-9b97-0c7167266b69.png" scale="750" height="350" />
</div>
 
La arquitectura como se manifiesta en la Ilustración anterior, en la cual se observar el funcionamiento e interacciones entre los componentes empleados en el desarrollo del agente conversacional. Los elementos principales, están distinguidos entre Usuario y el conjunto de todo el sistema que está almacenado en contenedores y estos son administrados desde la nube por los servicios de Microsoft Azure y Google Cloud que hacen de hospedadores para los tres contenedores en los que se divide el sistema.

## Base de conocimiento
Para la elaboración del conjunto de datos se realizó un preprocesamiento del conjunto de datos CORD-19, ya que cuenta con un total aproximado de un millón de artículos y trabajar con esta basta cantidad de datos generaría cuellos de botella en el procesamiento del sistema. Por lo cual se prepararon aproximadamente cincuenta mil artículos procedentes de bases de datos científicas y medicas como lo son Sciencedirect, Elsevier, NCBI (National Center for Biotechnology Information) y PuMed; donde se funcionaron en un conjunto de datos en el cual se extrajeron diferentes campos como son: sha, title, abstract, publish_time, authors, url, body_text, con los que se creó un dataframe de todos los trabajos de investigación necesarios para poder buscar en ellos, todo este proceso se puede observar en los archivos .ipynb, CreacionLimpiezaDataset y PreprocesamientoDatos en la carpeta Base de conocimiento.
Para la creación del contenedor Docker se utilizó un contenedor elasticsearch, a continuación, se presentan los comandos utilizados.

<div align="center">
	 <img src ="https://user-images.githubusercontent.com/33547749/159567754-8f723663-b81b-479c-8c22-a180a7a56875.png" width="700" height="150" />
</div>

Luego se realiza la conexión con el contenedor y se agregan los documentos.

<div align="center">
	 <img src ="https://user-images.githubusercontent.com/33547749/159567770-df6d701e-87d3-4e48-8636-471cf7bf8d9f.png" width="700" height="400" />
</div>


## Creación de la API
La creación de la API se la realizó mediante el framework FastAPI, aquí se realizó la conexión con el contenedor de ElasticSearch y luego mediante la librería Haystack se logró obtener la respuesta a la pregunta. Posteriormente el api fue agregado a un contenedor de Docker para facilitar su uso.

<div align="center">
	 <img src ="https://user-images.githubusercontent.com/33547749/159567786-0a18b0f0-296e-4e66-9b54-33e487f029ed.png" width="550" height="550" />
</div>



## Interfaz
Finalmente se codifico la parte de la interfaz, la cual se la codifico con la librería Streamlit, se realizó la conexión con el contenedor del api y se agregaron los campos necesarios para su funcionamiento, los cuales le permiten al usuario realizar una pregunta al agente y elegir el numero de respuestas que desea obtener. 

<div align="center">
	 <img src ="https://user-images.githubusercontent.com/33547749/159361179-e5cae02e-8a26-42cc-acb7-e1c4a0401e1f.png" width="600" height="350" />
</div>

El resultado final de este proyecto lo puede ver <A HREF="https://streamlittesis-m36rwfdc5q-uc.a.run.app/"> aqui. </A>
