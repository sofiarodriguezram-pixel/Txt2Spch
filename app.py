import streamlit as st
import os
import time
import glob
from gtts import gTTS
from PIL import Image
import base64

--- Estilo tipo libro antiguo ---

page_bg = """

<style> [data-testid="stAppViewContainer"] { background-color: #f5f0e6; background-image: radial-gradient(#e4d7c7 1px, transparent 1px); background-size: 20px 20px; font-family: "Georgia", serif; color: #3e2f1c; } [data-testid="stSidebar"] { background-color: #efe9dc; color: #3e2f1c; font-family: "Georgia", serif; } h1, h2, h3, h4 { font-family: "Palatino Linotype", "Book Antiqua", Palatino, serif; font-style: italic; color: #3e2f1c; text-align: center; } textarea, .stTextInput, .stSelectbox { border-radius: 8px !important; border: 1px solid #c1a97f !important; } div.block-container { padding-top: 2rem; padding-bottom: 2rem; border-left: 6px double #c1a97f; border-right: 6px double #c1a97f; background-color: #faf7f2; box-shadow: 0px 0px 20px rgba(160, 130, 90, 0.3); border-radius: 12px; } .stAudio { background-color: #f5f0e6; border-radius: 10px; padding: 5px; } a { color: #6b4a1d; font-weight: bold; text-decoration: none; } a:hover { color: #a67c3b; text-decoration: underline; } </style>

"""
st.markdown(page_bg, unsafe_allow_html=True)

--- Contenido principal ---

st.title("📖 Conversión de Texto a Audio")

image = Image.open("gato_raton.png")
st.image(image, width=300, caption="‘El gato y el ratón’ – Fábula corta")

with st.sidebar:
st.subheader("✍️ Escribe o selecciona texto para escuchar")

os.makedirs("temp", exist_ok=True)

st.subheader("Una pequeña fábula — Franz Kafka")
st.markdown("""
"¡Ay! —dijo el ratón—. El mundo se hace cada día más pequeño.
Al principio era tan grande que le tenía miedo. Corría y corría,
y me alegraba ver esos muros, a diestra y siniestra, en la distancia.
Pero esas paredes se estrechan tan rápido que me encuentro en el último cuarto,
y ahí en el rincón está la trampa sobre la cual debo pasar."
— Franz Kafka
""")

st.markdown("### 🎧 ¿Quieres escucharlo? Escribe o copia el texto:")

text = st.text_area("Texto a convertir en audio:")

option_lang = st.selectbox("Selecciona el idioma:", ("Español", "English"))
lg = "es" if option_lang == "Español" else "en"

def text_to_speech(text, tld, lg):
tts = gTTS(text, lang=lg)
file_name = text[:20] if text else "audio"
tts.save(f"temp/{file_name}.mp3")
return file_name

if st.button("📜 Convertir a Audio"):
if text.strip():
result = text_to_speech(text, "com", lg)
audio_file = open(f"temp/{result}.mp3", "rb")
audio_bytes = audio_file.read()
st.markdown("## 🔊 Tu audio:")
st.audio(audio_bytes, format="audio/mp3", start_time=0)
    with open(f"temp/{result}.mp3", "rb") as f:
        data = f.read()

    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{result}.mp3">⬇️ Descargar archivo de audio</a>'
    st.markdown(href, unsafe_allow_html=True)
else:
    st.warning("Por favor, ingresa un texto antes de convertir.")
def remove_files(n):
mp3_files = glob.glob("temp/*.mp3")
now = time.time()
n_days = n * 86400
for f in mp3_files:
if os.stat(f).st_mtime < now - n_days:
os.remove(f)

remove_files(7)
