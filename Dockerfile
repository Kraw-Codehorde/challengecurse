# Stage 1: Build dependencies
FROM python:3.12-alpine as builder

# Install build dependencies
RUN apk add --no-cache gcc musl-dev linux-headers

WORKDIR /usr/src/app

# Install Python dependencies
COPY requirements_docker.txt .
RUN pip install --upgrade pip
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements_docker.txt

# Stage 2: Final image
FROM python:3.12-alpine

# Create a non-root user
RUN addgroup -S app && adduser -S app -G app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set db type
ENV DB_TYPE=postgres

WORKDIR /app

# Install runtime dependencies
RUN apk add --no-cache libpq netcat-openbsd

# Copy wheels from builder and install
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements_docker.txt .
RUN pip install --no-cache /wheels/*

# Copy project files
COPY . /app

# Copy the entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Ensure management commands are copied
COPY accounts/management/commands/*.py /app/accounts/management/commands/

# Change ownership of the app directory
RUN chown -R app:app /app

# Switch to non-root user
USER app

# Remove the ENTRYPOINT line to skip using entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

# Run the application (use CMD as the default command)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
