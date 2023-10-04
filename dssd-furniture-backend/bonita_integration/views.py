# bonita_integration/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import BonitaAPICall,BonitaCookies
from .utils import bonita_login,bonita_check_processes,bonita_instantiate_process,bonita_user_tasks,bonita_execute_user_task,update_cookie_header
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import permissions

# Import the BonitaCookies model
from .models import BonitaCookies

# ...

class BonitaLogin(APIView):
    permission_classes = (permissions.IsAuthenticated,)
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
            
            # Save the cookies into the BonitaCookies table
            BonitaCookies.objects.create(
                user=request.user,  
                BOS_Locale=cookies_data[0].get('value', ''),
                JSESSIONID=cookies_data[1].get('value', ''),
                X_Bonita_API_Token=cookies_data[2].get('value', '')
            )
            
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        return response


class BonitaCheckProcesses(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    @swagger_auto_schema(
        operation_description="Check Bonita processes",
        responses={
            200: "Processes retrieved successfully",
            401: "Unauthorized",
            500: "Internal Server Error",
        },
    )
    def get(self, request):

        user_identifier = request.user.email 
        
        try:
            # Retrieve the BonitaCookies associated with the user
            bonita_cookies = BonitaCookies.objects.filter(user__email=user_identifier).latest('created_at')
        except BonitaCookies.DoesNotExist:
            return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)
        
        bonita_header_cookies=update_cookie_header(bonita_cookies)
        # Call the Bonita API to check processes
        response = bonita_check_processes(bonita_header_cookies)

        # Store the API call in the database
        bonita_api_call = BonitaAPICall(
            endpoint_called='/bonita/API/bpm/process?c=100&p=0',
            request_data='',
            response_data=response.json()  # Store the response data
        )
        bonita_api_call.save()

        return Response(response.json(), status=status.HTTP_200_OK)

class BonitaInstantiateProcess(APIView):
    permission_classes = (permissions.IsAuthenticated,)
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
        user_identifier = request.user.email 
        
        try:
            # Retrieve the BonitaCookies associated with the user
            bonita_cookies = BonitaCookies.objects.filter(user__email=user_identifier).latest('created_at')
        except BonitaCookies.DoesNotExist:
            return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)
        
        bonita_header_cookies=update_cookie_header(bonita_cookies)
        
        # Extract request data from the request body
        request_data = request.data

        # Add headers for the request
        headers = {
            'X-Bonita-API-Token': bonita_cookies.X_Bonita_API_Token,
            'Content-Type': 'application/json',
        }

        # Send a POST request to instantiate the Bonita process
        response = bonita_instantiate_process(process_id, request_data, headers,bonita_header_cookies)
        
        # Store the API call in the database
        bonita_api_call = BonitaAPICall(
            endpoint_called=f'/bonita/API/bpm/process/{process_id}/instantiation',
            request_data=request_data,
            response_data=response.json()  # Store the response data
        )
        bonita_api_call.save()

        return Response(response.json(), status=status.HTTP_200_OK)

class BonitaUserTasks(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        user_identifier = request.user.email 
        
        try:
            # Retrieve the BonitaCookies associated with the user
            bonita_cookies = BonitaCookies.objects.filter(user__email=user_identifier).latest('created_at')
        except BonitaCookies.DoesNotExist:
            return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)
        
        bonita_header_cookies=update_cookie_header(bonita_cookies)
        
        # Fetch user tasks from Bonita API
        response = bonita_user_tasks(bonita_header_cookies)

        # Save the API call to the database
        bonita_api_call = BonitaAPICall(
            endpoint_called='/bonita/API/bpm/userTask?c=100&p=0',
            request_data='',
            response_data=response.json()  # Assuming Bonita API returns JSON response
        )
        bonita_api_call.save()

        return Response(response.json(), status=status.HTTP_200_OK)

class BonitaExecuteUserTask(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'ticket_comment': openapi.Schema(type=openapi.TYPE_STRING, description='Comment for the user task'),
            },
        ),
    )
    def post(self, request, task_id):
        user_identifier = request.user.email 
        
        try:
            # Retrieve the BonitaCookies associated with the user
            bonita_cookies = BonitaCookies.objects.filter(user__email=user_identifier).latest('created_at')
        except BonitaCookies.DoesNotExist:
            return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)
        
        bonita_header_cookies=update_cookie_header(bonita_cookies)
        
        
        # Define the JSON data and headers for the user task execution
        request_data = request.data
        
        headers = {
            "X-Bonita-API-Token": bonita_cookies.X_Bonita_API_Token,
            "Content-Type": "application/json",
        }

        response = bonita_execute_user_task(task_id, request_data, headers,bonita_header_cookies)

        return Response(response.json(), status=status.HTTP_200_OK)