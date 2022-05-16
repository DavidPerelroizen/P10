from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Contributors


class IsProjectCreator(BasePermission):

    def has_object_permission(self, request, view, obj):
        requester = request.user
        if requester == obj.author_user_id:
            return True


class IsProjectContributor(BasePermission):

    def has_object_permission(self, request, view, obj):
        requester = request.user
        contributors_list = Contributors.objects.filter(project_id=obj.id)
        if requester in contributors_list and request.method in SAFE_METHODS:
            return True




