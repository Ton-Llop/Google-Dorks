# Ninjadorks - Advanced Search Automation Toolkit

Proyecto personal en Python orientado a búsquedas avanzadas, automatización, exportación de resultados y análisis local de archivos.

La herramienta permite lanzar consultas avanzadas usando Google o DuckDuckGo, exportar resultados en distintos formatos, descargar ciertos tipos de archivos encontrados y realizar búsquedas locales con regex o IA sobre los ficheros obtenidos.

> Uso educativo, defensivo y de investigación autorizada únicamente.

---

## Qué hace el proyecto

Este toolkit está pensado para practicar automatización y conceptos relacionados con OSINT, scripting y ciberseguridad aplicada.

Funciones principales:

- búsquedas avanzadas con Google o DuckDuckGo
- exportación de resultados a JSON y HTML
- descarga de archivos encontrados por extensión
- análisis local de archivos usando expresiones regulares
- análisis local con prompts de IA
- generación asistida de dorks con IA
- automatización de búsqueda con Selenium

---

## Estructura principal

- `ninjadorks.py` → punto de entrada principal
- `googlesearch.py` → búsquedas con Google
- `duckduckgosearch.py` → búsquedas con DuckDuckGo
- `results_parser.py` → muestra y exporta resultados
- `file_downloader.py` → descarga archivos filtrando por extensión
- `smartsearch.py` → búsqueda local con regex o IA
- `browserautosearch.py` → automatización con navegador
- `ai_agent.py` → generación de dorks con IA
- `showcase_menu.py` → menú visual/demo
- `docx_reader.py` → utilidades de lectura de documentos

---

## Requisitos

Instala las dependencias:

~~~bash
pip install -r requirements.txt
~~~

---

## Configuración

La herramienta utiliza un fichero `.env` para guardar la configuración del motor de búsqueda y las claves API.

Para crear o actualizar la configuración:

~~~bash
python ninjadorks.py -c
~~~

Durante la configuración se te pedirá:

- motor de búsqueda: `google` o `duckduckgo`
- claves API necesarias según el motor elegido
- configuración opcional para OpenAI si vas a usar generación con IA

---

## Cómo funciona

El flujo general es este:

1. Configuras el motor de búsqueda con `-c`
2. Ejecutas una consulta con `-q`
3. Opcionalmente exportas resultados con `--json` o `--html`
4. Opcionalmente descargas ciertos archivos con `--download`
5. Opcionalmente analizas los archivos descargados con `--smart-search`

---

## Uso básico

### Ver ayuda

~~~bash
python ninjadorks.py -h
~~~

### Configurar el entorno

~~~bash
python ninjadorks.py -c
~~~

### Ejecutar una búsqueda simple

~~~bash
python ninjadorks.py -q 'site:example.com filetype:pdf'
~~~

### Buscar varias páginas de resultados

~~~bash
python ninjadorks.py -q 'site:example.com "internal document"' --pages 3 --start-page 1
~~~

### Cambiar el idioma de la búsqueda

~~~bash
python ninjadorks.py -q 'site:example.com login' --lang lang_en
~~~

---

## Exportación de resultados

### Exportar a JSON

~~~bash
python ninjadorks.py -q 'site:example.com filetype:pdf' --json resultados.json
~~~

### Exportar a HTML

~~~bash
python ninjadorks.py -q 'site:example.com filetype:pdf' --html resultados.html
~~~

### Exportar a ambos formatos

~~~bash
python ninjadorks.py -q 'site:example.com filetype:pdf' --json resultados.json --html resultados.html
~~~

---

## Descarga de archivos encontrados

Puedes descargar ciertos tipos de archivos encontrados en los resultados.

### Descargar PDFs

~~~bash
python ninjadorks.py -q 'site:example.com filetype:pdf' --download pdf
~~~

### Descargar varios tipos de archivo

~~~bash
python ninjadorks.py -q 'site:example.com' --download pdf,docx,txt
~~~

