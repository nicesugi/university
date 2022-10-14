from django.db import models


class Country(models.Model):
    code = models.CharField('국가 2자리 코드', max_length=2)
    name = models.CharField('국가 영문이름', max_length=255)
    created_at = models.DateTimeField('생성일시', auto_now_add=True)

    def __str__(self):
        return f'{self.code} / {self.name}'
    
class University(models.Model):
    country = models.ForeignKey(Country, verbose_name='국가', on_delete=models.SET_NULL, null=True)
    webpage = models.CharField('대학교 사이트 주소', max_length=255, null=True)
    name = models.CharField('대학교 이름', max_length=255, null=True)
    created_at = models.DateTimeField('생성일시', auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class UniversityPreference(models.Model):
    university = models.ForeignKey(University, verbose_name='대학교', on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey('users.User', verbose_name='사용자', on_delete=models.CASCADE)
    created_at = models.DateTimeField('생성일시', auto_now_add=True)
    deleted_at = models.DateTimeField('삭제일시', auto_now=True)
    
    def __str__(self):
        return f'{self.user}님이 선호하는 {self.university}'