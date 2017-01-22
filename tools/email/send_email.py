import smtplib
from email.mime.text import MIMEText

msg = MIMEText("The body of the email is here")

msg['Subject'] = "Test mail"
msg['From'] = "mymail@gmail.com" # check email
msg['To'] = "mymail@gmail.com" # check email

send = smtplib.SMTP('localhost')
# send.send_message(msg)
send.quit()