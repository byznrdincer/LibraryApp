from django_cron import CronJobBase, Schedule
from .models import IssuedBook
from django.core.mail import send_mail
from django.conf import settings
from datetime import date

class SendReminderEmailsCronJob(CronJobBase):
    RUN_EVERY_MINS = 1440  # 24 saat

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'library_core.send_reminder_emails'  # benzersiz kod

    def do(self):
        today = date.today()
        books = IssuedBook.objects.filter(approved=True)

        for book in books:
            days_left = (book.expirydate - today).days
            if days_left == 0:
                student_email = book.student.user.email
                student_name = book.student.user.first_name
                book_name = book.book.name

                send_mail(
                    subject='Reminder: Book due today',
                    message=f"Dear {student_name}, today is the last day to return the book '{book_name}'.Please return it on time to avoid penalty.",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[student_email],
                    fail_silently=False,
                )

