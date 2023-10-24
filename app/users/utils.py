import os
import secrets
from PIL import Image
from flask import url_for, current_app as app
from app import mail
from flask_mail import Message

# functions =======================================================================

def upload_image(picture):
    _, file_ext = os.path.splitext(picture.filename)
    secret_hex = secrets.token_hex(8)
    image_name = secret_hex + file_ext
    image_path = os.path.join(app.root_path, 'static/images/profile_pics', image_name)
    
    output_size = (125, 125)
    resized_image = Image.open(picture)

    output_image = resized_image.resize(output_size)

    output_image.save(image_path)

    return image_name


def send_reset_mail(user):
    token = user.get_reset_token()
    sender = 'support@guarantywealth.com'
    subject = 'Password Reset Token'
    receipients = [user.email]
    msg = Message(subject=subject, sender=sender, recipients=receipients)
    msg.body = f'''
    Hi {user.email}, to reset your password, visit the following link
    {url_for('users.reset_password', token=token, _external=True)}
    If you did not initiate this request, please ignore this mail and no changes will be made, thank you!
    '''
    mail.send(message=msg)
