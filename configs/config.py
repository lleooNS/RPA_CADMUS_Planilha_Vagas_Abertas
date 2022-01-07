import json
from logging import exception
from yaml import load, FullLoader
from os import environ, getcwd


def config():

    try:
        with open(f'{getcwd()}/configs/.config.yml', encoding='UTF-8') as f:
            data = load(f, Loader=FullLoader)

            environ['EMAIL_LOGIN'] = data['email_login']
            environ['PASSWORD'] = data['password']
            environ['EMAIL_TO'] = data['email_to']

    except Exception:
        exception('Erro no arquivo .gitlab-ci.yml')


config()
