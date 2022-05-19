from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.views import APIView
from .serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from .models import Projects, Contributors, Issues, Comments
from .permissions import IsProjectCreator, IsProjectContributor, CanAccessCreateIssue, IsIssueOwner
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
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
    permission_classes = [IsProjectCreator, IsProjectContributor]

    def get_queryset(self):
        return Projects.objects.all()


class ContributorsAPIView(APIView):
    permission_classes = [IsAuthenticated]

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
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({'Contributor posting failed'}, status=status.HTTP_404_NOT_FOUND)


class ContributorDeletion(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, user_id):
        try:
            contributor_to_delete = Contributors.objects.filter(Q(project_id=pk) & Q(user_id=user_id))
            contributor_to_delete.delete()
            return Response({'message': f'Contributor {user_id} deleted'})
        except Exception as e:
            print(e)
            return Response({'message': 'Contributor not found'}, status=status.HTTP_404_NOT_FOUND)


class IssuesAPIView(APIView):
    permission_classes = [CanAccessCreateIssue]

    def get(self, request, pk):
        issues = Issues.objects.filter(project_id=pk)
        serializer = IssueSerializer(issues, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        try:
            issue = Issues()
            issue.title = request.data['title']
            issue.desc = request.data['desc']
            issue.tag = request.data['tag']
            issue.priority = request.data['priority']
            issue.project_id = Projects.objects.get(id=pk)
            issue.status = request.data['status']
            issue.author_user_id = get_object_or_404(User, id=int(request.data['author_user_id']))
            issue.assignee_user_id = get_object_or_404(User, id=int(request.data['assignee_user_id']))
            issue.save()
            data = {'title': issue.title, 'desc': issue.desc, 'tag': issue.tag, 'priority': issue.priority,
                    'project_id': issue.project_id.id, 'status': issue.status,
                    'author_user_id': issue.author_user_id.id,
                    'assignee_user_id': issue.assignee_user_id.id, 'created_time': issue.created_time}
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({'Issue posting failed'}, status=status.HTTP_404_NOT_FOUND)


class IssuesModifyAPIView(APIView):
    permission_classes = [IsIssueOwner]

    def get(self, request, pk, issue_id):
        issue_to_get = Issues.objects.filter(Q(project_id=pk) & Q(id=issue_id))
        serializer = IssueSerializer(issue_to_get, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, issue_id):
        try:
            issue_to_delete = Issues.objects.filter(Q(project_id=pk) & Q(id=issue_id))
            issue_to_delete.delete()
            return Response({'message': f'Issue {issue_id} deleted'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'message': 'Issue not found'})

    def put(self, request, pk, issue_id):
        try:
            issue = Issues.objects.filter(Q(project_id=pk) & Q(id=issue_id))
            issue_to_update = issue[0]
            issue_to_update.title = request.data['title']
            issue_to_update.desc = request.data['desc']
            issue_to_update.tag = request.data['tag']
            issue_to_update.priority = request.data['priority']
            issue_to_update.project_id = Projects.objects.get(id=pk)
            issue_to_update.status = request.data['status']
            issue_to_update.author_user_id = get_object_or_404(User, id=int(request.data['author_user_id']))
            issue_to_update.assignee_user_id = get_object_or_404(User, id=int(request.data['assignee_user_id']))
            issue_to_update.save()
            return Response({'message': f'Issue {issue_id} modified'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'message': 'Issue not found'}, status=status.HTTP_404_NOT_FOUND)


class CommentsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, issue_id):
        issue = Issues.objects.filter(Q(project_id=pk) & Q(id=issue_id))
        issue_to_get = issue[0]
        comments = Comments.objects.filter(issue_id=issue_to_get.id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk, issue_id):
        try:
            issue = Issues.objects.filter(Q(project_id=pk) & Q(id=issue_id))
            issue_to_get = issue[0]
            comment = Comments()
            comment.description = request.data['description']
            comment.issue_id = issue_to_get
            comment.author_user_id = get_object_or_404(User, id=int(request.data['author_user_id']))
            comment.save()
            data = {'description': comment.description, 'issue_id': comment.issue_id.id,
                    'author_user_id': comment.author_user_id.id}
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({'Comment posting failed'}, status=status.HTTP_400_BAD_REQUEST)


class CommentsModifyAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, issue_id, comment_id):
        issue = Issues.objects.filter(Q(project_id=pk) & Q(id=issue_id))
        issue_to_get = issue[0]
        comment = Comments.objects.filter(Q(issue_id=issue_to_get.id) & Q(id=comment_id))
        serializer = CommentSerializer(comment, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, issue_id, comment_id):
        try:
            issue = get_object_or_404(Issues, Q(project_id=pk) & Q(id=issue_id))
            comment_to_delete = get_object_or_404(Comments, Q(id=comment_id) & Q(issue_id=issue.id))
            comment_to_delete.delete()
            return Response({'message': f'Issue {comment_id} deleted'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'message': 'Comment not found'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, issue_id, comment_id):
        try:
            issue = Issues.objects.filter(Q(project_id=pk) & Q(id=issue_id))
            issue_to_get = issue[0]
            comment_to_update = get_object_or_404(Comments, Q(issue_id=issue_to_get.id) & Q(id=comment_id))
            comment_to_update.description = request.data['description']
            comment_to_update.author_user_id = get_object_or_404(User, id=int(request.data['author_user_id']))
            comment_to_update.issue_id = issue_to_get
            comment_to_update.save()
            return Response({'message': f'Issue {comment_id} modified'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'message': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)

