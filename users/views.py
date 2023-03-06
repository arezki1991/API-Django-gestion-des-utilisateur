from django.shortcuts import get_object_or_404
from rest_framework import generics
from .models import User, Profile
from .serializers import UserSerializer, ProfileSerializer
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.urls import reverse
@api_view(['GET', 'POST'])
def user_list_create(request, format=None):
    if request.method == 'GET':
        users = Profile.objects.all()
        serializer = ProfileSerializer(users, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@permission_classes([AllowAny])

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user_list_create', args=None, request=request, format=format),
    })

class UserListCreate(generics.ListCreateAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.all()
        city = self.request.query_params.get('city', None)
        age_min = self.request.query_params.get('age_min', None)
        age_max = self.request.query_params.get('age_max', None)
        gender = self.request.query_params.get('gender', None)

        if city:
            queryset = queryset.filter(profile__hometown=city)
        if age_min and age_max:
            queryset = queryset.filter(profile__age__gte=age_min, profile__age__lte=age_max)
        if gender:
            queryset = queryset.filter(profile__gender=gender)

        print("Queryset: ", queryset)
        print("Serialized data: ", UserSerializer(queryset, many=True).data)

        return queryset

    def perform_create(self, serializer):
        profile_serializer = ProfileSerializer(data=self.request.data['profile'])
        profile_serializer.is_valid(raise_exception=True)
        profile = profile_serializer.save()
        serializer.save(profile=profile)
class UserList(generics.ListAPIView):
    serializer_class = UserSerializer
    @api_view(['POST'])
    @permission_classes([AllowAny])
    def get_queryset(self):
        queryset = User.objects.all()
        city = self.request.query_params.get('city', None)
        age_min = self.request.query_params.get('age_min', None)
        age_max = self.request.query_params.get('age_max', None)
        gender = self.request.query_params.get('gender', None)

        if city:
            queryset = queryset.filter(profile__hometown=city)
        if age_min and age_max:
            queryset = queryset.filter(profile__age__gte=age_min, profile__age__lte=age_max)
        if gender:
            queryset = queryset.filter(profile__gender=gender)

        print("Queryset: ", queryset)
        print("Serialized data: ", UserSerializer(queryset, many=True).data)

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ProfileDetail(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

