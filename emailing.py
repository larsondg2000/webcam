import glob
import smtplib
import imghdr
import os
from email.message import EmailMessage
from threading import Thread

"""
username = "larsondg2000@gmail.com"
password = os.getenv("PASSWORD")
"""
PASSWORD = os.getenv("PASSWORD")
SENDER = "larsondg2000@gmail.com"
RECEIVER = "larsondg2000@gmail.com"


def clean_folder():
    """
    Cleans folder after email is sent
    :return:
    """
    print("start clean")
    images = glob.glob("images/*.png")
    for image in images:
        os.remove(image)


def send_email(image_path):
    print("start email")
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
    print("end email")

    # setup thread for clean_folder() call
    clean_thread = Thread(target=clean_folder)
    clean_thread.daemon = True

    # call clean function after email sent
    clean_thread.start()


if __name__ == "__main__":
    send_email(image_path="images/")
