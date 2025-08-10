import os
import requests

class FileDownloader:
    def __init__(self, directorio_destino):
        self.directorio = directorio_destino
        self.crear_directorio()

    def crear_directorio(self):
        if not os.path.exists(self.directorio):
            os.makedirs(self.directorio)
    
    def descargar_archivo(self, url):
        try:
            respuesta = requests.get(url)
            nombre_archivo = url.split("/")[-1] # nos quedamos con el ultimo valor de la URL, suele ser .pdf o .doc etc...
            ruta_completa = os.path.join(self.directorio, nombre_archivo) #tenemos la ruta, lo hacemos con el os para que varie dependiendo del sistema (wind/linux)
            # Guardamos el archivo en disco
            with open(ruta_completa,'wb',) as archivo:
                archivo.write(respuesta.content)
            print(f"Archivo {nombre_archivo} descargando en {ruta_completa}.")
        except Exception as e:
            print(f"Error al descargar el archivo {nombre_archivo}: {e}")

    def filtrar_descargar_archivos(self, urls, tipos_archivos = ["all"]): # por defecto descargamos todos los archivos
        if tipos_archivos == ["all"]: # Tiene que ser una lista pq en el main le pasamos como lista no como string
            for url in urls:
                self.descargar_archivo(url)
        else:
            for url in urls:
                if any(url.endswith(f".{tipo}") for tipo in  tipos_archivos):
                    self.descargar_archivo(url)
                