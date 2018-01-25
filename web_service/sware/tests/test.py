#coding: utf-8
import smtplib
from email.mime.text import MIMEText
from email.header import Header

sender = 'sunlxt123@126.com'
receiver = 'sunlxt123@126.com'
subject = 'python email test'
smtpserver = 'smtp.126.com'
username = 'sunlxt123@126.com'
password = 'zxcvbnm789'

msg = MIMEText( 'Hello Python', 'text', 'utf-8' )
msg['Subject'] = Header( subject, 'utf-8' )

smtp = smtplib.SMTP()
smtp.connect( smtpserver )
smtp.login( username, password )
smtp.sendmail( sender, receiver, msg.as_string() )
smtp.quit()