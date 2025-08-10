import requests

class DuckDuckGoSearch:
    def __init__(self,api_key):
        """
        Inicializa Duck Search

        Permite automatizar las busquedas a la API de duckduck

        Args:
            api_key (str)= la api de duckduck
        """
        self.api_key = api_key
    def search(self,query, engine="google",start_page=1,pages=1,lang ="lang_es"):
        """
        Realiza busqueda en duckduck con su API

        Args:
            query (str): consulta
            start_page (int): primera pagina
            pages (int): num de pags que queremos ver
            lang (str): idioma
        """
        final_results = []
        results_per_page = 10 # google muestra 10 results por pagina
        for page in range(pages):
            # Calcular el resultado de comienzo de cada pag
            start_index = (start_page - 1 )*results_per_page + 1 + (page * results_per_page)
            URL = f"https://serpapi.com/search?engine={engine}&q={query}&api_key={self.api_key}&kl={lang}&start={start_index}"
            response = requests.get(URL) # comprovem si correcta 200 = OK
            if response.status_code == 200:
                data = response.json()
                results = data.get("organic_results", []) # EN GOOGLE ES ITEMS, PERO EN DUCKDUCKGO ES organic_results
                cresults = self.custom_results(results)
                final_results.extend(cresults)
            else:
                print(f"ERROR obtenido al consultar la pagina: {page}: HTTP{response.status_code}")
                break # no volem que iteri si es erroni
        return final_results

    def custom_results(self,results):
        """
        Filtra resultats, nosaltres agafem titol, descripcio i link. Es podria agafar més coses

        Args:
            Results = el resultats de la consulta anterior
        """
        customs_results = []
        for r in results:
            cresult = {}
            cresult["title"] = r.get("title")
            cresult["descripcion"] = r.get("snippet")
            cresult["link"] = r.get("link")
            customs_results.append(cresult)
        return customs_results