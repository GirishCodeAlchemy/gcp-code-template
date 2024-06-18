import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(sender_email, recipient_email,  subject, html_content, body=None, image_files=None):
    # SMTP server configuration
    smtp_server = 'smtp-gmail.com'
    smtp_port = 25

    # Create email message
    msg = MIMEMultipart("related")
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    if body:
        # Attach body text
        text_part = MIMEText(body, "plain")
        msg.attach(MIMEText(text_part))
    elif html_content:
        html_part = MIMEText(html_content, "html")
        msg.attach(html_part)

    for index, each_file in enumerate(image_files):
        # Attach image
        print(f"Attaching image file: {each_file}")
        with open(each_file, 'rb') as file:
            img_data = file.read()
        image = MIMEImage(img_data, name=each_file)
        image.add_header("Content-Id", f"<imagedata{index}>")
        msg.attach(image)

    # Connect to SMTP server and send email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.sendmail(sender_email, recipient_email, msg.as_string())
