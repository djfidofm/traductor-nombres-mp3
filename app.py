import streamlit as st
from deep_translator import GoogleTranslator
import os
import zipfile
import io

st.title("🎧 Traductor de MP3 a ZIP")
st.write("Sube tus archivos MP3, traduciremos sus nombres al español y te entregaremos un único archivo ZIP con todos ellos.")

archivos_subidos = st.file_uploader(
    "Selecciona tus archivos MP3", 
    type=['mp3'], 
    accept_multiple_files=True
)

if archivos_subidos:
    st.subheader("Procesando archivos...")
    
    # 1. Crear un espacio en la memoria para el archivo ZIP
    zip_buffer = io.BytesIO()
    
    # 2. Abrir el archivo ZIP en modo escritura
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        
        for archivo in archivos_subidos:
            nombre_original, extension = os.path.splitext(archivo.name)
            
            try:
                # Traducir el nombre
                traductor = GoogleTranslator(source='en', target='es')
                nombre_traducido = traductor.translate(nombre_original)
                nuevo_nombre_archivo = f"{nombre_traducido}{extension}"
                
                # Mostrar en pantalla el cambio para que veas el progreso
                st.write(f"✅ `{archivo.name}` ➡️ `{nuevo_nombre_archivo}`")
                
                # 3. Guardar el audio dentro del ZIP con el nuevo nombre
                zip_file.writestr(nuevo_nombre_archivo, archivo.getvalue())
                
            except Exception as e:
                st.error(f"Hubo un error al traducir '{archivo.name}': {e}")
    
    st.markdown("---")
    st.success("¡Todos los archivos han sido procesados y empaquetados!")
    
    # 4. Botón único para descargar el ZIP completo
    st.download_button(
        label="📦 Descargar todos en un ZIP",
        data=zip_buffer.getvalue(),
        file_name="audios_traducidos.zip",
        mime="application/zip"
    )
