import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import os
from rest_framework.response import Response

from .serializers import *
from .emails import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import get_user_model
User = get_user_model()


class UserSerializerNested(serializers.Serializer):
    id = serializers.IntegerField()
    email = serializers.EmailField()
    avatar = serializers.CharField()
    username = serializers.CharField()


class ProjectSerializer(serializers.ModelSerializer):
    user = UserSerializerNested()

    class Meta:
        model = Project
        fields = ['id', 'user', 'progress', 'status', 'link_drive']




url = 'http://127.0.0.1:8001/api/train/'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class CreateProjectAPI(APIView):
    def post(self, request):
        print("Sending....")
        user_id = request.data.get('user_id')
        project_id = request.data.get('project_id')
        file = request.FILES.get("file")
        name = request.data.get("name")
        create_time = request.data.get("create_at")
        print("user_id: ", user_id)
        print("project_id: ", project_id)
        print("name: ", name)

        data = {
            'user_id': user_id,
            'project_id': project_id,
            'name': name,
            'create_time':create_time
        }

        files = {'file': file}
        response = requests.post(url, data=data, files=files)
        return Response({"message":"Create project"}, status=status.HTTP_200_OK)
        # if response.status_code == 201:
        #     print("Code 200")
        #     return Response({"message":"Create project"}, status=status.HTTP_201_CREATED)
        # else:
        #     print("Gửi thất bại")
        #     return Response({'message': 'Lỗi khi gửi dự án'}, status=status.HTTP_400_BAD_REQUEST)


# class RegisterAPI(APIView):
#     def post(self, request):
#         print("->>>>>>>>>>>>>>>>>>>>>>>", request.data)
#         data = request.data
#         serializers = UserSerializer(data=data)

#         if serializers.is_valid():
#             serializers.save()
#             send_otp_via_email(serializers.data['email'])
#             return Response({
#                 'status': 200,
#                 'message': 'User registered successfully, please check your Email to confirm',
#                 'data': serializers.data
#             })

#         return Response({
#             'status': 400,
#             'message': 'User registration failed, please try again',
#             'data': serializers.errors
#         })


class VerifyOTP(APIView):
    def post(self, request):
        try:
            data = request.data
            serializers = VerifyAccountSerializer(data=data)

            if serializers.is_valid():
                email = serializers.data['email']
                otp = serializers.data['otp']

                user = User.objects.filter(email=email)
                if not user.exists():
                    return Response({
                        'status': 400,
                        'message': 'User registration failed, please try again',
                        'data': 'invalid email'
                    })

                if not user[0].otp == otp:
                    return Response({
                        'status': 400,
                        'message': 'User registration failed, please try again',
                        'data': 'wrong OTP'
                    })

                user = user.first()
                user.is_verified = True
                user.save()

                return Response({
                    'status': 200,
                    'message': 'Account has been verified',
                    'data': {
                        'email': user.email
                    }
                })

            else:
                return Response({
                    'status': 400,
                    'message': 'User registration failed, please try again',
                    'data': serializers.errors
                })
        except Exception as e:
                print('Error')
 
class LoginAPI(APIView):
    def post(self, request):
        try:
            serializers = LoginSerializer(data=request.data)

            if serializers.is_valid():
                email = serializers.validated_data['email']
                password = serializers.validated_data['password']

                user = User.objects.filter(email=email)

                if user.exists() and user.count() == 1:
                    user_data = user.first()

                    if user_data.check_password(password):
                        return Response({
                            'status': 200,
                            'message': 'User login successful',
                            'data': {
                                'user': UserSerializer(user_data).data
                            }
                        })
                    else:
                        return Response({
                            'status': 400,
                            'message': 'Wrong password or email, please try again',
                        })
                else:
                    return Response({
                        'status': 400,
                        'message': 'User login failed, please try again',
                    })
        except serializers.ValidationError:
            print(serializers.ValidationError)

class InforUser(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        projects = Project.objects.filter(user=user)
        serializer = ProjectSerializer(projects, many=True)
        user_data = UserSerializerNested(user).data

        response_data = {
            'message': f'Information for user with id {user_id}',
            'data': {
                'user': user_data,
                'projects': serializer.data
            }
        }

        return Response(response_data, status=status.HTTP_200_OK)


class Me(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')

        try:
            user = User.objects.get(id=user_id)
        except Project.DoesNotExist:
            return Response({"message": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

        response_data = {
            'message': 'Get Information successfully',
            'data': {
                'user': UserSerializer(user).data
            }
        }

        return Response(response_data, status=status.HTTP_200_OK)

