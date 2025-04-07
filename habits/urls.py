from django.urls import path, include
from rest_framework.routers import DefaultRouter
from habits.views import HabitViewSet, PublicHabitListView, RegisterView, LoginView

router = DefaultRouter()
router.register(r'habits', HabitViewSet, basename='habit')

urlpatterns = [
    path('', include(router.urls)),
    path('habits/public/', PublicHabitListView.as_view(), name='public-habits'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
]
