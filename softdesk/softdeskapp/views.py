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
from django.db.models import CharField, Value, Q

# Create your views here.


class ProjectsViewset(ModelViewSet):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Projects.objects.all()


class ContributorsAPIView(APIView):

    def get(self, request, pk):
        contributors = Contributors.objects.filter(project_id=pk)
        serializer = ContributorSerializer(contributors, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        try:
            contributor = Contributors()
            contributor.user_id = get_object_or_404(User, id=int(request.data['user_id']))
            contributor.project_id = Projects.objects.get(id=pk)
            contributor.permission = request.data['permission']
            contributor.role = request.data['role']
            contributor.save()
            data = {'user_id': contributor.user_id.id, 'project_id': contributor.project_id.id,
                    'permission': contributor.permission, 'role': contributor.role}
            return Response(data)
        except Exception as e:
            print(e)
            return Response({})


class ContributorDeletion(APIView):
    def get(self, request, pk, user_id):
        try:
            contributor_to_delete = Contributors.objects.filter(Q(project_id=pk) & Q(user_id=user_id))
            contributor_to_delete.delete()
            return Response({'message': f'Contributor {user_id} deleted'})
        except Exception as e:
            print(e)
            return Response({'message': 'Contributor not found'})

class IssuesViewset(ModelViewSet):
    serializer_class = IssueSerializer

    def get_queryset(self):
        return Issues.objects.all()


class CommentsViewset(ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comments.objects.all()
