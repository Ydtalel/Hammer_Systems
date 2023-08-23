# Используем базовый образ Python
FROM python:3.9

# Устанавливаем переменную среды для отключения буферизации вывода
ENV PYTHONUNBUFFERED 1

# Создаем директорию внутри контейнера для кода приложения
RUN mkdir /app

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Копируем остальные файлы приложения
COPY . /app/

# Запускаем миграции базы данных
RUN python manage.py migrate --noinput

# Открываем порт для доступа к приложению
EXPOSE 8000

# Запускаем сервер Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
