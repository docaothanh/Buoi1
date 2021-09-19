
from django.urls import path, re_path, include
from . import  views
from rest_framework.routers import DefaultRouter
#from .admin import admin_site


router = DefaultRouter()
router.register('courses', views.CourseViewSet)
router.register('lessons', views.LessonViewSet)
router.register('users', views.UserViewSet)
router.register('categories', views.CategoryViewSet)


#/courses/ - GET
#/courses/ - POST
#/courses/{course_id}/ - GET
#/courses/{course_id}/ - PUT
#/courses/{course_id}/ - DELETE


urlpatterns = [
    path('', include(router.urls)),
    #path('', views.index, name="index"),
    path('welcome/<str:year>/', views.welcome, name="welcome"),
    re_path(r'^welcome2/(?P<year>[0-9]{4})/$', views.welcome2, name="welcome2"),
    re_path('test/', views.TestView.as_view()),
    #path('admin/', admin.site.urls),
    #path('admin/', admin_site.urls),
]