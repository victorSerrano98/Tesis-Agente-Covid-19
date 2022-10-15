<p align="center"><img src="https://user-images.githubusercontent.com/33547749/195964318-e2ebf200-8881-4448-8be5-d2475b88c6fd.png"/></p> 



## Tabla de contenidos:
---
- [Autores](#autores)
- [Introducción](#introduccion)
- [Desarrollo:](#desarrollo)
  - [Ajuste del modelo](#ajuste-del-modelo)
  - [Base de conocimiento](#base-de-conocimiento)
  - [Arquitectura del Agente](#arquitectura-del-agente)
  - [Creación de la API](#creación-de-la-api)
  - [Interfaz](#interfaz)
- [Guía de instalación](#guía-de-instalación)
- [Guía de usuario](#guía-de-usuario)
- [Información adicional](#información-adicional)

## Autores
---
El presente Trabajo de Titulación fue desarrollado por:
-   Victor Yamil Serrano Zari - victor.serrano@unl.edu.ec
-   José Alexis Carrión Ojeda - jose.a.carrion.o@unl.edu.ec<br/>

## Introduccion
---
El presente repositorio almacena los archivos utilizados para el desarrollo del trabajo de titulacion "Agente virtual para brindar asistencia acerca del Covid-19", se encuentra divido en carpetas en las cuales se pueden encontrar los archivos que fueron necesarios para el ajuste de modelo BERT, la creacion de la base conocimientos utilizando Elasticsearch, la API con ayuda del framework FastApi y la interfaz desarrollada con Streamlit, bajo el lenguaje Python junto a Pytorch.

## Desarrollo
---
El objetivo del Agente Conversacional es dar Respuestas a preguntas relacionadas con el Covid-19, con el fin de solventar las dudas respecto al virus y permitir el acceso a una información plena y confiable, obtenida de documentos cientificos empleando el procesamiento de lenguaje natural (PNL), junto al modelo de lenguaje BERT el cual fue ajustado al ambito del coronavirus para poder rescatar información de los diversos documentos que contienen información.

- ## Ajuste del modelo
---
Para el afinado del modelo se utilizó la herramienta Google Colab, ya que permite la utilización de GPU’s con mejores características que las que se poseía. Cada archivo json de entrenamiento está estructurado con una serie de preguntas, respuestas, contexto, y la posición inicial de la respuesta en el contexto. (Los contextos se pueden repitir ya que pueden existir varias preguntas por contexto).
Primero, se obtiene la posición de la respuesta en el pasaje (se nos da la posición inicial en el json) y con ella calculamos la posición final de la respuesta.

 ![image](https://user-images.githubusercontent.com/33547749/159567671-47c105d7-3b39-48ed-9bc7-19e735f6544d.png) <br/>

A continuación, debemos convertir las posiciones de inicio y fin de la respuesta en posiciones de inicio y fin de token.
 ![image](https://user-images.githubusercontent.com/33547749/159567689-b2da3a20-994e-4775-b6c4-b48fb63408bd.png) <br/>

Se colocan los datos en conjunto de datos de PyTorch para poder usarlos fácilmente para el entrenamiento.
 ![image](https://user-images.githubusercontent.com/33547749/159567700-e545c218-ee1f-44fd-a357-8e91596b94f6.png)<br/>

Finalmente se realiza el entrenamiento y se procede a guardar el modelo entrenado.
 ![image](https://user-images.githubusercontent.com/33547749/159567709-064b4cc9-d733-4447-a937-ceb06f1a797b.png)

- ## Arquitectura del Agente
---
La arquitectura fue destinada para implementarla en una aplicación web en donde se emplearon las plataformas de Microsoft Azure y Google Cloud junto herramienta Docker con los contenedores que almacenaron cada módulo del sistema para su desarrollo y posterior levantamiento web, gracias a que permite exponer hacia el exterior cualquier servicio web local que haya desarrollado como en este caso, además permite especificar en qué puerto realizar la conexión al servicio de Streamlit (puerto 9200), FastAPI (puerto 8080) y Streamlit y así facilitar el acceso al modelo ajustado desde cualquier navegador web.

<div align="center">
	 <img src ="https://user-images.githubusercontent.com/33547749/188732620-5c4b19d0-0341-43e1-807a-d7c017d1e160.jpg" scale="750" height="350" />
</div>
 
La arquitectura como se manifiesta en la Ilustración anterior, en la cual se observar el funcionamiento e interacciones entre los componentes empleados en el desarrollo del agente conversacional. Los elementos principales, están distinguidos entre Usuario y el conjunto de todo el sistema que está almacenado en contenedores y estos son administrados desde la nube por los servicios de Microsoft Azure y Google Cloud que hacen de hospedadores para los tres contenedores en los que se divide el sistema.

- ## Base de conocimiento
---
Para la elaboración del conjunto de datos se realizó un preprocesamiento del conjunto de datos CORD-19, ya que cuenta con un total aproximado de un millón de artículos y trabajar con esta basta cantidad de datos generaría cuellos de botella en el procesamiento del sistema. Por lo cual se prepararon aproximadamente cincuenta mil artículos procedentes de bases de datos científicas y medicas como lo son Sciencedirect, Elsevier, NCBI (National Center for Biotechnology Information) y PuMed; donde se funcionaron en un conjunto de datos en el cual se extrajeron diferentes campos como son: sha, title, abstract, publish_time, authors, url, body_text, con los que se creó un dataframe de todos los trabajos de investigación necesarios para poder buscar en ellos, todo este proceso se puede observar en los archivos .ipynb, CreacionLimpiezaDataset y PreprocesamientoDatos en la carpeta Base de conocimiento.
Para la creación del contenedor Docker se utilizó un contenedor elasticsearch, a continuación, se presentan los comandos utilizados.

<div align="center">
	 <img src ="https://user-images.githubusercontent.com/33547749/159567754-8f723663-b81b-479c-8c22-a180a7a56875.png" width="700" height="150" />
</div>

Luego se realiza la conexión con el contenedor y se agregan los documentos.

<div align="center">
	 <img src ="https://user-images.githubusercontent.com/33547749/159567770-df6d701e-87d3-4e48-8636-471cf7bf8d9f.png" width="700" height="400" />
</div>

- ## Creación de la API
---
La creación de la API se la realizó mediante el framework FastAPI, aquí se realizó la conexión con el contenedor de ElasticSearch y luego mediante la librería Haystack se logró obtener la respuesta a la pregunta. Posteriormente el api fue agregado a un contenedor de Docker para facilitar su uso.

<div align="center">
	 <img src ="https://user-images.githubusercontent.com/33547749/159567786-0a18b0f0-296e-4e66-9b54-33e487f029ed.png" width="550" height="550" />
</div>

- ## Interfaz
---
Finalmente se codifico la parte de la interfaz, la cual se la codifico con la librería Streamlit, se realizó la conexión con el contenedor del api y se agregaron los campos necesarios para su funcionamiento, los cuales le permiten al usuario realizar una pregunta al agente y elegir el numero de respuestas que desea obtener. 

<div align="center">
	 <img src ="https://user-images.githubusercontent.com/33547749/188732165-489503d7-a4d0-403d-b897-793c42917395.png" width="600" height="350" />
</div>

El resultado final de este proyecto lo puede ver <A HREF="http://34.171.25.128:8080/"> aqui. </A>

 	
## Guía de instalación
---
Para comenzar con la instalación del software se recomienda emplear Docker para un despliegue rápido y adecuado, además de una GPU Nvidia mayor a 4 GB de RAM, almacenamiento mínimo de 7 GB y memoria RAM mayor a 6 GB.
<br/>

Para la creación de las imágenes Docker se debe ingresar a la carpeta a través del terminal y ejecutar el archivo setuo.sh mediante el comando: <br/>
- sh setup.sh <br/>

Y una vez terminada la creación de la imagen dependiendo de cuál sea se ejecutarán los siguientes comandos: <br/>
- Iniciar imagen de la base de conocimiento Elasticsearch, en el puerto 9200. <br/>
	- docker run -p 9200:9200 (imagenid) <br/>

- Iniciar imagen del API, en el puerto 85. <br/>
	- ldocker run --gpus all -p 85:8080 -e es_ip='172.17.0.1' -e es_port=9200 (imagenid) <br/>
 		- es_ip y es_port: son el ip y puerto del contenedor de la base de conocimiento. <br/>
 
- Iniciar imagen de la interfaz  <br/>
	- docker run -p 80:8080 -e qa_ip='172.17.0.1' -e qa_port=85  (imagenid) <br/>
 		- es_ip y es_port: son el ip y puerto del contenedor del API. <br/>


## Guía de usuario
---
El Agente Conversacional Covid-19, se carácteriza por tener un menú desplegable superior en la parte izquierda, el cúal ofrece una sección de "Opciones", que se compone de:  <br/>

Selección del tipo de búsqueda: 
  - Normal: Esta búsqueda se realiza en dentro de todos los documentos de la base de conocimiento y extrae los 5 documentos con mayor coincidencia en base a los contextos de la pregunta realizada y devuelve el la mejor respuesta junto con su contexto de donde fue extraida gracias al modelo ajustado. Está búsqueda es más superficial pero ofrece buenas respuestas y en un tiempo relativamente corto.
  - Avanzada: Esta búsqueda se realiza en dentro de todos los documentos de la base de conocimiento y extrae los 10 documentos con mayor coincidencia en base a los contextos de la pregunta realizada y devuelve el la mejor respuesta junto con su contexto de donde fue extraida gracias al modelo ajustado. Está búsqueda es más profunda al buscar en el doble de documentos, pero el tiempo de procesamiento es mayor acorde al número de documentos que se procesan.  <br/>

Selección del idioma: 
\* Cabe mencionar que el modelo trabaja bajo el idioma inglés y para poder tomar y ofrecer respuestas en español se empleó una libreria para la traducción. *
  - Español: Se traducen las preguntas y respuestas, al emplear una libreria la traducción puede dar lugar a sesgos.
  - Inglés: Ofrece respuestas en este idioma, las cuales son obtenidas directamente de los documentos científicos consultados. 
  - Información del Agente:  Se describe brevemente el funcionamiento y el enlace al repositorio del proyecto de titulación. <br/>

Página principal:
  - Cuadro de búsqueda: para poder introduccir las preguntas relacionadas con el Covid-19.
  - Cuadro de resultado: expone la respuesta encontrada.

## Información adicional
---
CORD-19: https://github.com/allenai/cord19 <br/>
Haystack: https://github.com/deepset-ai/haystack <br/>
ElasticSearch: https://www.elastic.co/es/ <br/>
Docker: https://www.docker.com/ <br/>

Las Tecnologías y Herramientas utilizadas fueron:
 - Plataforma de Microsoft Azure
 - Plataforma de Google Cloud
 - Plataforma de Google Colaboratory
 - Sistema Operativo Centos 7
 - Lenguaje de Programación Pyhton versión > 3.6
 - Gestor de Base de Datos: ElasticSearch
 - Framework Haystack
 - Framework Pytorch
 - Framework Streamlit
<br/>
