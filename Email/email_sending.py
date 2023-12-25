import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText
from os.path import basename

from Config.config import SMTP_SERVER, SMTP_PORT
from Config.config import EMAIL_LOGIN, EMAIL_PASSWORD, email_login_password


class EmailSending:
    def __init__(self, subject='Вы зарегистрированы на курс', from_email=EMAIL_LOGIN, to='', cc='', bcc='',
                 text='', html='', smtp_server=SMTP_SERVER, smtp_port=SMTP_PORT,
                 login=EMAIL_LOGIN, password=EMAIL_PASSWORD, manager=None, files_path=[]):
        """

        :type text: Plain text Email, if html not support
        """
        self.subject = subject
        self.from_email = from_email
        self.to_address = []
        self.to = to
        self.cc = cc
        self.bcc = bcc
        for x in [self.to, self.cc, self.bcc]:
            if type(x) is list:
                self.to_address.extend(x)
            elif x != '':
                self.to_address.append(x)

        self.text = text
        self.html = html
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.user = login
        self.password = password
        if manager:
            try:
                self.password = email_login_password[manager]
                self.user = manager
                self.from_email = manager
            except KeyError:
                pass
        self.files = files_path

    def send_email(self):
        try:
            msg = EmailMessage()
            msg['From'] = self.from_email
            msg['Subject'] = self.subject
            msg['To'] = self.to
            msg['Cc'] = self.cc
            msg['Bcc'] = self.bcc

            for file in self.files:
                with open(file, 'rb') as f:
                    file_data = f.read()
                    file_name = basename(file)
                    msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)
            if self.text != '':
                part1 = MIMEText(self.text, 'plain')
                msg.attach(part1)
            if self.html != '':
                part2 = MIMEText(self.html, 'html')
                msg.attach(part2)
            # Attach parts into message container.
            # According to RFC 2046, the last part of a multipart message, in this case
            # the HTML message, is best and preferred.

            smtp = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
            smtp.login(self.user, self.password)
            smtp.sendmail(from_addr=self.from_email, to_addrs=self.to_address, msg=msg.as_string())
            smtp.quit()
            print(f'Email send {self.to_address}')
            return f'Email send {self.to_address}'

        except Exception as e:
            return f'Error {e}'
