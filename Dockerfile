# Dockerfile

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install dependencies
COPY pyproject.toml poetry.lock* /app/
RUN pip install --upgrade pip && pip install poetry && poetry config virtualenvs.create false && poetry install --no-root

# Copy project files
COPY . /app/

# Default command
CMD ["gunicorn", "glucose_tracker_api.wsgi:application", "--bind", "0.0.0.0:8000"]
