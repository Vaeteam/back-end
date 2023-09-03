from common.constants import RESPONSE_FORMAT


def form_response(data=None, message=None, detail=None):
    data and RESPONSE_FORMAT.update({"data": data})
    message and RESPONSE_FORMAT.update({"data": message})
    detail and RESPONSE_FORMAT.update({"data": detail})
    return RESPONSE_FORMAT
