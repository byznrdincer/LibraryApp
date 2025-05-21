FROM python:3.10

# GEREKEN EKLEME: Sistem bağımlılıkları
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
