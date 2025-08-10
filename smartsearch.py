import os
import re
import argparse
from transformers import GPT2Tokenizer
from openai import OpenAI
from dotenv import load_dotenv
from docx_reader import leer_archivo_contenido




class SmartSearch:
    """Clase que permite realizar búsquedas en archivos de un directorio mediante expresiones regulares.

    Attributes:
        dir_path (str): La ruta del directorio donde se encuentran los archivos.
        files (dict): Diccionario que contiene el nombre de cada archivo y su contenido como clave y valor respectivamente.
    """

    def __init__(self, dir_path):
        """Inicializa la clase SmartSearch.

        Args:
            dir_path (str): Ruta del directorio donde se realizarán las búsquedas.
        """
        self.dir_path = dir_path
        self.files = self._read_files()

    def _read_files(self):
        """Lee los archivos de un directorio y guarda su contenido en un diccionario.

        Returns:
            dict: Diccionario donde cada clave es el nombre de un archivo y cada valor es su contenido.
        """
        files = {}
        # Iterar sobre todos los archivos en el directorio especificado
        for archivo in os.listdir(self.dir_path):
            file_path = os.path.join(self.dir_path, archivo)
            try:
                contenido = leer_archivo_contenido(file_path)
                files[archivo] = contenido
            except Exception as e:
                print(f"Error al leer el archivo {file_path}: {e}")
        return files

    def regex_search(self, regex):
        """Realiza una búsqueda utilizando una expresión regular en todos los archivos del directorio.

        Args:
            regex (str): La expresión regular utilizada para la búsqueda.

        Returns:
            dict: Un diccionario donde cada clave es un archivo y cada valor es una lista de coincidencias encontradas.
        """
        coincidencias = {}
        for file, text in self.files.items():
            respuesta = ""
            while respuesta not in ("y", "n", "yes", "no"):
                respuesta = input(f"El archivo {file} tiene una longitud de {len(text)} caracteres, ¿seguro que deseas continuar? (y/n): ")
            if respuesta in ("n", "no"):
                continue
            matches = re.findall(regex, text, re.IGNORECASE)
            if matches:
                coincidencias[file] = matches
        return coincidencias
    
    def ia_search(self, prompt, model_name='gpt-3.5-turbo-0125', max_tokens=100):
        """
        Realiza busquedas en ficheros con IA
        """
        coincidencias = {}
        for file, text in self.files.items():
            respuesta = ""
            tokens, coste = self._calcular_coste(text, prompt, model_name, max_tokens)
            while respuesta not in ("y", "yes", "n", "no"):
                respuesta = input(f"El fichero {file} tiene una longitud de {tokens} tokens (aprox. {coste}$). Quieres continuar? (y/n))")
            if respuesta in ("n", "no"):
                continue
            # Divimos el fichero en segmentos, no nos deja pasarle mas de 16k tokens
            file_segments = self._split_file(text, model_name)

            # Inicializamos el cliente de openAI
            load_dotenv()
            client = OpenAI()
            resultados_segmentos = []
            # Enumerate para que me enseñe el index
            for index, segment in enumerate(file_segments):
                print(f"Procesando el segmento {index + 1}/{len(file_segments)}...")
                chat_completion = client.chat.completions.create(
                    messages =[
                    {
                        "role": "user",
                        "content": f"{prompt}\n\nTexto:\n{segment}",
                    }
                    ],
                    model = model_name,
                    max_tokens = max_tokens,
                    n=1,
                )
                resultados_segmentos.append(chat_completion.choices[0].message.content)
            coincidencias[file] = resultados_segmentos
        return coincidencias


    def _split_file(self, file_text, model_name):

        context_window_sizes = {
            "gpt-4-0125-preview": 128000,
            "gpt-4-1106-preview": 128000,
            "gpt-4": 16000,
            "gpt-4-32k": 32000,
            "gpt-3.5-turbo-0125": 16000,
            "gpt-3.5-turbo-instruct": 4000
        }
        # Vamos desde 0 a la long del texto y hara saltos dependiendo del tamaño del context window. Por ejemplo de 0 a 16000 y asi sucesivamente sumando.
        return [file_text[i:i+context_window_sizes[model_name]]
                for i in range(0,len(file_text), context_window_sizes[model_name])]

    def _calcular_coste(self, text, prompt, model_name, max_tokens):
        """
        Calcula el coste para el model de OPENAI
        """
        # Precios por cada 1000 tokens
        precios = {
            "gpt-4-0125-preview": {"input_cost": 0.01, "output_cost": 0.03},
            "gpt-4-1106-preview": {"input_cost": 0.01, "output_cost": 0.03},
            "gpt-4-1106-vision-preview": {"input_cost": 0.01, "output_cost": 0.03},
            "gpt-4": {"input_cost": 0.03, "output_cost": 0.06},
            "gpt-4-32k": {"input_cost": 0.06, "output_cost": 0.12},
            "gpt-3.5-turbo-0125": {"input_cost": 0.0005, "output_cost": 0.0015},
            "gpt-3.5-turbo-instruct": {"input_cost": 0.0015, "output_cost": 0.002}
        }
        # Vemos tokens por texto
        tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        len_tokens_prompt = len(tokenizer.tokenize(prompt))
        len_token_text = len(tokenizer.tokenize(text))
        #Calc el coste
        input_cost = ((len_tokens_prompt + len_token_text) / 1000) * precios[model_name]["input_cost"]
        output_cost = (max_tokens / 1000) * precios[model_name]["output_cost"]
        return (len_token_text + len_tokens_prompt, input_cost + output_cost)
        