import requests
import json
from backend import settings
from constant.common import Url


class Facebook:
    """
    Facebook class to fetch the user info and return it
    """

    @staticmethod
    def validate(fb_access_token):
        """
        validate method Queries the facebook GraphAPI to fetch the user info
        """
        func_name = "facebook_validate"
        profile = {}
        try:
            is_valid = Facebook.check_valid_access_token(fb_access_token)
            if is_valid:
                profile = Facebook.get_user_info(fb_access_token)
        except Exception as e:
            print("Error in {}: {}".format(func_name, e))
        return profile

    @staticmethod
    def check_valid_access_token(fb_access_token):
        func_name = "check_valid_access_token"
        params = {
            'input_token': fb_access_token,
            'access_token': "{}|{}".format(settings.FACEBOOK_CLIENT_ID, settings.FACEBOOK_SECRET_ID),
        }

        try:
            # log input before call
            print("call in func {}, {}, {}".format(func_name, Url.FACEBOOK_DEBUG_URL, json.dumps(params)))
            response = requests.get(Url.FACEBOOK_DEBUG_URL, params=params)
            # log response here
            print("response in func {}, {}".format(func_name, response.json()))
            data = response.json()
            if 'error' in data:
                print("Có lỗi trong quá trình kiểm tra fb access token {}".format(fb_access_token))
            
            else:
                app_id_matched = data.get('data', {}).get('app_id') == settings.FACEBOOK_CLIENT_ID
                if data.get('data', {}).get('is_valid') and app_id_matched:
                    # check token is ok 
                    return True     
                else:
                    print("fb access token không thuộc về ứng dụng {}".format(fb_access_token))
        except Exception as e:
            print("Error in func {}: {}".format(func_name, e))
        return False

    @staticmethod
    def get_user_info(access_token):
        func_name = "facebook_get_user_info"
        params = {
            'access_token': access_token,
            'fields': 'id,name,email'
        }
        user_data = dict()
        try:
            if bool(access_token):
                # log input before call
                print("call in func {}, {}, {}".format(func_name, Url.FACEBOOK_INFO_URL, json.dumps(params)))
                response = requests.get(Url.FACEBOOK_INFO_URL, params=params)
                # log response here
                print("response in func {}, {}".format(func_name, response.json()))
                if response.status_code == 200:
                    user_data = response.json()
                else:
                    print('Facebook get user info fail with status code:', response.status_code)
        except Exception as e:
            print("Error in func {}: {}".format(func_name, e))
        return user_data
