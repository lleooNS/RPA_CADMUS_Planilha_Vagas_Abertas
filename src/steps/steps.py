import configs.config
from datetime import datetime
from logging import exception, info, INFO, basicConfig
from os import getcwd, getenv
from os.path import isfile
from pathlib import Path
from time import sleep
from pandas import DataFrame
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as e_c
from selenium.webdriver.common.by import By
from src.helpers.Email import Email
basicConfig(level=INFO)

elements = {

    'div_jobs': 'pfolio',
    'accept_button': 'aceitar',
    'list_divs': './div',
    'job_name': './div/h3',
    'job_location': './div/p[1]',
    'description_button': './div/p[2]/a',
    'job_description': '/html/body/section/div/div[2]/div[1]/div[1]/p'

}

list_job_names = []
list_job_locations = []
list_job_descriptions = []


def validate_element(web_driver, by_type, element_value):

    try:
        element = WebDriverWait(web_driver, 30).until(e_c.presence_of_element_located((by_type, element_value)))
    except TimeoutException:
        raise TimeoutException('O elemento não foi encontrado no tempo determinado.')
    except Exception as error:
        raise exception(f'Erro inesperado = {error.__cause__}')
    else:
        return element


def find_divs_jobs(web_driver):

    global list_job_names, list_job_locations, list_job_descriptions
    scroll_counter = 1

    try:
        # Aceitar os cookies da página
        try:
            sleep(5)
            accept_button = validate_element(web_driver, By.ID, elements['accept_button'])
            accept_button.click()
        except Exception:
            info('O botão para aceitar todos os cookies não foi encontrado na página')

        sleep(3)
        # Rolar a página até as vagas abertas
        web_driver.execute_script('window.scrollBy(0, 700)')
        sleep(3)

        # Div que contem todas as vagas abertas
        div_jobs = validate_element(web_driver, By.ID, elements['div_jobs'])
        list_divs = div_jobs.find_elements(By.XPATH, elements['list_divs'])

        # Percorrer a lista
        for i, items in enumerate(list_divs, start=1):

            # Atualizar variáveis
            div_jobs = validate_element(web_driver, By.ID, elements['div_jobs'])
            job = validate_element(div_jobs, By.XPATH, f'./div[{i}]')

            job_name = validate_element(job, By.XPATH, elements['job_name'])
            job_location = validate_element(job, By.XPATH, elements['job_location'])

            # Adicionar na lista
            list_job_names.append(job_name.text)
            list_job_locations.append(job_location.text)

            # Botão detalhes
            description_button = validate_element(job, By.XPATH, elements['description_button'])
            web_driver.execute_script('arguments[0].click();', description_button)
            sleep(5)

            try:
                job_description = validate_element(web_driver, By.XPATH, elements['job_description'])

                # Adicionar na lista
                list_job_descriptions.append(job_description.text)

            except Exception:
                list_job_descriptions.append('Sem Descrição')

            # Retornar para a lista de vagas abertas
            web_driver.back()
            sleep(5)

            # Rolar a página
            if scroll_counter == 4:
                web_driver.execute_script('window.scrollBy(0, 200)')
                scroll_counter = 1
            else:
                scroll_counter += 1

    except TimeoutException:
        exception('Erro de TimeoutException.')
    except Exception as error:
        exception(error.__cause__)


def generate_excel_spreadsheet():

    global list_job_names, list_job_locations, list_job_descriptions

    info('Gerando planilha excel...')

    dictionary = {'Nome': list_job_names, 'Local': list_job_locations, 'Descrição': list_job_descriptions}
    dataframe = DataFrame(dictionary)
    dataframe.to_excel(str(Path(getcwd(), 'documents', 'downloads', 'Vagas_Abertas_Cadmus.xlsx')), sheet_name='Vagas_Abertas', header=True, index=False, na_rep='#N/D')


def send_email():

    now_dt = datetime.now()
    now_str = now_dt.strftime('%d/%m/%Y')
    dir_excel_spreadsheet = str(Path(getcwd(), 'documents', 'downloads', 'Vagas_Abertas_Cadmus.xlsx'))

    # Os emails e a senha devem ser modificados no arquivo configs/.config.yml
    email_login = getenv('EMAIL_LOGIN')
    password = getenv('PASSWORD')
    email_to = getenv('EMAIL_TO')
    port = 587
    type_host = 'gmail'

    email = Email(email_login, password, email_to, port, type_host)
    email.subject = 'Planilha Vagas Abertas'
    email.body = f'Prezados, segue em anexo a planilha com as vagas em aberto do dia {now_str} ' + '\n\nAtenciosamente,\nRPA | CADMUS'

    # Verificar se a planilha existe no diretório
    if isfile(dir_excel_spreadsheet):
        info('Enviando email...')
        email.envia(dir_excel_spreadsheet)
    else:
        info('A planilha excel não foi encontrada.')


def track_steps(web_driver):

    find_divs_jobs(web_driver)
    generate_excel_spreadsheet()
    send_email()

