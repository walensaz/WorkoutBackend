from flask_restful import Resource, request
from flask_mail import Message
from flask import current_app

class ForgotPassword(Resource):
    def post(self):
        # Get data from request
        data = request.get_json()

        subject = 'Forgot Password?'
        body = "This is the body!"
        recipient = request.json.get('recipient')

        if not recipient:
            return 'Missing field: recipient', 400

        try:
            # Create message
            msg = Message(subject=subject, recipients=[recipient], body=body)
            # Send email
            current_app.mail.send(msg)
            return {'message': f'Email sent to {recipient}'}, 200
        except Exception as e:
            return {'message': f'Failed to send email. Error: {e}'}, 500