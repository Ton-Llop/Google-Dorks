from dotenv import load_dotenv, set_key
from results_parser import ResultsParser
import os
from googlesearch import GoogleSearch
from duckduckgosearch import DuckDuckGoSearch
import argparse
import sys
from file_downloader import FileDownloader
from ai_agent import OpenAIGenerator, GPT4All_Generator, IAAgent
from smartsearch import SmartSearch
from docx import Document
from browserautosearch import BrowserAutoSearch

def env_config():
    """
    Configuar el .env con los valores proporcionados
    """
    search_engine = input("Introduce que engine quieres (duckduckgo/google):")
    set_key(".env","SEARCH_ENGINE",search_engine)
    hace_falta_configurar = input("Quieres configurar las APIS? (si/no)")
    if hace_falta_configurar == "si":
        if search_engine == "google":
            api_key_google = input("Introduce tu API KEY de Google:")
            engine_id = input("Introduce el ID del buscador de Google:")
            set_key(".env", "API_KEY_GOOGLE",api_key_google)
            set_key(".env", "SEARCH_ENGINE_ID",engine_id)
        elif search_engine =="duckduckgo":
            api_key_duckduckgo = input("Introduce tu API KEY de duckduckgo:")
            set_key(".env", "API_KEY_DUCKDUCKGO",api_key_duckduckgo)
        else:
            print("Escoge duckduckgo o google")
            sys.exit(1)
def openai_config():
    """
    Configura la OPEN_AI_KEY en el fichero .env, cada uno tiene una diferente.
    """
    api_key_gpt= input("Introduce la API KEY de OPENAI")
    set_key(".env","OPENAI_API_KEY",api_key_gpt)

def load_env(configure):
    #Comprovar si existe el .env
    env_exists = os.path.exists(".env")
    if not env_exists or configure:
        #CREAR O CONFIG .ENV
        env_config()
        print("Archivo .env configurado correctamente")
        sys.exit(1) # parar ejecucion del programa

    # Cargar .env
    load_dotenv()

    # Leer claves
    API_KEY_GOOGLE = os.getenv("API_KEY_GOOGLE")
    SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")
    API_KEY_DUCKDUCKGO = os.getenv("API_KEY_DUCKDUCKGO")
    SEARCH_ENGINE = os.getenv("SEARCH_ENGINE", "google")  # valor por defecto

    return (API_KEY_DUCKDUCKGO,API_KEY_GOOGLE,SEARCH_ENGINE_ID,SEARCH_ENGINE)

    
    

