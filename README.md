# university


### API
<img width="600" alt="스크린샷 2022-10-14 오후 10 21 20" src="https://user-images.githubusercontent.com/104303285/195862324-d2d55c3f-240b-4dab-a542-71d3dd1b8a61.png">

---

### ERD
<img width="600" alt="스크린샷 2022-10-14 오후 10 23 47" src="https://user-images.githubusercontent.com/104303285/195862393-805db56f-7bef-4e42-84ed-04a483d467e7.png">

---

### 컨벤션
- 코드
    - Class : Pascal
    - Variable : Snake
    - Function : Snake
    - Constant : Pascal + Snake
    
- commit
    - add/ 새로운 프로젝트, 앱, 설정
    - feat/ 기능
    - enhan/ 기존 코드의 기능을 추가
    - refac/ 코드 리팩토링
    - fix/ 버그
    - test/ 테스트 코드
    - docs/ 파일을 수정
    - comment/ 주석

---

### 문제 해결 과정

1. Django 권장 password 규칙을 적용한 사용자 회원가입 -> AUTH_PASSWORD_VALIDATORS 적용

```python
class UserSignupSerializer(serializers.ModelSerializer):
    def validate(self, data):
        validate_password(data["password"])
        return data
```

2. 대학교 검색

<br>

2-1. 검색기능
```python
search = self.request.GET.get('search', '')
if search == '':
    return Response ({'detail': '검색어가 비어있습니다'}, status=status.HTTP_404_NOT_FOUND)

university_search = University.objects.filter(
    Q(name__icontains=search) 
    | Q(country__code__icontains=search)
    )
```

2-2. 정렬기능
```python
`search_list = university_search.order_by('-pk')`
````

2-3. 페이징
```python
page_limit = int(self.request.GET.get('page-limit', 10))
page = int(self.request.GET.get('page', 1))
start_obj = page_limit * (page-1)
end_obj = page * page_limit

serializer = UniversitySerializer(search_list[start_obj:end_obj], many=True)
````

3. 사용자 더미데이터 생성 로직
seed_users.py 에 새로운 명령어에 대한 로직 작성<br>
아래의 명령어를 통해 사용자의 더미데이터 1000개 생성 구현
```shell
python manage.py seed_users --total 1000
```

4. 사용자별 선호대학 더미데이터 생성 로직
모든 사용자에게 랜덤한 20개의 선호대학교 할당 <br>
데이터 분석을 위해 대학교는 1000개로 제한

```python
all_user = User.objects.all()
  for user in all_user:
      while user.universitypreference_set.count() <= 20:
          UniversityPreference.objects.create(user=user, university_id=randrange(1,1000))
```

5. View를 반복 실행하더라도 오버되는 데이터 생성을 방지하기 위해, `get_or_create` 사용

---

### 내가 수정한 사항들
- UniversityPreference 모델에서 `user_id` 를 `User FK` 로 사용
- soft delete 를 구현하기 위해 UniversityPreference 모델의 `is_active` 추가

---

### 추가하고 싶은 기능들
- 로직들이 무겁기 때문에 apsheduler 사용하는 등 사용자가 없는 시간대에 무거운 로직들이 시행되도록 적용
- 로그인한 사용자는 본인 뿐만 아니라 다른 사용자들의 선호대학교 데이터를 바탕으로 대학교 순위 기능 구현

