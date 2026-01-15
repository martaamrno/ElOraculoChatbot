import streamlit as st
import json
from difflib import get_close_matches

# Configuración estética
st.set_page_config(page_title="El Oráculo Mágico", page_icon="🔮")
st.markdown("""
    <style>
    .main { background-color: #1a1a2e; color: #e94560; }
    h1 { text-align: center; color: #f9d342; font-family: 'serif'; }
    </style>
    """, unsafe_allow_html=True)

st.title("✨ EL ORÁCULO PREDICE TU FUTURO ✨")

# --- DICCIONARIO DE SINÓNIMOS PARA PRECISIÓN ---
MAPEO_TEMAS = {
    "Dinero": ["rico", "fortuna", "lotería", "billete", "millonario", "plata", "sueldo"],
    "Amor": ["novio", "novia", "pareja", "ligar", "casar", "cita", "enamorar"],
    "Trabajo": ["jefe", "empleo", "ascenso", "oficina", "currículum", "despido"],
    "Belleza": ["look", "pelo", "flequillo", "guapo", "guapa", "espejo", "ropa"],
    "Salud": ["morir", "vivir", "años", "enfermo", "dieta", "pizza", "arterias"]
}

def buscar_destino(query, datos):
    query = query.lower()
    
    for categoria, palabras in MAPEO_TEMAS.items():
        for palabra in palabras:
            if palabra in query:
                for item in datos:
                    if item['categoria'] == categoria:
                        return item['respuesta']

    preguntas = [item['pregunta'] for item in datos]
    match = get_close_matches(query, preguntas, n=1, cutoff=0.2)
    if match:
        for item in datos:
            if item['pregunta'] == match[0]:
                return item['respuesta']
    
    return "El Oráculo está confundido... Tus palabras no están escritas en las estrellas. Prueba con temas de amor, dinero o salud."

# Interfaz
pregunta_usuario = st.text_input("Haz tu pregunta a la máquina del destino:")

if st.button("Consultar a El Oráculo"):
    if pregunta_usuario:
        with open('respuestas.json', 'r', encoding='utf-8') as f:
            datos = json.load(f)
        
        with st.spinner('El Oráculo está consultando las estrellas...'):
            respuesta = buscar_destino(pregunta_usuario, datos)
            st.subheader(f"🔮 {respuesta}")
    else:
        st.write("¡Introduce una pregunta primero!")