import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from tasks_restfull.models import CustomToken
from django.utils import timezone
from datetime import timedelta, datetime

User = get_user_model()

class CustomTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get('Authorization')
        if not token:
            return None
        try:
            token = token.split(' ')[1]
            custom_token = CustomToken.objects.get(key=token)
        except (CustomToken.DoesNotExist, IndexError):
            raise AuthenticationFailed('Invalid token')
        
        if custom_token.is_expired():
            raise AuthenticationFailed('Token has expired')
        return (custom_token.user, custom_token)
    

class CustomJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None
        
        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=['HS256'])
            user_id = payload.get('user_id')
            user = User.objects.get(id=user_id)
            return (user, token)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except (jwt.InvalidTokenError, User.DoesNotExist):
            raise AuthenticationFailed('Invalid token')