from django import forms
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from . import forms, models
from django.contrib.auth.models import Group
from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime, timedelta, date
from django.core.mail import send_mail

def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, "library_core/index.html")


def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, "library_core/adminclick.html")


def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, "library_core/studentclick.html")


def studentsignup_view(request):
    form1 = forms.StudentUserForm()
    form2 = forms.StudentExtraForm()
    mydict = {'form1': form1, 'form2': form2}
    
    if request.method == 'POST':
        form1 = forms.StudentUserForm(request.POST)
        form2 = forms.StudentExtraForm(request.POST)
        
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.set_password(user.password)
            user.save()
            f2 = form2.save(commit=False)
            f2.user = user
            user2 = f2.save()
            
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)

        return HttpResponseRedirect('studentlogin')
    
    return render(request, 'library_core/studentsignup.html', context=mydict)









def returnbook(request):
    pass
def afterlogin_view(request):
    pass
def addbook_view(request):
    pass
def viewbook_view(request):
    pass
def issuebook_view(request):
    pass
def viewissuedbook_view(request):
    pass
def viewsStudent_view(request):
    pass
def viewissuedbookbystudent(request):
    pass