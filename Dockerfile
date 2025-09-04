FROM python:3.9-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy project files
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Create entrypoint script
RUN echo '#!/bin/sh' > /entrypoint.sh \
    && echo 'python manage.py migrate' >> /entrypoint.sh \
    && chmod +x /entrypoint.sh

# Expose port
EXPOSE 8000

# Use entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "django_project.wsgi:application"]
