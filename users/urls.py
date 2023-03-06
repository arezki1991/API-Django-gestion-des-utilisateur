from django.urls import path
from .views import UserListCreate, UserDetail, ProfileDetail, api_root, user_list_create
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', api_root, name='api_root'),
    path('<int:pk>/', UserDetail.as_view(), name='user_detail'),
    path('profiles/<int:pk>/', ProfileDetail.as_view(), name='profile_detail'),
    path('users/', user_list_create, name='user_list_create'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
