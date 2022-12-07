import json
from random import randrange

import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.db.models import Q
from university.models import Country, University, UniversityPreference
from university.serializers import UniversitySerializer
from users.models import User


class TaskView(APIView):
    """
    post : 웹 페이지에서 제공하는 Json Data를 토대로 데이터 삽입
    """

    def post(self, request):
        url = requests.get("http://universities.hipolabs.com/search")
        text = url.text
        data = json.loads(text)
        country_name_list = []
        country_code_list = []

        for univercity_data in data:
            if univercity_data["country"] not in country_name_list:
                country_name_list.append(univercity_data["country"])
                country_code_list.append(univercity_data["alpha_two_code"])

        for index, A in enumerate(country_name_list):
            Country.objects.get_or_create(name=A, code=country_code_list[index])

        for univercity_data in data:
            country_id = Country.objects.get(name=univercity_data["country"])
            if University.objects.filter(name=univercity_data["name"]):
                pass
            else:
                University.objects.get_or_create(
                    name=univercity_data["name"],
                    webpage=univercity_data["web_pages"][0],
                    country=country_id,
                )

        all_user = User.objects.all()
        for user in all_user:
            while user.universitypreference_set.count() <= 20:
                UniversityPreference.objects.create(
                    user=user, university_id=randrange(1, 1000)
                )

        return Response({"detail": "정보 저장이 완료되었습니다"}, status=status.HTTP_201_CREATED)


class SearchView(APIView):
    def get(self, request):
        """
        대학교 검색
        search (str) : 대학교 이름이나 국가코드 검색
        page_limit (int) : 한 페이지에 보여지는 게시글 수
        page (int) : 보고자하는 페이지

        return = 검색어 있을 때 : 적용된 대학교의 pk값 내림차순을 최대 10개까지 페이징처리된 serializer.data
                검색어 없을 때 : '검색어가 비어있습니다' 알림
        """
        search = self.request.GET.get("search", "")
        if search == "":
            return Response({"detail": "검색어가 비어있습니다"}, status=status.HTTP_404_NOT_FOUND)

        university_search = University.objects.filter(
            Q(name__icontains=search) | Q(country__code__icontains=search)
        )
        search_list = university_search.order_by("-pk")

        page_limit = int(self.request.GET.get("page-limit", 10))
        page = int(self.request.GET.get("page", 1))
        start_obj = page_limit * (page - 1)
        end_obj = page * page_limit

        serializer = UniversitySerializer(search_list[start_obj:end_obj], many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RreferenceView(APIView):
    """
    post : 선호 대학 등록
    delete : 선호 대학 삭제(soft delete)
    """

    def post(self, request, university_id):
        user = request.user
        university = University.objects.get(id=university_id)

        getted_obj, created_obj = UniversityPreference.objects.get_or_create(
            university=university, user=user
        )

        if created_obj:
            if getted_obj.user.universitypreference_set.count() <= 20:
                return Response(
                    {"detail": "선호 대학으로 등록했습니다"}, status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {"detail": "선호 대학은 20개까지만 가능합니다"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        elif getted_obj.is_active is False:
            getted_obj.is_active = True
            getted_obj.save()
            return Response(
                {"detail": "선호 대학으로 등록했습니다"}, status=status.HTTP_201_CREATED
            )
        return Response(
            {"detail": "이미 선호 대학목록에 있습니다"}, status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, university_id):
        user = request.user
        university = University.objects.get(id=university_id)

        preferenced = UniversityPreference.objects.get(university=university, user=user)
        preferenced.is_active = False
        preferenced.save()
        return Response({"detail": "선호 대학목록에서 제외했습니다"}, status=status.HTTP_200_OK)
