"""librarymanagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from library_core import views
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth import views as auth_views
from library_core.views import simple_test

urlpatterns = [
    path('test/', simple_test),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.home_view, name='home_view'),
    path('issuebook/', views.issuebook, name='issuebook'),
    path('studentclick', views.studentclick_view, name='studentclick'),
    path('studentsignup', views.studentsignup_view),
    path('studentlogin', LoginView.as_view(template_name='library/studentlogin.html'), name='studentlogin'),
    path('accounts/login/', auth_views.LoginView.as_view(redirect_authenticated_user=True, next_page='afterlogin'), name='login'),
    path('returnbook/<int:id>/', views.returnbook, name='returnbook'),
    path('logout', LogoutView.as_view(template_name='library/index.html')),
    path('afterlogin', views.afterlogin_view, name='afterlogin'),
    path('viewissuedbookbystudent', views.viewissuedbookbystudent, name='viewissuedbookbystudent'),
]
