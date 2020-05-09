import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr

from django.conf import settings


def _format_address(s):
    name, address = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), address))


class EmailHelper:
    from_address = settings.EMAIL
    password = settings.EMAIL_PWD
    smtp_server = settings.EMAIL_SERVER
    smtp_server_host = settings.EMAIL_HOST  # default 25

    def __init__(self):
        self.msg = MIMEText('', 'plain', 'utf-8')
        self.to_address = None

    def set_content(self, content, to_address, subject, attachment: dict = None):
        """ 附件
        attachment = {
            'file':  bytes,
            'filename': str,
            'maintype': str,
            'subtype': str
        }
        """
        msg = MIMEMultipart()
        # msg['From'] = _format_address('LifeOA <{}>'.format(self.from_address))
        msg['To'] = _format_address('user <{}>'.format(to_address))
        msg['Subject'] = Header(subject, 'utf-8').encode()
        msg.attach(MIMEText(content, 'plain', 'utf-8'))

        if attachment:
            mime = MIMEBase(attachment['maintype'], attachment['subtype'], filename=attachment['filename'])
            mime.add_header('Content-Disposition', 'attachment', filename=attachment['filename'])
            mime.add_header('Content-ID', '<0>')
            mime.add_header('X-Attachment-Id', '0')
            mime.set_payload(attachment['file'])
            encoders.encode_base64(mime)
            msg.attach(mime)

        self.to_address = to_address
        self.msg = msg

    def send(self):
        # 问题: 每次调用都会实例化， 存在优化空间
        server = smtplib.SMTP(self.smtp_server, self.smtp_server_host)  # SMTP协议默认端口是25
        server.set_debuglevel(3)
        server.login(self.from_address, self.password)
        server.sendmail(self.from_address, [self.to_address], self.msg.as_string())
        server.quit()
