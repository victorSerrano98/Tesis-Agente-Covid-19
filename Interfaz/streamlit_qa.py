import streamlit as st
import requests, json
from annotated_text import annotated_text
import os
from googletrans import Translator
translator = Translator()
import time
import pandas as pd
import numpy as np

@st.cache
def classify(num):
    if num == 0:
        return 'setosa'
    else:
        return 'virginica'

def main():


    st.set_page_config(
        page_title="Agente Conversacional",
        page_icon="🧊",
    )
    col1, col2 = st.sidebar.columns([1,4])

    with col1:
        st.write(' ')

    with col2:
        st.image('unl_logo.png', width = 150)

    #new_title = '<p style="color:black; font-size: 45px;"><b>Agente Conversacional Covid-19</b></p>'
    #st.markdown(new_title, unsafe_allow_html=True)
    st.text("")
    st.text("")
    st.text("")
    st.text("")
    st.text("")
    st.text("")
    st.title('Agente Conversacional Covid-19')
    st.write("""---""")
    st.sidebar.header('Universidad Nacional de Loja')
    st.sidebar.write("""---""")


    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    header{visibility: hidden;}
    footer {visibility: hidden;}
    </style>

    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)




    
    st.sidebar.header("Opciones")
    #top_k_reader = st.sidebar.slider("Numero de Respuestas", min_value=1, max_value=10, value=1, step=1)
    #top_k_retriever = st.sidebar.slider("Numero de documentos", min_value=1, max_value=10, value=1, step=1)


    busqueda = st.sidebar.radio(
        "Seleccione el tipo de busqueda",
        ('Normal', 'Avanzada'), help="La busqueda avanzada se la realizará en un numero mayor de documentos")

    idioma = st.sidebar.radio(
        "Seleccione el idioma",
        ('Español', 'Ingles'),help="Idioma en el cual se enviará la pregunta y se devolverá la respuesta")


    question_es=st.text_input("Ingrese su pregunta", value="¿Cuáles son los síntomas del covid-19?", help="Recuerde formular de forma correcta su pregunta o podria obtener respuestas incorrectas")
    


    st.markdown(
        f"""
            <style>
            .stApp {{
                background-image: url("https://raw.githubusercontent.com/victorSerrano98/Tesis-Agente-Covid-19/main/Interfaz/tesisFondo.jpg");
                background-attachment: fixed;
                background-size: cover
            }}
            </style>
            """,
        unsafe_allow_html=True)

    
    if st.button('Aceptar'):
        st.text("")
        with st.spinner('\n Obteniendo Respuesta...'):
            q = question_es.split()
            if(not len(q)>1):
                st.error("Ingrese una pregunta")
            else:
                if idioma == 'Español':
                    question = translator.translate(question_es, 'en')
                    question = question.text
                else:
                    question = question_es

                if busqueda == 'Normal':
                    top_k_reader = 1
                    top_k_retriever = 5
                else:
                    top_k_reader = 1
                    top_k_retriever = 10
                print(idioma)
                print(busqueda)
                print(question)
                headers = {
                    'accept': 'application/json',
                    'Content-Type': 'application/json',
                }
                data = {
                    'question': question, 'num_answers': top_k_reader, 'num_docs': top_k_retriever
                }

                try:
                    # response = requests.post(f'https://fastapitesis-m36rwfdc5q-uc.a.run.appd/query', headers=headers, data=json.dumps(data))
                    response = requests.post(f'http://20.241.200.117:8080/query', headers=headers, data=json.dumps(data))
                    result = response.json()
                    print(result)
                    for each in result['answer']['answers']:
                        title = each['meta']['title']
                        url = each['meta']['url'].split(';')[0]
                        tokens = []
                        if idioma == 'Español':
                            
                            respuesta = translator.translate(each['context'][:each['offset_start']-1], dest='es')
                            tokens.append(respuesta.text)
                            respuesta = translator.translate(each['context'][each['offset_start']:each['offset_end']], dest='es')
                            tokens.append((respuesta.text,'Respuesta', '#BAF2A2'))
                            resp = respuesta.text
                            respuesta = translator.translate(each['context'][each['offset_end']:], dest='es')
                            tokens.append(respuesta.text)
                            
                        else:
                            tokens.append(each['context'][:each['offset_start']-1])
                            tokens.append((each['context'][each['offset_start']:each['offset_end']],'answer', '#BAF2A2'))
                            tokens.append(each['context'][each['offset_end']:])
                            resp = each['context'][each['offset_start']:each['offset_end']]                       

                        col1,col2 = st.columns([5,1])
                        col1.markdown(f'<span style="font-size: 16; font-weight:bold;">{title}   </span><a href={url} target="_blank" ><u>  Link </u></a>', unsafe_allow_html=True)
                        #col2.markdown(f'<input type="button" value="Confianza: {int(each["score"])}">', unsafe_allow_html=True)
                        st.text("")
                        col1, col2 = st.columns([3,3])
                        col1.markdown(f'<span style="font-size: 16; font-weight:bold;">Fecha de Publicacion: {each["meta"]["publish_time"]}\
                                    <br>Autores: {each["meta"]["authors"]}</span>', unsafe_allow_html=True)
                        
                        st.markdown(f'<span style="font-size: 16; font-weight:bold;">Respuesta:</span> {resp}',unsafe_allow_html=True)
                        st.markdown(f'<span style="font-size: 16; font-weight:bold;">Contexto:</span>',unsafe_allow_html=True)
                        annotated_text(*tokens)
                        st.text("")
                        st.text("")
                    
                except:
                    
                    col1,col2 = st.columns([5,1])
                    st.error("Ha ocurrido un error, vuelva a intentarlo")
                    st.text("")
                    col1, col2 = st.columns([2,4])

    st.sidebar.text("")
    st.sidebar.text("")
    st.sidebar.text("")
    st.sidebar.text("")
    st.sidebar.text("")
    st.sidebar.text("")
    st.sidebar.text("")
    with st.sidebar.expander("ℹ️ - Informacion del Agente", expanded=True):

        st.write(
            """     
    -   Agente conversacional para responder desarrollado con el modelo le lenguaje BERT, emplea NPL para obtener respuesta a preguntas tópicas del covid-19
    -   Código fuente: [Agente covid](https://github.com/victorSerrano98/AgenteVirtual_Covid).
            """
        )
    st.markdown("")

                
if __name__ == '__main__':
    main()

   
    

    