#MIRAR .ENV I CANVIAR SI ES GOOGLE O DUCKDUCKGO
def main(query, configure, start_page, pages, lang, output_json, output_html,
         download, gen_dork, smart_search_dir, regex, prompt,selenium,
         model="gpt-3.5-turbo-0125", max_tokens=100,):

    if gen_dork:
        #Preguntamos si quiere un modelo local o openai
        respuesta = ""
        while respuesta.lower() not in ("y","yes","no","n"):
            respuesta = input("Quieres utilizar GPT-4 de OpenAI (yes/no)?:")

        if respuesta.lower() in ("y", "yes"):
            #Comprobamos si esta definida la API key en el .env
            if not "OPENAI_API_KEY" in os.environ:
                openai_config()
                load_dotenv()
            # Generar el dork
            openai_generator = OpenAIGenerator()
            ia_agent = IAAgent(openai_generator)
        else:
            print("Utilizando gpt4all y ejecutando la generacion en local. Es un poco mas lento")
            gpt4all_generator = GPT4All_Generator()
            ia_agent = IAAgent(gpt4all_generator)
    
        respuesta = ia_agent.generate_gdork(gen_dork)
        print(f"\nResultado:\n {respuesta}")
        sys.exit(1)

    #if not query:
    #   print("Indica una consulta con el comando -q. Escribe -h para ayuda")
    #   sys.exit(1)

    if selenium:
        browser = BrowserAutoSearch()
        browser.search_google(query=query)
        resultados = browser.google_search_results()
        browser.quit()

    
    if query:
        API_KEY_DUCKDUCKGO, API_KEY_GOOGLE, SEARCH_ENGINE_ID, SEARCH_ENGINE= load_env(configure=configure)
        print(f"-------BUSQUEDA FETA AMB {SEARCH_ENGINE}------------")
        # Selección dinámica del motor
        if SEARCH_ENGINE.lower() == "google":
            gsearch = GoogleSearch(API_KEY_GOOGLE, SEARCH_ENGINE_ID)
            results = gsearch.search(query, pages=pages, start_page=start_page, lang=lang)
        elif SEARCH_ENGINE.lower() == "duckduckgo":
            duckducksearch = DuckDuckGoSearch(API_KEY_DUCKDUCKGO)
            results = duckducksearch.search(query, pages=pages, start_page=start_page, lang=lang)
        else:
            raise ValueError("Motor de búsqueda no reconocido. Usa 'google' o 'duckduckgo'.")

        rparser = ResultsParser(results)
        rparser.mostrar_pantalla()

        if output_html:
            rparser.exportar_html(output_html)

        if output_json:
            rparser.exportar_json(output_json)

        if download:
            # Separar extensiones de los archivos en una lista
            file_types = download.split(",")
            # Nos quedamos con las urls de los resultados obtenidos
            urls = [result['link'] for result in results]
            fdownloader = FileDownloader("Downloads")
            fdownloader.filtrar_descargar_archivos(urls, file_types)


    if smart_search_dir:
        searcher = SmartSearch(smart_search_dir)

        if regex:
            resultados = searcher.regex_search(regex)
            print("\n--- Resultados Regex ---")
            for file, matches in resultados.items():
                print(file)
                for m in matches:
                    print(f"\t- {m}")

        if prompt:
            resultados = searcher.ia_search(prompt, model_name=model, max_tokens=max_tokens)
            print("\n--- Resultados IA ---")
            for file, results in resultados.items():
                print(file)
                for r in results:
                    print(f"\t- {r}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Herramienta para búsquedas web y locales en ficheros")
    parser.add_argument("-q", "--query", type=str, help="Dork o consulta")
    parser.add_argument("-c", "--configure", action="store_true", help="Configurar .env")
    parser.add_argument("--start-page", type=int, default=1, help="Página de inicio")
    parser.add_argument("--pages", type=int, default=1, help="Número de páginas")
    parser.add_argument("--lang", type=str, default="lang_es", help="Idioma")
    parser.add_argument("--json", type=str, help="Exportar resultados en JSON")
    parser.add_argument("--html", type=str, help="Exportar resultados en HTML")
    parser.add_argument("--download", type=str, default="None", help="Descargar archivos (pdf,doc,sql,...)")
    parser.add_argument("-gd", "--generate-dork", type=str, help="Generar dork con IA")

    # --- ARGUMENTOS SMARTSEARCH ---
    parser.add_argument("--smart-search", type=str, help="Directorio donde buscar en ficheros")
    parser.add_argument("--regex", type=str, help="Expresión regular para SmartSearch")
    parser.add_argument("--prompt", type=str, help="Prompt para búsqueda IA en SmartSearch")
    parser.add_argument("--model", type=str, default="gpt-3.5-turbo-0125", help="Modelo IA")
    parser.add_argument("--max-tokens", type=int, default=100, help="Máx tokens IA")
    parser.add_argument("--selenium", action="store_true", default=False,
                        help="Utiliza selenium para realizar la busqueda con un navegador de manera automatica")

    args = parser.parse_args()

    main(query=args.query,
         configure=args.configure,
         start_page=args.start_page,
         pages=args.pages,
         lang=args.lang,
         output_json=args.json,
         output_html=args.html,
         download=args.download,
         gen_dork=args.generate_dork,
         smart_search_dir=args.smart_search,
         regex=args.regex,
         prompt=args.prompt,
         model=args.model,
         max_tokens=args.max_tokens,
         selenium=args.selenium)