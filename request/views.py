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
from .models import User
from django.db.models import Q


class UserSerializerNested(serializers.Serializer):
    id = serializers.IntegerField()
    email = serializers.EmailField()
    avatar = serializers.CharField()
    username = serializers.CharField()



# url = 'http://127.0.0.1:8001/api/train/'
url = 'https://0ef4-117-2-255-218.ngrok.io/api/'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class CreateProjectAPI(APIView):
    def post(self, request):
        print("Sending....")
        user_id = request.data.get('user_id')
        file = request.FILES.get("file")
        name = request.data.get("name")
        create_time = request.data.get("create_at")
        
        try:
            user = User.objects.get(id=user_id)
        except:
            print("Couldn't create", user_id)
        serializer = ProjectSerializerCreate(data={
            'user': user.id,
            # 'user': user,
            'name': request.data.get('name'),
            'progress': 0,
            'status': 'waiting',
            'link_drive': ""
        })
        
        if serializer.is_valid():
            project = serializer.save()
            prj_id = project.id
            print("--------000---", prj_id)
            data = {
                'user_id': user_id,
                'project_id': prj_id,
                'name': name,
                'create_time':create_time
                }
            files = {'file': file}
            url_worker_create = url + 'train/'
            response = requests.post(url_worker_create, data=data, files=files)
            return Response({"message": "Create Projecf Succesfully.", "data": serializer.data}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UpdateProject(APIView):
    def put(self, request, project_id):
        try:
            project = Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            return Response({'error': 'Project does not exist', 'status': 404}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            Response({'message': "Update project successfully", 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'message': "Update project Fail", 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class ListAllProjects(APIView):
    def get(self, request):
        projects = Project.objects.all()
        data = []

        for project in projects:
            project_serializer = ProjectSerializer(project)
            data.append(project_serializer.data)
        
        return Response({'message': "Get project successfully", 'data': data}, status=status.HTTP_200_OK)


class GetProjectByID(APIView):
    def get(self, request):
        project_id = request.query_params.get('q')
        try:
            project = Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            return Response({'error': 'Project does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProjectSerializer(project)
        return Response({'message': "Get project successfully", 'data': serializer.data}, status=status.HTTP_200_OK)

class GetUserByID(APIView):
    def get(self, request):
        user_id = request.query_params.get('q')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

       
        user_data = UserSerializerNested(user).data

        response_data = {
            'message': f'Information for user with id {user_id}',
            'data': {
                'user': user_data,
            }
        }

        return Response(response_data, status=status.HTTP_200_OK)

class DeleteProject(APIView):
    def delete(self, request, project_id):
        try:
            project = Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            return Response({'error': 'Project does not exist'}, status=status.HTTP_404_NOT_FOUND)

        project.delete()
        return Response({'message': f'Project id={project_id} deleted successfully'}, status=status.HTTP_200_OK)
    
class SearchAPI(APIView):
    def get(self, request):
        query = request.query_params.get('q')
        if query:
            user_results = User.objects.filter(Q(username__icontains=query) | Q(email__icontains=query))
            user_serializer = UserSerializer(user_results, many=True)

            project_results = Project.objects.filter(name__icontains=query)
            project_serializer = ProjectSerializer(project_results, many=True)

            response_data = {
                'users': user_serializer.data,
                'projects': project_serializer.data
            }

            return Response({'data':response_data, 'message': 'Get Data By Query' }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No search query provided'}, status=status.HTTP_400_BAD_REQUEST)

class RegisterAPI(APIView):
    def post(self, request):
        data = request.data
        serializers = UserSerializer(data=data)

        if serializers.is_valid():
            serializers.save()
            return Response({
                'status': 200,
                'message': 'User registered successfully, please check your Email to confirm',
                'data': serializers.data
            })

        return Response({
            'status': 400,
            'message': 'User registration failed, please try again',
            'data': serializers.errors
        })


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
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

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
                'message': 'Invalid input, please provide valid email and password',
            })

class InforUser(APIView):
    def get(self, request):
        user_id = request.query_params.get('q')
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
    
class DashboardProjectAPI(APIView):
    def get(self, request):
        users = User.objects.all()
        user_data = []
        
        for user in users:
            projects = Project.objects.filter(user=user)
            serializer = ProjectSerializer(projects, many=True)
            user_data.append({
                'user': UserSerializer(user).data,
                'projects': serializer.data
            })

        response_data = {
            'message': "Get all projects successfully",
            'data': user_data
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


class CheckWorker(APIView):
    def get(self, request):
        url_check_status = url + 'use_manage/check/'
        res = requests.get(url_check_status)
        if(res.status_code == 200):
            return Response({'message': 'Running...'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Inactive...'}, status=status.HTTP_404_NOT_FOUND)


