from django.contrib import admin
from .models import StudentExtra, Book, IssuedBook

from django.contrib import admin
from .models import StudentExtra, Book, IssuedBook

from django.contrib import admin
from .models import StudentExtra, Book, IssuedBook

# StudentExtra 
@admin.register(StudentExtra)
class StudentExtraAdmin(admin.ModelAdmin):
    list_display = ('user', 'enrollment', 'branch')
    search_fields = ('user__first_name', 'enrollment', 'branch')

# Book 
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'isbn', 'author', 'category_display')
    search_fields = ('name', 'isbn', 'author')
    list_filter = ('category',)

    def category_display(self, obj):
        return obj.get_category_display()
    category_display.short_description = 'Category'

# IssuedBook 
@admin.register(IssuedBook)
class IssuedBookAdmin(admin.ModelAdmin):
    list_display = ('student', 'book', 'issuedate', 'expirydate', 'status')
    list_filter = ('status', 'issuedate')
    search_fields = ('student__user__first_name', 'student__enrollment', 'book__name', 'book__isbn')
    actions = ['approve_issues']

    @admin.action(description="Approve selected book issues")
    def approve_issues(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f"{updated} book issue(s) approved.")
