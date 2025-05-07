import os
from django.core.mail import send_mail
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

# DJANGO_SETTINGS_MODULE ortam değişkenini ayarla
os.environ['DJANGO_SETTINGS_MODULE'] = 'LibraryApp.settings'  # Projeye göre ayarlayın

# E-posta gönderme
send_mail(
    subject='Kütüphane uygulamasi',  # E-posta konusunu belirleyin
    message='kendime mail gonderiyorum.',  # E-posta içeriği
    from_email='beyzanurdincer502@gmail.com',  # Gönderen e-posta adresi
    recipient_list=['beyzanurdincer502@gmail.com'],  # Alıcı e-posta adresi
    fail_silently=False,  # Hata durumunda sessiz olma
)
