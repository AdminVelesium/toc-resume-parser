# 1. Use Python image
FROM python:3.10-slim

# 2. Make folder inside container
WORKDIR /app

# 3. Copy everything
COPY . .

# 4. Install dependencies
RUN pip install -r requirements.txt

# 5. Tell Docker to use port 5000
EXPOSE 5000

# 6. Run the Flask app
CMD ["python", "app.py"]
