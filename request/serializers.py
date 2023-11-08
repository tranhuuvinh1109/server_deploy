from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ['id', 'username', 'email', 'password']
        fields = ('id', 'username', 'email','avatar', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            avatar=validated_data['avatar']
        )
        return user


class VerifyAccountSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(required=True)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)



class ProjectSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'user', 'name' , 'progress', 'status', 'link_drive']
class ProjectSerializer(serializers.ModelSerializer):
    user = UserSerializer() 
    class Meta:
        model = Project
        fields = ['id', 'user', 'name' , 'progress', 'status', 'link_drive']

