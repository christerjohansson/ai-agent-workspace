# AI Agent Instructions: DevOps and Infrastructure

## Overview
This document provides guidelines for AI agents managing DevOps, CI/CD pipelines, infrastructure, and deployment for web applications.

## Infrastructure Setup

### 1. Environment Configuration

#### Development Environment
```bash
# Install development dependencies
npm install

# Setup environment variables
cp .env.example .env.local

# Required variables:
# DATABASE_URL=postgresql://user:password@localhost:5432/dbname
# REDIS_URL=redis://localhost:6379
# API_SECRET=your-secret-key
# NODE_ENV=development
```

#### Production Environment
```bash
# Install production dependencies only
npm ci --omit=dev

# Set production environment variables
export NODE_ENV=production
export API_SECRET=<secure-secret>
export DATABASE_URL=<production-db>
```

### 2. Docker Configuration

Create `Dockerfile`:
```dockerfile
FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --omit=dev

# Copy application code
COPY . .

# Build Next.js
RUN npm run build

# Expose port
EXPOSE 3000

# Start application
CMD ["npm", "start"]
```

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      DATABASE_URL: postgresql://user:password@db:5432/appdb
      REDIS_URL: redis://redis:6379
      NODE_ENV: production
    depends_on:
      - db
      - redis

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: appdb
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

### 3. Kubernetes Deployment

Create `k8s/deployment.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
  labels:
    app: web-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web-app
  template:
    metadata:
      labels:
        app: web-app
    spec:
      containers:
      - name: app
        image: your-registry/web-app:latest
        ports:
        - containerPort: 3000
        env:
        - name: NODE_ENV
          value: production
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: database-url
        livenessProbe:
          httpGet:
            path: /api/health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /api/health
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

Create `k8s/service.yaml`:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-app-service
spec:
  selector:
    app: web-app
  ports:
  - protocol: TCP
    port: 80
    targetPort: 3000
  type: LoadBalancer
```

### 4. CI/CD Pipeline (GitHub Actions)

Create `.github/workflows/ci-cd.yml`:
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  lint-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm ci
      - run: npm run lint
      - run: npm run type-check
      - run: npm test -- --coverage
      - uses: codecov/codecov-action@v3

  build:
    runs-on: ubuntu-latest
    needs: lint-and-test
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v3
      - uses: docker/setup-buildx-action@v2
      - uses: docker/login-action@v2
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/build-push-action@v4
        with:
          context: .
          push: ${{ github.event_name == 'push' }}
          tags: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy-staging:
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/develop'
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Staging
        run: |
          kubectl apply -f k8s/
          kubectl rollout status deployment/web-app

  deploy-production:
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Production
        run: |
          kubectl apply -f k8s/
          kubectl rollout status deployment/web-app
```

## Monitoring and Logging

### Health Check Endpoint

Create `src/app/api/health/route.ts`:
```typescript
export async function GET() {
  const health = {
    status: 'healthy',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
  };

  return Response.json(health, { status: 200 });
}
```

### Logging Setup

Install logger:
```bash
npm install winston
```

Create `src/lib/logger.ts`:
```typescript
import winston from 'winston';

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.json(),
  defaultMeta: { service: 'web-app' },
  transports: [
    new winston.transports.File({ filename: 'logs/error.log', level: 'error' }),
    new winston.transports.File({ filename: 'logs/combined.log' }),
  ],
});

if (process.env.NODE_ENV !== 'production') {
  logger.add(
    new winston.transports.Console({
      format: winston.format.simple(),
    })
  );
}

export default logger;
```

### Monitoring with Prometheus

Install metrics:
```bash
npm install prom-client
```

Create `src/app/api/metrics/route.ts`:
```typescript
import { register } from 'prom-client';

export async function GET() {
  return new Response(await register.metrics(), {
    headers: { 'Content-Type': register.contentType },
  });
}
```

## Database Migrations

### Prisma Setup

```bash
npm install @prisma/client
npm install -D prisma

# Initialize Prisma
npx prisma init

# Create migration
npx prisma migrate dev --name init

# Deploy migration
npx prisma migrate deploy
```

### Database Backup

```bash
# PostgreSQL backup
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore backup
psql $DATABASE_URL < backup_20231210_120000.sql
```

## Performance Optimization

### CDN Configuration
```bash
# Upload static assets to CDN
aws s3 sync ./public s3://your-bucket/
```

### Caching Strategy
```typescript
// Cache control headers
export const revalidate = 3600; // 1 hour

export default function Page() {
  // Page will be statically revalidated every hour
}
```

### Database Query Optimization
```bash
# Add indexes for frequently queried columns
npx prisma db execute --stdin < add_indexes.sql
```

## Disaster Recovery

### Backup Strategy
- Daily automated backups
- Weekly full backups
- Monthly archive backups
- Test restore procedures monthly

### Rollback Procedure
```bash
# Rollback to previous deployment
kubectl rollout undo deployment/web-app

# Rollback database migration
npx prisma migrate resolve --rolled-back <migration-name>
```

## Security Best Practices

### Secrets Management
```bash
# Using GitHub Secrets for sensitive data
# Add secrets in GitHub Actions settings
# Reference: ${{ secrets.API_KEY }}
```

### SSL/TLS Configuration
```nginx
# Nginx SSL configuration
server {
  listen 443 ssl http2;
  ssl_certificate /etc/ssl/certs/cert.pem;
  ssl_certificate_key /etc/ssl/private/key.pem;
  ssl_protocols TLSv1.2 TLSv1.3;
  ssl_ciphers HIGH:!aNULL:!MD5;
}
```

### Rate Limiting
```typescript
import rateLimit from 'express-rate-limit';

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
});

app.use('/api/', limiter);
```

## Monitoring Dashboard

Recommended tools:
- **Datadog**: Comprehensive monitoring
- **New Relic**: APM and infrastructure monitoring
- **CloudWatch**: AWS native monitoring
- **Grafana**: Open-source metrics visualization
- **ELK Stack**: Log aggregation and analysis

## Common DevOps Tasks

### Scale Application
```bash
kubectl scale deployment web-app --replicas=5
```

### Update Environment Variables
```bash
kubectl set env deployment/web-app NODE_ENV=production
```

### Check Pod Status
```bash
kubectl get pods
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

### Execute Commands in Pod
```bash
kubectl exec -it <pod-name> -- npm run db:migrate
```

---

**Last Updated**: December 10, 2025
