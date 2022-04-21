from django.urls import path

from person import views

urlpatterns = [
    path('create/', views.CreateUserApiView.as_view(), name='user-create'),
    path('update_password/', views.ChangePasswordApiView.as_view(), name='user-update-password'),
    path('reset_password/', views.ResetForgetPasswordView.as_view(), name='reset-password'),
    path('check_sending_password/', views.ConfirmingSendPasswordView.as_view(), name='check-send-password'),
    path('change_password/', views.ChangePasswordView.as_view(), name='change-password')
]
