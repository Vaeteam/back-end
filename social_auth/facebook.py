import requests
import json
import traceback
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
        func_name = "facebook_validate"
        try:
            access_token = Facebook.exchange_code_for_token(auth_token)
            profile = Facebook.get_user_info(access_token)
            return profile
        except Exception as e:
            print("Error in {}: {}".format(func_name, e))

    @staticmethod
    def exchange_code_for_token(code):
        func_name = "facebook_exchange_code_for_token"
        api_url = 'https://graph.facebook.com/v12.0/oauth/access_token'
        params = {
            'client_id': settings.FACEBOOK_CLIENT_ID,
            'client_secret': settings.FACEBOOK_SECRET_ID,
            'redirect_uri': settings.FRONTEND_URL,
            'code': code
        }
        access_token = ""
        try:
            # log input before call
            print("call in func {}, {}, {}".format(func_name, api_url, json.dumps(params)))
            response = requests.get(api_url, params=params)
            # log response here
            print("resonpse in func {}, {}".format(func_name, response.json()))
            if response.status_code == 200:
                token_data = response.json()
                access_token = token_data['access_token']
            else:
                print('Facebook token exchange failed with status code:', response.status_code)
        except Exception as e:
            print("Error in func {}: {}".format(func_name, e))
        return access_token

    @staticmethod
    def get_user_info(access_token):
        func_name = "facebook_get_user_info"
        api_url = 'https://graph.facebook.com/v12.0/me'
        params = {
            'access_token': access_token,
            'fields': 'id,name,email'
        }
        user_data = dict()
        try:
            if bool(access_token):
                # log input before call
                print("call in func {}, {}, {}".format(func_name, api_url, json.dumps(params)))
                response = requests.get(api_url, params=params)
                # log response here
                print("resonpse in func {}, {}".format(func_name, response.json()))
                if response.status_code == 200:
                    user_data = response.json()
                else:
                    print('Facebook get user info fail with status code:', response.status_code)
        except Exception as e:
            print("Error in func {}: {}".format(func_name, e))
        return user_data
