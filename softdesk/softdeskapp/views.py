from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from .models import Projects, Contributors, Issues, Comments
from rest_framework.response import Response
from rest_framework.decorators import action

# Create your views here.


class ProjectsViewset(ModelViewSet):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Projects.objects.all()


class ContributorsViewset(ModelViewSet):
    serializer_class = ContributorSerializer
    queryset = Contributors.objects.all()

    @action(detail=True, methods=['get'])
    def users(self, request, pk):
        project_contributors = Contributors.objects.filter(project_id=pk)
        serializer = self.get_serializer(project_contributors, many=True)
        return Response(serializer.data)


class IssuesViewset(ModelViewSet):
    serializer_class = IssueSerializer

    def get_queryset(self):
        return Issues.objects.all()


class CommentsViewset(ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comments.objects.all()
