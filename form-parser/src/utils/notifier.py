"""
Уведомитель на почту о прохождении опроса - Notifier.
"""

from email.mime.text import MIMEText
from smtplib import SMTP, SMTP_SSL


class Notifier:
    """
    Уведомитель на почту о прохождении опроса.

    :ivar smtp_host: SMTP хост.
    :ivar smtp_port: SMTP порт.
    :ivar use_ssl: Флаг использования SSL.
    :ivar sending_email: Почта отправителя.
    :ivar sending_email_password: Пароль отправителя.
    """

    def __init__(self,
                 smtp_host: str,
                 smtp_port: int,
                 use_ssl: bool,
                 sending_email: str,
                 sending_email_password: str):
        """
        Конструктор Notifier.

        :param smtp_host: SMTP хост.
        :param smtp_port: SMTP порт.
        :param use_ssl: Флаг использования SSL.
        :param sending_email: Почта отправителя.
        :param sending_email_password: Пароль отправителя.
        """

        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.use_ssl = use_ssl
        self.sending_email = sending_email
        self.sending_email_password = sending_email_password

    def notify(self, mail, lst):
        """
        Отправляет на почту письмо с оповещением о прохождении опроса.

        :param mail: Почта получателя.
        :param lst: Список пар (слово, статус)
        """

        if self.use_ssl:
            smtp_client = SMTP_SSL(host=self.smtp_host, port=self.smtp_port)
        else:
            smtp_client = SMTP(host=self.smtp_host, port=self.smtp_port)

        smtp_client.login(self.sending_email, self.sending_email_password)

        html_text = self._get_html_text(lst)
        html_text['From'] = self.sending_email
        html_text['To'] = mail
        html_text['Subject'] = "Прохождение опроса"
        smtp_client.send_message(html_text)

    @classmethod
    def _get_html_text(cls, lst) -> MIMEText:
        """
        Создаёт текст html.

        :param lst: Список пар (слово, статус).
        :return: Текст html.
        """

        # Лучше использовать Jinja2
        table_body = ''
        for word, status in lst:
            table_body += f"""
                           <tr>
                               <td>{word}</td>
                               <td>{status}</td>
                           </tr>
                           """

        html = f"""\
               <html>
                    <head></head>
                    <body style="width: 100%;
                          font-family: Helvetica;
                          font-size: 18px;
                          color: black;">
                        <h1 align="center"; font-size: 24px;>
                            Спасибо за прохождение опроса
                        </h1>
                        <p>
                            Ваш ввод:
                        </p>
                        <table>
                            <thead>
                                <tr>
                                    <th>Слово</th>
                                    <th>Статус</th>
                                </tr>
                            </thead>
                            <tbody>
                                {table_body}
                            </tbody>
                        </table>
                    </body>
               </html>
               """

        html_text = MIMEText(html, _subtype='html', _charset='utf-8')

        return html_text
