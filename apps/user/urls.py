from django.urls import path
from .views import Index, Login, Register, Logout, MyBlog, WriteBlog, Detail
app_name = 'user'

urlpatterns = [
    path('', Index, name='index'),
    path('login/', Login, name='login'),
    path('register/', Register, name='register'),
    path('logout/', Logout, name='logout'),
    path('myblog/', MyBlog, name='myblog'),
    path('writeblog/', WriteBlog, name='writeblog'),
    path('detail/', Detail, name='detail'),
]
