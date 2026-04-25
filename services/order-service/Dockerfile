# product-service/Dockerfile

# 1. Start with a lightweight version of Python
FROM python:3.10-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy just the requirements file first (for caching purposes)
COPY requirements.txt .

# 4. Install the dependencies inside the container
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your actual code into the container
COPY . .

# 6. Expose the port this service uses
EXPOSE 8002

# 7. The command to run when the container starts
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]