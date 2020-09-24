from django.urls import path
from user.views import CreateUserApi, CreateTokenView, ManageUserView

app_name = 'user'

urlpatterns = [
    path('create/', CreateUserApi.as_view(), name='create'),
    path('token/', CreateTokenView.as_view(), name='token'),
    path('me/', ManageUserView.as_view(), name='me')
]
