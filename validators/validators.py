import json


def validate_wifi_status(data):
    status = True
    messages = []
    if not 'status' in data:
        messages.append('\'status\' key missing in input json')
        status = False
    elif data['status'] != True and data['status'] != False:
        messages.append('\'status\' should be either true or false')
        status = False
    return status, messages