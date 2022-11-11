# university
대학교 정보의 ***오픈 소스 데이터셋을 활용*** 하여 해외 대학의 정보를 수집 ***사용자들의 대학 선호도를 확인*** 할 수 있는 API를 구현하기 위한 개인 프로젝트

<img src="https://img.shields.io/badge/Python-3.9.10-3776AB?style=flat-square&logo=Python&logoColor=white"/> <img src="https://img.shields.io/badge/Django-092E20?style=flat-square&logo=Django&logoColor=white"/> <img src="https://img.shields.io/badge/Django REST framework-092E20?style=flat-square&logo=Django REST framework&logoColor=white"/> [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


### 목차
[1. 구현기능](#구현기능) <br>
[2. API](#api) <br>
[3. ERD](#erd) <br>
[4. 컨벤션](#컨벤션) <br>

---

### 구현기능

<details>
<summary>
1. Django 권장 password 규칙을 적용한 사용자 회원가입
</summary>
</br>
    
AUTH_PASSWORD_VALIDATORS 적용
    
```python
class UserSignupSerializer(serializers.ModelSerializer):
    def validate(self, data):
        validate_password(data["password"])
        return data

```
</details>

<details>
<summary>
2. 사용자 더미데이터 생성 로직
</summary>
</br>

seed_users.py 에 새로운 명령어에 대한 로직 작성<br>
아래의 명령어를 통해 사용자의 더미데이터 1000개 생성 구현
```shell
python manage.py seed_users --total 1000
```

</details>

<details>
<summary>
3. 대학교 검색
</summary>
</br>

1. 검색기능

```python
search = self.request.GET.get('search', '')
if search == '':
    return Response ({'detail': '검색어가 비어있습니다'}, status=status.HTTP_404_NOT_FOUND)

university_search = University.objects.filter(
    Q(name__icontains=search) 
    | Q(country__code__icontains=search)
    )
```

2. 정렬기능

```python
`search_list = university_search.order_by('-pk')`
````

3. 페이징
```python
page_limit = int(self.request.GET.get('page-limit', 10))
page = int(self.request.GET.get('page', 1))
start_obj = page_limit * (page-1)
end_obj = page * page_limit

serializer = UniversitySerializer(search_list[start_obj:end_obj], many=True)
````

</details>

<details>
<summary>
4. 사용자별 선호대학 더미데이터 생성 로직 모든 사용자에게 랜덤한 20개의 선호대학교 할당
</summary>
</br>

데이터 분석을 위해 대학교는 1000개로 제한

```python
all_user = User.objects.all()
  for user in all_user:
      while user.universitypreference_set.count() <= 20:
          UniversityPreference.objects.create(user=user, university_id=randrange(1,1000))
```

</details>

<details>
<summary>
5. View를 반복 실행하더라도 오버되는 데이터 생성을 방지
</summary>
</br>

`get_or_create` 사용

</details>


---

### API

<img width="700" alt="스크린샷 2022-10-21 오후 12 19 48" src="https://user-images.githubusercontent.com/104303285/197103729-d67e3e67-66bd-4c24-a068-6008e2801cd4.png">




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
