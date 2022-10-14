from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from university.models import University
from university.serializers import UniversitySerializer


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
        search = self.request.GET.get('search', '')
        if search == '':
            return Response ({'detail': '검색어가 비어있습니다'}, status=status.HTTP_404_NOT_FOUND)
        
        university_search = University.objects.filter(
            Q(name__icontains=search) 
            | Q(country__code__icontains=search)
            )
        search_list = university_search.order_by('-pk')
    
        page_limit = int(self.request.GET.get('page-limit', 10))
        page = int(self.request.GET.get('page', 1))
        start_obj = page_limit * (page-1)
        end_obj = page * page_limit
        
        serializer = UniversitySerializer(search_list[start_obj:end_obj], many=True)
        return Response (serializer.data, status=status.HTTP_200_OK)