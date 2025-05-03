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
    list_display = ('enrollment', 'isbn', 'issuedate', 'expirydate', 'status')
    list_filter = ('status', 'issuedate')
    search_fields = ('enrollment', 'isbn')

