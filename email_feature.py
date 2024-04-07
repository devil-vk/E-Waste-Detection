import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

FROM_EMAIL = 'dvkr20cs@gmail.com'
FROM_EMAIL_PASSWORD = "jsexrygeuimnpgkb"

def send_email(recipient_email, subject, message, pdf_path):
    with open(pdf_path, 'rb') as f:
        pdf_data = f.read()
    
    msg = MIMEMultipart()
    msg['From'] = FROM_EMAIL
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))
    
    pdf_attachment = MIMEApplication(pdf_data, name='report.pdf')
    msg.attach(pdf_attachment)

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(FROM_EMAIL, FROM_EMAIL_PASSWORD)
            server.sendmail(FROM_EMAIL, recipient_email, msg.as_string())
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error: {e}")