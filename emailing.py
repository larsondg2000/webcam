import smtplib
import imghdr
import os
from email.message import EmailMessage

"""
username = "larsondg2000@gmail.com"
password = os.getenv("PASSWORD")
"""
PASSWORD = os.getenv("PASSWORD")
SENDER = "larsondg2000@gmail.com"
RECEIVER = "larsondg2000@gmail.com"


def send_email(image_path):
    email_message = EmailMessage()
    email_message["Subject"] = "New customer"
    email_message.set_content("Just saw new customer")

    with open(image_path, "rb") as file:
        content = file.read()

    email_message.add_attachment(content, maintype="image", subtype=imghdr.what(None, content))

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER, PASSWORD)
    gmail.sendmail(SENDER, RECEIVER, email_message.as_string())
    gmail.quit()


if __name__ == "__main__":
    send_email(image_path="images/")
