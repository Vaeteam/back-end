from rest_framework.authentication import get_authorization_header, BaseAuthentication
from rest_framework import exceptions
from django.conf import settings
from .models import CustomUser
import jwt

class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        auth_header = get_authorization_header(request)
        auth_data = auth_header.decode("utf-8")

        auth_token = auth_data.split(" ")

        if not auth_token:
            return None

        if len(auth_token) == 1:
            # Invalid token header. No credentials provided. Do not attempt to
            # authenticate.
            return None
        
        elif len(auth_token) > 2:
            # Invalid token header. The Token string should not contain spaces. Do
            # not attempt to authenticate.
            return None
        
        token = auth_token[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms= 'HS256')
            user_id = payload['id']
            
            if payload['type'] != 'access_token':
                raise exceptions.AuthenticationFailed({'error': 'token is not valid'})
            try:
                user = CustomUser.objects.get(id= user_id)
            except:
                raise exceptions.NotFound({'error': 'user is not exist'})
            
            return (user, token)

        except jwt.ExpiredSignatureError as ex:
            raise exceptions.AuthenticationFailed({'error': 'token is expire, login again'})
        
        except jwt.DecodeError as ex:
            raise exceptions.AuthenticationFailed({'error': 'token is not valid'})

