import logging
import requests
import json
from backend import settings


logger = logging.getLogger(__name__)
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
            logger.error("Error in {}: {}".format(func_name, e))

    @staticmethod
    def exchange_code_for_token(code):
        func_name = "google_exchange_code_for_token"
        api_url = 'https://oauth2.googleapis.com/token'
        params = {
            'client_id': settings.GOOGLE_CLIENT_ID,
            'client_secret': settings.GOOGLE_SECRET_ID,
            'redirect_uri': settings.GOOGLE_FRONTEND_URL,
            'code': code,
            'grant_type': 'authorization_code'
        }
        access_token = ""
        try:
            # log input before call
            logger.info(f"CALL API: call GG authen api with {api_url}, {str(params)}")
            response = requests.post(api_url, params=params)
            # log response here
            logger.info(f"API RESPONSE: GG api response with value {str(response.json())}")
            if response.status_code == 200:
                token_data = response.json()
                access_token = token_data['access_token']
            else:
                logger.info(f'Google token exchange failed with status code: {response.status_code} {str(response.json())}')
        except Exception as e:
            logger.error("Error in func {}: {}".format(func_name, e))
        return access_token

    @staticmethod
    def get_user_info(access_token):
        api_url = 'https://www.googleapis.com/oauth2/v2/userinfo'
        headers = {'Authorization': f'Bearer {access_token}'}
        
        try:
            logger.info(f"CALL API GG USER DATA:{api_url} {headers}")
            response = requests.get(api_url, headers=headers)
            logger.info(f"GET USER DATA RESPONSE: status code {response.status_code} data {str(response.json())}")
            if response.status_code == 200:
                return response.json()
        
        except Exception as e:
            logger.error(F"GET USER DATA ERROR: {str(e)}")
