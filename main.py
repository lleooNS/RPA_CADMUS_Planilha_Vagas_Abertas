from logging import exception
from time import sleep
from src.helpers.ChromeHelper import ChromeDriver
from src.steps.steps import track_steps


def main():

    try:
        url = 'https://cadmus.com.br/vagas-tecnologia/'

        web_driver = ChromeDriver().driver()
        web_driver.get(url)

        # Controlar as etapas
        track_steps(web_driver)

        sleep(5)
        web_driver.close()

    except Exception:
        exception('Erro no projeto')


if __name__ == '__main__':

    main()
