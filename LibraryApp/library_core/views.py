from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from datetime import date
from django.core.mail import send_mail
from . import forms, models
from django.contrib import messages
from datetime import date
from .models import StudentExtra
from django.conf import settings
# Ana sayfa
def home_view(request):
    #if request.user.is_authenticated:
        #return HttpResponseRedirect('afterlogin')
    return render(request, "library/index.html")

# Öğrenci giriş sayfasına yönlendirme
def studentclick_view(request):
    # if request.user.is_authenticated:
    #     return HttpResponseRedirect('afterlogin')
    return render(request, "library/studentclick.html")

# Öğrenci kayıt işlemi
def studentsignup_view(request):
    form1 = forms.StudentUserForm()
    form2 = forms.StudentExtraForm()
    mydict = {'form1': form1, 'form2': form2}

    if request.method == 'POST':
        form1 = forms.StudentUserForm(request.POST)
        form2 = forms.StudentExtraForm(request.POST)

        if form1.is_valid() and form2.is_valid():
            user = form1.save(commit=False)
            user.set_password(user.password)
            user.save()

            f2 = form2.save(commit=False)
            f2.user = user
            f2.save()

            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)

            return HttpResponseRedirect('studentlogin')

    return render(request, 'library/studentsignup.html', context=mydict)

# Öğrenci mi kontrolü
def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

def afterlogin_view(request):
    if request.user.groups.filter(name='STUDENT').exists():
        student = get_object_or_404(StudentExtra, user=request.user)
        context = {
            'student': student,
            'user': request.user
        }
        return render(request, 'library/studentafterlogin.html', context)

    elif request.user.is_superuser:
        return redirect('/admin')

    else:
        return redirect('home_view')

# Kitap iade işlemi
def returnbook(request, id):
    issued_book = get_object_or_404(models.IssuedBook, pk=id)
    issued_book.status = "Returned"
    issued_book.save()
    return redirect('viewissuedbookbystudent')


@login_required(login_url='studentlogin')
def issuebook_view(request):
    form = forms.IssuedBookForm()
    if request.method == 'POST':
        form = forms.IssuedBookForm(request.POST)
        if form.is_valid():
            enrollment = request.POST.get('enrollment2')
            isbn = request.POST.get('isbn2')
            
            try:
                student = models.StudentExtra.objects.get(enrollment=enrollment)
                book = models.Book.objects.get(isbn=isbn)
            except models.StudentExtra.DoesNotExist:
                return render(request, 'library/issuebook.html', {'form': form, 'error': 'Student not found'})
            except models.Book.DoesNotExist:
                return render(request, 'library/issuebook.html', {'form': form, 'error': 'Book not found'})

            # Kitap talebi oluştur
            obj = models.IssuedBook()
            obj.student = student
            obj.book = book
            obj.approved = False  # Admin onayı bekleniyor
            obj.save()

            return render(request, 'library/bookrequested.html')  # "Talebiniz alındı" gibi bir sayfa

    return render(request, 'library/issuebook.html', {'form': form})

@login_required(login_url='studentlogin')
def viewissuedbookbystudent(request):
    student = models.StudentExtra.objects.filter(user_id=request.user.id).first()
    issuedbooks = models.IssuedBook.objects.filter(student=student, approved=True)
    
    # Ödünçte olan kitapların ISBN listesi
    issued_books_isbn = models.IssuedBook.objects.filter(status='Issued').values_list('book__isbn', flat=True)
    
    # Ödünçte olmayan kitaplar
    all_books = models.Book.objects.exclude(isbn__in=issued_books_isbn)

    li1 = []
    li2 = []

    for ib in issuedbooks:
        book = ib.book
        t1 = (request.user, student.enrollment, student.branch, book.name, book.author)
        li1.append(t1)

        issdate = f"{ib.issuedate.day}-{ib.issuedate.month}-{ib.issuedate.year}"
        expdate = f"{ib.expirydate.day}-{ib.expirydate.month}-{ib.expirydate.year}"
        
        days = (date.today() - ib.issuedate).days
        fine = 0
        if days > 15:
            fine = (days - 15) * 10

        t2 = (issdate, expdate, fine, ib.status, ib.id)
        li2.append(t2)

    return render(request, 'library/viewissuedbookbystudent.html', {
        'li1': li1,
        'li2': li2,
        'all_books': all_books,
        'student': student  
    })
@login_required(login_url='studentlogin')
def issuebook(request):
    if request.method == 'POST':
        isbn = request.POST.get('isbn2')
        enrollment = request.POST.get('enrollment2')

        student = models.StudentExtra.objects.filter(enrollment=enrollment).first()
        book = models.Book.objects.filter(isbn=isbn).first()

        if student and book:
            # Zaten aynı kitap onaylı veya beklemede mi diye kontrol edebilirsin
            issued_book = models.IssuedBook.objects.filter(student=student, book=book, approved=False).first()
            if issued_book:
                messages.warning(request, 'You already requested this book and it is pending approval.')
            else:
                # Yeni talep ekle
                models.IssuedBook.objects.create(student=student, book=book, approved=False, status='Pending')
                messages.success(request, 'Book request submitted successfully.')
        else:
            messages.error(request, 'Invalid student or book.')

        return redirect('viewissuedbookbystudent')

    else:
        return redirect('viewissuedbookbystudent')
from django.core.mail import send_mail
from django.http import HttpResponse

def test_mail(request):
    try:
        send_mail(
            'Test Mail',
            'Bu bir test mailidir.',
            'beyzanurdincer502@gmail.com',
            ['beyzanurdincer65@gmil.com'],  # Kendi mail adresini veya test için kendininkini koy
            fail_silently=False,
        )
        return HttpResponse("Mail gönderildi.")
    except Exception as e:
        return HttpResponse(f"Mail gönderilemedi, hata: {e}")

