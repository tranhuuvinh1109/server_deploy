import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import os

url = 'http://127.0.0.1:8001/api/train/'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class CreateProjectAPI(APIView):
    def post(self, request):
        print("đang gửi dự án....")
        user_id = request.data.get('user_id')
        project_id = request.data.get('project_id')
        file = request.FILES.get("file")
        name = request.data.get("name")
        create_time = '2023'
        print("user_id: ", user_id)
        print("project_id: ", project_id)
        print("name: ", name)

        data = {
            'user_id': user_id,
            'project_id': project_id,
            'name': name
        }

        files = {'file': file}
        response = requests.post(url, data=data, files=files)

        if response.status_code == 201:
            print("Mã 200")
            return Response({"data":"ok"}, status=status.HTTP_201_CREATED)
        else:
            print("Gửi thất bại")
            return Response({'message': 'Lỗi khi gửi dự án'}, status=status.HTTP_400_BAD_REQUEST)
