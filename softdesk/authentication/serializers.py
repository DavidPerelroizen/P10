from rest_framework.serializers import ModelSerializer, CharField, EmailField
from django.contrib.auth.models import User


class UserSerializer(ModelSerializer):
    first_name = CharField(required=True)
    last_name = CharField(required=True)
    email = EmailField(required=True, validators=None)
    password = CharField(required=True, min_length=8, write_only=True)
    username = CharField(required=True)

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], first_name=validated_data['first_name'],
                                        last_name=validated_data['last_name'],
                                        email=validated_data['email'], password=validated_data['password'])
        return user

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
