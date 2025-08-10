import requests

class GoogleSearch:
    def __init__(self,api_key,engine_id):
        """
        Inicializa Google Search

        Permite automatizar las busquedas a la API de google

        Args:
            api_key (str)= la api de google
            engine_id (str) = ID del motor de busqueda de google
        """
        self.api_key = api_key
        self.engine_id = engine_id
    def search(self,query,start_page=1,pages=1,lang ="lang_es"):
        """
        Realiza busqueda en google con su API

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
            URL =f"https://www.googleapis.com/customsearch/v1?key={self.api_key}&cx={self.engine_id}&q={query}&start={start_index}&lr={lang}"
            response = requests.get(URL) # comprovem si correcta 200 = OK
            if response.status_code == 200:
                data = response.json()
                results = data.get("items")
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