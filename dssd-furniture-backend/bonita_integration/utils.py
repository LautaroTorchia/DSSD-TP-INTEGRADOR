import requests
from rest_framework.response import Response
from rest_framework import status
from ljj_muebles.settings import BONITA_URL
import json

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
        return Response(f"Failed to login: {response.text}", status=response.status_code)
    

def bonita_check_processes(bonita_cookies):
    # Define the Bonita check processes endpoint URL
    bonita_check_processes_url = f'{BONITA_URL}/bonita/API/bpm/process?c=100&p=0'

    # Send a GET request to the Bonita API with the provided cookies
    response = requests.get(bonita_check_processes_url, cookies=bonita_cookies)
    if response.status_code == 200:
        return Response(response.json(), status=status.HTTP_200_OK)
    else:
        return Response(f"Failed to retrieve processes: {response.text}", status=response.status_code)


def bonita_instantiate_process(id, data, headers,cookies):
    # Send a POST request to the Bonita API for process instantiation
    url = f'{BONITA_URL}/bonita/API/bpm/process/{id}/instantiation'
    
    response = requests.post(url, json=data, headers=headers, cookies=cookies)

    if response.status_code == 200:
        return Response(response.json(), status=status.HTTP_200_OK)
    else:
        Response(f"Failed to instantiate process: {response.text}", status=response.status_code)


def bonita_user_tasks(cookies):
    # Define the Bonita user tasks endpoint URL
    bonita_user_tasks_url = f'{BONITA_URL}/bonita/API/bpm/userTask?c=100&p=0'

    response = requests.get(bonita_user_tasks_url, cookies=cookies)

    if response.status_code == 200:
        return Response(response.json(), status=status.HTTP_200_OK)
    else:
        Response(f"Failed to retrieve user tasks: {response.text}", status=response.status_code)


def bonita_execute_user_task(task_id, data, headers,cookies):
    # Define the Bonita execute user task endpoint URL
    bonita_execute_user_task_url = f'{BONITA_URL}/bonita/API/bpm/userTask/{task_id}/execution?assign=true'

    response = requests.post(bonita_execute_user_task_url, json=data, headers=headers, cookies=cookies)
    
    if response.status_code == 204:
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        Response(f"Failed to execute user task: {response.text}", status=response.status_code)


def bonita_get_variable(id,variable,bonita_header_cookies):
    
    # Define the URL for the Bonita API
    bonita_case_variable_url = f'{BONITA_URL}/bonita/API/bpm/caseVariable/{id}/{variable}'

    # Make the GET request to the Bonita API
    response = requests.get(bonita_case_variable_url, cookies=bonita_header_cookies)

    if response.status_code == 200:
        return Response(response.json(), status=status.HTTP_200_OK)
    else:
        return Response(f"Failed to fetch Bonita case variable: {response.text}", status=response.status_code)
    

def change_bonita_variable(id_instancia,variablename,bonita_cookies,bonita_header_cookies,data):
    
    # Define the URL for the Bonita API
    bonita_case_variable_url = f'{BONITA_URL}/bonita/API/bpm/caseVariable/{id_instancia}/{variablename}'

    headers = {
        'X-Bonita-API-Token': bonita_cookies.X_Bonita_API_Token,
        'Content-Type': 'application/json',
    }

    # Make the PUT request to the Bonita API
    response = requests.put(bonita_case_variable_url,headers=headers,cookies=bonita_header_cookies,json=data)

    if response.status_code == 200:
        return Response("Bonita case variable updated successfully", status=status.HTTP_200_OK)
    else:
        return Response(f"Failed to update Bonita case variable: {response.text}", status=response.status_code)
