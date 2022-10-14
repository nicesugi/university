# Generated by Django 4.1.2 on 2022-10-14 10:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=2, verbose_name='국가 2자리 코드')),
                ('name', models.CharField(max_length=255, verbose_name='국가 영문이름')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성일시')),
            ],
        ),
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('webpage', models.CharField(max_length=255, null=True, verbose_name='대학교 사이트 주소')),
                ('name', models.CharField(max_length=255, null=True, verbose_name='대학교 이름')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성일시')),
                ('country', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='university.country', verbose_name='국가')),
            ],
        ),
        migrations.CreateModel(
            name='UniversityPreference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성일시')),
                ('deleted_at', models.DateTimeField(auto_now=True, verbose_name='삭제일시')),
                ('university', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='university.university', verbose_name='대학교')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='사용자')),
            ],
        ),
    ]
