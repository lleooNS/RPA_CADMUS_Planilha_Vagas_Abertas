#pip install chromedriver-autoinstaller

import chromedriver_autoinstaller
from os import getcwd
from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException
from selenium.webdriver.chrome.options import Options
from logging import info
from pathlib import Path


class ChromeDriver:

    def __init__(self):
        self.__chrome_options = Options()
        self.__root_dir = getcwd()

        self.__prefs = {"download": {
            "default_directory": str(Path(self.__root_dir, 'documents', 'downloads')),
            "directory_upgrade": True,
            "extensions_to_open": ""
        }}

    def driver(self) -> webdriver.Chrome:
        try:
            chromedriver_autoinstaller.install()

            options = Options()
            options.add_argument("--start-maximized")
            driver = webdriver.Chrome(options=options)

        except SessionNotCreatedException:
            raise Exception('Versão do Chrome incompatível com a do driver')

        except Exception:
            raise Exception('Não foi possível inicializar o Chrome Driver do Selenium')

        else:
            info('Sessão do Chrome iniciada com sucesso!')

            return driver
