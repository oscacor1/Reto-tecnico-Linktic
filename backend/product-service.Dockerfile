FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY product_service/app ./app

ENV DATABASE_URL=sqlite:///./products.db
ENV INTERNAL_API_KEY=super-secret-key

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
