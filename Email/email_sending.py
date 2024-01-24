import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from os.path import basename

from Telegram.config import SMTP_SERVER, SMTP_PORT, EMAIL_LOGIN, EMAIL_PASSWORD, email_login_password


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
        msg = MIMEMultipart()
        msg['From'] = self.from_email
        msg['Subject'] = self.subject
        msg['To'] = self.to
        msg['Cc'] = self.cc
        # msg['Bcc'] = self.bcc

        msg.attach(MIMEText(self.text, 'plain'))
        msg.attach(MIMEText(self.html, 'html'))

        for f in self.files:
            with open(f, "rb") as fil:
                part = MIMEApplication(
                    fil.read(),
                    Name=basename(f)
                )
            # After the file is closed
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
            msg.attach(part)

        smtp = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
        smtp.login(self.user, self.password)
        smtp.sendmail(from_addr=self.user, to_addrs=self.to_address, msg=msg.as_string())
        smtp.quit()
        print(f'Email send {self.to_address}')
        return f'Email send {self.to_address}'
