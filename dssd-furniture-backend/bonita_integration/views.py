# bonita_integration/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import BonitaAPICall,BonitaCookies
from general_permissions.permissions import IsPermittedRBAC
from .utils import bonita_check_processes,bonita_instantiate_process,bonita_user_tasks,bonita_execute_user_task
from .utils import update_cookie_header,bonita_get_variable,change_bonita_variable,bonita_archived_tasks
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import permissions
from .models import BonitaCookies

class BonitaCheckProcesses(APIView):
    permission_classes = (permissions.IsAuthenticated,IsPermittedRBAC,)
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
            print("hola",bonita_cookies.X_Bonita_API_Token)
        except BonitaCookies.DoesNotExist:
            return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)
        
        bonita_header_cookies=update_cookie_header(bonita_cookies)
        # Call the Bonita API to check processes
        response = bonita_check_processes(bonita_header_cookies)

        # Store the API call in the database
        bonita_api_call = BonitaAPICall(
            endpoint_called='/bonita/API/bpm/process?c=100&p=0',
            request_data='',
            response_data=''  # Store the response data
        )
        bonita_api_call.save()

        return response

class BonitaInstantiateProcess(APIView):
    permission_classes = (permissions.IsAuthenticated,IsPermittedRBAC,)
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
            response_data='' # Store the response data
        )
        bonita_api_call.save()

        return response

class BonitaUserTasks(APIView):
    permission_classes = (permissions.IsAuthenticated,IsPermittedRBAC,)
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
            response_data=''  # Assuming Bonita API returns JSON response
        )
        bonita_api_call.save()

        return response

class BonitaArchivedTasksView(APIView):
    permission_classes = (permissions.IsAuthenticated, IsPermittedRBAC,)

    def get(self, request):
        user_identifier = request.user.email

        try:
            # Retrieve the BonitaCookies associated with the user
            bonita_cookies = BonitaCookies.objects.filter(user__email=user_identifier).latest('created_at')
        except BonitaCookies.DoesNotExist:
            return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)

        bonita_header_cookies = update_cookie_header(bonita_cookies)

        # Fetch user tasks from Bonita API using the bonita_user_tasks function
        response = bonita_archived_tasks(bonita_header_cookies)

        # Save the API call to the database
        bonita_api_call = BonitaAPICall(
            endpoint_called='/bonita/API/bpm/archivedTask?c=100&p=0',
            request_data='',
            response_data=response.data  # Assuming Bonita API returns JSON response
        )
        bonita_api_call.save()

        return response
    
class BonitaExecuteUserTask(APIView):
    permission_classes = (permissions.IsAuthenticated,IsPermittedRBAC,)
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
        
        return response


class BonitaCaseVariable(APIView):
    permission_classes = (permissions.IsAuthenticated,IsPermittedRBAC,)

    def get(self, request, id_instancia, variablename):
        user_identifier = request.user.email

        try:
            # Retrieve the BonitaCookies associated with the user
            bonita_cookies = BonitaCookies.objects.filter(user__email=user_identifier).latest('created_at')
        except BonitaCookies.DoesNotExist:
            return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)

        bonita_header_cookies = update_cookie_header(bonita_cookies)

        return bonita_get_variable(id_instancia,variablename,bonita_header_cookies)



class BonitaUpdateCaseVariable(APIView):
    permission_classes = (permissions.IsAuthenticated,IsPermittedRBAC,)
    @swagger_auto_schema(
        operation_description="Update a Bonita case variable",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "type": openapi.Schema(type=openapi.TYPE_STRING, description="The variable type"),
                "value": openapi.Schema(type=openapi.TYPE_STRING, description="The new value"),
            },
            required=["type", "value"],
        ),
        responses={
            200: "Variable updated successfully",
            401: "Unauthorized",
            500: "Internal Server Error",
        },
    )
    
    def put(self, request, id_instancia, variablename):
        user_identifier = request.user.email

        try:
            # Retrieve the BonitaCookies associated with the user
            bonita_cookies = BonitaCookies.objects.filter(user__email=user_identifier).latest('created_at')
        except BonitaCookies.DoesNotExist:
            return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)

        bonita_header_cookies = update_cookie_header(bonita_cookies)
        data = request.data
        print(data)
        return change_bonita_variable(id_instancia,variablename,bonita_cookies,bonita_header_cookies,data)