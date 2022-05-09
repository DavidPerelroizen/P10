from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from .models import Projects, Contributors, Issues, Comments

# Create your views here.


class ProjectsViewset(ModelViewSet):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Projects.objects.all()


class ContributorsViewset(ModelViewSet):
    serializer_class = ContributorSerializer

    def get_queryset(self):
        return Contributors.objects.all()


class IssuesViewset(ModelViewSet):
    serializer_class = IssueSerializer

    def get_queryset(self):
        return Issues.objects.all()


class CommentsViewset(ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comments.objects.all()
