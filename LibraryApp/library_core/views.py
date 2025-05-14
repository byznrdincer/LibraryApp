from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from datetime import date
from django.core.mail import send_mail
from . import forms, models

# Ana sayfa
def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, "library/index.html")

# Admin giriş sayfasına yönlendirme
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, "library/adminclick.html")

# Öğrenci giriş sayfasına yönlendirme
def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
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
            user.set_password(user.password)  # Şifreyi hash'le
            user.save()
            
            f2 = form2.save(commit=False)
            f2.user = user
            f2.save()

            # Öğrenciyi 'STUDENT' grubuna ekle
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)

            return HttpResponseRedirect('studentlogin')  # Bu satır if bloğuna alındı
    
    return render(request, 'library/studentsignup.html', context=mydict)

# Admin mi kontrolü
def is_admin(user):
    return user.is_superuser or user.is_staff

# Öğrenci mi kontrolü
def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

# Giriş sonrası yönlendirme
def afterlogin_view(request):
    if is_admin(request.user):
        return render(request, 'library/adminafterlogin.html')
    elif is_student(request.user):
        return render(request, 'library/studentafterlogin.html')

# Kitap iade işlemi
def returnbook(request, id):
    issued_book = get_object_or_404(models.IssuedBook, pk=id)
    issued_book.status = "Returned"
    issued_book.save()
    return redirect('viewissuedbookbystudent')

# Kitap ekleme
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def addbook_view(request):
    form = forms.BookForm()
    if request.method == 'POST':
        form = forms.BookForm(request.POST)
        if form.is_valid():
            user = form.save()  # Senin isteğinle bu satır değişmedi
            return render(request, 'library_core/bookadded.html')
    return render(request, 'library/addbook.html', {'form': form})

# Tüm kitapları listeleme
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewbook_view(request):
    books = models.Book.objects.all()
    return render(request, 'library/viewbook.html', {'books': books})

# Kitap ödünç verme
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def issuebook_view(request):
    form = forms.IssuedBookForm()
    if request.method == 'POST':
        form = forms.IssuedBookForm(request.POST)
        if form.is_valid():
            obj = models.IssuedBook()
            obj.enrollment = request.POST.get('enrollment2')
            obj.isbn = request.POST.get('isbn2')
            obj.save()

            # Kitap ödünç verildikten sonra e-posta gönder
            student_email = models.StudentExtra.objects.get(enrollment=obj.enrollment).user.email
            book_name = models.Book.objects.get(isbn=obj.isbn).name
            send_mail(
                subject='Kitap Teslim Bilgisi',
                message=f"'{book_name}' adlı kitabı aldınız. Teslim süresi 30 gündür.",
                from_email='seninmailin@gmail.com',
                recipient_list=[student_email],
                fail_silently=False,
            )
            return render(request, 'library/bookissued.html')
    return render(request, 'library/issuebook.html', {'form': form})

# Tüm ödünç kitapları görüntüle (admin)
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewissuedbook_view(request):
    issuedbooks = models.IssuedBook.objects.all()
    li = []

    for ib in issuedbooks:
        issdate = f"{ib.issuedate.day}-{ib.issuedate.month}-{ib.issuedate.year}"
        expdate = f"{ib.expirydate.day}-{ib.expirydate.month}-{ib.expirydate.year}"
        
        # Gecikme ve ceza hesapla
        days = (date.today() - ib.issuedate).days
        fine = 0
        if days > 15:
            fine = (days - 15) * 10

        books = models.Book.objects.filter(isbn=ib.isbn)
        students = models.StudentExtra.objects.filter(enrollment=ib.enrollment)

        for student in students:
            for book in books:
                t = (
                    student.get_name, student.enrollment,
                    book.name, book.author,
                    issdate, expdate, fine, ib.status
                )
                li.append(t)

    return render(request, 'library/viewissuedbook.html', {'li': li})

# Tüm öğrencileri listele (admin)
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewstudent_view(request):
    students = models.StudentExtra.objects.all()
    return render(request, 'library/viewstudent.html', {'students': students})

# Giriş yapan öğrencinin kitaplarını görüntülemesi
@login_required(login_url='studentlogin')
def viewissuedbookbystudent(request):
    student = models.StudentExtra.objects.filter(user_id=request.user.id).first()
    issuedbooks = models.IssuedBook.objects.filter(enrollment=student.enrollment)

    li1 = []
    li2 = []

    for ib in issuedbooks:
        books = models.Book.objects.filter(isbn=ib.isbn)
        for book in books:
            t1 = (request.user, student.enrollment, student.branch, book.name, book.author)
            li1.append(t1)

        issdate = f"{ib.issuedate.day}-{ib.issuedate.month}-{ib.issuedate.year}"
        expdate = f"{ib.expirydate.day}-{ib.expirydate.month}-{ib.expirydate.year}"
        
        # Ceza hesapla
        days = (date.today() - ib.issuedate).days
        fine = 0
        if days > 15:
            fine = (days - 15) * 10

        t2 = (issdate, expdate, fine, ib.status, ib.id)
        li2.append(t2)

    return render(request, 'library/viewissuedbookbystudent.html', {'li1': li1, 'li2': li2})
