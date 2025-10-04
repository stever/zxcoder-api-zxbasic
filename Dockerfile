FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# Create a non-root user to run the application
RUN groupadd -g 1000 zxbasic && \
    useradd -r -u 1000 -g zxbasic -m -d /home/zxbasic -s /bin/bash zxbasic

WORKDIR /app

# Copy requirements as root for installation
COPY ./requirements.txt /app/requirements.txt

# Install dependencies as root
RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean

RUN pip install -r /app/requirements.txt \
    && rm -rf /root/.cache/pip

# Copy application code and set ownership
COPY --chown=zxbasic:zxbasic . /app/

# Create a directory for temporary files with proper permissions
RUN mkdir -p /tmp/zxbasic && \
    chown -R zxbasic:zxbasic /tmp/zxbasic && \
    chmod 755 /tmp/zxbasic

# Ensure the app directory is owned by zxbasic user
RUN chown -R zxbasic:zxbasic /app

# Switch to non-root user
USER zxbasic

# Set environment variable for temp directory (optional - Python tempfile will use system default)
# ENV TMPDIR=/tmp/zxbasic

# The container will run with the default command from the base image