from rest_framework import serializers
from . models import Song
from django.contrib.auth.models import User


class SongSerializer(serializers.ModelSerializer):

    class Meta:
        model = Song
        fields = ('title', 'artist')


class TokenSerializer(serializers.Serializer):
    """
    This serializer serializes the token data
    """
    token = serializers.CharField(max_length=200)

class UserCreateSerializer(serializers.ModelSerializer):


    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])    
        user.save()
        return user

    class Meta:
        model = User
        fields=('username','password')


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username',)