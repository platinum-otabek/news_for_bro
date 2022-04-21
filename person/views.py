import os
import string
import random

from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status, views
from django.core.mail import send_mail
from person.models import CustomeUser, ResetPasswordModel
from person.serializers import UserSerializer, ChangePasswordSerializer, SendEmailForgetPasswordSerializer, \
    ChangePasswordWithoutCredentialsSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class CreateUserApiView(generics.CreateAPIView):
    queryset = CustomeUser.objects.all()
    serializer_class = UserSerializer


class ChangePasswordApiView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated, ]

    # queryset = CustomeUser.objects.all()

    def get_object(self, queryset=None):
        user = self.request.user
        return user

    # def update(self, request, *args, **kwargs):
    #     user = self.get_object()
    #     serializer = ChangePasswordSerializer(data=request.data)
    #     if serializer.is_valid():
    #         print(serializer.validated_data['old_password'])
    #         print(serializer.validated_data)
    #         if not user.check_password(serializer.validated_data['old_password']):
    #             return Response({'old_password': ["Wrong password"]}, status=status.HTTP_400_BAD_REQUEST)
    #         user.set_password(serializer.data.get('new_password'))
    #         user.save()
    #         response = {
    #             'status': 'success',
    #             'code': status.HTTP_200_OK,
    #             'message': 'Password updated successfully',
    #             'data': []
    #         }
    #         return Response(response)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetForgetPasswordView(views.APIView):
    permission_classes = []
    serializer_class = SendEmailForgetPasswordSerializer

    def post(self, request, *args, **kwargs):
        request.data['password'] = str(random.randint(100000, 999999))
        user_email = CustomeUser.objects.filter(email=request.data['email'])
        if user_email:
            try:
                obj = ResetPasswordModel.objects.get(email=request.data['email'])
                serializer = SendEmailForgetPasswordSerializer(obj, data=request.data)
            except ResetPasswordModel.DoesNotExist:
                serializer = SendEmailForgetPasswordSerializer(data=request.data)
            if serializer.is_valid():
                data = serializer.validated_data
                email = data.get('email')
                serializer.save()
                send_mail(
                    'Your verification password  ',
                    'Password: {}'.format(data['password']),
                    email,
                    [os.getenv('EMAIL_HOST_USER')],
                    fail_silently=False,
                )
                return Response({"success": "Successfully send. Confirm this"})
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'errors': "this email is not found"})


class ConfirmingSendPasswordView(views.APIView):
    def post(self, request, *args, **kwargs):
        try:
            sendingPassword = ResetPasswordModel.objects.get(email=request.data['email'])
            serializer = SendEmailForgetPasswordSerializer(sendingPassword)

            if serializer.data['password'] == request.data['password']:
                return Response({'status': 'success'}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'wrong password'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        except ResetPasswordModel.DoesNotExist:
            return Response({'errors': "This email is not found"}, status=status.HTTP_404_NOT_FOUND)


class ChangePasswordView(views.APIView):
    def post(self, request, *args, **kwargs):
        try:
            user = CustomeUser.objects.get(email=request.data['email'])
            serializer = ChangePasswordWithoutCredentialsSerializer(user, request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': "password changed"}, status=status.HTTP_200_OK)
            else:
                return Response({'errors': serializer.errors})
        except CustomeUser.DoesNotExist:
            return Response({'errors': 'user not found'})
