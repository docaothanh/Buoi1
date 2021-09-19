from django.shortcuts import render
from django.http import  HttpResponse
from django.views import View
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, permissions, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.pagination import PageNumberPagination

from .models import Course, Lesson, User, Category
from .serializers import CourseSerializer, LessonSerializer, UserSerializer, CategorySerializer
# Create your views here.

class CategoryViewSet(viewsets.ViewSet,generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None #tắt phân trang trong danh mục(Category)


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.RetrieveAPIView, generics.ListAPIView):#generics.ListAPIView
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, ]

    def get_permissions(self):
        if self.action == 'retrieve':
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

# test
#ad


class CoursePagination(PageNumberPagination):
    page_size = 3


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.filter(active=True)
    serializer_class = CourseSerializer
    pagination_class = CoursePagination

    @action(methods=['get'], detail=True, url_path="lessons")
    # /lessons/{pk}/hide_lesson
    def get_lessons(self, request, pk):
            course = self.get_object().lessons.filter(active=True)
            lessons = course
            return Response(LessonSerializer(lessons, many= True).data, status=status.HTTP_200_OK)
    #swagger_schema = None
    #permission_classes = [permissions.IsAuthenticated]
    #list (GET) --> xem danh sach khoa hoc
    #..(POST) --> them khoa hoc
    #detail --> xem chi tiet 1 khoa hoc
    #... (PUT) --> cap nhat
    #... (DELETE) --> xoa khoa hoc


    #def get_permissions(self):
        #if self.action == 'list':
            #return [permissions.AllowAny()]
        #return [permissions.IsAuthenticated()]


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.filter(active=True)
    serializer_class = LessonSerializer

    @swagger_auto_schema(
        operation_description='API nay dung de an lesson',
        responses={
            status.HTTP_200_OK: LessonSerializer()
        }
    )


    @action(methods=['post'], detail=True, url_path="hide-lesson", url_name="hide-lesson")
    #/lessons/{pk}/hide_lesson
    def hide_lesson(self, request, pk):
        try:
            l = Lesson.objects.get(pk=pk)
            l.active = False
            l.save()
        except Lesson.DoesNoExits:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(data=LessonSerializer(l, context={'request': request}).data, status=status.HTTP_200_OK)


def index(request):
    return render(request, template_name='index.html', context={'name': 'Thanh Do' })


def welcome(request, year):
    return HttpResponse("HELLO" + str(year))


def welcome2(request, year):
    return HttpResponse("HELLO " + str(year))


class TestView(View):
    def get(self, request):
        return HttpResponse("TESTING")

    def post(self, request):
        pass