FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY inventory_service/app ./app

ENV INTERNAL_API_KEY=super-secret-key
ENV PRODUCT_SERVICE_BASE_URL=http://product-service:8000

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
