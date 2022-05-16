from django.urls import path, include
from .views import ProjectsViewset, IssuesAPIView, IssuesModifyAPIView, ContributorsAPIView, ContributorDeletion
from rest_framework import routers


router = routers.SimpleRouter()

router.register('', ProjectsViewset, basename='projects')

urlpatterns = [
    path('projects/', include(router.urls)),
    path('projects/<int:pk>/contributors/', ContributorsAPIView.as_view(), name='contributors'),
    path('projects/<int:pk>/contributors/<int:user_id>/', ContributorDeletion.as_view(), name='delete_contributors'),
    path('projects/<int:pk>/issues/', IssuesAPIView.as_view(), name='issues'),
    path('projects/<int:pk>/issues/<int:issue_id>/', IssuesModifyAPIView.as_view(), name='modify_issues'),
    ]
