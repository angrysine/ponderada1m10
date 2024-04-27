from functools import wraps
from flask import request, jsonify
import jwt
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')  # Get token from query string
        if token and token.startswith('Bearer '):
            token = token.split(' ')[1]
            
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, "secret", algorithms=["HS256"])
            current_user = data['id']
        except Exception as e:
            print(e)
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated