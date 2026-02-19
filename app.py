import streamlit as st
from deep_translator import GoogleTranslator
import os

st.title("🎧 Traductor de Nombres para MP3")
st.write("Sube tus archivos MP3 con nombres en inglés y descárgalos exactamente igual, pero con el nombre traducido al español.")

archivos_subidos = st.file_uploader("Selecciona tus archivos MP3", type=['mp3'], accept_multiple_files=True)

if archivos_subidos:
    st.subheader("Archivos procesados:")
    for archivo in archivos_subidos:
        nombre_original, extension = os.path.splitext(archivo.name)
        try:
            traductor = GoogleTranslator(source='en', target='es')
            nombre_traducido = traductor.translate(nombre_original)
            nuevo_nombre_archivo = f"{nombre_traducido}{extension}"
            
            st.write(f"📄 **Original:** `{archivo.name}`  ➡️  **Nuevo:** `{nuevo_nombre_archivo}`")
            
            st.download_button(
                label=f"⬇️ Descargar {nuevo_nombre_archivo}",
                data=archivo.getvalue(),
                file_name=nuevo_nombre_archivo,
                mime="audio/mpeg",
                key=archivo.name # Llave única por botón
            )
            st.markdown("---")
        except Exception as e:
            st.error(f"Hubo un error al traducir '{archivo.name}': {e}")
