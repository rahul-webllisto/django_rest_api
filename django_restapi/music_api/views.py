from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from . models import Song
from . serializers import SongSerializer, TokenSerializer, UserCreateSerializer, UserListSerializer

from rest_framework_jwt.settings import api_settings
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class ListSongsView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = (permissions.AllowAny,)

# @api_view(['GET', 'POST'])
# def song_list(request):
#     """
#     List all songs, or create a new song.

#     """

#     if request.method == 'GET':
#         songs = Song.objects.all()
#         serializer = SongSerializer(songs, many=True)        
#         return Response(serializer.data)

#     elif request.method == 'POST':                
#         serializer = SongSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def song_detail(request, pk):  
    """
    Retrieve, update or delete a song.

    """
    try:
        song = Song.objects.get(pk=pk)
    except Song.DoesNotExists:
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SongSerializer(song)        
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SongSerializer(data=request.data)
        if serializer.is_valid:
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        song.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class LoginView(generics.CreateAPIView):
    """
    POST auth/login/
    """
    # This permission class will overide the global permission
    # class setting
    permission_classes = (permissions.AllowAny,)
    serializer_class=TokenSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        username = request.data.get('username',"")
        password = request.data.get('password',"")
        user = authenticate(request,username= username, password=password)
        if user is not None:
            login(request,user)
            serializer = TokenSerializer(data={
                # using drf jwt utility functions to generate a token
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )})
            if serializer.is_valid():
                return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)



class RegisterUserView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserCreateSerializer


    def post(self,request,*args,**kwargs):
        user_serializer = UserCreateSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            data = generate_jwt_token(user, {})
            user_serializer = UserListSerializer(user)
            username=request.data.get('username',"")
            password=request.data.get('password',"")           

            return Response({
                'status': True,
                'token': data['token'],
                'data': user_serializer.data,
            }, status=status.HTTP_200_OK)

        
        else:
            return Response(data={'message':'username and passwordare required for registration'},
                status=status.HTTP_400_BAD_REQUEST
                )
        
        


def generate_jwt_token(user, data):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    data['token'] = token
    return data