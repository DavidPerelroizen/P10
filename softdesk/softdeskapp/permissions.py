from rest_framework.permissions import BasePermission


class IsProjectCreator(BasePermission):

    def has_object_permission(self, request, view, obj):
        requester = request.user
        if requester == obj.author_user_id:
            return True
