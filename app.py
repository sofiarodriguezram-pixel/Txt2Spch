import streamlit as st
import os
import time
import glob
from gtts import gTTS
from PIL import Image
import base64

# ==============================
# Estilo visual tipo libro
# ==============================
st.markdown("""
    <style>
    /* Fondo tipo papel envejecido */
    .stApp {
        background: radial-gradient(circle at center, #f8f1e1 0%, #e6dcc2 100%);
        color: #3e2f1c;
        font-family: "Georgia", serif;
    }

    /* Títulos cursivos tipo libro */
    h1, h2, h3 {
        font-family: "Georgia", serif;
        font-style: italic;
        color: #3b2f1e;
        text-shadow: 1px 1px 2px rgba(80,60,30,0.2);
    }

    /* Quitar recuadro blanco superior y bordes */
    [data-testid="stDecoration"], 
    [data-testid="stHeader"],
    [data-testid="stToolbar"], 
    [data-testid="stStatusWidget"],
    [data-testid="stAppHeader"],
    [data-testid="stFileUploaderDropzone"] {
        background: none !important;
        box-shadow: none !important;
        border: none !important;
    }

    /* Estilo para el área de texto */
    [data-baseweb="textarea"] {
        background-color: rgba(255, 250, 230, 0.6) !important;
        border: 1px solid #d1b48c !important;
        border-radius: 10px !important;
        color: #3e2f1c !important;
        font-family: "Georgia", serif !important;
    }

    /* Botones suaves tipo libro */
    button[kind="primary"] {
        background-color: #d4b483 !important;
        color: #3e2f1c !important;
        border-radius: 10px !important;
        font-family: "Georgia", serif !important;
        border: 1px solid #c4a46a !important;
    }

    /* Quitar fondos blancos residuales */
    section[data-testid="stSidebar"], 
    section[data-testid="stMain"] {
        background: transparent !important;
    }

    /* Imagen centrada con borde suave */
    img {
        border-radius: 12px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.15);
    }

    /* Subtítulos estilo libro */
    .stMarkdown p {
        font-size: 1.05rem;
        color: #3f3324;
        text-align: justify;
    }
    </style>
""", unsafe_allow_html=True)

# ==============================
# App principal
# ==============================

st.title("Conversión de Texto a Audio")

image = Image.open('gato_raton.png')
st.image(image, width=350)

with st.sidebar:
    st.subheader("Escribe o selecciona texto para escuchar.")

try:
    os.mkdir("temp")
except:
    pass

st.subheader("Una pequeña Fábula.")
st.write('¡Ay! -dijo el ratón-. El mundo se hace cada día más pequeño. Al principio era tan grande que le tenía miedo. '  
         'Corría y corría y por cierto que me alegraba ver esos muros, a diestra y siniestra, en la distancia. ' 
         'Pero esas paredes se estrechan tan rápido que me encuentro en el último cuarto y ahí en el rincón está '  
         'la trampa sobre la cual debo pasar. Todo lo que debes hacer es cambiar de rumbo dijo el gato... y se lo comió. ' 
         '—Franz Kafka.'
        )

st.markdown("¿Quieres escucharlo? Copia o escribe el texto:")

text = st.text_area("Ingrese el texto a escuchar.")

option_lang = st.selectbox(
    "Selecciona el lenguaje",
    ("Español", "English"))

lg = 'es' if option_lang == "Español" else 'en'

def text_to_speech(text, lg):
    tts = gTTS(text, lang=lg)
    try:
        my_file_name = text[0:20]
    except:
        my_file_name = "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, text

if st.button("Convertir a Audio"):
    result, output_text = text_to_speech(text, lg)
    audio_file = open(f"temp/{result}.mp3", "rb")
    audio_bytes = audio_file.read()
    st.markdown("## Tu audio:")
    st.audio(audio_bytes, format="audio/mp3", start_time=0)

    with open(f"temp/{result}.mp3", "rb") as f:
        data = f.read()

    def get_binary_file_downloader_html(bin_file, file_label='File'):
        bin_str = base64.b64encode(data).decode()
        href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Descargar {file_label}</a>'
        return href
    st.markdown(get_binary_file_downloader_html("audio.mp3", file_label="Audio"), unsafe_allow_html=True)

def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)

remove_files(7)
