FROM node:22-alpine AS frontend
WORKDIR /build
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 SPLITWISE_STORAGE=sqlite
WORKDIR /app
COPY backend/requirements-lock.txt /app/backend/requirements-lock.txt
RUN pip install --no-cache-dir -r backend/requirements-lock.txt "psycopg[binary]>=3.2,<4"
COPY backend/ /app/backend/
COPY --from=frontend /build/dist /app/frontend/dist
COPY deployment/ /app/deployment/
RUN chmod +x /app/deployment/start.sh && useradd --create-home appuser && chown -R appuser:appuser /app
USER appuser
EXPOSE 8000
CMD ["/app/deployment/start.sh"]
