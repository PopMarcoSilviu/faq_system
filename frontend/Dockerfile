
FROM python:3.11-slim

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /frontend_app


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /frontend_app


EXPOSE 8501

RUN echo "Starting streamlit server"
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
