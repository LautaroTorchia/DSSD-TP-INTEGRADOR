# bonita_integration/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import BonitaAPICall
from .serializers import BonitaAPICallSerializer
from .utils import bonita_login,bonita_check_processes
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