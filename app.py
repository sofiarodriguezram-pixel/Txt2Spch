import streamlit as st
import os
import time
import glob
from gtts import gTTS
from PIL import Image
import base64

# --- ESTILOS DE LIBRO ---
st.markdown("""
    <style>
    body {
        background-color: #f5f1e6;
    }
    .book-wrapper {
        background-color: #fdf8e6;
        width: 85%;
        margin: 50px auto;
        padding: 50px 70px;
        border-radius: 15px;
        box-shadow: inset 0 0 20px rgba(0,0,0,0.1), 5px 5px 25px rgba(0,0,0,0.3);
        font-family: 'Georgia', serif;
        color: #3b2d1f;
        line-height: 1.8;
        text-align: justify;
        column-count: 2;
        column-gap: 70px;
        border-left: 8px solid #d2b48c;
        border-right: 8px solid #d2b48c;
    }
    .book-title {
        font-family: 'Cursive';
        font-size: 2.8em;
        text-align: center;
        color: #4b2e05;
        margin-bottom: 20px;
        column-span: all;
    }
    .book-subtitle {
        text-align: center;
        font-style: italic;
        color: #6b4a2b;
        margin-bottom: 20px;
        column-span: all;
    }
    .book-image {
        display: block;
        margin: 0 auto 25px auto;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        width: 260px;
        column-span: all;
    }
    .center {
        text-align: center;
        column-span: all;
    }
    </style>
""", unsafe_allow_html=True)

# --- INTERFAZ ---
with st.sidebar:
    st.subheader("Escribe o selecciona texto para escuchar.")

try:
    os.mkdir("temp")
except:
    pass

# --- CONTENIDO DEL LIBRO ---
st.markdown("<div class='book-wrapper'>", unsafe_allow_html=True)
st.markdown("<h1 class='book-title'>Conversión de Texto a Audio</h1>", unsafe_allow_html=True)

image = Image.open('gato_raton.png')
st.image(image, use_column_width=False, width=260)

st.markdown("<h3 class='book-subtitle'>Una pequeña Fábula</h3>", unsafe_allow_html=True)
st.markdown("""
<p>
¡Ay! —dijo el ratón—. El mundo se hace cada día más pequeño.  
Al principio era tan grande que le tenía miedo. Corría y corría y por cierto  
que me alegraba ver esos muros, a diestra y siniestra, en la distancia.  
Pero esas paredes se estrechan tan rápido que me encuentro en el último cuarto  
y ahí en el rincón está la trampa sobre la cual debo pasar.  
“Todo lo que debes hacer es cambiar de rumbo”, dijo el gato... y se lo comió.
</p>
<p class='center'><b>Franz Kafka</b></p>
""", unsafe_allow_html=True)

st.markdown("<hr style='margin-top:40px;margin-bottom:30px;'>", unsafe_allow_html=True)
st.markdown("<p class='center'><b>¿Quieres escucharlo? Copia o escribe el texto:</b></p>", unsafe_allow_html=True)

text = st.text_area("Ingrese el texto a escuchar:")

option_lang = st.selectbox(
    "Selecciona el idioma",
    ("Español", "English")
)
lg = 'es' if option_lang == "Español" else 'en'

def text_to_speech(text, tld, lg):
    tts = gTTS(text, lang=lg)
    try:
        my_file_name = text[0:20]
    except:
        my_file_name = "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, text

if st.button("Convertir a Audio"):
    result, output_text = text_to_speech(text, 'com', lg)
    audio_file = open(f"temp/{result}.mp3", "rb")
    audio_bytes = audio_file.read()
    st.markdown("<h3 class='center'>🎧 Tu audio:</h3>", unsafe_allow_html=True)
    st.audio(audio_bytes, format="audio/mp3", start_time=0)

    with open(f"temp/{result}.mp3", "rb") as f:
        data = f.read()

    def get_binary_file_downloader_html(bin_file, file_label='File'):
        bin_str = base64.b64encode(data).decode()
        href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}" style="color:#4b2e05;">Descargar {file_label}</a>'
        return href

    st.markdown(get_binary_file_downloader_html("audio.mp3", file_label="Archivo de Audio"), unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)

remove_files(7)
