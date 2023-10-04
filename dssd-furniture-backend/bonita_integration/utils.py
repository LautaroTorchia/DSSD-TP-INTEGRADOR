import requests
from rest_framework.response import Response
from rest_framework import status
from ljj_muebles.settings import BONITA_URL


def update_cookie_header(bonita_cookies):
    
    bonita_cookies_data = {
        'BOS_Locale': bonita_cookies.BOS_Locale,
        'JSESSIONID': bonita_cookies.JSESSIONID,
        'X-Bonita-API-Token': bonita_cookies.X_Bonita_API_Token,
    }
    return bonita_cookies_data


def bonita_login(username, password):
    # Define the Bonita login endpoint URL
    print(f'{BONITA_URL}/bonita/loginservice')
    bonita_login_url = f'{BONITA_URL}/bonita/loginservice'

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
    

def bonita_check_processes(bonita_cookies):
    # Define the Bonita check processes endpoint URL
    bonita_check_processes_url = f'{BONITA_URL}/bonita/API/bpm/process?c=100&p=0'

    # Send a GET request to the Bonita API with the provided cookies
    print(bonita_cookies)
    response = requests.get(bonita_check_processes_url, cookies=bonita_cookies)

    if response.status_code == 200:
        return response
    else:
        raise Exception(f"Bonita check processes failed with status code {response.status_code}: {response.text}")


def bonita_instantiate_process(id, data, headers,cookies):
    # Send a POST request to the Bonita API for process instantiation
    url = f'{BONITA_URL}/bonita/API/bpm/process/{id}/instantiation'
    
    response = requests.post(url, json=data, headers=headers, cookies=cookies)

    if response.status_code == 200:
        return response
    else:
        raise Exception(f"Bonita check processes failed with status code {response.status_code}: {response.text}")


def bonita_user_tasks(cookies):
    # Define the Bonita user tasks endpoint URL
    bonita_user_tasks_url = f'{BONITA_URL}/bonita/API/bpm/userTask?c=100&p=0'

    response = requests.get(bonita_user_tasks_url, cookies=cookies)

    if response.status_code == 200:
        return response
    else:
        raise Exception(f"Fetching Bonita user tasks failed with status code {response.status_code}: {response.text}")


def bonita_execute_user_task(task_id, data, headers,cookies):
    # Define the Bonita execute user task endpoint URL
    bonita_execute_user_task_url = f'{BONITA_URL}/bonita/API/bpm/userTask/{task_id}/execution'

    response = requests.post(bonita_execute_user_task_url, json=data, headers=headers, cookies=cookies)
    
    if response.status_code == 200:
        return response
    else:
        raise Exception(f"Bonita check processes failed with status code {response.status_code}: {response.text}")