Los archivos se guardan en la carpeta `Downloads/`.

---

## Smart Search sobre archivos locales

Esto permite analizar de forma local una carpeta de archivos descargados.

### Buscar con regex

~~~bash
python ninjadorks.py --smart-search ./Downloads --regex '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'
~~~

### Buscar patrones sensibles simples

~~~bash
python ninjadorks.py --smart-search ./Downloads --regex '(?i)(password|passwd|token|secret|apikey)'
~~~

### Buscar con IA usando un prompt

~~~bash
python ninjadorks.py --smart-search ./Downloads --prompt 'Resume cualquier dato sensible, credenciales expuestas o información interna encontrada en estos archivos'
~~~

### Elegir modelo y número máximo de tokens

~~~bash
python ninjadorks.py --smart-search ./Downloads --prompt 'Extrae indicadores relevantes' --model gpt-3.5-turbo-0125 --max-tokens 150
~~~

---

## Generación de dorks con IA

El proyecto también permite generar consultas avanzadas a partir de una instrucción en lenguaje natural.

~~~bash
python ninjadorks.py --generate-dork "Encuentra documentos PDF públicos relacionados con paneles de administración"
~~~

Al ejecutarlo, el script preguntará si quieres usar OpenAI o un modelo local con GPT4All.

---

## Automatización con Selenium

También puede abrir un navegador y automatizar la búsqueda.

~~~bash
python ninjadorks.py -q 'site:example.com filetype:pdf' --selenium
~~~

Ejemplo combinando búsqueda automatizada y descarga:

~~~bash
python ninjadorks.py -q 'site:example.com filetype:pdf' --selenium --download pdf
~~~

---

## Ejemplos de uso completos

### Caso 1: buscar y exportar resultados

~~~bash
python ninjadorks.py -q 'site:example.com filetype:pdf' --pages 2 --json resultados.json --html resultados.html
~~~

### Caso 2: buscar, descargar y analizar archivos

~~~bash
python ninjadorks.py -q 'site:example.com filetype:txt' --download txt
python ninjadorks.py --smart-search ./Downloads --regex '(?i)(user|username|password|token)'
~~~

### Caso 3: análisis local con IA

~~~bash
python ninjadorks.py --smart-search ./Downloads --prompt 'Indica si hay credenciales, correos, URLs internas o información sensible'
~~~

---

## Argumentos principales

| Argumento | Descripción |
|---|---|
| `-q`, `--query` | consulta o dork |
| `-c`, `--configure` | configura el `.env` |
| `--start-page` | página inicial |
| `--pages` | número de páginas a consultar |
| `--lang` | idioma de búsqueda |
| `--json` | exporta resultados a JSON |
| `--html` | exporta resultados a HTML |
| `--download` | descarga archivos por extensión |
| `-gd`, `--generate-dork` | genera dorks con IA |
| `--smart-search` | directorio para análisis local |
| `--regex` | patrón regex para búsqueda local |
| `--prompt` | prompt para análisis con IA |
| `--model` | modelo de IA |
| `--max-tokens` | máximo de tokens |
| `--selenium` | automatiza búsqueda con navegador |

---

## Consideraciones

- algunas funciones requieren configuración previa en `.env`
- la generación de dorks con IA puede usar OpenAI o GPT4All
- la descarga depende de los enlaces encontrados en los resultados
- el análisis local funciona mejor sobre carpetas de archivos ya descargados

---

## Uso responsable

Este proyecto está desarrollado con fines educativos, defensivos y de automatización sobre información pública o entornos autorizados.

No debe utilizarse contra sistemas, datos o infraestructuras sin permiso explícito.

---

## Posibles mejoras futuras

- mejor estructura modular del proyecto
- más formatos de exportación
- mejora del menú visual
- mejores filtros para descargas
- documentación ampliada con casos de uso y capturas

---

## Autor

Proyecto personal para seguir aprendiendo Python, automatización, ciberseguridad y flujos tipo DevOps.
