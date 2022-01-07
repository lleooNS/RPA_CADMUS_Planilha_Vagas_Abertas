import os
import smtplib

from logging import exception, info, INFO, basicConfig
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
basicConfig(level=INFO)

class Email:

    def __init__(self, email_login, password, email_to, port, type_host):

        self.__email = email_login
        self.__password = password
        self.__email_to = email_to
        self.__subject = ''
        self.__body = ''
        self.__host = f'smtp.{type_host}.com'
        self.__port = port

    def envia(self, anexo_dir=None):

        server = None

        try:
            server = smtplib.SMTP(self.__host, self.__port)
            server.ehlo_or_helo_if_needed()
            server.starttls()
            server.login(self.__email, self.__password)

            if anexo_dir is not None:
                msg = self.__mensagem_com_anexo(anexo_dir)
            else:
                msg = self.__mensagem_sem_anexo()

        except Exception:
            exception('Erro ao enviar o email!')

        else:
            server.sendmail(self.__email, self.__email_to, msg.as_string())

            info('Email enviado com sucesso!')

        finally:
            if server is not None:
                server.quit()

    def __mensagem_sem_anexo(self):
        return self.__mensagem()

    def __mensagem_com_anexo(self, anexo_dir):

        msg = self.__mensagem()

        # open the file to be sent
        attachment = open(anexo_dir, "rb")

        # instance of MIMEBase and named as p
        p = MIMEBase('application', 'octet-stream')

        # To change the payload into encoded form
        p.set_payload(attachment.read())

        # encode into base64
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', "attachment; filename= %s" % os.path.basename(anexo_dir))

        # attach the instance 'p' to instance 'msg'
        msg.attach(p)

        return msg

    def __mensagem(self):

        msg = MIMEMultipart()

        msg['From'] = self.__email
        msg['To'] = self.__email_to
        msg['Subject'] = self.__subject

        msg.attach(MIMEText(self.__body, 'plain'))

        return msg

    @property
    def body(self):
        return self.__body

    @body.setter
    def body(self, value):
        self.__body = value

    @property
    def subject(self):
        return self.__subject

    @subject.setter
    def subject(self, value):
        self.__subject = value
