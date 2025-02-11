import os
os.system("pip install git+https://github.com/openai/whisper.git")
os.system("pip install torch torchaudio")

import streamlit as st
import whisper
from docx import Document
import tempfile
from pathlib import Path
from time import sleep

# Configurare interfață
st.set_page_config(page_title="Transcriere Audio cu Whisper", layout="centered")
st.title("🎙️ Transcriere Audio folosind OpenAI Whisper")

# Incarcă modelul Whisper
@st.cache_resource
def load_whisper_model():
    return whisper.load_model("large")

model = load_whisper_model()

# Drag-and-drop pentru fișier audio
uploaded_file = st.file_uploader("Încarcă un fișier audio (MP3, WAV, etc.)", type=["mp3", "wav", "m4a", "ogg", "flac"])

if uploaded_file is not None:
    st.audio(uploaded_file, format="audio")
    
    # Salvăm temporar fișierul încărcat
    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
        tmp_file.write(uploaded_file.getbuffer())
        tmp_audio_path = tmp_file.name
    
    st.write("🔄 Procesare audio... Acest lucru poate dura câteva momente.")
    progress_bar = st.progress(0)
    
    # Simulare progres
    for percent in range(0, 101, 10):
        sleep(0.3)
        progress_bar.progress(percent)
    
    # Transcriere cu Whisper
    result = model.transcribe(tmp_audio_path, language="ro")
    transcribed_text = result["text"]
    
    # Afișare transcriere
    st.subheader("📜 Transcriere")
    st.text_area("Text transcris:", transcribed_text, height=200)
    
    # Salvare în Word
    doc_path = tempfile.NamedTemporaryFile(delete=False, suffix=".docx").name
    doc = Document()
    doc.add_paragraph(transcribed_text)
    doc.save(doc_path)
    
    # Oferire fișier pentru descărcare
    with open(doc_path, "rb") as doc_file:
        st.download_button("📥 Descarcă Transcrierea (Word)", doc_file, file_name="transcriere.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    
    # Curățare fișiere temporare
    os.remove(tmp_audio_path)
    os.remove(doc_path)
