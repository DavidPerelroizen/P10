from rest_framework.serializers import ModelSerializer
from .models import Projects, Contributors, Issues, Comments


class ProjectSerializer(ModelSerializer):

    class Meta:
        model = Projects
        fields = ['title', 'description', 'type', 'author_user_id']


class ContributorSerializer(ModelSerializer):

    class Meta:
        model = Contributors
        fields = ['user_id', 'project_id', 'permission', 'role']


class IssueSerializer(ModelSerializer):
    class Meta:
        model = Issues
        fields = ['title', 'desc', 'tag', 'priority', 'project_id', 'status', 'author_user_id', 'assignee_user_id']


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comments
        fields = ['description', 'author_user_id', 'issue_id']