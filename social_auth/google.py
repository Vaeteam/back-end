from google.auth.transport import requests
from google.oauth2 import id_token


class Google:
    """Google class to fetch the user info and return it"""

    @staticmethod
    def validate(auth_token):
        """
            validate method Queries the facebook GraphAPI to fetch the user info
        """
        func_name = "google_validate"
        try:
            access_token = Google.exchange_code_for_token(auth_token)
            profile = Google.get_user_info(access_token)
            return profile
        except Exception as e:
            print("Error in {}: {}".format(func_name, e))

    @staticmethod
    def exchange_code_for_token(code):
        func_name = "google_exchange_code_for_token"
        api_url = 'https://oauth2.googleapis.com/token'
        params = {
            'client_id': settings.FACEBOOK_CLIENT_ID,
            'client_secret': settings.FACEBOOK_SECRET_ID,
            'redirect_uri': settings.FRONTEND_URL,
            'code': code,
            'grant_type': 'authorization_code'
        }
        access_token = ""
        try:
            response = requests.get(token_url, params=params)
            # log response here
            print(response, response.json(), params)
            if response.status_code == 200:
                token_data = response.json()
                access_token = token_data['access_token']
            else:
                print('Google token exchange failed with status code:', response.status_code)
        except Exception as e:
            print("Error in {}: {}".format(func_name, e))
        return access_token

    @staticmethod
    def get_user_info(access_token):
        func_name = "google_get_user_info"
        api_url = 'https://www.googleapis.com/oauth2/v2/userinfo'
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        user_info = {}
        try:
            if bool(access_token):
                response = requests.get(api_url, headers=headers)
                if response.status_code == 200:
                    user_info = response.json()
                else:
                    print('Google get user info fail with status code:', response.status_code)
        except Exception as e:
            print("Error in {}: {}".format(func_name, e))
        return user_info
