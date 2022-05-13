from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.views import APIView
from .serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from .models import Projects, Contributors, Issues, Comments
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action, api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.db import models
import json
from django.contrib.auth.models import User

# Create your views here.


class ProjectsViewset(ModelViewSet):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Projects.objects.all()


class ContributorsAPIView(APIView):

    def get(self, request, pk):
        print(User.objects.all())
        contributors = Contributors.objects.get(project_id=pk)
        serializer = ContributorSerializer(contributors)
        return Response(serializer.data)

    def post(self, request, pk):
        contributor = Contributors()
        contributor.user_id = request.data['user_id']
        contributor.project_id = pk
        contributor.permission = request.data['permission']
        contributor.role = request.data['role']
        serializer = ContributorSerializer(contributor)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IssuesViewset(ModelViewSet):
    serializer_class = IssueSerializer

    def get_queryset(self):
        return Issues.objects.all()


class CommentsViewset(ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comments.objects.all()
