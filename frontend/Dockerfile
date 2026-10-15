# Multi-stage build for React + TypeScript + Vite frontend

# Build stage
FROM node:22 AS builder

WORKDIR /app

# Copy dependency manifests
COPY package.json package-lock.json ./

# Install dependencies
RUN npm ci

# Copy application code
COPY tsconfig.json tsconfig.node.json vite.config.ts index.html ./
COPY src/ ./src/

# Build for production
RUN npm run build

# Production stage with nginx
FROM nginx:alpine

# Accept BACKEND_HOST as build arg and set as env var for template substitution
ARG BACKEND_HOST=backend
ENV BACKEND_HOST=${BACKEND_HOST}

# Copy nginx configuration template
COPY nginx.conf /etc/nginx/templates/default.conf.template

# Copy built assets from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# nginx image's entrypoint handles template substitution and starts nginx
# x-preview-port annotation in docker-compose.yml
