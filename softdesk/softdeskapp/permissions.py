from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Contributors, Issues


class IsProjectCreator(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        requester = request.user
        if requester.id == obj.author_user_id.id:
            return True


class IsProjectContributor(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        requester = request.user
        contributors_list = Contributors.objects.filter(project_id=obj.id)
        if requester in contributors_list and request.method in SAFE_METHODS:
            return True


class CanAccessCreateCommentIssue(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        requester = request.user
        contributors_list = Contributors.objects.filter(project_id=obj.project_id)
        if requester in contributors_list:
            return True


class IsIssueOwner(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        requester = request.user
        issue_author_id = obj.author_user_id
        if requester.id == issue_author_id.id:
            return True


