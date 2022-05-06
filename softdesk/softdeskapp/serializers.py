from rest_framework.serializers import ModelSerializer
from .models import Projects


class ProjectSerializer(ModelSerializer):

    class Meta:
        model = Projects
        fields = ['project_id', 'title', 'description', 'type', 'author_user_id']
