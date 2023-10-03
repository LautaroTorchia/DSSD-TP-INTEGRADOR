# bonita_integration/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import BonitaAPICall
from .serializers import BonitaAPICallSerializer
from .utils import bonita_login,bonita_check_processes,bonita_instantiate_process,bonita_user_tasks,bonita_execute_user_task
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class BonitaLogin(APIView):
    @swagger_auto_schema(
        operation_description="Authenticate with Bonita",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['username', 'password'],
        ),
        responses={
            204: "Authentication successful",
            400: "Bad Request",
            401: "Unauthorized",
            500: "Internal Server Error",
        },
    )
    def post(self, request):
        
        username = request.data.get('username')
        password = request.data.get('password')

        response = bonita_login(username, password)
        print(response.status_code)
        if response.status_code == 204:
            cookies = response.cookies
            cookies_data = [{'name': cookie.name, 'value': cookie.value} for cookie in cookies]

            bonita_api_call = BonitaAPICall(
                endpoint_called='/bonita/loginservice',
                request_data=f"username={username}&password={password}",
                response_data=cookies_data 
            )
            bonita_api_call.save()
            
            #Guardo las cookies en la session del usuario para proximas requests
            request.session['bonita_cookies'] = {cookie.name: cookie.value for cookie in cookies}
            request.session.modified = True
            
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        return response


class BonitaCheckProcesses(APIView):
    @swagger_auto_schema(
        operation_description="Check Bonita processes",
        responses={
            200: "Processes retrieved successfully",
            401: "Unauthorized",
            500: "Internal Server Error",
        },
    )
    def get(self, request):
        # Check if the user is authenticated based on session cookies
        bonita_cookies = request.session.get('bonita_cookies')
        
        if not bonita_cookies:
            return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)

        # Call the Bonita API to check processes
        response = bonita_check_processes(bonita_cookies)
        
        # Store the API call in the database
        bonita_api_call = BonitaAPICall(
            endpoint_called='/bonita/API/bpm/process?c=100&p=0',
            request_data='',
            response_data=response.json()  # Store the response data
        )
        bonita_api_call.save()

        return Response(response.json(), status=status.HTTP_200_OK)

class BonitaInstantiateProcess(APIView):
    @swagger_auto_schema(
        operation_description="Instantiate a Bonita process",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "ticket_account": openapi.Schema(type=openapi.TYPE_STRING),
                "ticket_description": openapi.Schema(type=openapi.TYPE_STRING),
                "ticket_subject": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            201: "Process instantiated successfully",
            401: "Unauthorized",
            500: "Internal Server Error",
        },
    )
    def post(self, request, process_id):
        # Check if the user is authenticated based on session cookies
        bonita_cookies = request.session.get('bonita_cookies')
        if not bonita_cookies:
            return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)

        # Extract request data from the request body
        request_data = request.data

        # Add headers for the request
        headers = {
            'X-Bonita-API-Token': bonita_cookies['X-Bonita-API-Token'],
            'Content-Type': 'application/json',
        }

        # Send a POST request to instantiate the Bonita process
        response = bonita_instantiate_process(process_id, request_data, headers,bonita_cookies)
        
        # Store the API call in the database
        bonita_api_call = BonitaAPICall(
            endpoint_called=f'/bonita/API/bpm/process/{process_id}/instantiation',
            request_data=request_data,
            response_data=response.json()  # Store the response data
        )
        bonita_api_call.save()

        return Response(response.json(), status=status.HTTP_200_OK)

class BonitaUserTasks(APIView):
    def get(self, request):
        bonita_cookies = request.session.get('bonita_cookies')
        if not bonita_cookies:
            return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)
        
        # Fetch user tasks from Bonita API
        response = bonita_user_tasks(bonita_cookies)

        # Save the API call to the database
        bonita_api_call = BonitaAPICall(
            endpoint_called='/bonita/API/bpm/userTask?c=100&p=0',
            request_data='',
            response_data=response.json()  # Assuming Bonita API returns JSON response
        )
        bonita_api_call.save()

        return Response(response.json(), status=status.HTTP_200_OK)

class BonitaExecuteUserTask(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'ticket_comment': openapi.Schema(type=openapi.TYPE_STRING, description='Comment for the user task'),
            },
        ),
    )
    def post(self, request, task_id):
        bonita_cookies = request.session.get('bonita_cookies')
        if not bonita_cookies:
            return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)
        
        # Define the JSON data and headers for the user task execution
        request_data = request.data
        
        headers = {
            "X-Bonita-API-Token": bonita_cookies['X-Bonita-API-Token'],
            "Content-Type": "application/json",
        }

        response = bonita_execute_user_task(task_id, request_data, headers,bonita_cookies)

        return Response(response.json(), status=status.HTTP_200_OK)