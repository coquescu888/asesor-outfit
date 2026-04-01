import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="AI Fashion Studio", page_icon="👕")

# 2. CONEXIÓN SEGURA (Usando lo que ya aprendimos)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ Falta la API Key en los Secrets de Streamlit.")
    st.stop()

# 3. INTERFAZ DE USUARIO
st.title("🧥 Tu Asesor de Imagen Personal")
st.markdown("Sube una foto de tu outfit y recibe una crítica constructiva.")

# BARRA LATERAL: TU CLÓSET REAL
st.sidebar.title("🎒 Mi Armario Digital")
mis_prendas = st.sidebar.text_area(
    "Escribe aquí las prendas que tienes (separadas por comas):",
    "Pantalón negro, Camisa blanca, Tenis blancos, Chaqueta de mezclilla, Botas café"
)

# SELECCIÓN DE EVENTO
evento = st.sidebar.selectbox(
    "¿A dónde vas?",
    ["Clases en la UNAM", "Cena formal", "Gimnasio", "Cita casual", "Trámite administrativo"]
)

# 4. CARGA DE LA FOTO
foto = st.file_uploader("Elige una foto de tu vestimenta...", type=["jpg", "jpeg", "png"])

if foto is not None:
    imagen = Image.open(foto)
    st.image(imagen, caption="Tu outfit actual", use_container_width=True)
    
    if st.button("✨ Analizar Estilo"):
       with st.spinner("La IA está revisando tu estilo..."):
            try:
                # El nombre más simple y compatible
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Enviamos la lista con el texto y la imagen
                response = model.generate_content([prompt, imagen])
                
                st.subheader("📋 Veredicto de la IA")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Error técnico: {e}")
                st.info("Si ves un 404, intenta refrescar la página en 1 minuto.")
        
        # EL PROMPT MÁGICO (Instrucciones para la IA)
        prompt = f"""
        Actúa como un experto en moda y colorimetría. 
        Analiza esta imagen de vestimenta para un contexto de: {evento}.
        
        1. Califica el outfit del 1 al 10.
        2. Analiza la combinación de colores y texturas.
        3. Basado en que el usuario tiene estas otras prendas: {mis_prendas}, 
           sugiere qué podría cambiar o añadir para mejorar el look.
        4. Sé honesto pero motivador, como un buen amigo con estilo.
        """
        
        with st.spinner("La IA está revisando tu estilo..."):
            try:
                # Enviamos la imagen junto con el texto
                response = model.generate_content([prompt, imagen])
                st.subheader("📋 Veredicto de la IA")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Hubo un error al procesar la imagen: {e}")
