import requests
from backend import settings


class Facebook:
    """
    Facebook class to fetch the user info and return it
    """

    @staticmethod
    def validate(auth_token):
        """
        validate method Queries the facebook GraphAPI to fetch the user info
        """
        try:
            access_token = Facebook.exchange_code_for_token(auth_token)
            profile = Facebook.get_user_info(access_token)
            return profile
        except:
            return "The token is invalid or expired."

    @staticmethod
    def exchange_code_for_token(code):
        func_name = "exchange_code_for_token"
        token_url = 'https://graph.facebook.com/v12.0/oauth/access_token'
        params = {
            'client_id': settings.FACEBOOK_CLIENT_ID,
            'client_secret': settings.FACEBOOK_SECRET_ID,
            'redirect_uri': settings.FRONTEND_URL,
            'code': code
        }
        access_token = ""
        try:
            response = requests.get(token_url, params=params)
            # log response here
            print(response, response.json(), params)
            access_token = response.json().get('access_token')
        except Exception as e:
            print("Error in {}: {}".format(func_name, e))
        return access_token

    @staticmethod
    def get_user_info(access_token):
        func_name = "get_user_info"
        api_url = 'https://graph.facebook.com/v12.0/me'
        params = {
            'access_token': access_token,
            'fields': 'id,name,email'
        }
        user_data = dict()
        try:
            response = requests.get(api_url, params=params)
            # log response here
            print(response, response.json(), params)
            user_data = response.json()
        except Exception as e:
            print("Error in {}: {}".format(func_name, e))
        return user_data
