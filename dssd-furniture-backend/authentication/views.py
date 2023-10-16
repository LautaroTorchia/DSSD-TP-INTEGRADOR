from django.shortcuts import render
from rest_framework import generics, status, views, permissions
from .serializers import UserSerializer, RegisterSerializer, SetNewPasswordSerializer, ResetPasswordEmailRequestSerializer, EmailVerificationSerializer, LoginSerializer, LogoutSerializer
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.viewsets import ViewSet
from .models import User
from resources.models import Resource
from .utils import Util, StandardSend
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .renderers import UserRenderer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.shortcuts import redirect
from django.http import HttpResponsePermanentRedirect
import os
from rest_framework_tracking.mixins import LoggingMixin
from tablib import Dataset
from .resources import UserResource
from .serializers import UploadSerializer
from general_permissions.permissions import IsPermittedRBAC

class CustomRedirect(HttpResponsePermanentRedirect):

    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']


class RegisterView(LoggingMixin, generics.GenericAPIView):

    serializer_class = RegisterSerializer
    permission_classes = (permissions.IsAuthenticated, IsPermittedRBAC,)
    renderer_classes = (UserRenderer,)

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(LoggingMixin, views.APIView):
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated!'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:            
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:            
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(LoggingMixin, generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_authentication(request)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class RequestPasswordResetEmail(LoggingMixin, generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(
                request=request).domain
            relativeLink = reverse(
                'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

            redirect_url = request.data.get('redirect_url', '')
            absurl = 'http://'+current_site + relativeLink
            email_body = 'Hello, \n Use link below to reset your password  \n' + \
                absurl+"?redirect_url="+redirect_url
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your passsword'}
            Util.send_email(data)
        return Response({'success': 'We have sent you a link to reset your password. Please check.'}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(LoggingMixin, generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):

        redirect_url = request.GET.get('redirect_url')

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                if len(redirect_url) > 3:
                    return CustomRedirect(redirect_url+'?token_valid=False')
                else:
                    return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

            if redirect_url and len(redirect_url) > 3:
                return CustomRedirect(redirect_url+'?token_valid=True&message=Credentials Valid&uidb64='+uidb64+'&token='+token)
            else:
                return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

        except DjangoUnicodeDecodeError as identifier:
            try:
                if not PasswordResetTokenGenerator().check_token(user):                    
                    return CustomRedirect(redirect_url+'?token_valid=False')
                    
            except UnboundLocalError as e:                
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)



class SetNewPasswordAPIView(LoggingMixin, generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)


class LogoutAPIView(LoggingMixin, generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (permissions.IsAuthenticated, IsPermittedRBAC,)

    def post(self, request):        
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

class UserListAPIView(LoggingMixin, ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsPermittedRBAC,)

    def perform_create(self, serializer):        
        return serializer.save()

    def get_queryset(self):        
        return self.queryset
        

class UserDetailAPIView(LoggingMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsPermittedRBAC,)
    queryset = User.objects.all()
    lookup_field = "id"    

    def get_queryset(self):
        return self.queryset

class DynamicSearchFilter(SearchFilter):
    def get_search_fields(self, view, request):
        return request.GET.getlist('search_fields', [])

class UserListView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsPermittedRBAC,)
    queryset = User.objects.all()
    filter_backends = (DynamicSearchFilter, OrderingFilter)

class UploadViewSet(LoggingMixin, ViewSet):
    serializer_class = UploadSerializer
    permission_classes = (permissions.IsAuthenticated, IsPermittedRBAC,)

    def list(self, request):
        return Response("GET API")
    def create(self, request):        
        user_resource = UserResource()
        dataset = Dataset()
        try:
            file_uploaded = request.FILES.get('file_uploaded')
            content_type = file_uploaded.content_type
            if file_uploaded._name.endswith('.xlsx'):            
                imported_data = dataset.load(file_uploaded.read())        
                result = user_resource.import_data(dataset, dry_run=True)        
                if not result.has_errors():            
                    user_resource.import_data(dataset, dry_run=False)
                    return Response({'message': 'The data has been loaded correctly.'}, status=status.HTTP_200_OK)
                else:
                    error_detail = "Charging error. Details:\n\n"
                    for n in result.rows:
                        for e in n.__dict__['errors']:
                            error_detail += str(e.__dict__['error']) + "\n"
                    return Response({'error': error_detail}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'File error. Please select an XLSX file.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            from progralog.utils import generic_progra_log_error
            message = generic_progra_log_error()
            return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)
