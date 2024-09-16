import smtplib
import imghdr
import os
from email.message import EmailMessage
    
password = os.getenv('PASSWORD')
sender = "apptestbeno@gmail.com"
receiver = "safwatsadiq14@gmail.com"


def send_email(image_path):
    print("send_email function started...")
    email_message = EmailMessage()
    email_message['Subject'] = 'New customer showed up'
    email_message.set_content("Hey, we just saw a new customer!")
    
    with open(image_path, 'rb') as img:
        content = img.read()
    email_message.add_attachment(content, maintype='image', subtype=imghdr.what(None, content), filename='image.png')
    
    gmail = smtplib.SMTP('smtp.gmail.com', 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(sender, password)
    gmail.sendmail(sender, receiver, email_message.as_string())
    gmail.quit()
    print("email sent successfully")


if __name__ == "__main__":
    send_email("image.png")