from django.urls import path
from .views import IssuesAPIView, IssuesModifyAPIView, ContributorsAPIView, ContributorDeletion, \
    CommentsAPIView, CommentsModifyAPIView, ProjectsReadCreateAPIView, ProjectUpdateDeleteAPIView
from rest_framework import routers


router = routers.SimpleRouter()

urlpatterns = [
    path('projects/', ProjectsReadCreateAPIView.as_view(), name='projects'),
    path('projects/<int:pk>/', ProjectUpdateDeleteAPIView.as_view(), name='modify_projects'),
    path('projects/<int:pk>/contributors/', ContributorsAPIView.as_view(), name='contributors'),
    path('projects/<int:pk>/contributors/<int:user_id>/', ContributorDeletion.as_view(), name='delete_contributors'),
    path('projects/<int:pk>/issues/', IssuesAPIView.as_view(), name='issues'),
    path('projects/<int:pk>/issues/<int:issue_id>/', IssuesModifyAPIView.as_view(), name='modify_issues'),
    path('projects/<int:pk>/issues/<int:issue_id>/comments/', CommentsAPIView.as_view(), name='comments'),
    path('projects/<int:pk>/issues/<int:issue_id>/comments/<int:comment_id>/', CommentsModifyAPIView.as_view(),
         name='modify_comments'),
    ]

