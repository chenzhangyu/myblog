# -*- coding: utf-8 -*-

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
from config import info




def send_mail(to_addr, subject, content):
    def _format_addr(s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), \
                addr.encode('utf-8') if isinstance(addr, unicode) else addr))
    from_addr = info['email']['address']
    password = info['email']['password']
    smtp_server = info['email']['smtp']
    name = info['site']['name']

    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = _format_addr(u'%s <%s>' % (name, from_addr))
    msg['To'] = _format_addr(u'to <%s>' % to_addr)
    msg['Subject'] = Header(subject, 'utf-8').encode()

    server = smtplib.SMTP(smtp_server, 25)
    # server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()
