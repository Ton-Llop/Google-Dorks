## Google Dorks con Python
Este proyecto permite realizar búsquedas avanzadas en Google y DuckDuckGo utilizando técnicas conocidas como Google Dorks. Está pensado para ayudar en la ciberseguridad y en la búsqueda de información pública específica.

#¿Qué es un Google Dork?
Un Google Dork es una búsqueda avanzada que usa operadores especiales de Google para encontrar información que normalmente no es fácil de localizar, como archivos o datos sensibles expuestos accidentalmente.

# Archivos principales
googlesearch.py: busca en Google usando consultas personalizadas.

duckduckgosearch.py: busca en DuckDuckGo con parámetros especiales.

ninjadorks.py: genera y ejecuta listas de Google Dorks.

smartsearch.py: automatiza búsquedas avanzadas.

browserautosearch.py: controla el navegador para buscar y recopilar datos.

requirements.txt: dependencias necesarias para el proyecto.

# Requisitos
Para usar el proyecto, instala las dependencias con:

pip install -r requirements.txt
# Cómo usarlo
Por ejemplo, para ejecutar una búsqueda básica con googlesearch.py:

python ninjadorks.py -q 'udemy filetype:pdf' --download "pdf" --selenium

Puedes modificar el script para cambiar la consulta y adaptar las búsquedas a tus necesidades.
