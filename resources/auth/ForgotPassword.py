import datetime
from flask_jwt_extended import create_access_token
from flask_restful import Resource, request
from flask_mail import Message
from flask import current_app, url_for

from models.ConnectionPool import ConnectionPool

class ForgotPassword(Resource):
    def post(self):
        pool = ConnectionPool()

        subject = 'Password Reset Request'
        email = request.json.get('email')

        if not email:
            return {'message': 'Missing field: email'}, 400

        try:
            query = "SELECT COUNT(*) FROM user WHERE email = %s"
            result = pool.execute(query, (email,))

            # Check if user exists before actually sending an email, if they don't exist
            # We pretend we sent the email (Security)
            if 'rows' not in result or result['rows'] == 0:
                return {'message': f'Password reset email sent to {email}'}, 201

            # Generate reset token
            expires = datetime.timedelta(hours=1)
            reset_token = create_access_token(identity=email, expires_delta=expires)

            # Create reset URL
            reset_url = f"http://localhost:3000/reset-password/{reset_token}"
            body = f"To reset your password, click the following link: {reset_url}"

            # Send email
            msg = Message(subject=subject, recipients=[email], body=body)
            current_app.mail.send(msg)
            return {'message': f'Password reset email sent to {email}'}, 200
        except Exception as e:
            return {'message': f'Failed to send password reset email. Error: {e}'}, 500