# Google Dorks con Python
Este proyecto permite realizar búsquedas avanzadas en Google y DuckDuckGo utilizando técnicas conocidas como Google Dorks. Está pensado para ayudar en la ciberseguridad y en la búsqueda de información pública específica.

# ¿Qué es un Google Dork?
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
# 1️⃣ Búsqueda simple en Google con Dork
python ninjadorks.py -q 'site:example.com "confidential"'

# 2️⃣ Búsqueda simple en DuckDuckGo (configurar primero)
python ninjadorks.py -q 'filetype:pdf "proyecto interno"' -c

# 3️⃣ Descargar archivos encontrados (PDFs)
python ninjadorks.py -q 'site:example.com filetype:pdf' --download pdf

# 4️⃣ Smart Search con regex (buscar emails)
python ninjadorks.py --smart-search /home/kali/Downloads --regex "\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b"

# 5️⃣ Smart Search con IA (prompt)
python ninjadorks.py --smart-search /home/kali/Downloads --prompt "Extrae cualquier dirección de correo electrónico y contraseña que aparezca"

# 6️⃣ Generar un Dork con IA
python ninjadorks.py --generate-dork "Encuentra documentos internos sobre planes estratégicos"

# 7️⃣ Búsqueda automática con Selenium
python ninjadorks.py -q 'udemy filetype:pdf' --download "pdf" --selenium

# 8️⃣ Combinando descarga + Smart Search
python ninjadorks.py -q 'filetype:txt site:example.com' --download txt
python ninjadorks.py --smart-search ./Downloads --prompt "Busca usuarios y contraseñas"


Para ver todas las funcionalidades escribe:
python ninjadorks.py -h

Puedes modificar el script para cambiar la consulta y adaptar las búsquedas a tus necesidades.
