import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email_with_attachment(recipient_email, filename):
        """Sends an email with the specified attachment."""
        # SMTP server configuration
        smtp_server = ''
        smtp_port = 25
        # smtp_username = 'your_smtp_username'
        # smtp_password = 'your_smtp_password'

        # Email content
        sender_email = ' '
        subject = 'Mismatch Count Report'
        body = 'Please find the attached image for the mismatch count report.'

        msg = MIMEMultipart("related")
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        html_data = """
            <!DOCTYPE html>
            <html>
            <body>
            <h1>Please find the attached image for the mismatch count report.</h1>
             <img src="cid:mismatchimage">
            </body>
            </html>
            """
        # Create the HTML part
        html_part = MIMEText(html_data, "html")
        msg.attach(html_part)

        with open(filename, 'rb') as file:
            img_data = file.read()
        image = MIMEImage(img_data, name=filename)
        image.add_header("Content-Id", "<mismatchimage>")
        msg.attach(image)

        # Connect to SMTP server and send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            # server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())


to = 'Venkatareddygirish@gmail.com'
filename = 'mismatch_count.png'
send_email_with_attachment(to, filename)
