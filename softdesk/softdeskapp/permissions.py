from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Contributors


class IsProjectCreator(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            requester = request.user
            if requester.id == obj.author_user_id.id:
                print(requester.id)
                print(obj.author_user_id.id)
                return True
            else:
                return False
        else:
            return False


class IsProjectContributor(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            requester = request.user
            contributors_list = Contributors.objects.filter(project_id=obj.id)
            if requester in contributors_list and request.method in SAFE_METHODS:
                return True
        else:
            return False


class IsIssueOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.method in SAFE_METHODS:
                return True
            else:
                requester = request.user
                issue_author_id = obj.author_user_id
                if requester.id == issue_author_id.id:
                    return True
        else:
            return False


class IsCommentOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.method in SAFE_METHODS:
                return True
            else:
                requester = request.user
                issue_author_id = obj.author_user_id
                if requester.id == issue_author_id.id:
                    return True
        else:
            return False

