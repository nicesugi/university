from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializers import UserSignupSerializer


class UserView(APIView):
    def post(self, request):
        user_data_serializer = UserSignupSerializer(data=request.data)
        user_data_serializer.is_valid(raise_exception=True)
        user_data_serializer.save()
        return Response({"detail": "회원가입을 성공하였습니다"}, status=status.HTTP_201_CREATED)
