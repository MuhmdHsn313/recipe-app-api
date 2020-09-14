from django.urls import path
from user.views import CreateUserApi, CreateTokenView

app_name = 'user'

urlpatterns = [
    path('create', CreateUserApi.as_view(), name='create'),
    path('token', CreateTokenView.as_view(), name='token')
]
