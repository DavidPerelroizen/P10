from rest_framework.serializers import ModelSerializer
from .models import Projects, Contributors, Issues, Comments


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comments
        fields = ['description', 'author_user_id', 'issue_id']


class IssueSerializer(ModelSerializer):
    comments = CommentSerializer(many=True, required=False)

    class Meta:
        model = Issues
        fields = ['title', 'desc', 'tag', 'priority', 'project_id', 'status', 'author_user_id', 'assignee_user_id',
                  'comments']


class ContributorSerializer(ModelSerializer):

    class Meta:
        model = Contributors
        fields = ['user_id', 'project_id', 'permission', 'role']


class ProjectSerializer(ModelSerializer):
    contributors = ContributorSerializer(many=True, required=False)
    issues = IssueSerializer(many=True, required=False)

    class Meta:
        model = Projects
        fields = ['title', 'description', 'type', 'author_user_id', 'contributors', 'issues']
