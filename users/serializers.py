from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from users.models import User


class UserSignupSerializer(serializers.ModelSerializer):
    def validate(self, data):
        validate_password(data["password"])
        return data
    
    def create(self, *args, **kwargs):
        user = super().create(*args, **kwargs)
        pw = user.password
        user.set_password(pw)
        user.save()
        return user
    
    class Meta:
        model = User
        fields = '__all__'