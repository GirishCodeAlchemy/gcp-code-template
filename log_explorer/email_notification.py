import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email_with_attachment(recipient_email, filename):
        """Sends an email with the specified attachment."""
        # SMTP server configuration
        smtp_server = 'smtp-gmail.com'
        smtp_port = 25
        # smtp_username = 'your_smtp_username'
        # smtp_password = 'your_smtp_password'

        # Email content
        sender_email = 'Venkatareddygirish@gmail.com'
        subject = 'Mismatch Count Report'
        body = 'Please find the attached image for the mismatch count report.'

        # Create email message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        # Attach body text
        msg.attach(MIMEText(body, 'plain'))

        # Attach image
        with open(filename, 'rb') as file:
            img_data = file.read()
        image = MIMEImage(img_data, name=filename)
        msg.attach(image)

        # Connect to SMTP server and send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            # server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())


to = 'Venkatareddygirish@gmail.com'
filename = 'mismatch_count.png'
send_email_with_attachment(to, filename)