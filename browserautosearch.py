from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time

class BrowserAutoSearch:
    def __init__(self):
        self.browser = self._initialize_browser()
    
    def _initialize_browser(self):
        browsers = {
            "firefox": {
                "manager": GeckoDriverManager,
                "service": FirefoxService,
                "options": webdriver.FirefoxOptions(),
                "driver": webdriver.Firefox

            },
            "chrome": {
                "manager": ChromeDriverManager,
                "service": ChromeService,
                "options": webdriver.ChromeOptions(),
                "driver": webdriver.Chrome
            }
        }
        # Inicializamos
        for browser_name, browser_info in browsers.items():
            try:
                return browser_info["driver"](service=browser_info["service"](browser_info["manager"]().install()), options=browser_info["options"])
            except:
                print(f"Error al iniciar el navegador {browser_name}:")
        raise Exception("No se pudo iniciar ninguno de los navegadores, instala firefox/chrome")

    def accept_cookies(self, button_selector):
        """
        Acepta anuncio cookies del buscador
        """
        try:
            time.sleep(3)
            accept_button = WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.ID, button_selector)))# aquest es el ID del boto d'acceptar tot de les cookies. El id el veus fent inspeccionar a google
            time.sleep(3)
            accept_button.click()
        except Exception as e:
            print(f"Error al encontrar o clicar el boton de aceptar cookies: {e}")

    def search_google(self, query):
        """
        Realiza una busqueda en Google.
        """
        self.browser.get("http://www.google.com")
        self.accept_cookies(button_selector='L2AGLb')
        # Encuentra barra de busqueda, name = q( en el inspeccionar)
        search_box = self.browser.find_element(By.NAME, 'q')
        for char in query:
            search_box.send_keys(char)
            time.sleep(0.1)  # escribe carácter a carácter
        time.sleep(1)
        search_box.send_keys(Keys.ENTER)

        #busqueda = WebDriverWait(browser, 20).until(search_box.send_keys("Pyke guia" +  Keys.ENTER))
        time.sleep(7)

    def google_search_results(self):
        """
        Extrae resultados de la búsqueda en Google
        """
        try:
            # Esperar hasta que haya al menos 1 resultado
            WebDriverWait(self.browser, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.g'))
            )
            results = self.browser.find_elements(By.CSS_SELECTOR, 'div.g')
        except Exception as e:
            print(f"No se pudieron encontrar resultados: {e}")
            return []

        custom_results = []
        for result in results:
            try:
                cresult = {}
                cresult["title"] = result.find_element(By.CSS_SELECTOR, 'h3').text
                cresult["link"] = result.find_element(By.TAG_NAME, 'a').get_attribute('href')
                cresult["description"] = result.find_element(By.CSS_SELECTOR, 'div.VwiC3b').text
                custom_results.append(cresult)
            except Exception as e:
                # Algunos div.g pueden no tener título o descripción
                print(f"Un elemento no se pudo extraer completamente: {e}")
                continue

        return custom_results



