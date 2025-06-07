# Используем базовый образ Python
FROM python:3.11.12-slim

# Устанавливаем переменную окружения для отображения вывода в консоли
ENV PYTHONUNBUFFERED=1

# Устанавливаем рабочую директорию в /app
WORKDIR /app

# Обновляем pip, setuptools и wheel до последних версий с PyPI
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Копируем зависимости и устанавливаем их
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все содержимое текущей директории в контейнер в /app
COPY . /app/
