from home.views import index, person, login, PersonAPI, PeopleViewSet, RegisterAPI, LoginAPI
from django.urls import path, include

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'people', PeopleViewSet, basename='people')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterAPI.as_view(), name='api-register'),
    path('login/', LoginAPI.as_view(), name='api-login'),
    path('index/', index, name='api-index'),
    path('person/', person, name='api-person'),
    path('loginAPI/', login, name='api-login'),
    path('personAPI/', PersonAPI.as_view(), name='person-api'),
]
