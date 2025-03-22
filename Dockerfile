FROM python:3.8

LABEL maintainer="Shubham <chincholkar1711@gmail.com>"

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY ./app /app/app
WORKDIR /app/
EXPOSE 80

# Default command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
