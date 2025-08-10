import os
from docx import Document

def leer_archivo_contenido(ruta_archivo):
    ext = os.path.splitext(ruta_archivo)[1].lower()
    try:
        if ext == ".docx":
            doc = Document(ruta_archivo)
            texto = []
            for para in doc.paragraphs:
                texto.append(para.text)
            return '\n'.join(texto)
        else:
            with open(ruta_archivo, "r", encoding="utf-8") as f:
                return f.read()
    except Exception as e:
        print(f"Error al leer el archivo {ruta_archivo}: {e}")
        return ""
