FROM python:3.13.9-slim

# Install pipenv
RUN pip install --no-cache-dir pipenv

# Set working directory
WORKDIR /app

# Copy dependency files first (layer caching)
COPY Pipfile Pipfile.lock ./

# Install dependencies
RUN pipenv install --deploy --system

# Copy the rest of the application
COPY . .

# Optional but recommended
ENV PYTHONUNBUFFERED=1
