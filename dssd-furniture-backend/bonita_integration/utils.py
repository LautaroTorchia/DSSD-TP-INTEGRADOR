import requests

# bonita_integration/utils.py

import requests

def bonita_login(username, password):
    # Define the Bonita login endpoint URL
    bonita_login_url = 'http://192.168.1.56:8080/bonita/loginservice'

    # Create a dictionary with the login credentials
    data = {
        'username': username,
        'password': password,
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    response = requests.post(bonita_login_url, data=data, headers=headers)

    if response.status_code == 204:
        return response
    else:
        raise Exception(f"Bonita login failed with status code {response.status_code}: {response.text}")


def bonita_check_processes(cookies):
    # Define the Bonita check processes endpoint URL
    bonita_check_processes_url = 'http://localhost:8080/bonita/API/bpm/process?c=100&p=0'

    # Send a GET request to the Bonita API with the provided cookies
    response = requests.get(bonita_check_processes_url, cookies=cookies)

    if response.status_code == 200:
        return response
    else:
        raise Exception(f"Bonita check processes failed with status code {response.status_code}: {response.text}")
