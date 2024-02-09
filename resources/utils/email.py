from flask_mail import Message

def send_email(app, mail, subject, recipients, body):
    with app.app_context():
        msg = Message(subject, recipients=recipients, body=body)
        mail.send(msg)