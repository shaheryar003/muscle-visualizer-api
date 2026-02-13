# Stage 1: Build the frontend
FROM node:20-slim AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Stage 2: Build the backend and serve the application
FROM python:3.11-slim
WORKDIR /app/backend

# Install system dependencies if any (none needed for now)
# RUN apt-get update && apt-get install -y --no-install-recommends ...

# Copy requirements and install
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./

# Copy built frontend assets to the backend's static directory
RUN mkdir -p static
COPY --from=frontend-builder /app/frontend/dist ./static

# Expose the port (Render will override this with its own PORT env var, but let's default to 8000)
ENV PORT=8000
EXPOSE 8000

# Set Python path to ensure 'app' is found
ENV PYTHONPATH=/app/backend

# Run the application
CMD ["python", "app/main.py"]
