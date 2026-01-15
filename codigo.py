import streamlit as st
import json
import random 
from difflib import get_close_matches


st.set_page_config(page_title="El Oráculo Mágico", page_icon="🔮")
st.markdown("""
    <style>
    .main { background-color: #1a1a2e; color: #e94560; }
    h1 { text-align: center; color: #f9d342; font-family: 'serif'; }
    </style>
    """, unsafe_allow_html=True)

st.title("✨ EL ORÁCULO PREDICE TU FUTURO ✨")


MAPEO_TEMAS = {
    "Dinero": ["rico", "fortuna", "lotería", "billete", "millonario", "plata", "sueldo", "dinero", "monedas"],
    "Amor": ["novio", "novia", "pareja", "ligar", "casar", "cita", "enamorar", "crush", "amor"],
    "Trabajo": ["jefe", "empleo", "ascenso", "oficina", "currículum", "despido", "trabajo", "chamba"],
    "Belleza": ["look", "pelo", "flequillo", "guapo", "guapa", "espejo", "ropa", "estilo"],
    "Salud": ["morir", "vivir", "años", "enfermo", "dieta", "pizza", "arterias", "salud"]
}

def buscar_destino(query, datos):
    query = query.lower().strip()
    

    for categoria, palabras in MAPEO_TEMAS.items():
        if any(p in query for p in palabras):
            
            posibles_respuestas = [item['respuesta'] for item in datos if item['categoria'] == categoria]
            if posibles_respuestas:
                return random.choice(posibles_respuestas)

    preguntas_json = [item['pregunta'] for item in datos]
    match = get_close_matches(query, preguntas_json, n=1, cutoff=0.3)
    
    if match:

        categoria_detectada = next((item['categoria'] for item in datos if item['pregunta'] == match[0]), None)
        posibles_respuestas = [item['respuesta'] for item in datos if item['categoria'] == categoria_detectada]
        return random.choice(posibles_respuestas)
    
    return "El Oráculo está confundido... Las nubes tapan tu destino. Intenta preguntar sobre amor, dinero, trabajo o salud."

pregunta_usuario = st.text_input("Haz tu pregunta a la máquina del destino:", placeholder="¿Seré millonario?")

if st.button("Consultar a El Oráculo"):
    if pregunta_usuario:
        try:
            with open('respuestas.json', 'r', encoding='utf-8') as f:
                datos = json.load(f)
            
            with st.spinner('El Oráculo está consultando las estrellas...'):
                respuesta = buscar_destino(pregunta_usuario, datos)
                st.subheader(f"🔮 {respuesta}")
        except FileNotFoundError:
            st.error("No se encontró el archivo 'respuestas.json'")
    else:
        st.warning("El Oráculo no puede leer el silencio. Escribe una pregunta.")
