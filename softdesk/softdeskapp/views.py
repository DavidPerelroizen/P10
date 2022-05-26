from rest_framework.views import APIView
from .serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from .models import Projects, Contributors, Issues, Comments
from .permissions import IsProjectCreator, IsProjectContributor, IsIssueOwner, IsCommentOwner
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Q

# Create your views here.


class ProjectsReadCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        contributions = Contributors.objects.filter(user_id=request.user)
        contributed_projects = []
        for contribution in contributions:
            contributed_projects.append(contribution.project_id.id)

        projects = Projects.objects.filter(Q(author_user_id=request.user) | Q(id__in=contributed_projects))
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            project = Projects()
            project.title = request.data['title']
            project.description = request.data['description']
            project.type = request.data['type']
            project.author_user_id = get_object_or_404(User, id=int(request.user.id))
            project.save()

            data = {'title': project.title, 'description': project.description, 'type': project.type,
                    'author_user_id': project.author_user_id.id}

            contributor = Contributors()
            contributor.user_id = get_object_or_404(User, id=int(request.user.id))
            contributor.project_id = project
            contributor.permission = 'C'
            contributor.role = 'A'
            contributor.save()

            return Response(data, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return Response({'Project posting failed'}, status=status.HTTP_400_BAD_REQUEST)


class ProjectUpdateDeleteAPIView(APIView):
    permission_classes = [IsProjectCreator, IsProjectContributor]

    def get(self, request, pk):
        project = get_object_or_404(Projects, id=pk)
        self.check_object_permissions(request, project)
        serializer = ProjectSerializer(project, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):

        try:
            project = get_object_or_404(Projects, id=pk)
            self.check_object_permissions(request, project)
            project.title = request.data['title']
            project.description = request.data['description']
            project.type = request.data['type']
            project.author_user_id = get_object_or_404(User, id=int(request.user.id))
            project.save()
            data = {'title': project.title, 'description': project.description, 'type': project.type,
                    'author_user_id': project.author_user_id.id}
            return Response(data, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return Response({'Project update failed'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            project = get_object_or_404(Projects, id=pk)
            self.check_object_permissions(request, project)
            project.delete()
            return Response({'message': f'Project {pk} deleted'}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({'message': f'Project {project.id} could not be deleted'},
                            status=status.HTTP_400_BAD_REQUEST)


class ContributorsAPIView(APIView):
    """
    This view allows the user to consult or create a contributor for a given project
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        contributors = Contributors.objects.filter(project_id=pk)
        contributors_id_list = []
        for contributor in contributors:
            contributors_id_list.append(contributor.user_id.id)
        if request.user.id in contributors_id_list:
            serializer = ContributorSerializer(contributors, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': f'Access to project {pk} contributors list denied'},
                            status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, pk):
        project = get_object_or_404(Projects, id=pk)
        if request.user.id == project.author_user_id.id:
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
                return Response({'message': 'Contributor posting failed'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'message': f'Authorization for adding contributors to project {pk} denied'},
                            status=status.HTTP_401_UNAUTHORIZED)


class ContributorDeletion(APIView):
    """
    This view redefines the method get in order to delete contributors from a given project
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, user_id):
        project = get_object_or_404(Projects, id=pk)
        if request.user.id == project.author_user_id.id:
            try:
                contributor_to_delete = Contributors.objects.filter(Q(project_id=pk) & Q(user_id=user_id))
                contributor_to_delete.delete()
                return Response({'message': f'Contributor {user_id} deleted'})
            except Exception as e:
                print(e)
                return Response({'message': 'Contributor not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'message': f'Authorization for deleting contributors from project {pk} denied'},
                            status=status.HTTP_401_UNAUTHORIZED)


class IssuesAPIView(APIView):
    """
    This view helps the user to consult or to create issues for a given project
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        contributors = Contributors.objects.filter(project_id=pk)
        contributors_id_list = []
        for contributor in contributors:
            contributors_id_list.append(contributor.user_id.id)
        if request.user.id in contributors_id_list:
            issues = Issues.objects.filter(project_id=pk)
            serializer = IssueSerializer(issues, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': f'Authorization for getting issues from project {pk} denied'},
                            status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, pk):
        contributors = Contributors.objects.filter(project_id=pk)
        contributors_id_list = []
        for contributor in contributors:
            contributors_id_list.append(contributor.user_id.id)
        if request.user.id in contributors_id_list:
            try:
                issue = Issues()
                issue.title = request.data['title']
                issue.desc = request.data['desc']
                issue.tag = request.data['tag']
                issue.priority = request.data['priority']
                issue.project_id = Projects.objects.get(id=pk)
                issue.status = request.data['status']
                issue.author_user_id = get_object_or_404(User, id=int(request.user.id))
                if request.data['assignee_user_id'] == '':
                    issue.assignee_user_id = request.user
                else:
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
        else:
            return Response({'message': f'Authorization for creating issues in project {pk} denied'},
                            status=status.HTTP_401_UNAUTHORIZED)


class IssuesModifyAPIView(APIView):
    """
    This view helps the user to consult, delete or modify a specific issue from a specific project
    """
    permission_classes = [IsIssueOwner]

    def get(self, request, pk, issue_id):
        issue_to_get = Issues.objects.filter(Q(project_id=pk) & Q(id=issue_id))
        self.check_object_permissions(request, issue_to_get)
        serializer = IssueSerializer(issue_to_get, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, issue_id):
        try:
            issue_to_delete = Issues.objects.filter(Q(project_id=pk) & Q(id=issue_id))
            self.check_object_permissions(request, issue_to_delete)
            issue_to_delete.delete()
            return Response({'message': f'Issue {issue_id} deleted'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'message': f'Authorization for issue {issue_id} deletion denied'},
                            status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, pk, issue_id):
        try:
            issue = Issues.objects.filter(Q(project_id=pk) & Q(id=issue_id))
            issue_to_update = issue[0]
            self.check_object_permissions(request, issue_to_update)
            issue_to_update.title = request.data['title']
            issue_to_update.desc = request.data['desc']
            issue_to_update.tag = request.data['tag']
            issue_to_update.priority = request.data['priority']
            issue_to_update.project_id = Projects.objects.get(id=pk)
            issue_to_update.status = request.data['status']
            issue_to_update.author_user_id = get_object_or_404(User, id=int(request.user.id))
            if request.data['assignee_user_id'] == '':
                issue_to_update.assignee_user_id = request.user
            else:
                issue_to_update.assignee_user_id = get_object_or_404(User, id=int(request.data['assignee_user_id']))
            issue_to_update.save()
            return Response({'message': f'Issue {issue_id} modified'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'message': f'Authorization for issue {issue_id} modification denied'},
                            status=status.HTTP_401_UNAUTHORIZED)


class CommentsAPIView(APIView):
    """
    This view helps the user to consult or to create comments about a specific issue for a specific project.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, issue_id):
        contributors = Contributors.objects.filter(project_id=pk)
        contributors_id_list = []
        for contributor in contributors:
            contributors_id_list.append(contributor.user_id.id)
        if request.user.id in contributors_id_list:
            issue = Issues.objects.filter(Q(project_id=pk) & Q(id=issue_id))
            issue_to_get = issue[0]
            comments = Comments.objects.filter(issue_id=issue_to_get.id)
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': f'Authorization for getting comments from issue {issue_id} denied'},
                            status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, pk, issue_id):
        contributors = Contributors.objects.filter(project_id=pk)
        contributors_id_list = []
        for contributor in contributors:
            contributors_id_list.append(contributor.user_id.id)
        if request.user.id in contributors_id_list:
            try:
                issue = Issues.objects.filter(Q(project_id=pk) & Q(id=issue_id))
                issue_to_get = issue[0]
                comment = Comments()
                comment.description = request.data['description']
                comment.issue_id = issue_to_get
                comment.author_user_id = get_object_or_404(User, id=int(request.user.id))
                comment.save()
                data = {'description': comment.description, 'issue_id': comment.issue_id.id,
                        'author_user_id': comment.author_user_id.id}
                return Response(data, status=status.HTTP_201_CREATED)
            except Exception as e:
                print(e)
                return Response({'Comment posting failed'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': f'Authorization for getting comments from issue {issue_id} denied'},
                            status=status.HTTP_401_UNAUTHORIZED)


class CommentsModifyAPIView(APIView):
    """
    This view helps to consult, modify or delete a specific comment, from a specific issue, from a specific project
    """
    permission_classes = [IsCommentOwner]

    def get(self, request, pk, issue_id, comment_id):
        issue = Issues.objects.filter(Q(project_id=pk) & Q(id=issue_id))
        issue_to_get = issue[0]
        comment = Comments.objects.filter(Q(issue_id=issue_to_get.id) & Q(id=comment_id))
        self.check_object_permissions(request, comment)
        serializer = CommentSerializer(comment, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, issue_id, comment_id):
        try:
            issue = get_object_or_404(Issues, Q(project_id=pk) & Q(id=issue_id))
            comment_to_delete = get_object_or_404(Comments, Q(id=comment_id) & Q(issue_id=issue.id))
            self.check_object_permissions(request, comment_to_delete)
            comment_to_delete.delete()
            return Response({'message': f'Comment {comment_id} deleted'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'message': 'Comment not found'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, issue_id, comment_id):
        try:
            issue = Issues.objects.filter(Q(project_id=pk) & Q(id=issue_id))
            issue_to_get = issue[0]
            comment_to_update = get_object_or_404(Comments, Q(issue_id=issue_to_get.id) & Q(id=comment_id))
            self.check_object_permissions(request, comment_to_update)
            comment_to_update.description = request.data['description']
            comment_to_update.author_user_id = get_object_or_404(User, id=int(request.user.id))
            comment_to_update.issue_id = issue_to_get
            comment_to_update.save()
            return Response({'message': f'Comment {comment_id} modified'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'message': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
