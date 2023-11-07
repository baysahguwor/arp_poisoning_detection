import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from database import get_email_settings, save_attack_log

def send_email(subject, message):
    try:
        # Get email settings from the database
        smtp_server, smtp_port, smtp_username, smtp_password = get_email_settings()

        # Create a MIMEText object to represent the email message
        msg = MIMEMultipart()
        msg['From'] = smtp_username
        msg['To'] = smtp_username  # Using the same email for sender and recipient for this example
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        # Establish a secure SSL connection to the SMTP server
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)

        # Log in to the SMTP server
        server.login(smtp_username, smtp_password)

        # Send the email
        server.sendmail(smtp_username, [smtp_username], msg.as_string())


        # Close the connection
        server.quit()

        print("Email sent successfully!")
    except Exception as e:
        print("An error occurred:", str(e))
