from models import User
from rest_framework.validators import UniqueValidator
from rest_framework.serializers import ModelSerializer, CharField, EmailField


class UserSerializer(ModelSerializer):
    first_name = CharField(required=True)
    last_name = CharField(required=True)
    email = EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())],
                       error_messages='This email is already used')
    password = CharField(required=True, min_length=8)

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['first_name'], validated_data['last_name'],
                                        validated_data['email'], validated_data['password'])
        return user

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password']
